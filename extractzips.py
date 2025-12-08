import re

def extract_zip_data_from_file(filename):
    """
    Extract ZIP code data from the tab-delimited file format
    and return a dictionary mapping ZIP codes to city/state/county info
    """
    zip_mapping = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            # Skip header line if it exists
            start_index = 0
            if lines and lines[0].startswith('State\tZIP Code'):
                start_index = 1
            
            for line in lines[start_index:]:
                line = line.strip()
                if not line:
                    continue
                
                # Split by tabs
                parts = line.split('\t')
                
                if len(parts) >= 5:
                    state = parts[0].strip()
                    zip_code = parts[1].strip()
                    classification = parts[2].strip()
                    city = parts[3].strip()
                    county = parts[4].strip()
                    
                    # Skip P.O. Box only entries if desired
                    # if classification == 'P.O. Box':
                    #     continue
                    
                    # Create the mapping entry
                    zip_mapping[zip_code] = {
                        'city': city,
                        'state': state,
                        'county': county
                    }
                    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return {}
    except Exception as e:
        print(f"Error reading file: {e}")
        return {}
    
    return zip_mapping

def save_zip_mapping_to_js(zip_mapping, output_filename):
    """
    Save the ZIP code mapping as a JavaScript object
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("function loadZipMapping() {\n")
            file.write("    // Comprehensive ZIP code to city/state/county mapping\n")
            file.write("    this.zipMapping = {\n")
            
            # Sort by ZIP code for consistent output
            sorted_zips = sorted(zip_mapping.keys())
            
            for i, zip_code in enumerate(sorted_zips):
                data = zip_mapping[zip_code]
                comma = "," if i < len(sorted_zips) - 1 else ""
                file.write(f"        '{zip_code}': {{ city: '{data['city']}', state: '{data['state']}', county: '{data['county']}' }}{comma}\n")
            
            file.write("    };\n")
            file.write("}\n")
            
        print(f"JavaScript mapping saved to {output_filename}")
        
    except Exception as e:
        print(f"Error saving JavaScript file: {e}")

def save_zip_mapping_to_python(zip_mapping, output_filename):
    """
    Save the ZIP code mapping as a Python dictionary
    """
    try:
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("# Comprehensive ZIP code to city/state/county mapping\n")
            file.write("ZIP_CODE_MAPPING = {\n")
            
            # Sort by ZIP code for consistent output
            sorted_zips = sorted(zip_mapping.keys())
            
            for i, zip_code in enumerate(sorted_zips):
                data = zip_mapping[zip_code]
                comma = "," if i < len(sorted_zips) - 1 else ""
                file.write(f"    '{zip_code}': {{ 'city': '{data['city']}', 'state': '{data['state']}', 'county': '{data['county']}' }}{comma}\n")
            
            file.write("}\n")
            
        print(f"Python mapping saved to {output_filename}")
        
    except Exception as e:
        print(f"Error saving Python file: {e}")

def filter_by_state(zip_mapping, state_code):
    """
    Filter the ZIP code mapping by state
    """
    return {zip_code: data for zip_code, data in zip_mapping.items() if data['state'] == state_code}

def search_by_city(zip_mapping, city_name):
    """
    Search for ZIP codes by city name (case-insensitive)
    """
    return {zip_code: data for zip_code, data in zip_mapping.items() if city_name.lower() in data['city'].lower()}

def main():
    # Configuration
    input_filename = "all_states_zip_codes_20251116_112044.txt"
    js_output_filename = "zip_mapping.js"
    python_output_filename = "zip_mapping.py"
    
    # Extract data from file
    print("Extracting ZIP code data from file...")
    zip_mapping = extract_zip_data_from_file(input_filename)
    
    if not zip_mapping:
        print("No data extracted. Please check the file format and path.")
        return
    
    print(f"Extracted {len(zip_mapping)} ZIP code entries")
    
    # Save as JavaScript
    save_zip_mapping_to_js(zip_mapping, js_output_filename)
    
    # Save as Python
    save_zip_mapping_to_python(zip_mapping, python_output_filename)
    
    # Example usage: Filter by state
    california_zips = filter_by_state(zip_mapping, "CA")
    print(f"\nFound {len(california_zips)} ZIP codes in California")
    
    # Example usage: Search by city
    la_zips = search_by_city(zip_mapping, "Los Angeles")
    print(f"Found {len(la_zips)} ZIP codes in Los Angeles")
    
    # Display first few entries as example
    print("\nSample entries:")
    sample_zips = list(zip_mapping.keys())[:5]
    for zip_code in sample_zips:
        print(f"  {zip_code}: {zip_mapping[zip_code]}")

# Alternative function for direct use
def load_zip_mapping(filename):
    """
    Load ZIP code mapping directly from file and return as dictionary
    """
    return extract_zip_data_from_file(filename)

if __name__ == "__main__":
    main()