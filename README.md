# Extract Zips

* Extract ZIP code data from the tab-delimited file format and return a dictionary mapping ZIP codes to city/state/county info
* Save the ZIP code mapping as a Python dictionary
* Save the ZIP code mapping as a JavaScript object
* Filter the ZIP code mapping by state
* Search for ZIP codes by city name (case-insensitive)
* Load ZIP code mapping directly from file and return as dictionary
  
# Zip Sort

* Sort ZIP codes numerically and export to a new file
* Convert ZIP codes to string and pad with leading zeros to ensure 5-digit format

**Usage:**

**Read the original file**

      input_file = "zip_full_dump.txt"
      
      output_file = "zip_codes_sorted.txt"

If none of the above works well enough for you, use libre office calc.

# ZIP Code Extractor - Selenium Web Scraper

A Chrome driver script used to extract zips codes off of https://www.zip-codes.com/ on all 50 states and territories using Selenium.

## Features

- Extracts ZIP code information including:
  - ZIP Code
  - Classification (Standard, PO Box, etc.)
  - City
  - County
  - Area Codes
  - Population
  - Population Percentage
- Supports all 50 states + territories
- Saves data in both CSV and text formats
- Comprehensive logging system
- Headless browser option
- Error handling and retry logic

## Installation

### 1. Prerequisites

- Python 3.7+
- Chrome browser installed
- ChromeDriver (can be installed automatically with `webdriver-manager`)

### 2. Clone the Repository


git clone https://github.com/airborne-commando/zip-extractor.git
cd zip-code-extractor


### 3. Create Virtual Environment (Recommended)


# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate


### 4. Install Dependencies


pip install -r requirements.txt


If `requirements.txt` doesn't exist, install packages manually:


pip install selenium pandas webdriver-manager


## Configuration

### ChromeDriver Setup

The script uses `webdriver-manager` to automatically handle ChromeDriver installation. However, if you prefer manual setup:

1. Download ChromeDriver from: https://sites.google.com/chromium.org/driver/
2. Ensure it matches your Chrome browser version
3. Add ChromeDriver to your system PATH or place it in the script directory

## Usage

### Basic Usage

Run the script with default settings:

python zip-extractor.py

### Running for Specific States

Modify the `states_to_scrape` list in the `main()` function:


# For specific states only
states_to_scrape = ['CA', 'NY', 'TX', 'FL']


## Output Files

The script generates two output files with timestamps:

1. **Text file** (`all_states_zip_codes_YYYYMMDD_HHMMSS.txt`):
   - Tab-separated values
   - Includes header row

2. **CSV file** (`all_states_zip_codes_YYYYMMDD_HHMMSS.csv`):
   - Comma-separated values
   - Can be opened in Excel, Google Sheets, etc.

### Output Format

| Column | Description |
|--------|-------------|
| state | State abbreviation (e.g., CA) |
| zip_code | 5-digit ZIP code |
| classification | ZIP code type (Standard, PO Box, etc.) |
| city | Associated city |
| county | County name |
| area_codes | Telephone area codes |
| population | Population count |
| population_percent | Population percentage |

## Logging

The script creates detailed log files:

- **Console output**: Real-time progress monitoring
- **Log file**: `zip_extraction_YYYYMMDD_HHMMSS.log`
- Log levels: DEBUG, INFO, WARNING, ERROR

## Troubleshooting

### Common Issues

1. **ChromeDriver version mismatch**
   - Solution: Use `webdriver-manager` or update ChromeDriver

2. **Timeout errors**
   - Solution: Increase wait times in the script
   - Check internet connection

3. **Element not found**
   - Solution: Website structure may have changed
   - Update selectors in the code

4. **Memory issues**
   - Solution: Process fewer states at once
   - Add more delays between requests

### Debug Mode

Run with increased verbosity by modifying the log level:


# Change in main() function
extractor = ZipCodeExtractor(headless=True, log_level=logging.DEBUG)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational purposes. Please ensure you comply with the target website's terms of service and applicable laws when using this script.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the log files
3. Open an issue in the GitHub repository

--------

**Charts**

--------

**Note: some zips have zero of a populous.**

