import requests
import os
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


key_choice = int(input("Do you understand that a key will be auto-generated for you? Type 1 to agree, type 2 to not agree: "))
#username = input("Enter desired username (for adding to MongoDB, if not, just enter something random): ")

def clear_terminal(): #clears terminal
    os.system('cls')


def add_keys(data, filename="user_key.json"): #add_keys to json file func
    for id in data["keydata"]:
        id.pop("_id", None)
    with open (filename, "w") as f: #f just alias
        json.dump(data, f, indent=4)

#with open ("user_key.json") as json_file:
    #data = json.load(json_file)
    #reader = data["keydata"]
    #random_dict = {"Username": username,
               #"Key": keypass}
    #reader.append(random_dict)

    #literally just moved the section above to the add_mongodb function LOL

def admin_choices():
    choices = int(input("1. Add a user + key to the MongoDB database. \n2. Delete a user + key from the MongoDB database. \n3. Find a user's info. \n4. Exit the tool.\n------------\nType in the number that correlates to the tool you want to use: "))

    if choices == 1:
        add_mongodb()
    elif choices == 2:
        delete_mongodb()
    elif choices == 3:
        find_mongodb()
    elif choices == 4:
        print(Fore.RED + "This terminal will be exited in 2 seconds.")
        print(Style.RESET_ALL) #resets colorama
        time.sleep(2)
        exit()
    else:
        print("You inputted an incorrect number.")
        time.sleep(1)
        print(Fore.MAGENTA + f"Sending back to admin panel.")
        print(Style.RESET_ALL) #resets colorama
        time.sleep(1)
        clear_terminal()
        admin_choices()


def add_mongodb():
    client = MongoClient("mongodb+srv://test:test@cluster0.gkz3ps5.mongodb.net/?retryWrites=true&w=majority")
    
    db = client.get_database('userkey_db') #database name
    records = db.key_records
    username = input("Enter desired username (for adding to MongoDB, if not, just enter something random): ")

    with open ("user_key.json") as json_file:
        data = json.load(json_file)
    reader = data["keydata"]
    random_dict = {"Username": username,
               "Key": keypass}
    reader.append(random_dict)

    yes = records.insert_one(random_dict)
    print(yes)
    print(Fore.GREEN + f"The username: {username} and the key: {keypass} have been added to the .JSON file")
    print(Fore.MAGENTA + f"The username: {username} and the key: {keypass} have been added to the MongoDB database")
    add_keys(data)
    print(Style.RESET_ALL) #resets colorama

def delete_mongodb():
    client = MongoClient("mongodb+srv://test:test@cluster0.gkz3ps5.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database('userkey_db') #database name
    records = db.key_records
    username_delete = input("What is the username that you wish to delete: ")

    delete_input = { "Username": username_delete }

    raw_input = delete_input["Username"]

    logs = records.delete_one(delete_input)
    print(logs)
    print(Fore.GREEN + "The username " + Fore.MAGENTA + raw_input + Fore.GREEN + " has been deleted from the MongoDB database.")
    print(Style.RESET_ALL) #resets colorama

def find_mongodb():
    client = MongoClient("mongodb+srv://test:test@cluster0.gkz3ps5.mongodb.net/?retryWrites=true&w=majority")
    db = client.get_database('userkey_db') #database name
    records = db.key_records
   
    find_input = input("What is the username of the info you are trying to find: ")

    find =  records.find_one({ "Username": find_input })
    print(find)

if key_choice == 1:
    admin_choices()
else:
    print(Fore.RED + "This terminal will be exited in 3 seconds.")
    print(Style.RESET_ALL) #resets colorama
    time.sleep(3)
    exit()

while True:
    admin_choices() #always reruns the admin_choices function when done, so the terminal is never blank
