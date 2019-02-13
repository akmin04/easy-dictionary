import requests
import json

print("This app uses Oxford Dictionaries API to get definitions.\nIn order to use this app, you will need an Oxford Dictionaries developer account\n\nYou can get one for free at:\nhttps://developer.oxforddictionaries.com\n\nOnce logged in, go to `API CREDENTIALS`, then find your Application ID and Application Key.\n\nEnter your")

while True:
    app_id = input("App ID: ")
    app_key = input("App key: ")

    url = 'https://od-api.oxforddictionaries.com:443/api/v1/'
    r = requests.get(url, headers = {'app_id': app_id, 'app_key': app_key})

    if r.status_code == 403:
        print("Not a valid App ID and/or key, try again.")
    else:
        break;

output = ""
errorOutput = []
words = []


print("\nValid ID/key.\n\nEnter words, enter \'quit\' when finished")

while True:
    word_id = input()

    if word_id == "quit":
        break

    words.append(word_id.lower())

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
print("No entries were found for the word(s): ")
for word in errorOutput:
    print(word)
