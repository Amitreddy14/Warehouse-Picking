import numpy as np
import pandas as pd
import itertools
from ast import literal_eval
import matplotlib.pyplot as plt
from scipy.cluster.vq import kmeans2, whiten
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import ward, fcluster
from utils.routing.distances import *

def cluster_locations(list_coord, distance_threshold, dist_method, clust_start):
    ''' Step 1: Create clusters of locations'''
    # Create linkage matrix
    if dist_method == 'euclidian':
        Z = ward(pdist(np.stack(list_coord)))
    else:
        Z = ward(pdist(np.stack(list_coord), metric = distance_picking_cluster))
    # Single cluster array
    fclust1 = fcluster(Z, t = distance_threshold, criterion = 'distance')
    return fclust1


def clustering_mapping(df, distance_threshold, dist_method, orders_number, wave_start, clust_start, df_type): # clustering_loc
    '''Step 2: Clustering and mapping'''
    # 1. Create Clusters
    list_coord, list_OrderNumber, clust_id, df = cluster_wave(df, distance_threshold, 'custom', clust_start, df_type)
    clust_idmax = max(clust_id) # Last Cluster ID
    # 2. Mapping Order lines
    dict_map, dict_omap, df, Wave_max = lines_mapping_clst(df, list_coord, list_OrderNumber, clust_id, orders_number, wave_start)
    return dict_map, dict_omap, df, Wave_max, clust_idmax


def cluster_wave(df, distance_threshold, dist_method, clust_start, df_type):
    '''Step 3: Create waves by clusters'''
    # Create Column for Clustering
    if df_type == 'df_mono':
        df['Coord_Cluster'] = df['Coord'] 
    # Mapping points
    df_map = pd.DataFrame(df.groupby(['OrderNumber', 'Coord_Cluster'])['SKU'].count()).reset_index() 	# Here we use Coord Cluster
    list_coord, list_OrderNumber = np.stack(df_map.Coord_Cluster.apply(lambda t: literal_eval(t)).values), df_map.OrderNumber.values
    # Cluster picking locations
    clust_id = cluster_locations(list_coord, distance_threshold, dist_method, clust_start)
    clust_id = [(i + clust_start) for i in clust_id]
    # List_coord
    list_coord = np.stack(list_coord)
    return list_coord, list_OrderNumber, clust_id, df
