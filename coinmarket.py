import requests
import json

url = 'https://v6.exchangerate-api.com/v6/9bda92af3a0339854122f7cb/latest/USD'

response = requests.get(url)
data = response.json()


#print(data(json.load["para_birimleri"]))
#print(data)