| State | State Full | State Capital | ZIP Range | ZIP Quantity | State founded |
|-------|------------|-----------|-----------|-----|-------------------|
| AL | Alabama | Montgomery | 35004 to 36925 | 838 | December 14, 1819 |
| AK | Alaska | Juneau | 99501 to 99950 | 274 | January 3, 1959 |
| AZ | Arizona | Phoenix | 85001 to 86556 | 567 | February 14, 1912 |
| AR | Arkansas | Little Rock | 71601 to 72959 | 709 | June 15, 1836 |
| CA | California | Sacramento | 90001 to 96162 | 2653 | September 9, 1850 |
| CO | Colorado | Denver | 80001 to 81658 | 662 | August 1, 1876 |
| CT | Connecticut | Hartford | 06001 to 06928 | 438 | January 9, 1788 |
| DE | Delaware | Dover | 19701 to 19980 | 98 | December 7, 1787 |
| FL | Florida | Tallahassee | 32003 to 34997 | 1490 | March 3, 1845 |
| GA | Georgia | Atlanta | 30002 to 39901 | 973 | January 2, 1788 |
| HI | Hawaii | Honolulu | 96701 to 96898 | 139 | August 21, 1959 |
| ID | Idaho | Boise | 83201 to 83877 | 325 | July 3, 1890 |
| IL | Illinois | Springfield | 60001 to 62999 | 1588 | December 3, 1818 |
| IN | Indiana | Indianapolis | 46001 to 47997 | 987 | December 11, 1816 |
| IA | Iowa | Des Moines | 50001 to 52809 | 1063 | December 28, 1846 |
| KS | Kansas | Topeka | 66002 to 67954 | 756 | January 29, 1861 |
| KY | Kentucky | Frankfort | 40003 to 42788 | 962 | June 1, 1792 |
| LA | Louisiana | Baton Rouge | 70001 to 71497 | 725 | April 30, 1812 |
| ME | Maine | Augusta | 03901 to 04992 | 488 | March 15, 1820 |
| MD | Maryland | Annapolis | 20588 to 21930 | 622 | April 28, 1788 |
| MA | Massachusetts | Boston | 01001 to 05544 | 703 | February 6, 1788 |
| MI | Michigan | Lansing | 48001 to 49971 | 1170 | January 26, 1837 |
| MN | Minnesota | Saint Paul | 55001 to 56763 | 1031 | May 11, 1858 |
| MS | Mississippi | Jackson | 38601 to 39776 | 533 | December 10, 1817 |
| MO | Missouri | Jefferson City | 63001 to 65899 | 1171 | August 10, 1821 |
| MT | Montana | Helena | 59001 to 59937 | 405 | November 8, 1889 |
| NE | Nebraska | Lincoln | 68001 to 69367 | 620 | March 1, 1867 |
| NV | Nevada | Carson City | 88901 to 89883 | 254 | October 31, 1864 |
| NH | New Hampshire | Concord | 03031 to 03897 | 284 | June 21, 1788 |
| NJ | New Jersey | Trenton | 07001 to 08989 | 731 | December 18, 1787 |
| NM | New Mexico | Santa Fe | 87001 to 88439 | 426 | January 6, 1912 |
| NY | New York | Albany | 00501 to 14925 | 2208 | July 26, 1788 |
| NC | North Carolina | Raleigh | 27006 to 28909 | 1090 | November 21, 1789 |
| ND | North Dakota | Bismarck | 58001 to 58856 | 407 | November 2, 1889 |
| OH | Ohio | Columbus | 43001 to 45999 | 1447 | March 1, 1803 |
| OK | Oklahoma | Oklahoma City | 73001 to 74966 | 776 | November 16, 1907 |
| OR | Oregon | Salem | 97001 to 97920 | 486 | February 14, 1859 |
| PA | Pennsylvania | Harrisburg | 15001 to 19640 | 2213 | December 12, 1787 |
| RI | Rhode Island | Providence | 02801 to 02940 | 91 | May 19, 1790 |
| SC | South Carolina | Columbia | 29001 to 29945 | 539 | May 23, 1788 |
| SD | South Dakota | Pierre | 57001 to 57799 | 394 | November 2, 1889 |
| TN | Tennessee | Nashville | 37010 to 38589 | 796 | June 1, 1796 |
| TX | Texas | Austin | 73301 to 88595 | 2655 | December 29, 1845 |
| UT | Utah | Salt Lake City | 84001 to 84791 | 347 | January 4, 1896 |
| VT | Vermont | Montpelier | 05001 to 05907 | 309 | March 4, 1791 |
| VA | Virginia | Richmond | 20101 to 24658 | 1241 | June 25, 1788 |
| WA | Washington | Olympia | 98001 to 99403 | 733 | November 11, 1889 |
| WV | West Virginia | Charleston | 24701 to 26886 | 856 | June 20, 1863 |
| WI | Wisconsin | Madison | 53001 to 54990 | 898 | May 29, 1848 |
| WY | Wyoming | Cheyenne | 82001 to 83414 | 195 | July 10, 1890 |

--------

**Area Codes**

--------

