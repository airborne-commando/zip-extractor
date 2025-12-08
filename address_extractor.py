from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import pandas as pd
import time
import logging
from datetime import datetime
import re

class AddressExtractor:
    def __init__(self, headless=True, log_level=logging.INFO):
        self.setup_logging(log_level)
        self.logger = logging.getLogger('AddressExtractor')
        self.setup_driver(headless)
        self.base_url = "https://pa.postcodebase.com/zipcode5/{}"
        
    def setup_logging(self, log_level):
        """Setup comprehensive logging configuration"""
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'address_extraction_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
                logging.StreamHandler()
            ]
        )
        
    def setup_driver(self, headless):
        """Setup Chrome driver with detailed logging"""
        self.logger.info("Initializing Chrome driver...")
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless")
            self.logger.debug("Running in headless mode")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.logger.info("Chrome driver initialized successfully")
        except WebDriverException as e:
            self.logger.error(f"Failed to initialize Chrome driver: {str(e)}")
            raise

    def clean_address(self, address):
        """Clean and simplify the address by removing range information"""
        try:
            # Remove the range information in parentheses
            # Pattern matches: "1871 (From 1871 To 1899 Odd) 2ND ST, ERIE, PA"
            # Becomes: "1871 2ND ST, ERIE, PA"
            cleaned = re.sub(r'\s*\([^)]*\)', '', address)
            
            # Clean up any extra spaces
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            
            return cleaned
            
        except Exception as e:
            self.logger.warning(f"Error cleaning address '{address}': {str(e)}")
            return address
    
    def get_zip_code_data(self, zip_code):
        """Extract address data for a specific ZIP code with pagination handling"""
        url = self.base_url.format(zip_code)
        self.logger.info(f"Starting extraction for ZIP code: {zip_code}")
        self.logger.debug(f"Target URL: {url}")
        
        all_addresses = []
        page = 0
        
        try:
            while True:
                if page > 0:
                    page_url = f"{url}?page={page}"
                else:
                    page_url = url
                
                self.logger.debug(f"Navigating to URL: {page_url}")
                self.driver.get(page_url)
                
                # Wait for the specific table that contains ZIP+4 codes to load
                self.logger.debug("Waiting for ZIP+4 table to load...")
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//table[.//th[contains(text(), 'ZIP+4 Code')]]"))
                )
                self.logger.info(f"ZIP+4 table found successfully on page {page + 1}")
                
                # Find the specific table with ZIP+4 codes
                tables = self.driver.find_elements(By.XPATH, "//table[.//th[contains(text(), 'ZIP+4 Code')]]")
                
                if not tables:
                    self.logger.error("No ZIP+4 table found!")
                    break
                
                table = tables[0]
                
                # Extract table data
                rows = table.find_elements(By.TAG_NAME, "tr")
                
                self.logger.info(f"Found {len(rows)} total rows in table (page {page + 1})")
                
                # Process each row (skip header row)
                for i, row in enumerate(rows[1:], 1):  # Skip header row
                    try:
                        # Get all columns in this row
                        cols = row.find_elements(By.TAG_NAME, "td")
                        
                        if len(cols) >= 2:
                            # Extract ZIP+4 code from the first column
                            zip_plus_4_element = cols[0].find_element(By.TAG_NAME, "a")
                            zip_plus_4 = zip_plus_4_element.text.strip()
                            
                            # Extract address from the second column
                            address_element = cols[1].find_element(By.TAG_NAME, "span")
                            original_address = address_element.text.strip()
                            
                            # Clean the address by removing range information
                            cleaned_address = self.clean_address(original_address)
                            
                            # Create simple address record
                            address_record = {
                                'address': cleaned_address,
                                'zip_code': zip_code,
                                'zip_plus_4': zip_plus_4,
                                'original_address': original_address,
                                'page': page + 1
                            }
                            all_addresses.append(address_record)
                            
                            # Log every 10th row to show progress
                            if i % 10 == 0:
                                self.logger.debug(f"Processed {i} rows on page {page + 1}")
                                self.logger.debug(f"Sample cleaned address: {cleaned_address}")
                            
                        else:
                            self.logger.warning(f"Row {i} has only {len(cols)} columns (expected 2)")
                            
                    except Exception as row_error:
                        self.logger.error(f"Error processing row {i} on page {page + 1}: {str(row_error)}")
                        continue
                
                # Check if there's a next page
                try:
                    pager = self.driver.find_element(By.CLASS_NAME, "pager")
                    next_links = pager.find_elements(By.CLASS_NAME, "pager-next")
                    
                    if next_links and next_links[0].is_displayed():
                        next_link = next_links[0].find_element(By.TAG_NAME, "a")
                        if next_link.is_enabled() and next_link.is_displayed():
                            page += 1
                            self.logger.info(f"Moving to page {page + 1}")
                            time.sleep(2)  # Be respectful to the server
                            continue
                        else:
                            self.logger.info("Next link is not clickable, stopping pagination")
                            break
                    else:
                        self.logger.info("No next page link found, stopping pagination")
                        break
                    
                except NoSuchElementException:
                    self.logger.info("No pager found, assuming single page")
                    break
                    
        except TimeoutException:
            self.logger.error(f"Timeout waiting for table to load for ZIP {zip_code}")
        except NoSuchElementException as e:
            self.logger.error(f"Element not found for ZIP {zip_code}: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error extracting data for ZIP {zip_code}: {str(e)}")
        
        self.logger.info(f"Successfully extracted {len(all_addresses)} addresses for ZIP {zip_code}")
        return all_addresses
    
    def get_multiple_zip_codes_data(self, zip_codes):
        """Extract data for multiple ZIP codes with comprehensive logging"""
        self.logger.info(f"Starting extraction for {len(zip_codes)} ZIP codes: {', '.join(zip_codes)}")
        all_addresses = []
        successful_zips = []
        failed_zips = []
        
        for zip_index, zip_code in enumerate(zip_codes, 1):
            self.logger.info(f"Processing ZIP code {zip_index}/{len(zip_codes)}: {zip_code}")
            
            zip_data = self.get_zip_code_data(zip_code)
            
            if zip_data:
                all_addresses.extend(zip_data)
                successful_zips.append(zip_code)
                self.logger.info(f"ZIP {zip_code} completed: {len(zip_data)} addresses")
            else:
                failed_zips.append(zip_code)
                self.logger.warning(f"ZIP {zip_code} failed - no data extracted")
            
            # Add a small delay between ZIP codes
            if zip_index < len(zip_codes):
                self.logger.debug("Waiting 3 seconds before next ZIP code...")
                time.sleep(3)
        
        # Summary logging
        self.logger.info("=" * 50)
        self.logger.info("EXTRACTION SUMMARY")
        self.logger.info("=" * 50)
        self.logger.info(f"Total ZIP codes processed: {len(zip_codes)}")
        self.logger.info(f"Successful ZIP codes: {len(successful_zips)} - {', '.join(successful_zips)}")
        self.logger.info(f"Failed ZIP codes: {len(failed_zips)} - {', '.join(failed_zips)}")
        self.logger.info(f"Total addresses extracted: {len(all_addresses)}")
        self.logger.info("=" * 50)
        
        return all_addresses
    
    def save_to_csv(self, data, filename="address_data.csv"):
        """Save extracted data to CSV file with logging"""
        self.logger.info(f"Attempting to save data to CSV file: {filename}")
        
        try:
            df = pd.DataFrame(data)
            
            # Reorder columns for better readability - address first, then zip code
            column_order = ['address', 'zip_code', 'zip_plus_4', 'page']
            # Only include columns that exist in the dataframe
            column_order = [col for col in column_order if col in df.columns]
            df = df[column_order]
            
            df.to_csv(filename, index=False)
            self.logger.info(f"Successfully saved {len(data)} records to {filename}")
            
            # Log some basic statistics about the data
            self.logger.debug(f"DataFrame shape: {df.shape}")
            if not df.empty:
                self.logger.debug(f"ZIP codes in data: {df['zip_code'].unique().tolist()}")
                self.logger.debug(f"Total pages processed: {df['page'].max()}")
                
        except Exception as e:
            self.logger.error(f"Failed to save CSV file {filename}: {str(e)}")
            raise
    
    def save_to_text_file(self, data, filename="address_data.txt"):
        """Save extracted data to a text file with logging - address and zip code only"""
        self.logger.info(f"Attempting to save data to text file: {filename}")
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                # Write data in simple format: ADDRESS\tZIP_CODE
                for i, item in enumerate(data, 1):
                    line = f"{item['address']}\t{item['zip_code']}\n"
                    file.write(line)
                    
                    # Log progress for large files
                    if i % 100 == 0:
                        self.logger.debug(f"Written {i} records to text file...")
            
            self.logger.info(f"Successfully saved {len(data)} records to {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to save text file {filename}: {str(e)}")
            raise
    
    def close(self):
        """Close the browser driver with logging"""
        self.logger.info("Closing browser driver...")
        try:
            self.driver.quit()
            self.logger.info("Browser driver closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing browser driver: {str(e)}")

