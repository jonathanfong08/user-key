import requests
import json
from colorama import Fore, Style
import time
import pymongo
from pymongo import MongoClient


pass_url = "https://www.psswrd.net/api/v1/password/?special=0&length=25" #password api url

req = requests.get(pass_url)

pass_data = req.json()

password_alone = pass_data["password"] #literally grabs the password key and retrieves the value

keypass = password_alone #idek why i did this ngl, might remove in next update

username = input("Enter desired username: ")
key_choice = int(input("Do you understand that a key will be generated for you? Type 1 to agree, type 2 to not agree: ")) #will raise error if not int


def add_keys(data, filename="user_key.json"):
    for id in data["keydata"]:
        id.pop("_id", None) #finds the ID and deletes it
    with open (filename, "w") as f: #f just alias
        json.dump(data, f, indent=4) #indent for aesthetics

with open ("user_key.json") as json_file: #name of .json file
    data = json.load(json_file)
    reader = data["keydata"] #lowkey used chatgpt or sum on this part
    random_dict = {"Username": username,
               "Key": keypass} #inputted user + random generated key
    reader.append(random_dict) #adds to the .JSON file



def mongo_db():
    client = MongoClient("mongodb+srv://your_username:your_password@cluster0.gkz3ps5.mongodb.net/?retryWrites=true&w=majority") #input ur own mongoDB link, this is just a placeholder
    db = client.get_database('userkey_db') #database name
    records = db.key_records #watched some indian mf so idk

    yes = records.insert_one(random_dict) #inserts into MongoDB 
    print(yes) #added print so you know if its working or not
    print(Fore.GREEN + f"The username: {username} and the key: {keypass} have been added to the .JSON file")
    add_keys(data) #i forgot
    print(Style.RESET_ALL) #resets colorama


if key_choice == 1:
    mongo_db()
else:
    print(Fore.RED + "This terminal will be exited in 3 seconds.")
    print(Style.RESET_ALL) #resets colorama
    time.sleep(3)
    exit()
