#!/usr/bin/env bash

# Smoke test for count_lines.py

echo "Running smoke tests for count_lines.py..."

# Test 1: Help flag
echo "[Test 1] Verify --help output"
python scripts/count_lines.py --help > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 1 Failed! Expected exit code 0 for help, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 1 Passed"

# Test 2: Count current directory
echo "[Test 2] Count scripts directory"
python scripts/count_lines.py scripts > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 2 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 2 Passed"

# Test 3: Non-existent path
echo "[Test 3] Non-existent path"
python scripts/count_lines.py /nonexistent/path 2> /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 3 ]; then
    echo "FAIL Test 3 Failed! Expected exit code 3, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 3 Passed"

# Test 4: With --no-empty flag
echo "[Test 4] With --no-empty flag"
python scripts/count_lines.py scripts --no-empty > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 4 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 4 Passed"

echo "All smoke tests passed successfully!"
exit 0
