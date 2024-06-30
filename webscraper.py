from bs4 import BeautifulSoup
import requests
import mysql.connector
from selenium import webdriver
import re
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Atharva@28",
  database="pricetracker"
)

mycursor = mydb.cursor()



def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs = ""
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs = text1[i - 1] + lcs
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return lcs

def partial_subsequence_match(pattern, text):
    lcs = longest_common_subsequence(pattern, text)
    return len(lcs) == min(len(pattern),len(text))


def get_google_search_results(id,website):
    query = ""
    query+=id+" "+website
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('a', href=True)
        urls = [link['href'] for link in search_results if link['href'].startswith("http")]
        for url in urls:          
            if(website=="croma"):
                
                pattern = 'www.croma.com'
                match = re.search(str(pattern), str(url))
                if match:
                    pattern = product_id_croma(url)
                    match = partial_subsequence_match(str(pattern),str(id))
                    if match:
                        return url
                    
            elif(website=="reliancedigital"):
                
                pattern = 'www.reliancedigital.in'
                match = re.search(str(pattern), str(url))
                
                if match:
                    pattern = product_id_reliance(url)
                    match = partial_subsequence_match(str(pattern),str(id))

                    if match:
                        return url
                    
            elif(website=="flipkart"):
                pattern = 'www.flipkart.com'
                match = re.search(str(pattern), str(url))
                if match:
                    pattern = product_id_flipkart(url)
                    match = partial_subsequence_match(str(pattern),str(id))
                    if match:
                        return url
                    
            else:
                pattern = 'www.vijaysales.com'
                match = re.search(str(pattern), str(url))
                if match:
                    pattern = product_id_vijaysales(url)
                    match = partial_subsequence_match(str(pattern),str(id))
                    if match:
                        return url

    else:
        print("Failed to fetch search results")
        return []
    
