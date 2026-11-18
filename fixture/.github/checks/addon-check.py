#!/usr/bin/env python3
"""Example of an addon's own check: runs next to the shared ones and can use the shared lib."""
from lib import log, toc

if "Fixture.name" not in (toc.SRC / f"{toc.ADDON}.lua").read_text(encoding="utf-8"):
    log.fail("Fixture.lua should set Fixture.name.")
log.passed("The addon's own Python check ran with the shared lib.")
