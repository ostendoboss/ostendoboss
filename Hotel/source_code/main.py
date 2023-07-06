import Hotel
import database_qry

"""
Description: evaluates closest hotel to the user's location and
one closest to user's to his destination
source: argument that represents user's location/origin
destination: argument representing user's destination
returns - JSON object containing closest hotels the user's location/origin
and user's desired relaxation destination
"""

#obtaining user inputs
origin = str(input("Whats your location? (city center, town, village, road, district, or any landmark you can identify)\n"))
final_destination = str(input("Where are you going? (Town, village, district or any landmark place you may know)\n"))

def main(source = None, destination = None):

    #getting location data for source
    src_data = hotel.get_location_data(source)
    #getting closest hotels for the source from database
    src_afs = database_qry.database_sync(src_data)
    #getting nearest hotel for the source
    src_nearest_af = hotel.closest_airfield(src_data, src_afs)
    
    print(f"\nThe closest hotel to your location ({source}) is:")
    for i,j in src_nearest_af.items():
        print(f"\t{i}: {j}")
    

    print("\n")
    #getting location data for the desiation
    dest_data = hotel.get_location_data(destination)
    #getting closest hotels to the destination from database
    dest_afs = database_qry.database_sync(dest_data)
    #getting nearest hotel for the destination
    dest_nearest_af = hotel.closest_hotelfindings(dest_data, dest_afs)
    
    print(f"\nThe closest hotel to your destination ({destination}) is;")
    for m,n in dest_nearest_af.items():
        print(f"\t{m}: {n}")

    print("\nhotel safe\n")
    
    return ([src_nearest_af, dest_nearest_af])
    
main(origin, final_destination)
input("Press Enter to Exit")
