from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import pandas as pd
import time
import os
import logging
from datetime import datetime

class ZipCodeExtractor:
    def __init__(self, headless=True, log_level=logging.INFO):
        self.setup_logging(log_level)
        self.logger = logging.getLogger('ZipCodeExtractor')
        self.setup_driver(headless)
        self.base_url = "https://www.zip-codes.com/state/{}.asp"
        
    def setup_logging(self, log_level):
        """Setup comprehensive logging configuration"""
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'zip_extraction_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
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
    
    def get_state_data(self, state_abbr):
        """Extract ZIP code data for a specific state with detailed logging"""
        url = self.base_url.format(state_abbr.lower())
        self.logger.info(f"Starting extraction for state: {state_abbr.upper()}")
        self.logger.debug(f"Target URL: {url}")
        
        try:
            self.logger.debug(f"Navigating to URL: {url}")
            self.driver.get(url)
            
            # Wait for the table to load with timeout handling
            self.logger.debug("Waiting for table element to load...")
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "tblZIP"))
            )
            self.logger.info("Table element found successfully")
            
            # Extract table data
            data = []
            table = self.driver.find_element(By.ID, "tblZIP")
            rows = table.find_elements(By.TAG_NAME, "tr")
            
            self.logger.info(f"Found {len(rows)} total rows in table")
            
            # Skip header row
            for i, row in enumerate(rows[1:], 1):
                try:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    
                    if len(cols) >= 7:  # Ensure we have all columns
                        row_data = {
                            'state': state_abbr.upper(),
                            'zip_code': cols[0].text.strip(),
                            'classification': cols[1].text.strip(),
                            'city': cols[2].text.strip(),
                            'county': cols[3].text.strip(),
                            'area_codes': cols[4].text.strip(),
                            'population': cols[5].text.strip().replace(',', ''),
                            'population_percent': cols[6].text.strip()
                        }
                        data.append(row_data)
                        
                        # Log every 50th row to show progress without spamming
                        if i % 50 == 0:
                            self.logger.debug(f"Processed {i} rows...")
                    
                    else:
                        self.logger.warning(f"Row {i} has only {len(cols)} columns (expected 7)")
                        
                except Exception as row_error:
                    self.logger.error(f"Error processing row {i}: {str(row_error)}")
                    continue
            
            self.logger.info(f"Successfully extracted {len(data)} ZIP codes for {state_abbr.upper()}")
            return data
            
        except TimeoutException:
            self.logger.error(f"Timeout waiting for table to load for {state_abbr.upper()}")
            return []
        except NoSuchElementException as e:
            self.logger.error(f"Element not found for {state_abbr.upper()}: {str(e)}")
            return []
        except Exception as e:
            self.logger.error(f"Unexpected error extracting data for {state_abbr.upper()}: {str(e)}")
            return []
    
    def get_all_states_data(self, states=None):
        """Extract data for multiple states with comprehensive logging"""
        if states is None:
            states = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI', 'WA', 'WV', 'WI', 'WY']
        
        self.logger.info(f"Starting extraction for {len(states)} states: {', '.join(states).upper()}")
        all_data = []
        successful_states = []
        failed_states = []
        
        for state_index, state in enumerate(states, 1):
            self.logger.info(f"Processing state {state_index}/{len(states)}: {state.upper()}")
            
            state_data = self.get_state_data(state)
            
            if state_data:
                all_data.extend(state_data)
                successful_states.append(state.upper())
                self.logger.info(f"State {state.upper()} completed: {len(state_data)} records")
            else:
                failed_states.append(state.upper())
                self.logger.warning(f"State {state.upper()} failed - no data extracted")
            
            # Add a small delay to be respectful to the server
            if state_index < len(states):  # Don't delay after the last state
                self.logger.debug("Waiting 2 seconds before next state...")
                time.sleep(2)
        
        # Summary logging
        self.logger.info("=" * 50)
        self.logger.info("EXTRACTION SUMMARY")
        self.logger.info("=" * 50)
        self.logger.info(f"Total states processed: {len(states)}")
        self.logger.info(f"Successful states: {len(successful_states)} - {', '.join(successful_states)}")
        self.logger.info(f"Failed states: {len(failed_states)} - {', '.join(failed_states)}")
        self.logger.info(f"Total records extracted: {len(all_data)}")
        self.logger.info("=" * 50)
        
        return all_data
    
    def save_to_text_file(self, data, filename="zip_codes_data.txt"):
        """Save extracted data to a text file with logging"""
        self.logger.info(f"Attempting to save data to text file: {filename}")
        
        try:
            with open(filename, 'w', encoding='utf-8') as file:
                # Write header
                file.write("State\tZIP Code\tClassification\tCity\tCounty\tArea Codes\tPopulation\tPopulation %\n")
                
                # Write data
                for i, item in enumerate(data, 1):
                    line = f"{item['state']}\t{item['zip_code']}\t{item['classification']}\t{item['city']}\t{item['county']}\t{item['area_codes']}\t{item['population']}\t{item['population_percent']}\n"
                    file.write(line)
                    
                    # Log progress for large files
                    if i % 100 == 0:
                        self.logger.debug(f"Written {i} records to text file...")
            
            self.logger.info(f"Successfully saved {len(data)} records to {filename}")
            
        except Exception as e:
            self.logger.error(f"Failed to save text file {filename}: {str(e)}")
            raise
    
    def save_to_csv(self, data, filename="zip_codes_data.csv"):
        """Save extracted data to CSV file with logging"""
        self.logger.info(f"Attempting to save data to CSV file: {filename}")
        
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False)
            self.logger.info(f"Successfully saved {len(data)} records to {filename}")
            
            # Log some basic statistics about the data
            self.logger.debug(f"DataFrame shape: {df.shape}")
            if not df.empty:
                self.logger.debug(f"States in data: {df['state'].unique().tolist()}")
                self.logger.debug(f"Classification types: {df['classification'].unique().tolist()}")
                
        except Exception as e:
            self.logger.error(f"Failed to save CSV file {filename}: {str(e)}")
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
    extractor = ZipCodeExtractor(headless=True, log_level=logging.DEBUG)
    
    start_time = time.time()
    extractor.logger.info("ZIP Code Extraction Script Started")
    
    try:
        # Define states to scrape
        states_to_scrape = ['AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'VI', 'WA', 'WV', 'WI', 'WY']  # Add more state abbreviations as needed
        
        extractor.logger.info(f"Starting extraction process for {len(states_to_scrape)} states")
        
        # Extract data
        all_data = extractor.get_all_states_data(states_to_scrape)
        
        if all_data:
            # Save to multiple formats
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            text_filename = f"all_states_zip_codes_{timestamp}.txt"
            csv_filename = f"all_states_zip_codes_{timestamp}.csv"
            
            extractor.save_to_text_file(all_data, text_filename)
            extractor.save_to_csv(all_data, csv_filename)
            
            # Final summary
            end_time = time.time()
            duration = end_time - start_time
            extractor.logger.info("=" * 60)
            extractor.logger.info("EXTRACTION COMPLETED SUCCESSFULLY!")
            extractor.logger.info(f"Total duration: {duration:.2f} seconds")
            extractor.logger.info(f"Records per second: {len(all_data)/duration:.2f}")
            extractor.logger.info(f"Output files: {text_filename}, {csv_filename}")
            extractor.logger.info("=" * 60)
            
        else:
            extractor.logger.error("No data was extracted from any state!")
            
    except Exception as e:
        extractor.logger.critical(f"Script failed with critical error: {str(e)}", exc_info=True)
    
    finally:
        extractor.close()
        extractor.logger.info("Script execution completed")

if __name__ == "__main__":
    main()