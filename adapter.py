import requests
import csv


api_key = "RJNVLFM0O88JP765"
response = requests.get(f"https://api.thingspeak.com/channels/2924635/feeds.json?api_key={api_key}")

if response.status_code == 200:
    data = response.json().get("feeds", [])
    with open("output.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print("Data has been written to output.csv")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")