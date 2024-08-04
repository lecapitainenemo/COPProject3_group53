
import math

def dijkstra(dict, source, destination):

    path_weight_list = [None for x in range(len(dict_all))]
    prev_vertex_list = [None for x in range(len(dict_all))]

    for idx, val in enumerate(dict):

        if source == idx:
            path_weight_list[idx] = 0
        else:
            path_weight_list[idx] = math.inf
        
    verts = list(range(len(dict_all)))
    unvisited_set = set(verts)
    visited_set = set()

    visited_set.add(source)
    unvisited_set.remove(source)

    while(len(unvisited_set) != 0):

        neighbors = dict[source]
        
        for neighbor in neighbors:

            if path_weight_list[neighbor] > path_weight_list[source] + neighbors[neighbor]:
                path_weight_list[neighbor] = path_weight_list[source] + neighbors[neighbor]
                prev_vertex_list[neighbor] = source

        min_dist = math.inf

        for unvisited_vert in unvisited_set:
            if path_weight_list[unvisited_vert] < min_dist:
                min_dist = path_weight_list[unvisited_vert]
                source = unvisited_vert

        visited_set.add(source)
        unvisited_set.remove(source)
     
    return path_weight_list[destination]


if __name__ == "__main__":

    # example from: https://www.youtube.com/watch?v=pVfj6mxhdMw
    # A:0, B:1, C:2, D:3, E:4
    

    dict0 = {
        1: 6,
        3: 1
        }

    dict1 = {
        0: 6,
        2: 5,
        3: 2,
        4: 2
        }

    dict2 = {
        1: 5,
        4: 5
        }

    dict3 = {
        0: 1,
        1: 2,
        4: 1
        }

    dict4 = {
        1: 2,
        2: 5,
        3: 1
        }

    dict_all = {
        0: dict0,
        1: dict1,
        2: dict2,
        3: dict3,
        4: dict4
        }

    shortest_dist = dijkstra(dict_all, 0, 4)

    print('shortest dist: ' + str(shortest_dist))

