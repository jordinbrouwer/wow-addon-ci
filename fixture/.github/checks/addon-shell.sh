#!/usr/bin/env bash
# Example of an addon's own shell check.
set -euo pipefail
grep -q '^## Title: Fixture$' src/Fixture.toc || { echo "[$LOG_PREFIX] FAILED: Missing title."; exit 1; }
echo "[$LOG_PREFIX] PASSED: The addon's own shell check ran."
