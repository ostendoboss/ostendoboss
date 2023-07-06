import requests
import database_qry
  
def get_location_data(location = None):
    """
    Returns: location data for any give location text string input
    description: queries the google maps api to obtain various location data
    Location: argument, address, street, building, you name it (must be a string)
    """

    print("getting location data")

    if location is None and location == "":
        return {"Error": "no input parameters from your end"}

    #google map api base urls for querying location data
    url1 = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
    url2 = "https://maps.googleapis.com/maps/api/place/details/json"

    #query string parameters for the api requests
    payload = {
        "input": location,
        'inputtype': "textquery",
        "key": ""
    } 

    #querying gmaps api via /findplacefromtext resource for location info to obtain place_id
    req1 = requests.get(url1, params = payload)

    #checking response status 
    if not req1.ok:
        print("Error with location request")
        return None

    req1_json = req1.json()

    try:
        id = req1_json["candidates"][0]["place_id"]        
    except Exception as err:
        print("error: problem accessing place id for location")
        return None

    #querying gmaps api via the /Place Detail resource for more info using ehe obtained place_id
    req2 = requests.get(url2, {"place_id": id, "key": ""})

    if not req2.ok:
        print("Error processing location request")
        return None

    req2_json = req2.json() 

    #saving key data response in dictionary
    try:        
        location_data = {
            "place": req2_json["result"]["name"],
            "place_id": id,
            "sub_locality": req2_json["result"]["address_components"][0]["long_name"] + ", " + req2_json["result"]["address_components"][1]["long_name"].split(" ")[-1],
            "District": req2_json["result"]["address_components"][-3]["long_name"].split(" ")[-1].title(),
            "Region": req2_json["result"]["address_components"][-2]["long_name"].split(" ")[0],
            "Country": req2_json["result"]["address_components"][-1]["long_name"].split(" ")[-1].title(),
            "Coordinates": [req2_json["result"]["geometry"]["location"]["lat"],
                            req2_json["result"]["geometry"]["location"]["lng"]]
        }
        return (location_data)
    except Exception as err:
        print(f"Error: {err}")
        return (None)

def get_distance_data(origin_id=None, destination_id=None):
    """
    takes two string srguments representing the place_id arguments for the source 
    and destination locations
    returns a dictionary object that contains distance information 
    """

    try:
        #google maps api base url for the distance matrix
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"

        #parameters for request query string 
        parameters = {
            "origins": "place_id:{}".format(origin_id),
            "destinations": "place_id:{}".format(destination_id),
            "key": ""
        }   

        #querying the gmaps distance matrix API 
        req = requests.get(url, params = parameters)

        #checking status code
        if not req.ok:
            print("ERROR: Were having trouble with your request, please try again")
            return None

        reqdata = req.json()

        #extracting key data from the json response
        distance_data = {
            "origin_address": reqdata["origin_addresses"],
            "destination_address": reqdata["destination_addresses"],
            "distance_inbetween": reqdata["rows"][0]["elements"][0]["distance"]["text"],
            "time_of_departure": reqdata["rows"][0]["elements"][0]["duration"]["text"]
            }  
        return distance_data
    except Exception as err:
        print("an error occured when getting the distance: ", err)
        return None



def closest_hotelspot(location, hotel_list):
    """
    Args:
        location (dictionary): dictionary containing information on location
        hotel_list (list of tuples): list of tuples having information a particular hotel

    Returns:
        dictionary: returns a dictionary with information on the nearest hotel found 
    """

    if hotel_list is None:
        return {"Location_Error": "Try another location nearby"}

    print("getting closest hotelspot")
    #obtaining place_ids for all the hotels
    ap_data = []
    for ap in hotel_list:
        location_string = "{}, {}".format(ap[0], ap[1])
        data = get_location_data(location_string)
        ap_data.append(data)
    
    #getting hotel closest to location
    try:
        closest_dist = float(get_distance_data(location["place_id"], ap_data[0]["place_id"])["distance_inbetween"].split(" ")[0])
        nearest_af = ap_data[0]
        index = 0
    except Exception as err:
        print("Error finding distance between hotels: ", err)
        return ({"Error": "No hotels found, please try a diffrent location nearby"})
    for afs in ap_data[1:]:
        try:
            dist = float(get_distance_data(location["place_id"], afs["place_id"])["distance_inbetween"].split(" ")[0])
            if dist < closest_dist:
                nearest_af = afs
                closest_dist = dist
                index += 1
        except Exception as err:
            continue    
    #populating final object with nearest airfield data        
    desired_as = {
        "Hotel_name": hotel_list[index][0],
        "Town": hotel_list[index][1],
        "District": nearest_af["District"],
        "Distance (km)": closest_dist,
        "ICA": hotel_list[index][-2],
        "IAT": hotel_list[index][-1],
        "Coordinates": {"lat": hotel_list[index][2], "long": hotel_list[index][3]}
    } 
    
    return desired_as