def get_img_src(url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                img_tag = soup.find('img', class_='img-responsive asp_img_cls')
                if img_tag:
                    src_value = img_tag.get('src')
                    return src_value
                else:
                    print("No img tag with the specified class found.")
            else:
                print(f"Failed to fetch page source. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")

def product_id_vijaysales(url):
    product_id = None
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        key = soup.find_all(class_='cls-ty sptyp')
        value = soup.find_all(class_='cls-vl spval')
        for i in range(0, len(key)):
            if(key[i].get_text().strip()=="MODEL NAME"):
                product_id = value[i].text.strip()
            if(key[i].get_text().strip()=="SKU"):
                product_id = value[i].text.strip()
                break
        return product_id
    except:
        return None

def product_id_croma(url):
    product_id = None
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        key = soup.find_all(class_='cp-specification-spec-title')
        value = soup.find_all(class_='cp-specification-spec-details')
        for i in range(len(key)):
            if(key[i].find('h4').get_text().strip() == "Model Number"):
                product_id = value[i].text.strip()
                break
            if(key[i].find('h4').get_text().strip() == "Model Series"):
                product_id = value[i].text.strip()
            
        return product_id
    except:
        return None

def product_id_reliance(url):
    product_id = None
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        key = soup.find_all(class_='pdp__tab-info__list__name blk__sm__6 blk__xs__6')
        value = soup.find_all(class_='pdp__tab-info__list__value blk__sm__6 blk__xs__6')
        for i in range(len(key)):
            if(key[i].get_text().strip()=="Model"):
                product_id = value[i].text.strip()
                break
        return product_id
    except MarkupResemblesLocatorWarning:
        return None

def product_id_flipkart(url):
    product_id = None
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        key = soup.find_all(class_='_1hKmbr col col-3-12')
        value = soup.find_all(class_='URwL2w col col-9-12')
        for i in range(len(key)):
            if(key[i].get_text().strip()=="Model Name"):
                product_id = value[i].text.strip()
            if(key[i].get_text().strip()=="Model Number"):
                product_id = value[i].text.strip()
                break
        return product_id
    except:
        return None

    
def populate_data(product_id,website):
    print("Product ID: {}".format(product_id))

    url_vijaysales = get_google_search_results(product_id,"vijaysales")
    if(url_vijaysales):
        r = requests.get(url_vijaysales)
        soup = BeautifulSoup(r.content, 'html.parser')
        key = soup.find_all(class_='cls-ty sptyp')
        value = soup.find_all(class_='cls-vl spval')
        brand = None
        category = None
        for i in range(0, len(key)):
            if(key[i].get_text().strip()=="BRAND"):
                brand = value[i].text.strip()
            if(key[i].get_text().strip()=="Generic Name" or key[i].get_text().strip()=="Type" ):
                category = value[i].text.strip()
        print(brand)
        print(category)
        prod_description = soup.find(class_='pdpinfor').text.strip().replace('Specifications Of ','')
        print(prod_description)
        img = get_img_src(url_vijaysales)
        print(img)
        Price_vijaysales = soup.find_all(class_='clsSpecPrc clsWithVSP')
        if(Price_vijaysales):
            Price_vijaysales = int(Price_vijaysales[0].text.strip().replace("Offer Price₹","").replace(",",""))
        else:
            Price_vijaysales = int(soup.find_all(class_='priceMRP')[0].text[4:].split("M")[0].replace(',',""))
        print("Vijaysales: ₹{}".format(Price_vijaysales))
        query = "INSERT IGNORE INTO product(product_id,category,brand,prod_description,image) VALUES ('{}','{}','{}','{}','{}');".format(product_id,category,brand,prod_description,img)
        mycursor.execute(query)
        mydb.commit()
        query = "INSERT INTO price(product_id,website,url,Price) VALUES ('{}','vijaysales','{}',{}) ON DUPLICATE KEY UPDATE Price={};".format(product_id,url_vijaysales,float(str(Price_vijaysales).replace(",","")),float(str(Price_vijaysales).replace(",","")))
        mycursor.execute(query)
        mydb.commit()


    url_croma = get_google_search_results(product_id,"croma")
    if(url_croma):
        r = requests.get(url_croma)
        soup = BeautifulSoup(r.content, 'html.parser') 
        Price_croma = 0
        script_tags = soup.find_all("script")
        for script in script_tags:
            data = script.get_text()
            if("\"price\"" in data):
                pattern = r'"price"\s*:\s*"(\d+)"'
                match = re.search(str(pattern), str(data))
                if match:
                    Price_croma = match.group(1)
                    break
        print("Croma: ₹{}".format(Price_croma))
        query = "INSERT INTO price(product_id,website,url,Price) VALUES ('{}','croma','{}',{}) ON DUPLICATE KEY UPDATE Price={};".format(product_id,url_croma,float(str(Price_croma).replace(",","")),float(str(Price_croma).replace(",","")))
        mycursor.execute(query)
        mydb.commit()

    url_reliance = get_google_search_results(product_id,"reliancedigital")
    if(url_reliance):
        r = requests.get(url_reliance)
        soup = BeautifulSoup(r.content, 'html.parser') 
        Price_reliance = soup.find(class_='pdp__priceSection__priceListText').text.strip()
        Price_reliance = Price_reliance.replace("Offer Price: ","")
        Price_reliance = Price_reliance.replace("₹","").strip()
        print("Reliance Digital: ₹{}".format(Price_reliance))
        query = "INSERT INTO price(product_id,website,url,Price) VALUES ('{}','reliancedigital','{}',{}) ON DUPLICATE KEY UPDATE Price={};".format(product_id,url_reliance,float(str(Price_reliance).replace(",","")),float(str(Price_reliance).replace(",","")))
        mycursor.execute(query)
        mydb.commit()
    

    
    
    url_flipkart = get_google_search_results(product_id,"flipkart")
    if(url_flipkart):
        r = requests.get(url_flipkart)
        soup = BeautifulSoup(r.content, 'html.parser') 
        Price_flipkart = soup.find(class_="_30jeq3 _16Jk6d").text.strip().replace("₹","")
        print("Flipkart: ₹{}".format(Price_flipkart))
        query = "INSERT INTO price(product_id,website,url,Price) VALUES ('{}','flipkart','{}',{}) ON DUPLICATE KEY UPDATE Price={};".format(product_id,url_flipkart,float(str(Price_flipkart).replace(",","")),float(str(Price_flipkart).replace(",","")))
        mycursor.execute(query)
        mydb.commit()

def get_product_id(URL):
    product_id = None
    website = None
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html.parser') 
    if("vijaysales" in URL):
        website = "vijaysales"
        key = soup.find_all(class_='cls-ty sptyp')
        value = soup.find_all(class_='cls-vl spval')
        for i in range(0, len(key)):
            if(key[i].get_text().strip()=="MODEL NAME"):
                product_id = value[i].text.strip()
            if(key[i].get_text().strip()=="SKU"):
                product_id = value[i].text.strip()
                break

    elif("croma" in URL):
        website = "croma"
        product_id=None
        key = soup.find_all(class_='cp-specification-spec-title')
        value = soup.find_all(class_='cp-specification-spec-details')
        for i in range(len(key)):
            if(key[i].find('h4').get_text().strip() == "Model Number"):
                product_id = value[i].text.strip()
                break

    elif("reliancedigital" in URL):
        website = "reliance digital"
        key = soup.find_all(class_='pdp__tab-info__list__name blk__sm__6 blk__xs__6')
        value = soup.find_all(class_='pdp__tab-info__list__value blk__sm__6 blk__xs__6')
        for i in range(len(key)):
            if(key[i].get_text().strip()=="Model"):
                product_id = value[i].text.strip()
                break

    elif("flipkart" in URL):
        website = "flipkart"
        key = soup.find_all(class_='_1hKmbr col col-3-12')
        value = soup.find_all(class_='URwL2w col col-9-12')
        for i in range(len(key)):
            if(key[i].get_text().strip()=="Model Name"):
                product_id = value[i].text.strip()
                break
        print(product_id)
    populate_data(product_id, website)


URL1 = "https://www.reliancedigital.in/lg-139-cm-55-inch-4k-uhd-smart-tv-55ur7550/p/493911478"
get_product_id(URL1)