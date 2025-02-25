import requests
import duckdb
import pandas as pd
import pymongo
import certifi
from pymongo import MongoClient

def extract_data_api():
    query = ['Plumber', 'Carpenter', 'Electrician', 'Painter', 'Mechanic', 'Hairdresser', 'Barber']

    data = []

    for q in range ( len(query)):
        print(f"Getting data for {query[q]}")
        url = "https://maps-data.p.rapidapi.com/searchmaps.php"

        querystring = {"query":{q},"limit":"1000","lang":"en","lat":"51.5072","lng":"0.12","offset":"0","zoom":"13"}

        headers = {
            "x-rapidapi-key": "40ef23d086msh3ddec6a13f4e3c0p161262jsn4bc961e40785",
            "x-rapidapi-host": "maps-data.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            data.append(response.json())
            # print(f"Data fetched successfully {data}")
        else:
            print("Error:", response.status_code)

    try:
        connection = "mongodb+srv://local_business_user:password@cluster0.0j2dc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        client = pymongo.MongoClient(connection, tlscaFile=certifi.where()) 
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Erro: {e}")
    
    print("Creating database and collection")
    db = client['local_business_db']
    collection = db['local_business_collection']
    
    print("Inserting data into database....")
    insert_data = collection.insert_many(data)
    print(f"Data inserted successfully {insert_data}")
    return data
extract_data_api()



    