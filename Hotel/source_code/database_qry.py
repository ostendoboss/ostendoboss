import mysql.connector

def database_sync(site_data = None):
    """
    site_data: dictionary argument containing location data
    decription: receives dictionary argument within location data, and returns a list of tuples
    with sorrounding airfield location data
    """    
    print("querying database for hotels available")

    #checking input parameter
    if site_data is None:
        return {"Error": "Please enter valid argument"}

    #connecting to database server
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="flyer"
    )   
    #checking database connection status
    if not conn.is_connected:
        return {"ERROR": "Database connection failed, Try again"}

    crs = conn.cursor()

    print("getting convenient hotels within district")

    #querying for hotel data from data base for hotels within location district
    query = "SELECT Hotel_name, Town, Latitude, Longitude, District_name, ICA, IAT FROM hotel_data JOIN district_data on hotel_data.District_id = district_data.District_id WHERE District_name = %s"
    crs.execute(query, (site_data["District"],))

    #checking if theres any within district
    Available_hotels = []
    for line in crs:
            Available_hotels.append(line)

    if len(Available_hotels) != 0:
        conn.close()
        return Available_hotels


    elif len(Available_hotels) == 0:
        print("getting convenient hotels within region")
        #querying for hotel data from database for hotels within location region
        query = "SELECT Hotel_name, Town, Latitude, Longitude, Region_name, ICA, IAT FROM hotel_data JOIN region_data on hotel_data.Region_id = region_data.Region_id WHERE Region_name = %s"
        crs.execute(query, (site_data["Region"],))

        #checking if theres any hotels in region
        for line in crs:
            Available_hotels.append(line)
        if len(Available_hotels) != 0:
            conn.close()
            return Available_hotels
        conn.close()   
        return None
