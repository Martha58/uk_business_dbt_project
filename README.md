# **Local Business Finder: An End-to-End Data Engineering Project**  

## **Project Overview**  
This project extracts, processes, and visualizes data on local service providers (e.g., plumbers, carpenters, electricians, hairdressers, barbers) in the UK using **RapidAPI**, **MongoDB**, **DuckDB**, **dbt**, and **Streamlit**. Users can search for businesses, view their locations, and assess customer ratings via an interactive Streamlit dashboard. Version control is maintained throughout the project using **Git**.  

## **Project Architecture**  
1. **Extract** business data from RapidAPI.  
2. **Load** raw data into MongoDB.  
3. **Extract** relevant data and load it into DuckDB.  
4. **Transform** data using dbt.  
5. **Deploy** an interactive frontend with Streamlit.  

## **1. Extracting Data from RapidAPI**  
To retrieve business data, I used the `requests` library to interact with RapidAPI. The API provides a list of businesses across various service categories, which I iterated through to extract detailed information.  

## **2. Loading Data into MongoDB**  
Since API data can change frequently, I opted to store raw data in MongoDB Atlas, ensuring access to unfiltered data without repeatedly making API requests.  

### **Challenges & Solutions**  
While integrating with MongoDB, I encountered and resolved the following errors:  

- **`[SSL: CERTIFICATE_VERIFY_FAILED]`** – This was due to incorrect system date and time settings. Fix: Ensured system time was accurate.  
- **`[SSL: TLSV1_ALERT_INTERNAL_ERROR]`** – This was a network-related issue caused by IP restrictions. Fix: Allowed my IP in MongoDB Atlas.  
- **`Bad auth: authentication failed`** – Occurred due to incorrect credentials. Fix: Created a new user with a known password.  

Once these were resolved, data was successfully loaded into MongoDB.  

## **3. Extracting & Loading Data into DuckDB**  
Since dbt requires a **SQL-compatible** database, I extracted the required data from MongoDB and loaded it into **DuckDB**, an **OLAP database management system** known for its speed and efficiency.  

- I structured the extracted data and stored it in a **dedicated database folder** within the project repository.  
- This step was completed without errors.  

The **EL (Extract & Load) process** was successfully executed. (Full EL code available in `main.py`.)  

## **4. Transforming Data with dbt**  
**dbt (Data Build Tool)** is used for **data transformation and modeling** within SQL-based environments.  

### **Steps to Set Up dbt:**  
1. Install dbt:  
   pip install dbt
2. Initialize a dbt project:  
   dbt init <project_name>
3. Configure `profiles.yml` to define database connections.  
   - **Key Files:**  
     - `dbt_project.yml` – Contains project metadata.  
     - `profiles.yml` – Stores database connection details.  

4. Debug configuration:  
   dbt debug
   - No errors were found.  

5. Create **dbt models** in the `/models` directory:  
   - Filter unique businesses and their locations.  
   - Categorize businesses based on good vs. bad ratings.  
   - Store results in descending order based on ratings.  

6. Compile and test models:  
   dbt compile
   dbt build  # Runs models, tests them, and prevents failures from propagating

At this stage, the **dbt models were successfully built and tested**.  

## **5. Deploying the Frontend with Streamlit**  
**Streamlit** is an open-source Python framework for creating interactive data applications with minimal effort.  

### **Key Features of the Streamlit App:**  
- Users can **search for businesses** by type and location.  
- Businesses are displayed **along with ratings** to help users find the best services.  
- Filters enable users to **refine searches** based on service type.  

### **Deployment Steps:**  
1. Developed the app using `streamlit`.  
2. Pushed the code to **GitHub** (mandatory for Streamlit deployment).  
3. Connected the GitHub repository to **Streamlit Cloud** for hosting.  

The full **Streamlit code** is in `streamlit_app.py`.  

## **Version Control with Git**  
Version control was implemented from the start:  
- Created a **local Git repository**.  
- Linked it to a **remote GitHub repository**.  
- Regularly committed and pushed updates.  

This ensured code integrity and collaboration readiness.  

## **Conclusion**  
This project successfully demonstrates an **end-to-end data engineering pipeline**, from data extraction to frontend deployment. The stack includes:  
- **RapidAPI** for data sourcing  
- **MongoDB** for raw data storage  
- **DuckDB** for structured storage  
- **dbt** for transformation  
- **Streamlit** for visualization  

This project serves as a **template for future data engineering workflows** and real-time business insights applications.

Here is the link to the streamlit app - https://dbtproject.streamlit.app/
