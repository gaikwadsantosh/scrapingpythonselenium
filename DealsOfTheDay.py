import json
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import math

class DealsOfTheDay:

    def __init__(self, driver, masterProductsFile, file, searchCategory, searchSubCategory):
        self.masterProductsFile = masterProductsFile
        self.file = file
        self.driver = driver
        self.searchCategory = searchCategory
        self.searchSubCategory = searchSubCategory

    def write_dealsoftheday(self, discriminator, headerCSS, productTitleCSS, productUrlCSS, imageUrlCSS, priceDiscountCSS, dealsEndtimeCSS, productCount):
        self.discriminator = discriminator
        self.headerCSS = headerCSS
        self.productTitleCSS = productTitleCSS
        self.productUrlCSS = productUrlCSS
        self.imageUrlCSS = imageUrlCSS
        self.priceDiscountCSS = priceDiscountCSS
        self.dealsEndtimeCSS  = dealsEndtimeCSS
        self.productCount = productCount

        # navigate to the starting page
        self.driver.get(self.driver.current_url)
        print("Processing Products from :" + str(self.productCount))
        #print(self.driver.title)
        #print(self.driver.current_url)

        # wait for the elements to load
        wait = WebDriverWait(self.driver, 10)

        #get all the product headings from amazon page
        dealsoftheday_headings = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.headerCSS)))
        #print(len(dealsoftheday_headings))

        #declare disctionary to store products information
        try:
            masterProducts_List = []

            contents = self.file.read()
            if contents:
                dealsOfTheDay_List = json.loads(contents)
            else:
                dealsOfTheDay_List = []
        except FileNotFoundError:
            dealsOfTheDay_List = []

        rowNumber = 0
        for dealsoftheday_heading in dealsoftheday_headings:
            try:
                self.productCount += 1
                rowNumber += 1
                dealsoftheday_product_titles = dealsoftheday_heading.find_elements(By.CSS_SELECTOR, self.productTitleCSS)
                dealsoftheday_product_urls = dealsoftheday_heading.find_elements(By.CSS_SELECTOR, self.productUrlCSS)
                dealsoftheday_image_urls = dealsoftheday_heading.find_elements(By.CSS_SELECTOR, self.imageUrlCSS)
                dealsoftheday_price_discounts = dealsoftheday_heading.find_elements(By.CSS_SELECTOR, self.priceDiscountCSS)
                dealsoftheday_deals_message = dealsoftheday_heading.find_elements(By.CSS_SELECTOR, self.dealsEndtimeCSS)

                itemIndex = 0
                try:
                    dealsoftheday_product_title = dealsoftheday_product_titles[itemIndex].text
                except IndexError:
                    continue
                dealsoftheday_product_url = dealsoftheday_product_urls[itemIndex].get_attribute('href')
                dealsoftheday_image_url = dealsoftheday_image_urls[itemIndex].get_attribute('src')
                dealsoftheday_price_discount = dealsoftheday_price_discounts[itemIndex].text
                try:
                    dealsoftheday_deal_Message = dealsoftheday_deals_message[itemIndex].text
                except IndexError:
                    dealsoftheday_deal_Message = ""

                progress = math.floor(rowNumber*100/len(dealsoftheday_headings))
                self.print_progress(progress)

                dealsOfTheDay_List.append({
                    'Discriminator': self.discriminator,
                    'RowNumber': self.productCount,
                    'SearchCategory': self.searchCategory,
                    'SearchSubCategory': self.searchSubCategory,
                    'ProductTitle': dealsoftheday_product_title,
                    'ProductUrl': dealsoftheday_product_url,
                    'ImageUrl': dealsoftheday_image_url,
                    'PriceDiscount': dealsoftheday_price_discount,
                    'DealMessage': dealsoftheday_deal_Message
                })

                masterProducts_List.append({
                    'Discriminator': "MasterData",
                    'RowNumber': self.productCount,
                    'SearchCategory': self.searchCategory,
                    'SearchSubCategory': self.searchSubCategory,
                    'ProductTitle': dealsoftheday_product_title
                })

            except StaleElementReferenceException:
                print(StaleElementReferenceException)
                dealsoftheday_headings = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, self.productTitleCSS)))
                continue

        #convert whole dictionary object to JSON and write to file
        # Dump the array of JSON objects to a temporary list
        temp_list = json.dumps(dealsOfTheDay_List, indent=None)
        # Write the temporary list to the file, excluding square brackets
        self.file.write(temp_list[1:-1])
        # Add a comma to separate JSON objects in the array
        self.file.write(",")
        ###############
        temp_list = json.dumps(masterProducts_List, indent=None)
        self.masterProductsFile.write(temp_list[1:-1])
        self.masterProductsFile.write(",")

        print('completed')

    def read_dealsoftheday(self, fileNames=[]):
        if not fileNames:
            fileNames = [self.fileName]

        merged_products = []
        for _fileName in fileNames:
            with open(_fileName + ".json", "r") as f:
                _productString = f.read()
                jsonContent = json.loads(_productString)
                merged_products.extend(jsonContent.values())

        merged_products_dict = {item['ProductTitle']: item for item in merged_products}
        sorted_products = sorted(merged_products_dict.values(), key=self.get_discount_value, reverse=True)
        type(sorted_products)
        for product in sorted_products:
            print(product)
            '''
            print(product['ProductTitle'])
            '''

    def print_progress(self, progress):
        print("\rProgress: [{0}] {1}%".format("#" * progress, progress), end="")

    # Define a function to extract the discount value
    def get_discount_value(product):
        # Extract the numeric value from the discount string
        discount_str = product['PriceDiscount']
        value_str = ''.join(filter(str.isdigit, discount_str))
        return int(value_str)
