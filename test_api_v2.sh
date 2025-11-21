#!/bin/bash
# Comprehensive API Test Script for Version 2

echo "=========================================="
echo "Testing Supply Chain Risk API v2"
echo "=========================================="

BASE_URL="http://localhost:5555"

echo ""
echo "1. Testing home endpoint..."
curl -s "$BASE_URL/" | python3 -m json.tool | head -20

echo ""
echo "2. Testing health endpoint..."
curl -s "$BASE_URL/api/health" | python3 -m json.tool

echo ""
echo "3. Testing models list..."
curl -s "$BASE_URL/api/models" | python3 -m json.tool

echo ""
echo "4. Testing countries endpoint (OECD)..."
curl -s "$BASE_URL/api/countries?model=oecd" | python3 -m json.tool | head -30

echo ""
echo "5. Testing sectors endpoint (OECD)..."
curl -s "$BASE_URL/api/sectors?model=oecd" | python3 -m json.tool | head -30

echo ""
echo "6. Testing risk assessment (USA + Food)..."
curl -s "$BASE_URL/api/assess?country=USA&sector=C10T12&model=oecd" | python3 -m json.tool | head -50

echo ""
echo "7. Testing risk assessment (CHN + Electronics)..."
curl -s "$BASE_URL/api/assess?country=CHN&sector=C26T27&model=oecd" | python3 -m json.tool | head -50

echo ""
echo "=========================================="
echo "API Tests Complete!"
echo "=========================================="