| State/Territory | Area Codes (Think phone number) |
|-----------------|------------|
| Alabama | 205, 251, 256, 334, 659, 938 |
| Alaska | 907 |
| Arizona | 480, 520, 602, 623, 928 |
| Arkansas | 327, 479, 501, 870 |
| California | 209, 213, 279, 310, 323, 341, 350, 369, 408, 415, 424, 442, 510, 530, 559, 562, 619, 626, 628, 650, 657, 661, 669, 707, 714, 747, 760, 805, 818, 820, 831, 840, 858, 909, 916, 925, 949, 951 |
| Colorado | 303, 719, 720, 970, 983 |
| Connecticut | 203, 475, 860, 959 |
| Delaware | 302 |
| Florida | 239, 305, 321, 324, 352, 386, 407, 448, 561, 645, 656, 689, 727, 728, 754, 772, 786, 813, 850, 863, 904, 941, 954 |
| Georgia | 229, 404, 470, 478, 678, 706, 762, 770, 912, 943 |
| Hawaii | 808 |
| Idaho | 208, 986 |
| Illinois | 217, 224, 309, 312, 331, 447, 464, 618, 630, 708, 730, 773, 779, 815, 847, 861, 872 |
| Indiana | 219, 260, 317, 463, 574, 765, 812, 930 |
| Iowa | 319, 515, 563, 641, 712 |
| Kansas | 316, 620, 785, 913 |
| Kentucky | 270, 364, 502, 606, 859 |
| Louisiana | 225, 318, 337, 504, 985 |
| Maine | 207 |
| Maryland | 227, 240, 301, 410, 443, 667 |
| Massachusetts | 339, 351, 413, 508, 617, 774, 781, 857, 978 |
| Michigan | 231, 248, 269, 313, 517, 586, 616, 734, 810, 906, 947, 989 |
| Minnesota | 218, 320, 507, 612, 651, 763, 952 |
| Mississippi | 228, 601, 662, 769 |
| Missouri | 235, 314, 417, 557, 573, 636, 660, 816, 975 |
| Montana | 406 |
| Nebraska | 308, 402, 531 |
| Nevada | 702, 725, 775 |
| New Hampshire | 603 |
| New Jersey | 201, 551, 609, 640, 732, 848, 856, 862, 908, 973 |
| New Mexico | 505, 575 |
| New York | 212, 315, 329, 332, 347, 363, 516, 518, 585, 607, 624, 631, 646, 680, 716, 718, 838, 845, 914, 917, 929, 934 |
| North Carolina | 252, 336, 472, 704, 743, 828, 910, 919, 980, 984 |
| North Dakota | 701 |
| Ohio | 216, 220, 234, 283, 326, 330, 380, 419, 436, 440, 513, 567, 614, 740, 937 |
| Oklahoma | 405, 539, 572, 580, 918 |
| Oregon | 458, 503, 541, 971 |
| Pennsylvania | 215, 223, 267, 272, 412, 445, 484, 570, 582, 610, 717, 724, 814, 835, 878 |
| Rhode Island | 401 |
| South Carolina | 803, 839, 843, 854, 864 |
| South Dakota | 605 |
| Tennessee | 423, 615, 629, 731, 865, 901, 931 |
| Texas | 210, 214, 254, 281, 325, 346, 361, 409, 430, 432, 469, 512, 682, 713, 726, 737, 806, 817, 830, 832, 903, 915, 936, 940, 945, 956, 972, 979 |
| Utah | 385, 435, 801 |
| Vermont | 802 |
| Virginia | 276, 434, 540, 571, 686, 703, 757, 804, 826, 948 |
| Washington | 206, 253, 360, 425, 509, 564 |
| Washington, DC | 202, 771 |
| West Virginia | 304, 681 |
| Wisconsin | 262, 274, 353, 414, 534, 608, 715, 920 |
| Wyoming | 307 |
| **Territories** | |
| American Samoa | 684 |
| Guam | 671 |
| Northern Mariana Islands | 670 |
| Puerto Rico | 787, 939 |
| Virgin Islands | 340 |

--------

Contains python scripts to extract and sort zip codes from a website, will edit this readme later.

[This text file](./zip_codes_sorted.txt) contains all the raw zip codes in a sorted text file in numerical order (lowest to highest), while this contains the zips from [highest to lowest](./zip_full_dump.txt).

Will have to figure out how to sort just by state, eventually.

# External Links:

[ZIP Code Database Listings, Maps, and Boundary Data - Zip-Codes](https://www.zip-codes.com/)

[United States ZIP Code - codigo postal](https://codigo-postal.co/en-us/usa/)

[US Area Code Listings by State - allareacodes](https://www.allareacodes.com/area_code_listings_by_state.htm)

[Voter extraction (lite)](https://github.com/airborne-commando/tampermonkey-collection?tab=readme-ov-file) Is a component of both of these.

[Voter reg status: tampermonkey edition](https://github.com/airborne-commando/tampermonkey-collection?tab=readme-ov-file#voter-reg-status-tampermonkey-edition)