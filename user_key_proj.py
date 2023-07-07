import requests
import json
from colorama import Fore, Style
import time
import pymongo
from pymongo import MongoClient


pass_url = "https://www.psswrd.net/api/v1/password/?special=0&length=25"

req = requests.get(pass_url)

pass_data = req.json()

password_alone = pass_data["password"]

keypass = password_alone

username = input("Enter desired username: ")
key_choice = int(input("Do you understand that a key will be generated for you? Type 1 to agree, type 2 to not agree: "))


def add_keys(data, filename="user_key.json"):
    for id in data["keydata"]:
        id.pop("_id", None)
    with open (filename, "w") as f: #f just alias
        json.dump(data, f, indent=4)

with open ("user_key.json") as json_file:
    data = json.load(json_file)
    reader = data["keydata"]
    random_dict = {"Username": username,
               "Key": keypass}
    reader.append(random_dict)



def mongo_db():
    client = MongoClient("mongodb+srv://test:test@cluster0.gkz3ps5.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database('userkey_db') #database name
    records = db.key_records

    yes = records.insert_one(random_dict)
    print(yes)
    print(Fore.GREEN + f"The username: {username} and the key: {keypass} have been added to the .JSON file")
    add_keys(data)
    print(Style.RESET_ALL) #resets colorama


if key_choice == 1:
    mongo_db()
else:
    print(Fore.RED + "This terminal will be exited in 3 seconds.")
    print(Style.RESET_ALL) #resets colorama
    time.sleep(3)
    exit()
