#!/usr/bin/env bash

# Smoke test for init_project.py

echo "Running smoke tests for init_project.py..."

# Create temp directory for testing
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Test 1: Help flag
echo "[Test 1] Verify --help output"
python scripts/init_project.py --help > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 1 Failed! Expected exit code 0 for help, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 1 Passed"

# Test 2: Dry run
echo "[Test 2] Running with --dry-run"
python scripts/init_project.py --target "$TEMP_DIR/test_project" --dry-run > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 2 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 2 Passed"

# Test 3: Missing required argument
echo "[Test 3] Running without --target"
python scripts/init_project.py 2> /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 2 ]; then
    echo "FAIL Test 3 Failed! Expected exit code 2, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 3 Passed"

# Test 4: Actual initialization
echo "[Test 4] Running actual initialization"
python scripts/init_project.py --target "$TEMP_DIR/real_project" --name "Test Project" > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 4 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
# Verify expected files exist
if [ ! -f "$TEMP_DIR/real_project/CLAUDE.md" ]; then
    echo "FAIL Test 4 Failed! CLAUDE.md not found"
    exit 1
fi
if [ ! -d "$TEMP_DIR/real_project/project/tools" ]; then
    echo "FAIL Test 4 Failed! project/tools not found"
    exit 1
fi
echo "PASS Test 4 Passed"

# Test 5: Non-empty directory without --force
echo "[Test 5] Running on non-empty directory without --force"
python scripts/init_project.py --target "$TEMP_DIR/real_project" 2> /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 3 ]; then
    echo "FAIL Test 5 Failed! Expected exit code 3, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 5 Passed"

# Test 6: Non-empty directory with --force
echo "[Test 6] Running on non-empty directory with --force"
python scripts/init_project.py --target "$TEMP_DIR/real_project" --force > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 6 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 6 Passed"

echo "All smoke tests passed successfully!"
exit 0
