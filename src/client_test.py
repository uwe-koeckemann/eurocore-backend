import requests

response = requests.get('https://api.aiod.eu/platforms/v1?offset=0&limit=10')

print(response)
print(response.json())
