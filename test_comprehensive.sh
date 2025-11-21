#!/bin/bash
echo "=== Comprehensive API Test ==="
echo ""
echo "1. Health check..."
curl -s http://localhost:5556/api/health | python3 -m json.tool
echo ""
echo "2. List models..."
curl -s http://localhost:5556/api/models | python3 -m json.tool
echo ""
echo "3. Test CHN Electronics..."
curl -s "http://localhost:5556/api/assess?country=CHN&sector=C26T27&model=oecd" | python3 -m json.tool | head -60
echo ""
echo "4. Test DEU Automotive..."
curl -s "http://localhost:5556/api/assess?country=DEU&sector=C29T30&model=oecd" | python3 -m json.tool | head -60
