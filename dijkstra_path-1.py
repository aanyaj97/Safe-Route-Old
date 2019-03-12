
# coding: utf-8

# In[ ]:


import osmnx as ox
import networkx as nx
import geopy.geocoders
from geopy.geocoders import Nominatim

#sample_end_address = '5807 S Woodlawn Ave'
#sample_start_address = '5481 S Maryland Ave'
   
def get_coordinates(start_address, end_address):
#pull coordinates from address input
    geolocator = Nominatim(user_agent="saferoute", format_string="%s, Chicago IL")
    start_loc = geolocator.geocode(start_address)
    end_loc = geolocator.geocode(end_address)
    start_coord = (start_loc.latitude, start_loc.longitude)
    end_coord = (end_loc.latitude, end_loc.longitude)
    return start_coord, end_coord

def get_bounding_box(start_coord, end_coord):

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
    
    B = ox.core.graph_from_bbox(n_lat, s_lat, e_lon, w_lon, network_type= 'walk', simplify=True,                                 retain_all=False, truncate_by_edge=False, name='bounded',                                 timeout=180, memory=None, max_query_area_size=2500000000,                                 clean_periphery=True, infrastructure='way["highway"]', custom_filter=None)
    
    B_undirected = ox.save_load.get_undirected(B)
    
    return B_undirected
                           

def update_edge_lengths(G, edges, scores):
    
    for start, end, attrs in edges:
        length = attrs['length']
        start_coord = (G.nodes[start]['x'], G.nodes[start]['y'])
        end_coord = (G.nodes[end]['x'], G.nodes[end]['y'])
        if start_coord not in scores:
            continue
        if end_coord not in scores:
            continue
        score = scores[(start_coord, end_coord)]
        weight = score * length
        attrs['length'] = weight
        
        
def get_path(start_coord, end_coord, G, edges, nodes, scores):
    
    update_edge_lengths(G, edges, scores)

    #find closest start_nodes
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

def plot_graph(path, G):
    pos = nx.spring_layout(G)
    h = G.subgraph(path)
    nx.draw_networkx_nodes(G,pos,nodelist=path,node_color='r')
    nx.draw_networkx_edges(G,pos=pos, edgelist = h.edges())

def go(start_address, end_address, scores):

    start_coord, end_coord = get_coordinates(start_address, end_address)
    if start_coord == None or end_coord == None:
        return "Please Enter Valid Address"
    n_lat, s_lat, e_lon, w_lon = get_bounding_box(start_coord, end_coord)
    
    G = get_graph(n_lat, s_lat, e_lon, w_lon)
    nodes = list(G.nodes(data = True))
    edges = [(start, end, attrs) for (start, end, attrs) in G.edges(data = True) if 'name' in attrs.keys()]
                           
    scores = None
    #scores = get score dictionary from G or use sample from google docs
    
    path = get_path(start_coord, end_coord, G, edges, nodes, scores)
    return path
    

