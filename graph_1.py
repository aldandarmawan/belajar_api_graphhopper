import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
lokasi1 = "Manado"
lokasi2 = "Bandung"
key = "c594c308-8a8b-44d6-8beb-1f95d4128ced"


url = geocode_url + urllib.parse.urlencode({
    "q": lokasi1,
    "limit": 1,
    "key": key
})

print("Geocode API URL for " + lokasi1 + ": \n" + url)


data = requests.get(url)
json_data = data.json()
json_status = data.status_code

print(json_data)
print("\ndengan response code: " + str(json_status))