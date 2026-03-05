#!/usr/bin/env bash

# Smoke test for list_tools.py

echo "Running smoke tests for list_tools.py..."

# Test 1: Successful execution with default registry
echo "[Test 1] Running without arguments"
python scripts/list_tools.py > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ Test 1 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "✅ Test 1 Passed"

# Test 2: Successful execution with explicit registry
echo "[Test 2] Running with explicit --registry"
python scripts/list_tools.py --registry registry/tools.yaml > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ Test 2 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "✅ Test 2 Passed"

# Test 3: Parameter Error (invalid flag)
echo "[Test 3] Running with invalid flag"
python scripts/list_tools.py --invalid-flag 2> /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 2 ]; then
    echo "❌ Test 3 Failed! Expected exit code 2, got $EXIT_CODE"
    exit 1
fi
echo "✅ Test 3 Passed"

# Test 4: Runtime Error (missing file)
echo "[Test 4] Running with missing registry file"
python scripts/list_tools.py --registry registry/does_not_exist.yaml 2> /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 3 ]; then
    echo "❌ Test 4 Failed! Expected exit code 3, got $EXIT_CODE"
    exit 1
fi
echo "✅ Test 4 Passed"

# Test 5: Verify --help
echo "[Test 5] Verify --help output"
python scripts/list_tools.py --help > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "❌ Test 5 Failed! Expected exit code 0 for help, got $EXIT_CODE"
    exit 1
fi
echo "✅ Test 5 Passed"

echo "🎉 All smoke tests passed successfully!"
exit 0
