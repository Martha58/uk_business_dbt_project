import streamlit as st
import duckdb

conn = duckdb.connect('database/local_business_db.duckdb')

st.title('BUSINESSES IN UNITED KINGDOM')
st.header('Get fast access to differnt services in the UK')
st.write("Looking for an easy way to get basic services like Barber, Plumber, Machanic, e.t.c? We've got you covered, all you need to do is search for what you want, and get recommendations")

option = st.selectbox("Common search", ["Services available", "Location we cover", "Vendors rating"])

if option:
    if option == "Location we cover":
        query = "SELECT * FROM unique_cities"
    elif option == "Services available":
        query = "SELECT * FROM unique_business"
    elif option == "Vendors rating":
        query = "SELECT * FROM business_rating"

    result = conn.execute(query).fetch_df()

    st.subheader(f"Result for {option}")

    if option == "Location we cover":
        location = ", ".join([str(city) if city is not None else "" for city in result['city'].tolist()])
        st.write("We cover these locations:")
        st.write(f"{location}")
    elif option == "Services available":
        services = ", ".join(result['business'].tolist())
        st.write("We currently provide information on these services:")
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
        
