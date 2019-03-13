# scores = ((start lon, start lat) , (end lon, end lat)): safety score


def update_edge_lengths(edges, scores):

    for start, end, attrs in edges:
        length = attrs['length']
        start_coord = (start['longitude'], start['latitude'])
        end_coord = (end['longitude'], end['latitude'])
        score = scores[(start_coord, end_coord)]
        weight = score * length
        attrs['length'] = weight
