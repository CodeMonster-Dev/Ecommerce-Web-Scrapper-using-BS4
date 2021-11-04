import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.vegas.pk/bl/Rude-pakistan#content"
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

webpage = requests.get(baseurl).text
soup = BeautifulSoup(webpage, 'html.parser')
productList = soup.find_all("div", {"class":"single-product"})


productLinks = []
productImg = []
for product in productList:
    productName = product.find("h4")
    link = productName.find("a").get("href")
    productLinks.append(link)

def getNum(stock):
    stockNum = [int(i) for i in stock.split() if i.isdigit()]
    stock = stockNum
    return stock

data = []
variationLists = []
c = 1
for link in productLinks:
    print("Getting Info of " + link)
    productPageRequest = requests.get(link).text
    productPage = BeautifulSoup(productPageRequest, 'html.parser')
    print("Adding Data for " + str(c) + " Product")
    try:
        name = productPage.find("div", {"class": "breadcrumbs"})
        pName = name.find("li", {"class": "category3"})
        finalName = pName.find("span").text
    except:
        name = None
        pName = None
    try:
        price = productPage.find("span", {"id": "dp"}).text
    except:
        price = None
    try:
        stock = productPage.find("span", {"id": "mtin"}).text
    except:
        stock = None
    try:
        category = productPage.find("div", {"class": "pro-info"}).find("li").text
        s2 = ":"
        categoryName = category[category.index(s2) + len(s2):]
    except:
        categoryName = "This"
    try:
        brand = productPage.find("div", {"class": "pro-info"}).find_all("li")[1].text
        s2 = ":"
        brandName = brand[brand.index(s2) + len(s2):]
    except:
        brand = None
    try:
        description = productPage.find("form", {"id": "add_to_cart"}).find_all("p")[1].text
    except:
        description: None
    try:
        VariationList = productPage.find("select", {"id": "color"}).find_all("option")
        variationId = 1
        for variation in VariationList:

            variationLists.append(variation.text)
            products = {"id": c, "name": finalName, "price": price, "stock": stock, "Variations": variation.text,
                        "Category": categoryName, "Brand": brandName, "Description": description}
            data.append(products)
            variationId = variationId + 1
    except:
        VariationList = None
        products = {"id": c, "name": finalName, "price": price, "stock": stock, "Variations": variation.text,
                    "Category": categoryName, "Brand": brandName, "Description": description}
        data.append(products)
        variationId = variationId + 1
    c = c+1
df = pd.DataFrame(data)
df.to_csv('Products.csv', encoding='utf-8')