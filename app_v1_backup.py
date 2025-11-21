"""
Supply Chain Risk Exposure Assessment API
Standalone Flask API for Heroku Deployment

This API provides comprehensive risk assessment across 5 risk types:
- Climate Risk (with expected loss calculations)
- Modern Slavery Risk
- Political Instability Risk
- Water Stress Risk
- Nature Loss Risk

Coverage: 67 countries × 34 OECD ICIO sectors
Multi-tier supply chain analysis with Tier-1 (100%), Tier-2 (40%), Tier-3 (16%)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
import os
import sys
import secrets

# Import risk calculation modules
from risk_calculator import MultiTierRiskCalculator
from climate_api_client import ClimateRiskAPIClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize risk calculator
risk_calculator = MultiTierRiskCalculator()
climate_client = ClimateRiskAPIClient()

# API Authentication Configuration
# Set API_KEY environment variable in Heroku config
# Example: heroku config:set API_KEY=your-secure-api-key-here
API_KEY = os.environ.get('API_KEY', None)
AUTH_ENABLED = API_KEY is not None

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AUTH_ENABLED:
            # Authentication disabled - allow all requests
            return f(*args, **kwargs)
        
        # Check for API key in header or query parameter
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                'error': 'Authentication required',
                'message': 'API key is required. Provide it via X-API-Key header or api_key query parameter.',
                'example_header': 'X-API-Key: your-api-key-here',
                'example_query': '/api/assess?country=CHN&sector=D26T27&api_key=your-api-key-here'
            }), 401
        
        if api_key != API_KEY:
            return jsonify({
                'error': 'Invalid API key',
                'message': 'The provided API key is not valid'
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    """API home endpoint with documentation"""
    auth_status = 'enabled' if AUTH_ENABLED else 'disabled'
    
    response = {
        'name': 'Supply Chain Risk Exposure Assessment API',
        'version': '2.0.0',
        'description': 'Comprehensive risk assessment framework for supply chain analysis',
        'authentication': auth_status,
        'coverage': {
            'countries': 67,
            'sectors': 34,
            'risk_types': 5
        },
        'endpoints': {
            'health': '/api/health',
            'countries': '/api/countries',
            'sectors': '/api/sectors',
            'assess': '/api/assess?country={ISO3}&sector={CODE}',
            'batch': '/api/batch (POST)'
        },
        'documentation': 'https://supplyrisk-bb4n56uc.manus.space',
        'features': [
            'Multi-tier supply chain analysis (Tier-1, Tier-2, Tier-3)',
            'OECD ICIO input-output table integration',
            'Climate expected loss calculations',
            'Separate risk scores for 5 independent risk types',
            'Real data from 12+ authoritative sources',
            'API key authentication for secure access'
        ]
    }
    
    if AUTH_ENABLED:
        response['authentication_note'] = 'API key required. Include X-API-Key header or api_key query parameter.'
    
    return jsonify(response)

@app.route('/api/health')
def health():
    """Health check endpoint (no authentication required)"""
    return jsonify({
        'status': 'healthy',
        'service': 'Supply Chain Risk API',
        'version': '2.0.0',
        'authentication': 'enabled' if AUTH_ENABLED else 'disabled',
        'data_coverage': {
            'countries': 67,
            'sectors': 34
        },
        'timestamp': str(os.environ.get('HEROKU_RELEASE_CREATED_AT', 'N/A'))
    })

@app.route('/api/countries')
@require_api_key
def get_countries():
    """Get list of all supported countries"""
    countries = risk_calculator.get_countries()
    return jsonify({
        'count': len(countries),
        'countries': countries
    })

@app.route('/api/sectors')
@require_api_key
def get_sectors():
    """Get list of all supported sectors"""
    sectors = risk_calculator.get_sectors()
    return jsonify({
        'count': len(sectors),
        'sectors': sectors
    })

@app.route('/api/assess')
@require_api_key
def assess_risk():
    """
    Assess risk exposure for a country-sector combination
    
    Query Parameters:
    - country: ISO 3-letter country code (e.g., CHN, USA, DEU)
    - sector: OECD ICIO sector code (e.g., D26T27, D01T02, D10T12)
    - api_key: (optional) API key for authentication (can also use X-API-Key header)
    
    Returns:
    - direct_risk: Inherent country-sector risk
    - indirect_risk: Risk from suppliers (weighted by I-O coefficients)
    - total_risk: Combined risk (60% direct + 40% indirect)
    - climate_details: Expected loss calculations from Climate API
    - tier_breakdown: Supplier contributions by tier
    """
    country = request.args.get('country')
    sector = request.args.get('sector')
    
    if not country or not sector:
        return jsonify({
            'error': 'Missing required parameters',
            'message': 'Both country and sector parameters are required',
            'example': '/api/assess?country=CHN&sector=D26T27'
        }), 400
    
    try:
        # Calculate multi-tier risk assessment
        assessment = risk_calculator.calculate_risk(country, sector)
        
        if assessment.get('error'):
            return jsonify(assessment), 404
        
        # Fetch climate expected loss data
        climate_data = climate_client.get_country_risk(
            assessment.get('country_name', country)
        )
        
        # Enhance assessment with climate data
        if climate_data and not climate_data.get('error'):
            assessment['climate_details'] = climate_data
        
        return jsonify(assessment)
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/batch', methods=['POST'])
@require_api_key
def batch_assess():
    """
    Batch risk assessment for multiple country-sector combinations
    
    Request Body:
    {
        "assessments": [
            {"country": "CHN", "sector": "D26T27"},
            {"country": "USA", "sector": "D10T12"},
            ...
        ]
    }
    
    Returns: Array of risk assessments
    """
    data = request.get_json()
    
    if not data or 'assessments' not in data:
        return jsonify({
            'error': 'Invalid request',
            'message': 'Request body must contain "assessments" array'
        }), 400
    
    assessments = data['assessments']
    results = []
    
    for item in assessments:
        country = item.get('country')
        sector = item.get('sector')
        
        if country and sector:
            try:
                assessment = risk_calculator.calculate_risk(country, sector)
                
                # Add climate data if available
                climate_data = climate_client.get_country_risk(
                    assessment.get('country_name', country)
                )
                if climate_data and not climate_data.get('error'):
                    assessment['climate_details'] = climate_data
                
                results.append(assessment)
            except Exception as e:
                results.append({
                    'country': country,
                    'sector': sector,
                    'error': str(e)
                })
    
    return jsonify({
        'count': len(results),
        'results': results
    })

@app.route('/api/generate-key', methods=['POST'])
def generate_api_key():
    """
    Generate a secure API key (for development/testing only)
    In production, manage keys through Heroku config vars
    """
    if AUTH_ENABLED:
        return jsonify({
            'error': 'Key generation disabled',
            'message': 'API key is already configured. Contact administrator to obtain access.'
        }), 403
    
    # Generate a secure random API key
    new_key = secrets.token_urlsafe(32)
    
    return jsonify({
        'message': 'API key generated successfully',
        'api_key': new_key,
        'instructions': [
            'Save this key securely - it will not be shown again',
            'Set it as environment variable: heroku config:set API_KEY=' + new_key,
            'Include in requests via X-API-Key header or api_key query parameter'
        ]
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist',
        'available_endpoints': [
            '/api/health',
            '/api/countries',
            '/api/sectors',
            '/api/assess',
            '/api/batch'
        ]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    if not AUTH_ENABLED:
        print("⚠️  WARNING: API authentication is DISABLED")
        print("   Set API_KEY environment variable to enable authentication")
        print("   Example: export API_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')")
    else:
        print("✓ API authentication is ENABLED")
    
    print(f"✓ Starting API server on port {port}")
    print(f"✓ Loaded {len(risk_calculator.get_countries())} countries")
    print(f"✓ Loaded {len(risk_calculator.get_sectors())} sectors")
    
    app.run(host='0.0.0.0', port=port, debug=False)