def main():
    # Initialize the extractor with verbose logging
    extractor = AddressExtractor(headless=True, log_level=logging.INFO)
    
    start_time = time.time()
    extractor.logger.info("Address Extraction Script Started")
    
    try:
        # Define ZIP codes to scrape
        zip_codes_to_scrape = [
            '16511'  # Test with just one ZIP code first
        ]
        
        extractor.logger.info(f"Starting extraction process for {len(zip_codes_to_scrape)} ZIP codes")
        
        # Extract data
        all_data = extractor.get_multiple_zip_codes_data(zip_codes_to_scrape)
        
        if all_data:
            # Save to multiple formats
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            text_filename = f"address_data_{timestamp}.txt"
            csv_filename = f"address_data_{timestamp}.csv"
            
            extractor.save_to_text_file(all_data, text_filename)
            extractor.save_to_csv(all_data, csv_filename)
            
            # Final summary
            end_time = time.time()
            duration = end_time - start_time
            extractor.logger.info("=" * 60)
            extractor.logger.info("EXTRACTION COMPLETED SUCCESSFULLY!")
            extractor.logger.info(f"Total duration: {duration:.2f} seconds")
            extractor.logger.info(f"Addresses per second: {len(all_data)/duration:.2f}")
            extractor.logger.info(f"Output files: {text_filename}, {csv_filename}")
            extractor.logger.info("=" * 60)
            
            # Print first few records as sample
            extractor.logger.info("SAMPLE DATA:")
            for i, record in enumerate(all_data[:5]):
                extractor.logger.info(f"  {i+1}. {record['address']}\t{record['zip_code']}")
            
        else:
            extractor.logger.error("No data was extracted from any ZIP code!")
            
    except Exception as e:
        extractor.logger.critical(f"Script failed with critical error: {str(e)}", exc_info=True)
    
    finally:
        extractor.close()
        extractor.logger.info("Script execution completed")

if __name__ == "__main__":
    main()