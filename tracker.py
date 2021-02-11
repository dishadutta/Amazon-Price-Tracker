import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = input("Enter the URL of the product you want to track price for: ")

my_user_agent = input("Enter your user agent: ")
headers = {"User-Agent":my_user_agent}

mailto = input("Enter your Email Id: ")


def check_price():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    #title of the product
    title = soup.find(id="productTitle").get_text()

    #current selling pice of the product
    price = soup.find(id="priceblock_ourprice").get_text()

    price_new=price.replace(',', '')
    converted_price = float(price_new[2:])

    #mrp of the product
    mrp_price = soup.find('span', {'class' :'priceBlockStrikePriceString'}).text

    mrp_price_new = mrp_price[2:].replace(',', '')
    converted_mrp_price = float(mrp_price_new)


    print(title.strip())
    print(price[2:].replace(',', '').strip())
    print(converted_price)
    print(mrp_price[2:].replace(',', '').strip())
    print(converted_mrp_price)


    if(converted_mrp_price - converted_price > 2000):
        send_mail()
    
    return converted_price



def send_mail():
    server=smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    mail_from = ''
    mail_password = ''		#App password

    server.login(mail_from, mail_password)

    subject = 'Price Fell Down'
    body = 'Check the amazon link ' + URL
    
    msg = f"Subject: {subject} \n\n {body}"

    server.sendmail(
        mail_from,
        mailto,
        msg
    )

    print("HEY EMAIL HAS BEEN SENT")
    server.quit()



while(True):
    check_price()
    time.sleep(86400)       #send you mail after each 24 hours only if the price falls down