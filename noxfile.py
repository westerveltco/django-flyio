from __future__ import annotations

import nox

PY310 = "3.10"
PY311 = "3.11"
PY312 = "3.12"
PY313 = "3.13"
PY_VERSIONS = [PY310, PY311, PY312, PY313]
PY_DEFAULT = PY310

DJ42 = "4.2"
DJ52 = "5.2"
DJ60 = "6.0"
DJ60_MIN_PY = PY312
DJMAIN = "main"
DJMAIN_MIN_PY = PY312
DJ_VERSIONS = [DJ42, DJ52, DJ60, DJMAIN]
DJ_DEFAULT = DJ42

PSYCOPG2 = "2"
PSYCOPG3 = "3"
PSYCOPG_VERSIONS = [PSYCOPG2, PSYCOPG3]
PSYCOPG_DEFAULT = PSYCOPG3


def version(ver: str) -> tuple[int, ...]:
    """Convert a string version to a tuple of ints, e.g. "3.10" -> (3, 10)"""
    return tuple(map(int, ver.split(".")))


def should_skip(python: str, django: str, psycopg: str) -> tuple[bool, str | None]:  # noqa: ARG001
    """Return True if the test should be skipped"""
    if django == DJMAIN and version(python) < version(DJMAIN_MIN_PY):
        return True, f"Django {DJMAIN} requires Python {DJMAIN_MIN_PY}+"

    if django == DJ60 and version(python) < version(DJ60_MIN_PY):
        return True, f"Django {DJ60} requires Python {DJ60_MIN_PY}+"

    return False, None


@nox.session(python=PY_VERSIONS)  # type: ignore[untyped-decorator]
@nox.parametrize("django", DJ_VERSIONS)  # type: ignore[untyped-decorator]
@nox.parametrize("psycopg", PSYCOPG_VERSIONS)  # type: ignore[untyped-decorator]
def tests(session: nox.Session, django: str, psycopg: str) -> None:
    skip = should_skip(session.python, django, psycopg)
    if skip[0]:
        session.skip(skip[1])

    session.install(".[test]")

    if django == DJMAIN:
        session.install("https://github.com/django/django/archive/refs/heads/main.zip")
    else:
        session.install(f"django=={django}")

    if psycopg == PSYCOPG2:
        session.install("psycopg2-binary")
    elif psycopg == PSYCOPG3:
        session.install("psycopg[binary]")

    session.run("pytest")
