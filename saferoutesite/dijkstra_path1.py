import osmnx as ox
import networkx as nx
import geopy.geocoders
from geopy.geocoders import Nominatim
from SQLRequest3 import Regression_List 
from current_weather import get_current_weather
   
def get_coordinates(start_address, end_address):
    '''
    Obtain (latitude, longitude) pairs from desired starting and ending 
    addresses
    
    Inputs:
      start_address (string): the starting point in the route
      end_address (string): the destination of the route
      
    Output:
      (tuple of tuples of floats): the coordinate pairs for the starting and
          ending addresses
    '''
    geolocator = Nominatim(user_agent="saferoute",\
                           format_string="%s, Chicago IL")

    start_loc = geolocator.geocode(start_address)
    end_loc = geolocator.geocode(end_address)
    start_coord = (start_loc.latitude, start_loc.longitude)
    end_coord = (end_loc.latitude, end_loc.longitude)
    return start_coord, end_coord


def get_bounding_box(start_coord, end_coord):
    '''
    Find coordinates representing the edges of the bounding box for the route
    
    Inputs:
      start_coord (tuple of floats): the coordinates of the starting point in
          the route
      end_coord (tuple of floats): the coordinates of the destination of the 
          route
     
    Output:
        (tuple of four floats): the northernmost and southernmost latitudes and
            the easternmost and westernmost longitudes of the bounding box
    '''
    start_lat = start_coord[0]
    start_lon = start_coord[1]
    end_lat = end_coord[0]
    end_lon = end_coord[1]
    
    if start_lat <= end_lat:
        s_lat = start_lat - 0.001
        n_lat = end_lat + 0.001
    elif start_lat > end_lat:
        n_lat = start_lat + 0.001
        s_lat = end_lat - 0.001
    
    if start_lon <= end_lon:
        w_lon = start_lon - 0.001
        e_lon = end_lon + 0.001
    elif start_lon > end_lon:
        e_lon = start_lon + 0.001
        w_lon = end_lon - 0.001
    
    return(n_lat, s_lat, e_lon, w_lon)
                           

def get_graph(n_lat, s_lat, e_lon, w_lon): 
    '''
    Using the bounding box, obtain an undirected graph representing the desired 
    section of the city in which the route will take place
    
    Inputs:
      n_lat (float): the northermost latitude of the bounding box
      s_lat (float): the southernmost latitude of the bounding box
      e_lon (float): the easternmost longitude of the bounding box
      w_lon (float): the westernmost longitude of the bounding box
     
    Output:
      A networkx graph  
    '''
    B = ox.core.graph_from_bbox(n_lat, s_lat, e_lon, w_lon,\
                                network_type= 'walk', simplify=True,\
                                retain_all=False, truncate_by_edge=False,\
                                name='bounded', timeout=180, memory=None,\
                                max_query_area_size=2500000000,\
                                clean_periphery=True,\
                                infrastructure='way["highway"]',\
                                custom_filter=None)
    
    B_undirected = ox.save_load.get_undirected(B)
    
    return B_undirected


def update_edge_lengths(G, scores):
    '''
    Update the lengths of each edge in the graph in order to weight them
    according to their safety scores
    
    Inputs:
      G (networkx graph): the graph
      scores (dictionary): the safety score for each edge
    '''
    set_edge_dict = {}
    new_attrs = {}
    for start, end, attrs in list(G.edges(data = True)):
        length = attrs['length']
        score = scores.get(edge_to_latlon_pair(G, (start, end)), 10**12)
        weight = score * length
        set_edge_dict[(start, end,0)] = {'length': weight}
    
    nx.set_edge_attributes(G, set_edge_dict)


