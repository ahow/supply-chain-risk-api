"""
Supply Chain Risk Exposure Assessment API (Version 2)
Standalone Flask API with Dual I-O Model Support

Features:
- Dual I-O model support (OECD ICIO + EXIOBASE)
- Model selection via API parameter
- Real I-O coefficient data
- Multi-tier supply chain analysis
- 5 independent risk types
- API key authentication
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from functools import wraps
import os

# Import I-O model infrastructure
from io_model_factory import IOModelFactory, create_io_model
from risk_calculator_v2 import MultiTierRiskCalculator
from climate_api_client import ClimateRiskAPIClient
from country_code_mapper import normalize_country_code, is_valid_for_model

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize climate client
climate_client = ClimateRiskAPIClient()

# API Authentication Configuration
API_KEY = os.environ.get('API_KEY', None)
AUTH_ENABLED = API_KEY is not None

# Cache for model instances (avoid reloading large coefficient matrices)
_model_cache = {}

def get_risk_calculator(model_type: str = 'oecd') -> MultiTierRiskCalculator:
    """
    Get or create a risk calculator for the specified model.
    Uses caching to avoid reloading large coefficient matrices.
    """
    if model_type not in _model_cache:
        io_model = create_io_model(model_type)
        _model_cache[model_type] = MultiTierRiskCalculator(io_model)
    return _model_cache[model_type]

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not AUTH_ENABLED:
            return f(*args, **kwargs)
        
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        
        if not api_key:
            return jsonify({
                'error': 'Authentication required',
                'message': 'API key is required. Provide it via X-API-Key header or api_key query parameter.'
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
    
    return jsonify({
        'name': 'Supply Chain Risk Exposure Assessment API',
        'version': '3.0.0',
        'description': 'Comprehensive risk assessment with dual I-O model support',
        'authentication': auth_status,
        'models': {
            'oecd': 'OECD ICIO Extended (85 countries, 56 sectors, 2020)',
            'exiobase': 'EXIOBASE 3 (49 regions, 163 industries, 2022) - Coming soon'
        },
        'endpoints': {
            'health': '/api/health',
            'models': '/api/models',
            'countries': '/api/countries?model={oecd|exiobase}',
            'sectors': '/api/sectors?model={oecd|exiobase}',
            'assess': '/api/assess?country={CODE}&sector={CODE}&model={oecd|exiobase}',
            'batch': '/api/batch (POST)',
            'compare': '/api/compare?country={CODE}&sector={CODE}'
        },
        'features': [
            'Dual I-O model support (OECD ICIO + EXIOBASE)',
            'Real I-O coefficient data from OECD',
            'Multi-tier supply chain analysis (Tier-1, Tier-2, Tier-3)',
            'Climate expected loss calculations',
            '5 independent risk types',
            'Model comparison endpoint',
            'API key authentication'
        ]
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    try:
        # Test OECD model loading
        oecd_calc = get_risk_calculator('oecd')
        oecd_countries = len(oecd_calc.get_countries())
        oecd_sectors = len(oecd_calc.get_sectors())
        
        return jsonify({
            'status': 'healthy',
            'authentication': 'enabled' if AUTH_ENABLED else 'disabled',
            'models': {
                'oecd': {
                    'status': 'available',
                    'countries': oecd_countries,
                    'sectors': oecd_sectors
                },
                'exiobase': {
                    'status': 'partially_available',
                    'note': 'Coefficient matrix pending'
                }
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/models')
@require_api_key
def list_models():
    """List available I-O models and their characteristics"""
    models = IOModelFactory.get_available_models()
    return jsonify({
        'models': models,
        'default': IOModelFactory.DEFAULT_MODEL
    })

@app.route('/api/models/<model_id>')
@require_api_key
def get_model_info(model_id):
    """Get detailed information about a specific model"""
    model_info = IOModelFactory.get_model_info(model_id)
    
    if not model_info:
        return jsonify({
            'error': 'Model not found',
            'available_models': list(IOModelFactory.MODELS.keys())
        }), 404
    
    try:
        calculator = get_risk_calculator(model_id)
        model_info['runtime_info'] = calculator.get_model_info()
    except Exception as e:
        model_info['runtime_info'] = {'error': str(e)}
    
    return jsonify(model_info)

@app.route('/api/countries')
@require_api_key
def get_countries():
    """Get list of countries for specified model"""
    model_type = request.args.get('model', 'oecd').lower()
    
    if not IOModelFactory.validate_model_type(model_type):
        return jsonify({
            'error': 'Invalid model type',
            'available_models': list(IOModelFactory.MODELS.keys())
        }), 400
    
    try:
        calculator = get_risk_calculator(model_type)
        countries = calculator.get_countries()
        
        return jsonify({
            'model': model_type,
            'count': len(countries),
            'countries': countries
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sectors')
@require_api_key
def get_sectors():
    """Get list of sectors for specified model"""
    model_type = request.args.get('model', 'oecd').lower()
    
    if not IOModelFactory.validate_model_type(model_type):
        return jsonify({
            'error': 'Invalid model type',
            'available_models': list(IOModelFactory.MODELS.keys())
        }), 400
    
    try:
        calculator = get_risk_calculator(model_type)
        sectors = calculator.get_sectors()
        
        return jsonify({
            'model': model_type,
            'count': len(sectors),
            'sectors': sectors
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assess')
@require_api_key
def assess_risk():
    """Assess supply chain risk for a country-sector using specified model"""
    country = request.args.get('country', '').upper()
    sector = request.args.get('sector', '').upper()
    model_type = request.args.get('model', 'oecd').lower()
    skip_climate = request.args.get('skip_climate', 'false').lower() == 'true'
    
    if not country or not sector:
        return jsonify({
            'error': 'Missing required parameters',
            'required': ['country', 'sector'],
            'optional': ['model (default: oecd)', 'skip_climate (default: false)']
        }), 400
    
    if not IOModelFactory.validate_model_type(model_type):
        return jsonify({
            'error': 'Invalid model type',
            'available_models': list(IOModelFactory.MODELS.keys())
        }), 400
    
    try:
        calculator = get_risk_calculator(model_type)
        result = calculator.assess_risk(country, sector, skip_climate=skip_climate)
        
        if result and 'error' in result:
            return jsonify(result), 404
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'error': 'Assessment failed',
            'message': str(e),
            'country': country,
            'sector': sector,
            'model': model_type
        }), 500

@app.route('/api/batch', methods=['POST'])
@require_api_key
def batch_assess():
    """Batch assessment for multiple country-sectors"""
    data = request.get_json()
    
    if not data or 'assessments' not in data:
        return jsonify({
            'error': 'Invalid request',
            'required': {
                'assessments': [
                    {'country': 'CHN', 'sector': 'D26T27'},
                    {'country': 'USA', 'sector': 'D10T12'}
                ]
            },
            'optional': {
                'model': 'oecd (default) or exiobase'
            }
        }), 400
    
    assessments = data.get('assessments', [])
    model_type = data.get('model', 'oecd').lower()
    
    if not IOModelFactory.validate_model_type(model_type):
        return jsonify({
            'error': 'Invalid model type',
            'available_models': list(IOModelFactory.MODELS.keys())
        }), 400
    
    try:
        calculator = get_risk_calculator(model_type)
        results = []
        
        for item in assessments:
            country = item.get('country', '').upper()
            sector = item.get('sector', '').upper()
            
            if not country or not sector:
                results.append({
                    'error': 'Missing country or sector',
                    'item': item
                })
                continue
            
            result = calculator.assess_risk(country, sector)
            results.append(result)
        
        return jsonify({
            'model': model_type,
            'count': len(results),
            'results': results
        })
    except Exception as e:
        return jsonify({
            'error': 'Batch assessment failed',
            'message': str(e)
        }), 500

@app.route('/api/compare')
@require_api_key
def compare_models():
    """Compare risk assessment results from both models"""
    country = request.args.get('country', '').upper()
    sector = request.args.get('sector', '').upper()
    
    if not country or not sector:
        return jsonify({
            'error': 'Missing required parameters',
            'required': ['country', 'sector']
        }), 400
    
    try:
        # Get results from both models
        oecd_calc = get_risk_calculator('oecd')
        oecd_result = oecd_calc.assess_risk(country, sector)
        
        # EXIOBASE not fully implemented yet
        exiobase_result = {
            'status': 'not_available',
            'message': 'EXIOBASE coefficient matrix pending'
        }
        
        return jsonify({
            'country': country,
            'sector': sector,
            'oecd': oecd_result,
            'exiobase': exiobase_result,
            'comparison': {
                'note': 'Full comparison available when EXIOBASE coefficients are loaded'
            }
        })
    except Exception as e:
        return jsonify({
            'error': 'Comparison failed',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
