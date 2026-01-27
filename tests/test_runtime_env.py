"""The Python 3.10 runtime lock.

Fails on 3.9 AND on 3.11+, so a branch built or run against the wrong
interpreter says so immediately instead of producing plausible numbers.

The floor half is what separates this family from 3.9: structural pattern
matching, PEP 604 unions at runtime, zip(strict=), EncodingWarning,
itertools.pairwise and dataclass slots all arrive in 3.10. 3.10 is also the
version at which every one of the 29 roster tools becomes installable, which
is not a coincidence -- thirteen of them declare exactly this floor.
"""
import sys


def test_interpreter_is_python_310():
    assert sys.version_info[:2] == (3, 10)


# ---- floor: everything below fails on 3.9 -------------------------------------

def test_structural_pattern_matching():
    # PEP 634, new in 3.10. The 3.9 family asserts the OPPOSITE.
    namespace = {}
    exec(
        "def classify(value):\n"
        "    match value:\n"
        "        case {'tier': 'gold'}:\n"
        "            return 'gold'\n"
        "        case [first, *_]:\n"
        "            return first\n"
        "        case _:\n"
        "            return 'other'\n",
        namespace,
    )
    assert namespace["classify"]({"tier": "gold"}) == "gold"
    assert namespace["classify"]([7, 8]) == 7
    assert namespace["classify"](object()) == "other"


def test_pep604_unions_at_runtime():
    # int | str as a TYPE, new in 3.10.
    union = int | str
    assert isinstance(3, union)
    assert isinstance("three", union)


def test_zip_strict():
    # zip(strict=) new in 3.10.
    try:
        list(zip([1, 2], [3], strict=True))
    except ValueError:
        return
    raise AssertionError("zip(strict=True) did not raise on unequal lengths")


def test_encoding_warning_exists():
    # PEP 597, new in 3.10.
    import builtins
    assert hasattr(builtins, "EncodingWarning")


def test_itertools_pairwise():
    # New in 3.10.
    import itertools
    assert list(itertools.pairwise([1, 2, 3])) == [(1, 2), (2, 3)]


def test_dataclass_slots_and_kw_only():
    # Both new in 3.10.
    import dataclasses

    @dataclasses.dataclass(slots=True, kw_only=True)
    class Line:
        sku: str
        qty: int = 1

    line = Line(sku="A")
    assert line.qty == 1
    assert not hasattr(line, "__dict__")


# ---- ceiling: everything below fails on 3.11+ ---------------------------------

def test_exception_groups_are_not_available():
    # PEP 654 landed in 3.11.
    import builtins
    assert not hasattr(builtins, "ExceptionGroup")


def test_except_star_does_not_compile():
    # PEP 654 syntax landed in 3.11.
    try:
        compile("try:\n    pass\nexcept* ValueError:\n    pass",
                "<lock>", "exec")
    except SyntaxError:
        return
    raise AssertionError("except* compiled -- this is not Python 3.10")


def test_tomllib_is_not_in_the_stdlib():
    # PEP 680 landed in 3.11. full_check.py depends on this being true: it
    # falls back to a line scanner precisely because no TOML parser is
    # guaranteed on this interpreter.
    try:
        import tomllib  # noqa: F401
    except ImportError:
        return
    raise AssertionError("tomllib imported -- this is not Python 3.10")


def test_typing_self_is_not_available():
    # typing.Self landed in 3.11.
    import typing
    assert not hasattr(typing, "Self")


def test_strenum_is_not_available():
    # enum.StrEnum landed in 3.11.
    import enum
    assert not hasattr(enum, "StrEnum")


def test_task_group_is_not_available():
    # asyncio.TaskGroup landed in 3.11.
    import asyncio
    assert not hasattr(asyncio, "TaskGroup")
