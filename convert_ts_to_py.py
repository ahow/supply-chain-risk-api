"""Convert TypeScript OECD data files to Python format"""
import json
import re

def convert_ts_to_python(ts_file, py_file, var_name):
    """Convert TypeScript data file to Python"""
    with open(ts_file, 'r') as f:
        content = f.read()
    
    # Extract the data array/object
    # Find the export statement
    match = re.search(r'export const ' + var_name + r'\s*=\s*(\[.*?\]);', content, re.DOTALL)
    if not match:
        print(f"Could not find {var_name} in {ts_file}")
        return
    
    data_str = match.group(1)
    
    # Convert TypeScript to Python-compatible JSON
    # Replace single quotes with double quotes
    data_str = data_str.replace("'", '"')
    
    try:
        data = json.loads(data_str)
        
        # Write Python file
        with open(py_file, 'w') as f:
            f.write(f'"""{var_name} data for risk assessment"""\n\n')
            f.write(f'{var_name} = ')
            f.write(json.dumps(data, indent=2))
            f.write('\n')
        
        print(f"Successfully converted {ts_file} to {py_file}")
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON from {ts_file}: {e}")

# Convert files
convert_ts_to_python(
    '/home/ubuntu/supply-chain-risk-platform/server/oecdCountries.ts',
    '/home/ubuntu/heroku-risk-api/oecd_data.py',
    'OECD_COUNTRIES'
)
