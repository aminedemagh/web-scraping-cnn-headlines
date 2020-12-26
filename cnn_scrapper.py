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
    href = li.find_elements_by_xpath(".//child::a")
    shref = [ref.get_attribute('href') for ref in href]
    atext = [ref.text for ref in href]
    print(li.text + "\n ------------------------------------\n" + str(shref)
     + "\n-----------------------------------------\n" + str(atext) 
      +"\n _______________________________________________________________ \n")

#intl_homepage1-zone-1