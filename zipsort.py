import pandas as pd

def sort_and_export_zip_codes():
    """
    Sort ZIP codes numerically and export to a new file
    """
    # Read the original file
    input_file = "zip_full_dump.txt"
    output_file = "zip_codes_sorted.txt"
    
    print(f"Reading data from {input_file}...")
    
    try:
        # Read the tab-separated file
        df = pd.read_csv(input_file, sep='\t')
        print(f"Successfully read {len(df)} ZIP codes")
        
        # Convert ZIP codes to string and pad with leading zeros to ensure 5-digit format
        df['ZIP'] = df['ZIP'].astype(str).str.zfill(5)
        
        # Sort by ZIP code numerically
        print("Sorting ZIP codes numerically...")
        df_sorted = df.sort_values('ZIP')
        
        # Reset index
        df_sorted = df_sorted.reset_index(drop=True)
        
        # Export to new file
        print(f"Exporting sorted data to {output_file}...")
        df_sorted.to_csv(output_file, sep='\t', index=False)
        
        # Display results
        print(f"\n✅ SUCCESS!")
        print(f"Input file: {input_file}")
        print(f"Output file: {output_file}")
        print(f"Total records exported: {len(df_sorted)}")
        print(f"First ZIP code: {df_sorted['ZIP'].iloc[0]}")
        print(f"Last ZIP code: {df_sorted['ZIP'].iloc[-1]}")
        
        # Show sample of sorted data
        print(f"\nFirst 15 sorted ZIP codes:")
        print("-" * 30)
        for i, (zip_code, state) in enumerate(zip(df_sorted['ZIP'].head(15), df_sorted['STATE'].head(15))):
            print(f"{i+1:2d}. {zip_code} - {state}")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: File '{input_file}' not found.")
        return False
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

# Run the function
if __name__ == "__main__":
    sort_and_export_zip_codes()