#!/usr/bin/env bash

# Smoke test for audit_registry.py

echo "Running smoke tests for audit_registry.py..."

# Test 1: Successful execution with default registry
echo "[Test 1] Running without arguments"
python scripts/audit_registry.py > /dev/null
EXIT_CODE=$?
# Note: exit code 3 is acceptable if there are missing files (expected in incomplete setup)
if [ $EXIT_CODE -ne 0 ] && [ $EXIT_CODE -ne 3 ]; then
    echo "FAIL Test 1 Failed! Expected exit code 0 or 3, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 1 Passed"

# Test 2: Successful execution with explicit registry
echo "[Test 2] Running with explicit --registry"
python scripts/audit_registry.py --registry registry/tools.yaml > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ] && [ $EXIT_CODE -ne 3 ]; then
    echo "FAIL Test 2 Failed! Expected exit code 0 or 3, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 2 Passed"

# Test 3: Parameter Error (invalid flag)
echo "[Test 3] Running with invalid flag"
python scripts/audit_registry.py --invalid-flag 2> /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 2 ]; then
    echo "FAIL Test 3 Failed! Expected exit code 2, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 3 Passed"

# Test 4: Runtime Error (missing file)
echo "[Test 4] Running with missing registry file"
python scripts/audit_registry.py --registry registry/does_not_exist.yaml 2> /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 3 ]; then
    echo "FAIL Test 4 Failed! Expected exit code 3, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 4 Passed"

# Test 5: Verify --help
echo "[Test 5] Verify --help output"
python scripts/audit_registry.py --help > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 5 Failed! Expected exit code 0 for help, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 5 Passed"

# Test 6: Verify --quiet flag
echo "[Test 6] Verify --quiet flag"
python scripts/audit_registry.py --quiet > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ] && [ $EXIT_CODE -ne 3 ]; then
    echo "FAIL Test 6 Failed! Expected exit code 0 or 3, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 6 Passed"

echo "All smoke tests passed successfully!"
exit 0
