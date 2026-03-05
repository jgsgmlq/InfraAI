#!/usr/bin/env bash

# Smoke test for list_skills.py

echo "Running smoke tests for list_skills.py..."

# Test 1: Default execution
echo "[Test 1] Running without arguments"
python scripts/list_skills.py > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 1 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 1 Passed"

# Test 2: With --verbose
echo "[Test 2] Running with --verbose"
python scripts/list_skills.py --verbose > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 2 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 2 Passed"

# Test 3: Filter by location
echo "[Test 3] Running with --location core"
python scripts/list_skills.py --location core > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 3 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 3 Passed"

# Test 4: Help flag
echo "[Test 4] Verify --help output"
python scripts/list_skills.py --help > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 4 Failed! Expected exit code 0 for help, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 4 Passed"

echo "All smoke tests passed successfully!"
exit 0
