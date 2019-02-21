import requests
import json
import os
import re

filePath = os.path.expanduser("~/.oxford_info")

if os.path.isfile(filePath):
    file = open(filePath, "r")
    json = json.load(file)
    app_id = json['id']
    app_key = json['key']
    print("Valid ID/key read from file.\n")
else:
    print("This app uses Oxford Dictionaries API to get definitions.\nIn order to use this app, you will need an Oxford Dictionaries developer account\n\nYou can get one for free at:\nhttps://developer.oxforddictionaries.com\n\nOnce logged in, go to `API CREDENTIALS`, then find your Application ID and Application Key.\n\nEnter your")

    while True:
        app_id = input("App ID: ")
        app_key = input("App key: ")

        url = 'https://od-api.oxforddictionaries.com:443/api/v1/'
        r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

        if r.status_code == 403:
            print("Not a valid App ID and/or key, try again.")
        else:
            break

    file = open(filePath, "w+")
    file.write("{\n\t\"id\": \"" + app_id + "\",\n\t\"key\": \"" + app_key + "\"\n}")
    file.close()
    print("\nValid ID/key. The ID and key has been stored in `~/.oxford_info`\n")

output = ""
errorOutput = []
words = []
regex = re.compile('[^a-zA-Z]')

print("Enter words, enter \'!d\' when finished")

while True:
    word_id = input()

    if word_id == "!d":
        break

    words.append(regex.sub('', word_id.lower()))

print("\nLoading...\n")

for word in words:
    url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/' + word.lower()

    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    if r.status_code == 404:
        errorOutput.append(word + " ")
        continue

    parsed = r.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]

    output += (word + "," + parsed + "\n")

print(output)

if len(errorOutput) != 0:
    print("No entries were found for the word(s): ")
for word in errorOutput:
    print(word)
