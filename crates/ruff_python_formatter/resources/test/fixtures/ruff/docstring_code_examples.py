# The simplest doctest to ensure basic formatting works.
def doctest_simple():
    """
    Do cool stuff.

    >>> cool_stuff( 1 )
    2
    """
    pass


# Another simple test, but one where the Python code
# extends over multiple lines.
def doctest_simple_continued():
    """
    Do cool stuff.

    >>> def cool_stuff( x ):
    ...     print( f"hi {x}" );
    hi 2
    """
    pass


# Test that we support multiple directly adjacent
# doctests.
def doctest_adjacent():
    """
    Do cool stuff.

    >>> cool_stuff( x )
    >>> cool_stuff( y )
    2
    """
    pass


# Test that a doctest on the last non-whitespace line of a docstring
# reformats correctly.
def doctest_last_line():
    """
    Do cool stuff.

    >>> cool_stuff( x )
    """
    pass


# Test that a doctest that continues to the last non-whitespace line of
# a docstring reformats correctly.
def doctest_last_line_continued():
    """
    Do cool stuff.

    >>> def cool_stuff( x ):
    ...     print( f"hi {x}" );
    """
    pass


# Test that a doctest is correctly identified and formatted with a blank
# continuation line.
def doctest_blank_continued():
    """
    Do cool stuff.

    >>> def cool_stuff ( x ):
    ...     print( x )
    ...
    ...     print( x )
    """
    pass


# Test that a doctest containing a triple quoted string gets formatted
# correctly and doesn't result in invalid syntax.
def doctest_with_triple_single():
    """
    Do cool stuff.

    >>> '''tricksy'''
    """
    pass


# Another nested multi-line string case, but with triple escaped double
# quotes inside a triple single quoted string.
def doctest_with_triple_escaped_double():
    """
    Do cool stuff.

    >>> '''\"\"\"'''
    """
    pass


# Tests that inverting the triple quoting works as expected.
def doctest_with_triple_inverted():
    '''
    Do cool stuff.

    >>> """tricksy"""
    '''
    pass


# Tests nested doctests are ignored. That is, we don't format doctests
# recursively. We only recognize "top level" doctests.
#
# This restriction primarily exists to avoid needing to deal with
# nesting quotes. It also seems like a generally sensible restriction,
# although it could be lifted if necessary I believe.
def doctest_nested_doctest_not_formatted():
    '''
    Do cool stuff.

    >>> def nested( x   ):
    ...     """
    ...     Do nested cool stuff.
    ...     >>> func_call( 5 )
    ...     """
    ...     pass
    '''
    pass


# Tests that the starting column does not matter.
def doctest_varying_start_column():
    '''
    Do cool stuff.

    >>> assert    ("Easy!")
      >>> import                      math
          >>> math.floor(  1.9  )
          1
    '''
    pass


# Checks that a simple but invalid doctest gets skipped.
def doctest_skipped_simple():
    """
    Do cool stuff.

    >>> cool-stuff( x ):
    2
    """
    pass


# Checks that a simple doctest that is continued over multiple lines,
# but is invalid, gets skipped.
def doctest_skipped_simple_continued():
    """
    Do cool stuff.

    >>> def cool-stuff( x ):
    ...     print( f"hi {x}" );
    2
    """
    pass


# Checks that a doctest with improper indentation gets skipped.
def doctest_skipped_inconsistent_indent():
    """
    Do cool stuff.

     >>> def cool_stuff( x ):
    ...     print( f"hi {x}" );
    hi 2
    """
    pass

# Checks that a doctest with some proper indentation and some improper
# indentation is "partially" formatted. That is, the part that appears
# before the inconsistent indentation is formatted. This requires that
# the part before it is valid Python.
def doctest_skipped_partial_inconsistent_indent():
    """
    Do cool stuff.

     >>> def cool_stuff( x ):
     ...     print( x )
    ...     print( f"hi {x}" );
    hi 2
    """
    pass


# Checks that a doctest with improper triple single
# quoted string gets skipped.
def doctest_skipped_triple_incorrect():
    """
    Do cool stuff.

    >>> foo( x )
    ... '''tri'''cksy'''
    """
    pass


# Tests that a doctest on a single line is skipped.
def doctest_one_line():
    ">>> foo( x )"
    pass
