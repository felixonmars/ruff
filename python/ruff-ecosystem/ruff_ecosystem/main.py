import asyncio
import dataclasses
import json
from enum import Enum
from pathlib import Path
from typing import TypeVar

from ruff_ecosystem import logger
from ruff_ecosystem.check import compare_check, summarize_check_result
from ruff_ecosystem.format import compare_format, summarize_format_result
from ruff_ecosystem.projects import (
    Project,
    RuffCommand,
)
from ruff_ecosystem.types import Comparison, Result, Serializable

T = TypeVar("T")


class OutputFormat(Enum):
    markdown = "markdown"
    json = "json"


async def main(
    command: RuffCommand,
    ruff_baseline_executable: Path,
    ruff_comparison_executable: Path,
    targets: list[Project],
    cache: Path | None,
    format: OutputFormat,
    max_parallelism: int = 50,
    raise_on_failure: bool = False,
) -> None:
    logger.debug("Using command %s", command.value)
    logger.debug("Using baseline executable at %s", ruff_baseline_executable)
    logger.debug("Using comparison executable at %s", ruff_comparison_executable)
    logger.debug("Using cache directory %s", cache)
    logger.debug("Checking %s targets", len(targets))

    semaphore = asyncio.Semaphore(max_parallelism)

    async def limited_parallelism(coroutine: T) -> T:
        async with semaphore:
            return await coroutine

    comparisons: list[Exception | Comparison] = await asyncio.gather(
        *[
            limited_parallelism(
                clone_and_compare(
                    command,
                    ruff_baseline_executable,
                    ruff_comparison_executable,
                    target,
                    cache,
                )
            )
            for target in targets
        ],
        return_exceptions=not raise_on_failure,
    )
    comparisons_by_target = dict(zip(targets, comparisons, strict=True))

    errors, successes = [], []
    for target, comparison in comparisons_by_target.items():
        if isinstance(comparison, Exception):
            errors.append((target, comparison))
            continue

        successes.append((target, comparison))

    result = Result(completed=successes, errored=errors)

    match format:
        case OutputFormat.json:
            print(json.dumps(result, indent=4, cls=JSONEncoder))
        case OutputFormat.markdown:
            match command:
                case RuffCommand.check:
                    print(summarize_check_result(result))
                case RuffCommand.format:
                    print(summarize_format_result(result))
                case _:
                    raise ValueError(f"Unknown target Ruff command {command}")
        case _:
            raise ValueError(f"Unknown output format {format}")

    return None


async def clone_and_compare(
    command: RuffCommand,
    ruff_baseline_executable: Path,
    ruff_comparison_executable: Path,
    target: Project,
    cache: Path,
) -> Comparison:
    """Check a specific repository against two versions of ruff."""
    assert ":" not in target.repo.owner
    assert ":" not in target.repo.name

    match command:
        case RuffCommand.check:
            compare, options = (
                compare_check,
                target.check_options,
            )
        case RuffCommand.format:
            compare, options = (
                compare_format,
                target.format_options,
            )
        case _:
            raise ValueError(f"Unknown target Ruff command {command}")

    checkout_dir = cache.joinpath(f"{target.repo.owner}:{target.repo.name}")
    cloned_repo = await target.repo.clone(checkout_dir)

    try:
        return await compare(
            ruff_baseline_executable,
            ruff_comparison_executable,
            options,
            cloned_repo,
        )
    except ExceptionGroup as e:
        raise e.exceptions[0] from e


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Serializable):
            return o.jsonable()
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, set):
            return tuple(o)
        if isinstance(o, Path):
            return str(o)
        if isinstance(o, Exception):
            return str(o)
        return super().default(o)