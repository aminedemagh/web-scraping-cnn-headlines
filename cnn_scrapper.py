from selenium import webdriver
from phantomjs import phantom
#driver = webdriver.Chrome(r"C:/Users/ACER/Desktop/chromedriver.exe")
def getWebDriver():
    ''' Returns a phantomjs WebDriver'''
    driver = webdriver.PhantomJS("phantomjs.exe")
    driver.set_window_size(1120, 550)
    return driver

def getHeadlines(webdriver):
    webdriver.get('https://edition.cnn.com')
    # Fetch the first section of the cnn website
    # id = intl_homepage1-zone-1
    section1 = webdriver.find_element_by_id("intl_homepage1-zone-1")
    # Titles are listed in li tags under section1
    lis = section1.find_elements_by_xpath(".//child::li")
    # Each li tag contains a set of a tags
    # Some a tags contain images and others text 
    # This app is only interested in text and their corresponding href
    for li in lis:
        # Ignore the iteration if the li tags doesn't contain any text
        if li.text == '' : continue    
        atags = li.find_elements_by_xpath(".//child::a")
        headlines = []
        for a in atags:
            # Extract the titles
            title = a.text
            # Ignore the iteration if there's no text in it
            if title == "" : continue
            # Extract the corresponding href
            href = a.get_attribute('href')
            headlines.append((title, href))
        print(li.text + "\n ------------------------------------\n" + str(headlines)
        +"\n _______________________________________________________________ \n")

driver = getWebDriver()
getHeadlines(driver)




