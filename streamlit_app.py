import streamlit as st
import duckdb

conn = duckdb.connect('database/local_business_db.duckdb')

st.title('DBT PROJECT')
st.header('This is a simple webapp used to display details from my dbt project')
st.write("This project is an ELT data project where I used request to pull data from an API, loaded the raw data into mongodb, extracted relevant data needed for analysis and saved to duckdb. Finally, used DBT for the transformation. You can view some of the major transformations carried out using the select box and text input.")
st.write("The API contains data about business/services(plumber, mechanic, hairdresser, carpenter, barber, etc on google available in the UK")
option = st.selectbox("Common search", ["Services available", "Location", "Vendors rating"])

if option:
    if option == "Location":
        query = "SELECT * FROM unique_cities"
    elif option == "Services available":
        query = "SELECT * FROM unique_business"
    elif option == "Vendors rating":
        query = "SELECT * FROM business_rating"

    result = conn.execute(query).fetch_df()

    st.subheader(f"Result for {option}")

    if option == "Location":
        location = ", ".join([str(city) if city is not None else "" for city in result['city'].tolist()])
        st.write("We cover these locations:")
        st.write(f"{location}")
    elif option == "Services available":
        services = ", ".join(result['business'].tolist())
        st.write("These are the services available:")
        st.write(f"{services}")
    elif option == "Vendors rating":
        for index, row in result.iterrows():
            st.markdown(f"**Name**: {row['name']} \n"
                        f"**City**: {row['city']} \n"
                        f"**Rating**: {row['rating']} \n"
                        f"**Business**: {row['business']} \n")
            
search = st.text_input('What service are you looking for?')

if search:
    query = f"SELECT * FROM local_business WHERE business ILIKE '%{search}%'"
    result = conn.execute(query).fetch_df()
    st.subheader(f"Here is a list of {search} available")

    for index, row in result.iterrows():
        st.markdown(f"**Name**: {row['name']} \n"
                    f"**Address**: {row['address']} \n"
                    f"**Business**: {row['business']} \n"
                    f"**Phone Number**: {row['phone_number']} \n"
                    f"**Rating**: {row['rating']} \n"
                    f"**Website**: {row['website']} \n"
                    f"**Rating**: {row['rating']} \n"
                    f"**Services They Render**: {row['types']} \n")
        
