Deals of the Day Scraper
This project is a Python-based web scraper designed to extract "Deals of the Day" from e-commerce websites like Amazon and Flipkart. The tool uses Selenium for web automation and dynamically retrieves information about products, such as titles, URLs, images, discounts, and deal expiry times.

Table of Contents
1. Features
2. Installation
3. Usage
    Menu Options
    Amazon and Flipkart Scraping
4. Dependencies
5. Code Overview
    DealsOfTheDay.py
    main.py
6. File Outputs
7. Known Limitations
8. License

Features
    Scrape daily deals from Amazon and Flipkart.
    Save product data, including:
    Product title
    Product URL
    Image URL
    Discount information
    Deal message (e.g., expiry time)
    Save data in JSON format for easy processing.
    Dynamically process paginated results for large data sets.
    Headless browser support for efficient execution.

Installation
    Clone this repository:
        git clone https://github.com/gaikwadsantosh/scrapingpythonselenium)
    Install the required Python packages:
        pip install selenium
        Download the appropriate ChromeDriver for your Chrome browser version from ChromeDriver Downloads and place it in the project directory.
    Ensure you have Python 3 installed. If not, download it from Python.org.

Usage
    Running the Script
        To start the application, run the main.py file:
            python main.py

    Menu Options
        The script provides the following menu options:
        1. Write Amazon Deals: Scrapes deals from Amazon and saves them in amazonDeals.json.
        2. Write Flipkart Deals: Scrapes deals from Flipkart and saves them in flipkartDeals.json.
        3. Read Amazon Deals: Reads and displays previously scraped Amazon deals.
        4. Read Flipkart Deals: Reads and displays previously scraped Flipkart deals.
        5. Read All Deals: Merges and displays deals from both Amazon and Flipkart.
        6. Quit: Exits the application.

    Amazon and Flipkart Scraping
        Amazon URL: https://www.amazon.in/deals?ref_=nav_cs_gb
        Flipkart URL: https://www.flipkart.com/offers-list/...
        The scraper navigates through multiple pages of deals and writes the results into JSON files.

Dependencies
    The project requires the following:
    1. Python 3.x
    2. Selenium: Install using pip install selenium.
    3. ChromeDriver: Ensure it matches your installed Chrome version.
    4. Google Chrome: Must be installed on your system.

Code Overview
    DealsOfTheDay.py
        This module contains the DealsOfTheDay class, which manages scraping and file operations. Key methods include:
        write_dealsoftheday(): Scrapes data from a given webpage, processes product details, and writes them into JSON files.
        read_dealsoftheday(): Reads JSON files and merges/sorts data by discounts.
        Utility Functions:
        get_discount_value(product): Extracts numeric discount values for sorting.
        print_progress(progress): Displays progress of scraping.
    main.py
        This script provides a user-friendly menu to interact with the scraper. Key functions include:
        writeAmazonDeals() and writeFlipkartDeals(): Automate scraping for Amazon and Flipkart respectively.
        readAmazonDeals() and readFlipkartDeals(): Load and display data for specific platforms.
        readAllDeals(): Merges data from all sources.
    File Outputs
        amazonDeals.json: Contains scraped Amazon deals.
        flipkartDeals.json: Contains scraped Flipkart deals.
        MasterProducts.json: A master list consolidating all product data.

Known Limitations
    Requires manual update of CSS selectors if website structures change.
    Limited to predefined Amazon and Flipkart URLs.
    Relies on Chrome and ChromeDriver for scraping.
