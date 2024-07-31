import mysql.connector
import pandas as pd
import streamlit as st

def fetch_data():
    # Connect to the MySQL database
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Shadi8903!",  
        database="bus_data"     
    )
    
    # Create a cursor object
    cursor = con.cursor(dictionary=True)
    
    # Execute the query to fetch all bus schedules
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
    st.title("Bus Schedule Data")  # Set the title of the Streamlit application
    
    # Call the fetch_data() function to get data from the database
    data = fetch_data()
    
    # Get unique route names from the data for filter options
    route_names = data['route_name'].unique()
    # Create a select box in the Streamlit app for route names
    selected_route = st.selectbox("Select Route Name", ["All"] + list(route_names))
    
    # Filter the data based on the selected route name
    if selected_route == "All":
        filtered_data = data.copy()  # Show all data if "All" is selected
    else:
        filtered_data = data[data['route_name'] == selected_route]  # Filter data by selected route name
    
    # Get unique bus types from the filtered data for filter options
    bus_types = filtered_data['bustype'].unique()
    # Create a select box in the Streamlit app for bus types
    selected_bustype = st.selectbox("Select Bus Type", ["All"] + list(bus_types))
    
    # Apply bus type filter to the data
    if selected_bustype != "All":
        filtered_data = filtered_data[filtered_data['bustype'] == selected_bustype]
    
    # Display the filtered data in the Streamlit app
    if not filtered_data.empty:
        for index, row in filtered_data.iterrows():
            st.write(f"**Route Name:** {row['route_name']}")
            st.write(f"**Bus Name:** {row['busname']}")
            st.write(f"**Bus Type:** {row['bustype']}")
            st.write(f"**Departing Time:** {row['departing_time']}")
            st.write(f"**Duration:** {row['duration']}")
            st.write(f"**Arriving Time:** {row['reaching_time']}")
            st.write(f"**Star Rating:** {row['star_rating']}")
            st.write(f"**Price:** {row['price']}")
            st.write(f"**Seats Available:** {row['seats_available']}")
            st.markdown(f"[Link to Route]({row['route_link']})")
            st.write("---")

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
