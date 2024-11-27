import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
from DealsOfTheDay import DealsOfTheDay

class Menu:

    def __init__(self):
        self.options = {
            "1": self.writeAmazonDeals,
            "2": self.writeFlipkartDeals,
            "3": self.readAmazonDeals,
            "4": self.readFlipkartDeals,
            "5": self.readAllDeals,
            "6": self.quit
        }

    def display(self):
        print("Please select an option:")
        print("1. Write Amazon Deals")
        print("2. Write Flipkart Deals")
        print("3. Read Amazon Deals")
        print("4. Read Flipkart Deals")
        print("5. Read All Deals")
        print("6. Quit")

    def run(self):
        while True:
            self.display()
            choice = input("Enter your choice (1-6): ")
            action = self.options.get(choice)
            if action:
                action()
            else:
                print("Invalid choice")

    def writeAmazonDeals(self):
        # Write Amazon Deals
        discriminator = "Amazon"
        masterProductsFileName = "MasterProducts"
        fileName = "amazonDeals"
        scrapeURL = "https://www.amazon.in/deals?ref_=nav_cs_gb"
        headerCSS = "div.DealGridItem-module__dealItemDisplayGrid_e7RQVFWSOrwXBX4i24Tqg.DealGridItem-module__withBorders_2jNNLI6U1oDls7Ten3Dttl.DealGridItem-module__withoutActionButton_2OI8DAanWNRCagYDL2iIqN"
        productTitleCSS = "div.DealContent-module__truncate_sWbxETx42ZPStTc9jwySW"
        productUrlCSS = "a.a-link-normal.DealCard-module__linkOutlineOffset_2fc037WfeGSjbFp1CAhOUn"
        imageUrlCSS = "img.DealImage-module__imageObjectFit_1G4pEkUEzo9WEnA3Wl0XFv"
        priceDiscountCSS = "div.BadgeAutomatedLabel-module__badgeAutomatedLabel_2Teem9LTaUlj6gBh5R45wd"
        dealsMessageCSS = "div.DealMessaging-module__dealMessaging_1EIwT6BUaB6vCKvPVEbAEV"
        searchCategory = "Today's Deals"
        searchSubCategory = "All Deals"
        self.writeAllPages(discriminator, masterProductsFileName, fileName, scrapeURL, headerCSS, productTitleCSS, productUrlCSS, imageUrlCSS, priceDiscountCSS,
                              dealsMessageCSS, searchCategory, searchSubCategory)

    def writeFlipkartDeals(self):
        # Write FlipKart Deals
        discriminator = "Flipkart"
        masterProductsFileName = "MasterProducts"
        fileName = "flipkartDeals"
        scrapeURL = "https://www.flipkart.com/offers-list/content?screen=dynamic&pk=themeViews%3DDOTD%3Aviewalldesktop~widgetType%3DdealCard~contentType%3Dneo&wid=2.dealCard.OMU&fm=neo%2Fmerchandising&iid=M_d93a8522-48f4-4de9-bbf9-ba69ad3014f3_1_372UD5BXDFYS_MC.G6ZC4RAJ9OHU&otracker=hp_rich_navigation_8_1.navigationCard.RICH_NAVIGATION_Top%2BOffers_G6ZC4RAJ9OHU&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_8_L0_view-all&cid=G6ZC4RAJ9OHU"
        headerCSS = "div._1FNrEw"
        productTitleCSS = "div._3LU4EM"
        productUrlCSS = "a._6WQwDJ"
        imageUrlCSS = "img._396cs4"
        priceDiscountCSS = "div._2tDhp2"
        dealsMessageCSS = "div._3khuHA"
        searchCategory = "Today's Deals"
        searchSubCategory = "All Deals"
        print("Processing .... Writing Deals of the Day to " + fileName+".json")
        self.writeAllPages(discriminator, masterProductsFileName, fileName, scrapeURL, headerCSS, productTitleCSS, productUrlCSS, imageUrlCSS, priceDiscountCSS,
                              dealsMessageCSS, searchCategory, searchSubCategory)

    def writeAllPages(self, discriminator, masterProductsFileName, fileName, scrapeURL, headerCSS, productTitleCSS, productUrlCSS, imageUrlCSS, priceDiscountCSS, dealsMessageCSS, searchCategory, searchSubCategory):
        print("Processing .... Writing Deals of the Day to " + fileName+".json")

        # Set Chrome options to run in headless mode
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_service = Service('../chromedriver.exe')
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        # navigate to the starting page
        driver.get(scrapeURL)

        # wait for the page to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, headerCSS)))

        #delete existing json file before creating new one
        if os.path.exists(fileName+".json"):
            os.remove(fileName+".json")
            print("Old File " + fileName + ".json deleted.")
        #create file object
        file = open(fileName+".json", "a+", encoding='utf-8')
        file_size = file.tell()
        if file_size == 0:
            file.write("[")  # Start JSON array if the file is empty
        else:
            # Remove the last character (probably a comma) from the file
            file.seek(file_size - 1)
            file.truncate()


        #create Master Products file
        if os.path.exists(masterProductsFileName+".json"):
            os.remove(masterProductsFileName+".json")
            print("Old File " + masterProductsFileName + ".json deleted.")
        #create Master Products file object
        masterProductsFile = open(masterProductsFileName +".json", "a+", encoding='utf-8')
        file_size = masterProductsFile.tell()
        if file_size == 0:
            masterProductsFile.write("[")  # Start JSON array if the file is empty
        else:
            # Remove the last character (probably a comma) from the file
            masterProductsFile.seek(file_size - 1)
            masterProductsFile.truncate()

        # create object of DealsOfTheDay class & process the page
        obj_dealsoftheday = DealsOfTheDay(driver, masterProductsFile, file, searchCategory, searchSubCategory)

        pageNumber = 0
        pageSize=60
        while True:
            os.system('cls')
            pageNumber += 1
            # temporarily stop processing after 10 pages, need to be removed at the time of actual run
            if pageNumber==11:
                break
            print("Processing Page:- " + str(pageNumber))
            print(driver.current_url)

            # set updated driver
            obj_dealsoftheday.driver = driver
            obj_dealsoftheday.write_dealsoftheday(discriminator, headerCSS, productTitleCSS, productUrlCSS, imageUrlCSS,
                                              priceDiscountCSS, dealsMessageCSS, productCount=pageSize*(pageNumber-1))

            # find the "Next" link element
            next_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Next")))

            # if no next link then exit loop
            if not next_link:
                print("Next Button not found, exiting...")
                break

            # click the "Next" link
            next_link.click()
            # wait for the elements to load
            time.sleep(5)
        # close the driver
        driver.close()
        driver.quit()

        # Read the entire file and truncate it
        file.seek(0)
        contents = file.read()
        file.seek(0)
        file.truncate()
        # Rewrite the contents excluding the last comma
        file.write(contents.rstrip(','))
        file.write("]")


        # Read the entire file and truncate it
        masterProductsFile.seek(0)
        contents = masterProductsFile.read()
        masterProductsFile.seek(0)
        masterProductsFile.truncate()
        # Rewrite the contents excluding the last comma
        masterProductsFile.write(contents.rstrip(','))
        masterProductsFile.write("]")

        #close file
        file.close()
        masterProductsFile.close()

    def readAllDeals(self):
        # Read All Deals
        dealsoftheday = DealsOfTheDay()
        print("Processing .... Reading All Deals of the Day")
        fileNames = ["flipkartDeals", "amazonDeals"]
        dealsoftheday.read_dealsoftheday(fileNames)

    def readAmazonDeals(self):
        # Read Amazon Deals
        fileName = "amazonDeals"
        dealsoftheday = DealsOfTheDay(fileName)
        print("Processing .... Reading Deals of the Day from " + fileName+".json")
        dealsoftheday.read_dealsoftheday()

    def readFlipkartDeals(self):
        # Read FlipKart Deals
        fileName = "flipkartDeals"
        dealsoftheday = DealsOfTheDay(fileName)
        print("Processing .... Reading Deals of the Day from " + fileName+".json")
        dealsoftheday.read_dealsoftheday()

    def quit(self):
        print("Goodbye!")
        exit()

if __name__ == "__main__":
    menu = Menu()
    menu.run()
