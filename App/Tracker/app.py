"""
This module contains everything necessary to track items on Newegg.ca
"""

import json
import traceback
import os
import uuid
import concurrent.futures
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup


class NeweggTracker:
    """
    This class contains all the methods necessary to track items on Newegg.ca
    """


    def __init__(self):
        """Creates instance of the current data
        """

        self.data = self.get_data()

    @staticmethod
    def get_data() -> dict:
        """Gets the json data in data.json"""

        with open("./Tracker/data.json") as file:
            data = json.load(file)
            return data


    #TODO: This function is too long.
    @staticmethod
    def fetch_html(tag:str, is_new:bool=False) -> dict:
        """
        Gets all the information necessary from Newegg.ca for a specific item and generates
        a dictionary in which everything about the product is contained.
        """

        try:
            source = requests.get(f"https://www.newegg.ca/{tag}").text
            soup = BeautifulSoup(source, "html.parser")
            try:
                product_title = soup.find("h1", {"class": "product-title"})
                price_is = soup.find("li", {"class": "price-current"})
                shipping = soup.find("li", {"class": "price-ship"})
                product_inventory = soup.find("div", {"class": "product-inventory"})
                price_was = soup.find("span", {"class": "price-was-data"}) #format is: $amount Shipping
                time_left_on_sale = soup.find("span", {"class": "price-save-endtime"})
                price_save_dollars = soup.find("span", {"class": "price-save-dollar"})
                price_save_percent = soup.find("span", {"class": "price-save-percent"})

            except:
                traceback.print_exc()
                print(f"Something went wrong while trying to parse the html tags for {tag}")
                return {}
        except:
            traceback.print_exc()
            print(f"Could not request html or create soup object for {tag}")
            return {}

        data = {}
        try:
            #Keeping only the first 4 words of the title
            title = product_title.text.split(" ")[0:4]
            data["product-name"] = title
            data["price"] = price_is.text
            data["shipping"] = shipping.text[:-9] if shipping else "" #see price_was in fetch_html
            data["metadata"] = {}
            if product_inventory.text == " OUT OF STOCK.":
                data["metadata"]["OOS"] = True
            if price_was:
                data["metadata"]['price-was'] = price_was.text
                if time_left_on_sale:
                    data["metadata"]['time-left'] = time_left_on_sale.text
                if price_save_dollars:
                    data["metadata"]["price-save"] = price_save_dollars.text
                    data["metadata"]["percent-save"] = price_save_percent.text
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
            data["img-token"] = src

        return {tag: data}


    def add_a_new_item(self, tag:str):
        """
        Adds a new item to the data.json file
        """

        if tag in self.data["items"].keys():
            print(f"{tag} is alredy tracked.")
            return

        new_item_data = self.fetch_html(tag, True)
        new_item = {"history": {str(dt.now().date()) : new_item_data[tag]["price"]},
                    "shipping": new_item_data[tag]["shipping"],
                    "metadata": new_item_data[tag]["metadata"],
                    "img-token": new_item_data[tag]["img-token"]}
        self.data["items"][tag] = new_item

        with open("./Tracker/data.json", "w") as file:
            json.dump(self.data, file, indent=4)


    def remove_an_existing_item(self, tag:str):
        """
        Removes an item from the data.json file and
        deletes the image associated.
        """

        try:
            image_token = self.data["items"][tag]["img-token"]
            os.remove(f"./Graphic/Images/{image_token}.png")
            del self.data["items"][tag]
            with open("./Tracker/data.json", "w") as file:
                json.dump(self.data, file, indent=4)
        except:
            traceback.print_exc()
            print(f"Something went wrong while trying to delete {tag}.\
            Maybe the item is no longer being tracked or was never tracked.")


    def update_data(self):
        """Updates the information about the items that are tracked in data.json"""

        if not self.data["items"]:
            return

        tracked_tags = list(self.data['items'].keys())
        self.data["last-updated"] = str(dt.now())
        self.data["number-of-items"] = len(tracked_tags)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            new_data_generator = executor.map(self.fetch_html, tracked_tags)
        for item in new_data_generator:
            for tag, data in item.items():
                self.data["items"][tag]["history"][str(dt.now().date())] = data["price"]
                self.data["items"][tag]["shipping"] = data["shipping"]
                self.data["items"][tag]["metadata"] = data["metadata"]

        with open("./Tracker/data.json", "w") as file:
            json.dump(self.data, file, indent=4)