def edge_to_latlon_pair(G, edge):
    '''
    Convert an edge to the pair of (latitude, longitude) coordinates
    corresponding to the nodes of the edge
    
    Inputs:
      G (networkx graph): the graph
      edge (networkx edge): the desired edge to convert
    
    Output:
      (tuple of tuple of floats): the pair of coordinates 
    '''
    node1 = G.nodes[edge[0]]
    node2 = G.nodes[edge[1]]
    n1 = (node1['y'], node1['x'])
    n2 = (node2['y'], node2['x'])
    return ((n1),(n2))


def get_path(start_coord, end_coord, G, nodes, scores):
    '''
    Find the closest nodes to the start and the destination in the graph
    and use them to compute the shortest weighted path in between
    
    Inputs:
      start_coord (tuple of floats): the coordinates of the starting point in
          the route
      end_coord (tuple of floats): the coordinates of the destination of the 
          route 
      G (networkx graph): the graph
      nodes (list of nodes): the list of graph nodes
      scores (dictionary): the safety score dictionary
    
    Output:
      (list of nodes) the safest path in terms of graph nodes
    '''
    update_edge_lengths(G, scores)

    s_min_lon_dist = 100
    s_min_lat_dist = 100
    e_min_lon_dist = 100
    e_min_lat_dist = 100
    start_node = None
    end_node = None
    
    for node, attrs in nodes:
        lat = attrs['y']
        lon = attrs['x']
        s_lat_dist = abs(start_coord[0] - lat)
        s_lon_dist = abs(start_coord[1] - lon)
        e_lat_dist = abs(end_coord[0] - lat)
        e_lon_dist = abs(end_coord[1] - lon)
        if s_lat_dist <= s_min_lat_dist and s_lon_dist <= s_min_lon_dist:
            s_min_lat_dist = s_lat_dist
            s_min_lon_dist = s_lon_dist
            start_node = node
        if e_lat_dist <= e_min_lat_dist and e_lon_dist <= e_min_lon_dist:
            e_min_lat_dist = e_lat_dist
            e_min_lon_dist = e_lon_dist
            end_node = node
    
    path = nx.dijkstra_path(G, start_node, end_node, weight='length')
    
    return path


def go(start_address, end_address, temp = None, precip = None):
    '''
    Pull data from the crime database and weather information in order to 
    compute the safety score dictionary and runs all previous code in 
    order to find the safest route from start_address to end_address.
    
    Inputs:
      start_address (string): the starting point in the route
      end_address (string): the destination of the route
      date (string): the desired date if provided, and the current date if not
      hour (int): the time of day if provided, and the current time if not
    
    Outputs:
      (list of lists of floats): the safest path in terms of (lat,lon) coordinates
    '''
    if not(temp):
        temp, precip = get_current_weather()
    start_coord, end_coord = get_coordinates(start_address, end_address)
    if start_coord == None or end_coord == None:
        return "Please Enter Valid Address"
    n_lat, s_lat, e_lon, w_lon = get_bounding_box(start_coord, end_coord)
    
    G = get_graph(n_lat, s_lat, e_lon, w_lon)
    nodes = list(G.nodes(data = True))
    edges = [(start, end, attrs) for (start, end, attrs) in G.edges(data = True) if 'name' in attrs.keys()]
    
    node_dic = dict(G.nodes(data = True))
    edges_lst = [edge_to_latlon_pair(G, edge) for edge in edges]
    #temperature and precipitation sensitivities
    t_sens = 8
    p_sens = precip
    time_low = hour - 2
    time_up = hour + 2
    scores = Regression_List(edges_lst, temp, precip, t_sens, p_sens, date, time_low, time_up)
    
    path = get_path(start_coord, end_coord, G, nodes, scores)
    
    path_coords = []
    path_coords.append([start_coord[0],start_coord[1]])
    for node in path:
        coord_list = []
        lat = G.nodes[node]['y']
        lon = G.nodes[node]['x']
        coord_list = [lat, lon]
        path_coords.append(coord_list)
    path_coords.append([end_coord[0],end_coord[1]])


    return path_coords