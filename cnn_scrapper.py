from selenium import webdriver
from phantomjs import phantom

def getWebDriver():
    ''' Returns a phantomjs WebDriver'''
    driver = webdriver.PhantomJS("phantomjs.exe")
    driver.set_window_size(1120, 550)
    return driver

def format_title(title):
    ''' Returns the given string without '•' character and after
        removing any leading or trailing whitespaces'''
    return title.replace('•', '').strip()

def group_titles(headlines):
    '''Returns a list of tuples where each tuple is of the form (list of
       titles corresponding to a signle href, the href).
       This list is generared from the given list of tuples of the form (title, href)
       that contains distinc tuples for different titles with the same href.
       This function groups the titles that share the same href in a single tuple
    
    Parameters:
    ---------
    headlines : list
        A list of tuples of the form (title, href)

    Returns
    -------
    list
        A list of tuples of the form ([list of titles], href)
    
    '''
    # Get a list of the unique hrefs
    unique_hrefs = list(set([href for _, href in headlines]))
    grouped_titles = []
    # Group the corresponding titles for each href
    for unique_href in unique_hrefs:
        titles = []
        # Loops through the headlines to look for
        # the titles that correspond to the current href
        for title, href in headlines:
            if href == unique_href:
                titles.append(title)
        grouped_titles.append((titles, href)) 

    return grouped_titles

def getHeadlines(webdriver):
    ''' Returns a list of tuples of the first headlines of https://edition.cnn.com
        Each tuple contains the title and the corresponding href

    Parameters
    ----------
    webdriver : webdriver
        A webdriver instance used to get the cnn webpage
    
    Returns
    -------
    list
        A list of tuples containing (the title, the href) of each headline
    '''
    webdriver.get('https://edition.cnn.com')
    # Fetch the first section of the cnn website
    # id = intl_homepage1-zone-1
    section1 = webdriver.find_element_by_id("intl_homepage1-zone-1")
    # Titles are listed in li tags under section1
    lis = section1.find_elements_by_xpath(".//child::li")
    # Each li tag contains a set of a tags
    # Some a tags contain images and others text 
    # This app is only interested in text and their corresponding href
    headlines = []
    for li in lis:
        # Ignore the iteration if the li tags doesn't contain any text
        if li.text == '' : continue    
        atags = li.find_elements_by_xpath(".//child::a")
        # The headlines for this list item
        li_headlines = []
        for a in atags:
            # Extract the titles
            title = a.text
            # Ignore the iteration if there's no text in it
            if title == "" : continue
            # Extract the corresponding href
            href = a.get_attribute('href')
            # Format title
            title = format_title(title)
            li_headlines.append((title, href))
        # Group the titles that share the same href
        headlines = headlines + group_titles(li_headlines)

    return headlines 

def is_article_supported(href):
    is_supported = False
    # Split the link into different part
    # The 3rd element indicates if the href is pointing 
    # to a general article: 'https://edition.cnn.com/2021/01/02/media/larry-king-covid-19/index.html'
    # or an article from a sub domain: 'https://edition.cnn.com/politics'
    # Here the number '2021'after 'edition.cnn.com' means that it's a general article that
    # is supported by this webscrapper.
    # The 'politics' in the second link means that it's from a subdomain and they
    # are not supported for now 
    link_elements = href.split('/')

    if link_elements[3].isnumeric():
        is_supported = True

    return is_supported

def get_articles(driver, headlines):
    #for headline in headlines:
    #    print(headline)
    for title, href in headlines:
        # Ignore the article if it's not supported
        if not is_article_supported(href) : continue
        driver.get(href)
        # Get the ptag that contains the date
        pdate = driver.find_elements_by_xpath('//p[@class="update-time"]')
        date = None
        if len(pdate) == 0:
            continue
        else:
            date = pdate[0].text
        
        # Get the paragraphs of the articles
        # They can be either in <div> or <p>
        paragraphs = driver.find_elements_by_xpath("//*[contains(@class, 'zn-body__paragraph')]")
        # Gather all the paragraphs in a signle content variable
        content = ""
        for p in paragraphs:
            content += p.text + "\n"
        
        for t in title:
            print("Article title: " + t + "\n"
                + "Article href: " + href + "\n"
                + "Article date: " + date + "\n\n"
                + "Article content:\n" + content + "\n"
                + "-------------------------------------------------------------------------\n")

driver = getWebDriver()
headlines = getHeadlines(driver)
get_articles(driver, headlines)




