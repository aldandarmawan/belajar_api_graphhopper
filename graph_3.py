import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
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
    loc_asal = input("Asal kamu darimana? ")
    if(loc_asal == "q"):
        break

    loc_tuju = input("Tujuan kamu mau kemana? ")
    if(loc_tuju == "q"):
        break

    pilihan_kdrn = ["car", "bike", "foot"]
    print("car = Mobil\nbike = Sepeda\nfoot = Jalan Kaki")
    kendaraan_input = input("Pilih kendaraan? ")
    if(kendaraan_input == "q"):
        break
    elif(kendaraan_input in pilihan_kdrn):
        kendaraan = kendaraan_input
    else:
        kendaraan = "car"
        print("Pilihan kendaraan tidak valid! Kendaraan mobil dipilih secara default.")
    

    asal_geocode = geocode(loc_asal)
    tuju_geocode = geocode(loc_tuju)


    print(asal_geocode)
    print(tuju_geocode)

    print("==================================================")
    if(not(
        asal_geocode[0] == 200
        and tuju_geocode[0] == 200
    )):
        #FAILED
        print("Terjadi kesalahan!")
        break

    #SUCCESS
    asal_query = "&point=" + str(asal_geocode[1]) + "%2C" + str(asal_geocode[2])
    tuju_query = "&point=" + str(tuju_geocode[1]) + "%2C" + str(tuju_geocode[2])

    routing_url = route_url + urllib.parse.urlencode({ "key": key, "vehicle": kendaraan }) + asal_query + tuju_query

    routing_data = requests.get(routing_url)
    routing_json = routing_data.json()
    routing_status = routing_data.status_code

    print("Routing API status: " + str(routing_status) + "\nAPI URL: " + routing_url)

    if(not routing_status == 200):
        print("Terjadi kesalahan ketika fetch API routing")
        if("message" in routing_json):
            print("Error message: " + routing_json["message"])
        break

    if(not (
        "paths" in routing_json
        and len(routing_json["paths"]) > 0
    )):
        print("Routing tidak ditemukan!")
        break

    print("==================================================")
    if(kendaraan == "bike"):
        kend_IND = "sepeda"
    elif(kendaraan == "foot"):
        kend_IND = "jalan kaki"
    else:
        kend_IND = "mobil"

    print("Petunjuk arah dari " + asal_geocode[3] + " menuju " + tuju_geocode[3] + " menggunakan " + kend_IND)
    
    miles = (routing_json["paths"][0]["distance"])/1000/1.61
    km = (routing_json["paths"][0]["distance"])/1000
    sec = int(routing_json["paths"][0]["time"]/1000%60)
    min = int(routing_json["paths"][0]["time"]/1000/60%60)
    hr = int(routing_json["paths"][0]["time"]/1000/60/60)

    print("Jarak tempuh: {0:.1f} miles / {1:.1f} km".format(miles, km))
    print("Durasi waktu: {0:02d}:{1:02d}:{2:02d}".format(hr, min, sec))
    print("==================================================")

    for each in range(len(routing_json["paths"][0]["instructions"])):
        path = routing_json["paths"][0]["instructions"][each]["text"]
        distance = routing_json["paths"][0]["instructions"][each]["distance"]

        distance_km = distance / 1000
        distance_mi = distance / 1000 / 1.61

        print("{0} ( {1:.1f} km / {2:.1f} miles )".format(path, distance_km, distance_mi) )

