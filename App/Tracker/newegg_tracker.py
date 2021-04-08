"""
This module contains all the functions necessary to manage the data in data.json
"""
import json
import traceback
import requests
import os
import uuid
from datetime import datetime as dt
from bs4 import BeautifulSoup


def get_data() -> dict:
    """Gets the json data in data.json"""
    with open("./Tracker/data.json") as file:
        data = json.load(file)
        return data


def add_a_new_item(tag:str):
    """Adds a new item to the data.json file"""
    current_data = get_data()
    #Although the tags won't dupplicate in the file
    #I don't want an unecessary operation to occur.
    if tag in current_data["items"].keys():
        print(f"{tag} is alredy tracked.")
        return
    new_item_data = fetch_html(tag, True)
    new_item = {"history": {str(dt.now().date()) : new_item_data[tag]["price"]},
                "shipping": new_item_data[tag]["shipping"],
                "metadata": new_item_data[tag]["metadata"],
                "img-token": new_item_data[tag]["img-token"]}
    current_data["items"][tag] = new_item
    with open("./Tracker/data.json", "w") as file:
        json.dump(current_data, file, indent=4)


def remove_an_existing_item(tag:str):
    """Removes an item from the data.json file"""
    current_data = get_data()
    try:
        del current_data["items"][tag]
        with open("./Tracker/data.json", "w") as file:
            json.dump(current_data, file, indent=4)
        #os.remove(f"../Graphic/Images/{tag}.png")
    except:
        traceback.print_exc()
        print(f"Something went wrong while trying to delete {tag}.\
        Maybe the item is no longer being tracked or was never tracked.")

def update_data():
    """Updates the information about the items that are tracked in data.json"""
    current_data = get_data()
    tracked_tags = list(current_data['items'].keys())
    current_data["last-updated"] = str(dt.now())
    current_data["number-of-items"] = len(tracked_tags)
    for tag in tracked_tags:
        new_data = fetch_html(tag)
        if new_data[tag]:
            current_data["items"][tag]["product-name"] = new_data[tag]["product-name"]
            current_data["items"][tag]["history"][str(dt.now().date())] = new_data[tag]['price']
            current_data["items"][tag]["shipping"] = new_data[tag]['shipping']
            current_data["items"][tag]["metadata"] = new_data[tag]["metadata"]
    with open("./Tracker/data.json", "w") as file:
        json.dump(current_data, file, indent=4)


#TODO: This function is too long and needs to be split into different parts
def fetch_html(tag: str, is_new:bool = False) -> dict:
    """
    Gets all the information necessary from Newegg.ca for a specific item and generates
    a dictionary in which everything about the product is contained.
    """
    try:
        source = requests.get(f'https://www.newegg.ca/{tag}').text
        soup = BeautifulSoup(source, "html.parser")
        try:
            price_is = soup.find("li", {"class": "price-current"})
            shipping = soup.find("li", {"class": "price-ship"})
            price_was = soup.find("span", {"class": "price-was-data"}) #format is: $amount Shipping
            product_inventory = soup.find("div", {"class": "product-inventory"})
            time_left_on_sale = soup.find("span", {"class": "price-save-endtime"})
            price_save_dollars = soup.find("span", {"class": "price-save-dollar"})
            price_save_percent = soup.find("span", {"class": "price-save-percent"})
            product_title = soup.find("h1", {"class": "product-title"})
        except:
            traceback.print_exc()
            print(f"Something went wrong while trying to parse the html tags for {tag}")
            return {}
    except:
        traceback.print_exc()
        print(f"Could not request html or create soup object for {tag}")
        return {}
    res = {}
    try:
        #Keeping only the first 4 words of the title
        title = product_title.text.split(" ")
        res["product-name"] = title[0] + " " + title[1] + " " + title[2] + title[3]
        res["price"] = price_is.text
        res["shipping"] = shipping.text[:-9] if shipping else "" #see price_was in fetch_html
        res["metadata"] = {}

        if product_inventory.text == " OUT OF STOCK.":
            res["metadata"]["OOS"] = True
        if(price_was):
            res["metadata"]['price-was'] = price_was.text
            if(time_left_on_sale):
                res["metadata"]['time-left'] = time_left_on_sale.text
            if(price_save_dollars):
                res["metadata"]["price-save"] = price_save_dollars.text
                res["metadata"]["percent-save"] = price_save_percent.text
    except:
        traceback.print_exc()
        print(f"Something went wrong while trying to structure the data for {tag}")
        return {}
    
    if is_new:
        #Download image from Newegg
        #I cannot save the image as tag.png because the tag often contains /
        #To resolve this issue, I will use the uuid library
        #Because of the smaller scale of the project, 
        #I believe generating a random uuid should be good enough
        src = str(uuid.uuid4())
        try:
            img_tag = soup.find("img", {"class": "product-view-img-original"})
            url = img_tag['src']
            img_data = requests.get(url).content
            with open(f'./Graphic/Images/{src}.png', "wb") as file:
                file.write(img_data)
        except:
            traceback.print_exc()
            print(f"Could not get or save the image for {tag}")
            src = ""
        res["img-token"] = str(src)

    return {tag: res}
