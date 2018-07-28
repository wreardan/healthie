import requests

url = "https://api.globalgateway.io/connection/v1/testauthentication"

response = requests.request("GET", url)

print(response.text)