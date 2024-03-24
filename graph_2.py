import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
key = "c594c308-8a8b-44d6-8beb-1f95d4128ced"

def geocode(lokasi):
    while(lokasi == ""):
        lokasi = input("Masukkan lokasi anda? ")

    url = geocode_url + urllib.parse.urlencode({
        "q": lokasi,
        "limit": 1,
        "key": key
    })

    print("Geocode API URL for " + lokasi + ": \n" + url)


    data = requests.get(url)
    json_data = data.json()
    json_status = data.status_code

    #print(json_data)
    #print("\ndengan response code: " + str(json_status))

    if(not json_status == 200):
        #ERROR/FAILED
        lat = None
        lng = None
        new_name = None
        print("Terjadi kesalahan!, status_code: " + str(json_status))
        if("message" in json_data):
            print("\ndengan pesan error: " + json_data["message"])

        return json_status, lat, lng, new_name
    
    #SUCCESS
    if(not ("hits" in json_data and len(json_data["hits"]) > 0)):
        lat = None
        lng = None
        new_name = lokasi
        print("Lokasi tidak ditemukan!")
        return json_status, lat, lng, new_name


    lat = json_data["hits"][0]["point"]["lat"]
    lng = json_data["hits"][0]["point"]["lng"]

    name = json_data["hits"][0]["name"]

    if("country" in json_data["hits"][0]):
        country = json_data["hits"][0]["country"]
    else:
        country = ""

    if("state" in json_data["hits"][0]):
        state = json_data["hits"][0]["state"]
    else:
        state = ""

    if(len(country) > 0 and len(state) > 0):
        new_name = name + ", " + state + ", " + country
    elif(len(state) > 0):
        new_name = name + ", " + state
    else:
        new_name = name
    return json_status, lat, lng, new_name


while True:
    loc = input("Asal kamu darimana? ")

    if(loc == "q"):
        break

    lokasi_geocode = geocode(loc)

    print(lokasi_geocode)