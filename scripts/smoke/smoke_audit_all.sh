#!/usr/bin/env bash

# Smoke test for audit_all.py
# Tests both exit codes AND output content

echo "Running smoke tests for audit_all.py..."

# Test 1: Run all audits
echo "[Test 1] Running full audit"
OUTPUT=$(python scripts/audit_all.py 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 1 Failed! Expected exit code 0, got $EXIT_CODE"
    echo "Output: $OUTPUT"
    exit 1
fi
# Verify output contains audit report header
if [[ ! "$OUTPUT" =~ "Unified Audit Report" ]]; then
    echo "FAIL Test 1 Failed! Output missing 'Unified Audit Report'"
    exit 1
fi
# Verify all scopes are audited
if [[ ! "$OUTPUT" =~ "SDK Packages" ]]; then
    echo "FAIL Test 1 Failed! Output missing 'SDK Packages'"
    exit 1
fi
if [[ ! "$OUTPUT" =~ "Skills" ]]; then
    echo "FAIL Test 1 Failed! Output missing 'Skills'"
    exit 1
fi
echo "PASS Test 1 Passed"

# Test 2: Run SDK audit only
echo "[Test 2] Running SDK audit only"
OUTPUT=$(python scripts/audit_all.py sdk 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 2 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
if [[ ! "$OUTPUT" =~ "SDK Packages" ]]; then
    echo "FAIL Test 2 Failed! Output missing SDK section"
    exit 1
fi
echo "PASS Test 2 Passed"

# Test 3: Run skills audit only
echo "[Test 3] Running skills audit only"
OUTPUT=$(python scripts/audit_all.py skills 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 3 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
if [[ ! "$OUTPUT" =~ "Skills" ]]; then
    echo "FAIL Test 3 Failed! Output missing Skills section"
    exit 1
fi
echo "PASS Test 3 Passed"

# Test 4: Run docs audit only
echo "[Test 4] Running docs audit only"
OUTPUT=$(python scripts/audit_all.py docs 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 4 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
if [[ ! "$OUTPUT" =~ "Documentation" ]]; then
    echo "FAIL Test 4 Failed! Output missing Documentation section"
    exit 1
fi
echo "PASS Test 4 Passed"

# Test 5: Verify --help
echo "[Test 5] Verify --help output"
HELP_OUTPUT=$(python scripts/audit_all.py --help 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 5 Failed! Expected exit code 0 for help, got $EXIT_CODE"
    exit 1
fi
if [[ ! "$HELP_OUTPUT" =~ "usage" ]] && [[ ! "$HELP_OUTPUT" =~ "Usage" ]]; then
    echo "FAIL Test 5 Failed! Help output missing usage info"
    exit 1
fi
echo "PASS Test 5 Passed"

# Test 6: Verify summary is present
echo "[Test 6] Verify summary output"
OUTPUT=$(python scripts/audit_all.py 2>&1)
if [[ ! "$OUTPUT" =~ "Summary" ]]; then
    echo "FAIL Test 6 Failed! Output missing Summary"
    exit 1
fi
if [[ ! "$OUTPUT" =~ "scopes audited" ]]; then
    echo "FAIL Test 6 Failed! Output missing scope count"
    exit 1
fi
echo "PASS Test 6 Passed"

echo "All smoke tests passed successfully!"
exit 0
