import pandas as pd
import mysql.connector
from datetime import datetime

# MySQL connection parameters
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Shadi8903!',
    'database': 'bus_data'
}

# Connect to MySQL
try:
    con = mysql.connector.connect(**db_config)
    cursor = con.cursor()

    # Read CSV file
    df = pd.read_csv('/Users/shadivaz/Desktop/all_combined_bus_data.csv')

    # Format columns
    df['Departing Time'] = pd.to_datetime(df['Departing Time'], format='%H:%M').apply(lambda x: datetime.combine(datetime.min, x.time()))
    df['Arriving Time'] = pd.to_datetime(df['Arriving Time'], format='%H:%M').apply(lambda x: datetime.combine(datetime.min, x.time()))
   

    df['Price'] = df['Price'].str.replace('INR', '').str.strip().astype(float)
    # Iterate over the DataFrame rows and insert each row into the database
    for index, row in df.iterrows():
        insert_query = """
            INSERT INTO bus_schedules 
            (route_name, busname, bustype, departing_time, duration, reaching_time, star_rating, price, seats_available, route_link) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            row['Bus Route'], row['Bus Name'], row['Bus Type'],
            row['Departing Time'], row['Duration'], row['Arriving Time'],
            row['Rating'], row['Price'], row['Seats Available'], row['Route Link']
        ))

    # Commit the transaction
    con.commit()
    print("Data inserted successfully!")

except mysql.connector.Error as e:
    print(f"Error inserting data into MySQL: {e}")

finally:
    # Close cursor and connection
    if cursor:
        cursor.close()
    if con:
        con.close()
