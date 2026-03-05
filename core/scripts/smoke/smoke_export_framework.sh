#!/usr/bin/env bash

# Smoke test for export_framework.py

echo "Running smoke tests for export_framework.py..."

# Create temp directory for testing
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Test 1: Help flag
echo "[Test 1] Verify --help output"
python scripts/export_framework.py --help > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 1 Failed! Expected exit code 0 for help, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 1 Passed"

# Test 2: Dry run
echo "[Test 2] Running with --dry-run"
python scripts/export_framework.py --dry-run > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 2 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 2 Passed"

# Test 3: Actual export
echo "[Test 3] Running actual export"
python scripts/export_framework.py --out "$TEMP_DIR/framework.zip" > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 3 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
# Verify file exists
if [ ! -f "$TEMP_DIR/framework.zip" ]; then
    echo "FAIL Test 3 Failed! framework.zip not found"
    exit 1
fi
echo "PASS Test 3 Passed"

# Test 4: Export with verbose
echo "[Test 4] Running with --verbose"
python scripts/export_framework.py --out "$TEMP_DIR/framework2.zip" --verbose > /dev/null
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "FAIL Test 4 Failed! Expected exit code 0, got $EXIT_CODE"
    exit 1
fi
echo "PASS Test 4 Passed"

# Test 5: Verify zip contents (manifest.json should exist)
echo "[Test 5] Verify zip contents"
if command -v unzip &> /dev/null; then
    unzip -l "$TEMP_DIR/framework.zip" | grep -q "manifest.json"
    if [ $? -ne 0 ]; then
        echo "FAIL Test 5 Failed! manifest.json not found in zip"
        exit 1
    fi
    echo "PASS Test 5 Passed"
else
    echo "SKIP Test 5 Skipped (unzip not available)"
fi

echo "All smoke tests passed successfully!"
exit 0
