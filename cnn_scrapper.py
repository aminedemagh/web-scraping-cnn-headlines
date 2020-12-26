from selenium import webdriver
from phantomjs import phantom
#driver = webdriver.Chrome(r"C:/Users/ACER/Desktop/chromedriver.exe")
driver = webdriver.PhantomJS("phantomjs.exe")
driver.set_window_size(1120, 550)
driver.get('https://edition.cnn.com')
# Fetch the first section of the cnn website
section1 = driver.find_element_by_id("intl_homepage1-zone-1")
lis = section1.find_elements_by_xpath(".//child::li")
hrefs = []
#print(lis.text)
for li in lis:
    if li.text == '': continue    
    atags = li.find_elements_by_xpath(".//child::a")
    headlines = []
    for a in atags:
        title = a.text
        if title == "": continue
        href = a.get_attribute('href')
        headlines.append((title, href))
    print(li.text + "\n ------------------------------------\n" + str(headlines)
    +"\n _______________________________________________________________ \n")

#intl_homepage1-zone-1