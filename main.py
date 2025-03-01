import requests
import duckdb
import pandas as pd
import pymongo
import certifi
import os
import re 
import time
from pymongo import MongoClient

def extract_data_api():
    query = ['Plumber', 'Carpenter', 'Electrician', 'Painter', 'Mechanic', 'Hairdresser', 'Barber']
    data = []

    for q in query: 
        print(f"Getting data for {q}")
        url = "https://maps-data.p.rapidapi.com/searchmaps.php"

        querystring = {
            "query": q, 
            "limit": "1000",
            "lang": "en",
            "lat": "51.5072",
            "lng": "0.12",
            "offset": "0",
            "zoom": "13",
            "timestamp": int(time.time()) 
        }

        print(f"Query string: {querystring}")

        headers = os.getenv("LOCAL_BUSINESS_API_KEY"

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            json_data = response.json()
            print(f"Response for {q}: {json_data}") 
            data.append({"query": q, "response": json_data})  
        else:
            print(f"Error fetching data for {q}: {response.status_code}")

    try:
        connection=os.getenv("LOCAL_BUSINESS_URI")
        client = pymongo.MongoClient(connection, tlsCAFile=certifi.where())
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Creating database and collection")
    db = client['local_business_db']
    collection = db['local_business_collection']

    if data:  
        insert_data = collection.insert_many(data)
        print(f"Data inserted successfully: {len(insert_data.inserted_ids)} records")
    else:
        print("No data to insert")
    
    return data

extract_data_api()

def extract_data_nosql_database():
    try:
        connection=os.getenv("LOCAL_BUSINESS_URI")
        client = pymongo.MongoClient(connection, tlsCAFile=certifi.where())  # Fixing tlsCAFile typo
        print("Connected to MongoDB")
    except Exception as e:
        print(f"Error: {e}")
        return []  # Return an empty list if connection fails

    # Extract specific data from the collection
    db = client['local_business_db']
    collection = db['local_business_collection']

    extracted_data = []

    for doc in collection.find({}, {'id': False}):
        query = doc.get("query", None)
        businesses = doc.get("response", {}).get("data", [])

        # Ensure businesses is a list before iterating
        if isinstance(businesses, list):
            for data in businesses:
                extracted_data.append({
                    'name': data.get('name', None),
                    'business': query,
                    'address': data.get('full_address', None),
                    'city': data.get('city', None),
                    'phone_number': data.get('phone_number', None),
                    'review_count': data.get('review_count', None),
                    'rating': data.get('rating', None),
                    'website': data.get('website', None),
                    'description': data.get('description', None),
                    'types': data.get('types', [])
                })
                for d in extracted_data:
                    d['types'] = re.sub(r'\[|\]', '', str(d.get('types', '')))
                    d['types'] = re.sub(r"\'|\'", '', str(d.get('types', '')))
    
    print(f"Extracted {len(extracted_data)} records")
    return extracted_data

extract_data = extract_data_nosql_database()

def load_data_to_duck_db(extract_data):
    # Convert json data to tuple
    data = [tuple(extract_data[i].values()) for i in range(len(extract_data))]

    conn = duckdb.connect('/home/martha/local_business_project/database/local_business_db.duckdb')
    conn.sql('CREATE TABLE IF NOT EXISTS local_business (name VARCHAR, business VARCHAR, address VARCHAR, city VARCHAR, phone_number VARCHAR, review_count INT, rating FLOAT, website VARCHAR, description VARCHAR, types VARCHAR)')
    conn.executemany('''INSERT INTO local_business VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)
    conn.commit()
    conn.close()
    print("Data loaded to DuckDB successfully...")
load_data_to_duck_db(extract_data)
