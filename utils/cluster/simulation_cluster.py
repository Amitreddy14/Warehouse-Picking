from utils.cluster.mapping_cluster import *
from utils.routing.routes import *


# Function 
def simulation_wave(y_low, y_high, orders_number, df_orderlines, list_results, distance_threshold, mono_method, multi_method):
    ''' Simulate the distance for a number of orders per wave'''
    # List to store values
    [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult] = [list_results[i] for i in range(len(list_results))]

    # Variables to store total distance
    distance_route = 0
    origin_loc = [0, y_low] 	

    # Mapping of orderlines with waves number
    df_orderlines, waves_number = df_mapping(df_orderlines, orders_number, distance_threshold, mono_method, multi_method)

    # Loop
    for wave_id in range(waves_number):
        # Listing of all locations for this wave 
        list_locs, n_locs, n_lines, n_pcs = locations_listing(df_orderlines, wave_id)
        # Create picking route
        wave_distance, list_chemin, distance_max = create_picking_route_cluster(origin_loc, list_locs, y_low, y_high)
        # Total walking distance
        distance_route = distance_route + wave_distance
        # Results by wave
        monomult = mono_method + '-' + multi_method

        # Add the results 
        list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult = append_results(list_wid, list_dst, list_route, list_ord, list_lines, 
        list_pcs, list_monomult, wave_id, wave_distance, list_chemin, orders_number, n_lines, n_pcs, monomult)

    # List results
    list_results = [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult]
    return list_results, distance_route


def loop_wave(y_low, y_high, df_orderlines, list_results, n1, n2, distance_threshold, mono_method, multi_method):
    ''' Simulate all scenarios for each number of orders per wave'''
    # Lists for records
    list_ordnum, list_dstw = [], []
    lines_number = len(df_orderlines)
    # Test several values of orders per wave
    for orders_number in range(n1, n2):
        # Scenario of orders/wave = orders_number 
        list_results, distance_route = simulation_wave(y_low, y_high, orders_number, df_orderlines, list_results,
            distance_threshold, mono_method, multi_method)
        # Append results per Wave
        list_ordnum.append(orders_number)
        list_dstw.append(distance_route)
        print("{} orders/wave: {:,} m".format(orders_number, distance_route))
    # Output list
    [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult] = [list_results[i] for i in range(len(list_results))]
    # Output results per wave
    df_results, df_reswave = create_dataframe(list_wid, list_dst, list_route, list_ord, 
        distance_route, list_lines, list_pcs, list_monomult, list_ordnum, list_dstw)
    return list_results, df_reswave