import mysql.connector
import pandas as pd
import streamlit as st

def fetch_data():
    
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Shadi8903!",  
        database="bus_data"     
    )
    
   
    cursor = con.cursor(dictionary=True)
    

    cursor.execute("SELECT * FROM bus_schedules")
    
    # Fetch all rows from the executed query
    rows = cursor.fetchall()
    
    # Close the cursor and connection
    cursor.close()
    con.close()
    
    # Convert rows to a DataFrame
    df = pd.DataFrame(rows)
    
    return df

# Streamlit application layout
def main():
    st.title("Bus Schedule Data")
    
    # Fetch data from the database
    data = fetch_data()
    
    # Filter options for route names
    route_names = data['route_name'].unique()
    selected_route = st.selectbox("Select Route Name", ["All"] + list(route_names))
    
    # Filter by route name
    if selected_route == "All":
        filtered_data = data.copy()  # Show all data if "All" routes selected
    else:
        filtered_data = data[data['route_name'] == selected_route]
    
    # Filter options for bus types
    bus_types = filtered_data['bustype'].unique()
    selected_bustype = st.selectbox("Select Bus Type", ["All"] + list(bus_types))
    
    # Apply bus type filter
    if selected_bustype != "All":
        filtered_data = filtered_data[filtered_data['bustype'] == selected_bustype]
    
    # Display filtered data
    if not filtered_data.empty:
        st.write(filtered_data)

# Run the application
if __name__ == "__main__":
    main()
