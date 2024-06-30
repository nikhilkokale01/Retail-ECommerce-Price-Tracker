from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import hashlib
import os
from bs4 import BeautifulSoup
import requests
import re
from smtplib import SMTP
import time

#function to get the lowest price , that particular website, and that url 
def update_prices(product_id):
    lowest_price = float('inf')
    lowest_price_website = ""
    lowest_price_url = ""
    try:
        query = "SELECT url FROM price WHERE product_id = '{}' AND website = 'vijaysales'".format(product_id)
        mycursor.execute(query)
        urls = mycursor.fetchone()
        url_vijaysales = urls[0]
        if(url_vijaysales):
            r = requests.get(url_vijaysales)
            soup = BeautifulSoup(r.content, 'html.parser') 
            Price_vijaysales = soup.find_all(class_='clsSpecPrc clsWithVSP')
            if(Price_vijaysales):
                Price_vijaysales = int(Price_vijaysales[0].text.strip().replace("Offer Price₹","").replace(",",""))
            else:
                Price_vijaysales = int(soup.find_all(class_='priceMRP')[0].text[4:].split("M")[0].replace(',',""))
            Price_vijaysales = float(str(Price_vijaysales).replace(",",""))
            if(Price_vijaysales < lowest_price):
                lowest_price = Price_vijaysales
                lowest_price_website = "vijaysales"
                lowest_price_url = url_vijaysales
            query = "UPDATE price SET Price = {} WHERE product_id = '{}' AND website = 'vijaysales'".format(Price_vijaysales, product_id)
            mycursor.execute(query)
            mydb.commit()

        query = "SELECT url FROM price WHERE product_id = '{}' AND website = 'croma'".format(product_id)
        mycursor.execute(query)
        urls = mycursor.fetchone()
        url_croma = urls[0]
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
            Price_croma = float(str(Price_croma).replace(",",""))
            if(Price_croma<lowest_price):
                lowest_price = Price_croma
                lowest_price_website = "croma"
                lowest_price_url = url_croma
            query = "UPDATE price SET Price = {} WHERE product_id = '{}' AND website = 'croma'".format(Price_croma,product_id)
            mycursor.execute(query)
            mydb.commit()

        query = "SELECT url FROM price WHERE product_id = '{}' AND website = 'reliancedigital'".format(product_id)
        mycursor.execute(query)
        urls = mycursor.fetchone()
        url_reliance = urls[0]  
        if(url_reliance):
            r = requests.get(url_reliance)
            soup = BeautifulSoup(r.content, 'html.parser') 
            Price_reliance = soup.find(class_='pdp__priceSection__priceListText').text.strip()
            Price_reliance = Price_reliance.replace("Offer Price: ","")
            Price_reliance = Price_reliance.replace("₹","").strip()
            Price_reliance= float(str(Price_reliance).replace(",",""))
            if(Price_reliance < lowest_price):
                lowest_price = Price_reliance
                lowest_price_website = "reliancedigital"
                lowest_price_url = url_reliance
            query = "UPDATE price SET Price = {} WHERE product_id = '{}' AND website = 'reliancedigital'".format(Price_reliance,product_id)
            mycursor.execute(query)
            mydb.commit()
        
        
        query = "SELECT url FROM price WHERE product_id = '{}' AND website = 'flipkart'".format(product_id)
        mycursor.execute(query)
        urls = mycursor.fetchone()
        url_flipkart = urls[0]
        if(url_flipkart):
            r = requests.get(url_flipkart)
            soup = BeautifulSoup(r.content, 'html.parser') 
            Price_flipkart = soup.find(class_="_30jeq3 _16Jk6d").text.strip().replace("₹","")
            Price_flipkart = float(str(Price_flipkart).replace(",",""))
            if(Price_flipkart < lowest_price):
                lowest_price = Price_flipkart
                lowest_price_website = "flipkart"
                lowest_price_url = url_flipkart
            query = "UPDATE price SET Price = {} WHERE product_id = '{}' AND website = 'flipkart'".format(Price_flipkart,product_id)
            mycursor.execute(query)
            mydb.commit()
            return lowest_price,lowest_price_website,lowest_price_url
    except:
        return lowest_price,lowest_price_website,lowest_price_url

while True:
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Atharva@28",   #change according to the db configuration
    database="pricetracker"
    )
    mycursor = mydb.cursor()

    SMTP_SERVER = "smtp.gmail.com"
    PORT = 587
    EMAIL_ID = "atharvalonhari@gmail.com"   #change according to the mail config and APP password
    PASSWORD = "illetnfwvszuyzsf"

    server = SMTP(SMTP_SERVER, PORT)
    server.starttls()
    server.login(EMAIL_ID, PASSWORD)

    query = "SELECT * FROM watchlist"
    mycursor.execute(query)
    list = mycursor.fetchall()
    for i in range(len(list)):
        user_id = list[0][0]
        product_id = list[0][1]
        original_price = list[0][2]
        lowest_price,website,url = update_prices(product_id)
        if(lowest_price < original_price):
            query = "UPDATE watchlist SET original_price = {} WHERE product_id = '{}' AND user_id = {}".format(lowest_price,product_id,user_id)
            mycursor.execute(query)
            mydb.commit()
            subject = "PRICE DROP ALERT!!"
            query = "SELECT prod_description FROM product WHERE product_id = '{}'".format(product_id)
            mycursor.execute(query)
            product = mycursor.fetchone()
            body = "Price dropped for {}\nThe new price is Rs.{} at {}\nPlease visit {} to avail the lowest price.".format(product[0],lowest_price,website,url)
            msg = f"Subject:{subject}\n\n{body}"
            query = "SELECT email FROM user WHERE user_id = {}".format(user_id)
            mycursor.execute(query)
            email = mycursor.fetchone()[0]
            server.sendmail(EMAIL_ID, email, msg)
            mycursor.close()
            mydb.close()
            server.quit()
    time.sleep(86400)                
