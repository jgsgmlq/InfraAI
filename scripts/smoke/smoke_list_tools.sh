#!/usr/bin/env bash

# Smoke test for list_tools.py
# Tests both exit codes AND output content

echo "Running smoke tests for list_tools.py..."

# Test 1: Successful execution with default registry
echo "[Test 1] Running without arguments"
OUTPUT=$(python scripts/list_tools.py 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 1 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
# Verify output contains expected content
if [[ ! "$OUTPUT" =~ "Command Palette" ]]; then
    echo "FAIL Test 1 Failed! Output missing 'Command Palette'"
    exit 1
fi
if [[ ! "$OUTPUT" =~ "list-tools" ]]; then
    echo "FAIL Test 1 Failed! Output missing 'list-tools'"
    exit 1
fi
echo "PASS Test 1 Passed"

# Test 2: Successful execution with explicit registry
echo "[Test 2] Running with explicit --registry"
OUTPUT=$(python scripts/list_tools.py --registry registry/tools.yaml 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 2 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
# Verify output format (Markdown)
if [[ ! "$OUTPUT" =~ "##" ]]; then
    echo "FAIL Test 2 Failed! Output not in Markdown format"
    exit 1
fi
echo "PASS Test 2 Passed"

# Test 3: Parameter Error (invalid flag)
echo "[Test 3] Running with invalid flag"
python scripts/list_tools.py --invalid-flag 2> /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 2 ]; then
    echo "FAIL Test 3 Failed! Expected exit code 2, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 3 Passed"

# Test 4: Runtime Error (missing file)
echo "[Test 4] Running with missing registry file"
ERROR_OUTPUT=$(python scripts/list_tools.py --registry registry/does_not_exist.yaml 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 3 ]; then
    echo "FAIL Test 4 Failed! Expected exit code 3, got $EXIT_CODE"
    exit 1
fi
# Verify error message is meaningful
if [[ ! "$ERROR_OUTPUT" =~ "not found" ]] && [[ ! "$ERROR_OUTPUT" =~ "Error" ]]; then
    echo "FAIL Test 4 Failed! Error message not meaningful"
    exit 1
fi
echo "PASS Test 4 Passed"

# Test 5: Verify --help
echo "[Test 5] Verify --help output"
HELP_OUTPUT=$(python scripts/list_tools.py --help 2>&1)
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 5 Failed! Expected exit code 0 for help, got $EXIT_CODE"
    exit 1
fi
# Verify help contains usage info
if [[ ! "$HELP_OUTPUT" =~ "usage" ]] && [[ ! "$HELP_OUTPUT" =~ "Usage" ]]; then
    echo "FAIL Test 5 Failed! Help output missing usage info"
    exit 1
fi
echo "PASS Test 5 Passed"

# Test 6: Verify output contains all registered tools
echo "[Test 6] Verify output lists multiple tools"
OUTPUT=$(python scripts/list_tools.py 2>&1)
TOOL_COUNT=$(echo "$OUTPUT" | grep -c "^\-\-\-$" || echo "0")
if [ "$TOOL_COUNT" -lt 3 ]; then
    # Alternative: count by ## headers
    TOOL_COUNT=$(echo "$OUTPUT" | grep -c "^## " || echo "0")
    if [ "$TOOL_COUNT" -lt 3 ]; then
        echo "FAIL Test 6 Failed! Expected at least 3 tools, got $TOOL_COUNT"
        exit 1
    fi
fi
echo "PASS Test 6 Passed"

echo "All smoke tests passed successfully!"
exit 0
