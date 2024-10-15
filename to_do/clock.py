import requests

response = requests.get("http://worldtimeapi.org/api/ip")

if response.status_code == 200:
    data = response.json()['datetime']
    print(data)
else:
    print(f"Error: {response.status_code}")