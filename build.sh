#!/bin/bash

# Build and test script for Xavier Event Cancellation System

echo "=================================================="
echo "Xavier University Event Cancellation System"
echo "Team Volcanoes - Build & Test Script"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
python --version
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Run all tests
echo "=================================================="
echo "Running All Tests"
echo "=================================================="
echo ""

echo "--- Testing Use Case RP1: Validation ---"
python tests/test_rp1_validation.py
echo ""

echo "--- Testing Use Case RP2: Notifications ---"
python tests/test_rp2_notifications.py
echo ""

echo "--- Testing Use Case RP3: Calendar Sync ---"
python tests/test_rp3_calendar_sync.py
echo ""

# Run complete demo
echo "=================================================="
echo "Running Complete Integration Demo"
echo "=================================================="
echo ""
python examples/complete_integration_demo.py

echo ""
echo "=================================================="
echo "Build and Test Complete!"
echo "=================================================="
