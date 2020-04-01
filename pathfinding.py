import math
import heapq
import folium
import sys


def calcHeuristic(lon1, lat1, lon2, lat2, type):  # uses haversine formula to calculate euclidean distance of 2 points
    rad_of_earth = 6373
    radlat1 = math.radians(lat1)
    radlat2 = math.radians(lat2)
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    # formula to calculate euclidean
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + \
        math.cos(radlat1) * math.cos(radlat2) * \
        math.sin(dlon / 2) * math.sin(dlon / 2)
    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    if type == 'shortest':
        return int(rad_of_earth * b * 1000)  # uses distance to estimate heuristic
    elif type == 'fastest':
        return int(rad_of_earth * b * 1000) / 320  # uses bus travel speed to estimate heuristic


def astar(graph, start, target, type):
    count = 0  # count to be used for displaying the amount of edges checked
    route = dict()  # dictionary to store then best path

    targLon = target.get_lon()  # stores target longitude
    targLat = target.get_lat()  # stores target lattitude
    start.set_t(0)
    start.set_g(0)  # set cost of start to 0
    start.set_h(
        calcHeuristic(start.get_lon(), start.get_lat(), targLon, targLat, type))  # init hueristic for start node
    start.set_f(start.get_g() + start.get_h())  # init f value

    # create tuple pair into the binary tree array, for all nodes in graph
    unvisited_queue = [(v.get_g(), v) for v in graph]
    for v in graph:
        v.set_h(
            calcHeuristic(v.get_lon(), v.get_lat(), targLon, targLat, type))  # sets heuristic for every vertex in graph

    heapq.heapify(unvisited_queue)  # heapify the binary tree array

    while len(unvisited_queue):  # while there is still unvisited nodes in the priority queue

        uv = heapq.heappop(unvisited_queue)  # Pops vertex with the smallest distance
        current = uv[1]
        current.set_visited()  # set current vertex to be visited to prevent infinite looping

        # loops for neighbouring edges in current adjacent:
        for neighbor in current.adjacent:
            count += 1
            if neighbor.visited:  # if visited, skip
                continue

            # this prevent algorithm to walk from hdb-busstop-hdb-busstop etc
            # vvvvvvv
            if (neighbor.get_id() != start.get_id() and neighbor.get_id() != target.get_id()) and neighbor.get_node_type()=='HDB':

                continue

            new_g = current.get_g() + current.get_weight(neighbor)  # get new g value
            new_f = neighbor.get_h() + new_g  # get new f value
            if new_f < neighbor.get_f():  # if new f is smaller than the neighbors' f then set neighbor to have the

                neighbor.set_g(new_g)
                neighbor.set_f(new_f)
                neighbor.set_t(current.get_t() + 1)
                route[neighbor] = current  # update best route
                print(
                    "updated : current = %s next = %s new_total_cost = %s" % (
                        current.get_id(), neighbor.get_id(), neighbor.get_g()))
                if neighbor.get_id() == target.get_id():  # exit if target node is reached
                    output = []
                    m = folium.Map(location=[start.get_lat(), start.get_lon()],
                                   zoom_start=17)  # sets starting location of map
                    folium.Marker(location=[target.get_lat(), target.get_lon()],
                                  icon=folium.Icon(color='red', icon='flag', prefix='fa')).add_to(
                        m)  # sets starting marker
                    return [outputRoute(output, route, start, target, type, m), neighbor.get_g(),
                            count]  # returns directions, end distance, and total edegs traversed
            else:  # if f is not smaller than neighbor do nothing
                print('not updated : current = %s next = %s new_total_cost = %s ' % (
                    current.get_id(), neighbor.get_id(), neighbor.get_g()))

        # Rebuild heap so queue wont have nodes that are visited
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_g(), v) for v in graph if not v.visited]
        heapq.heapify(unvisited_queue)  # heapify new queue
    print('No Route found sorry')
    return None


def dijkstra(graph, start, target, type):
    count = 0  # count to be used for displaying the amount of edges checked
    route = dict()  # dictionary to store then best path

    # Set the distance for the start node to zero
    start.set_g(0)
    start.set_t(-1)
    # Put tuple pair into the priority queue, for all nodes in graph
    unvisited_queue = [(v.get_g(), v) for v in graph]  # loads all nodes in graph into queue
    heapq.heapify(unvisited_queue)  # heapify the binary tree array

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()  # set current vertex to be visited to prevent infinite looping

        # loops for neighbouring edges in current adjacent:
        for neighbor in current.adjacent:
            count += 1

            # if visited, skip
            if neighbor.visited:
                continue

            # this prevent algorithm to walk from hdb-busstop-hdb-busstop etc
            # vvvvvvv
            if (neighbor.get_id() != start.get_id() and neighbor.get_id() != target.get_id()) and neighbor.get_node_type()=='HDB':
                continue

            new_dist = current.get_g() + current.get_weight(neighbor)

            if new_dist < neighbor.get_g():  # if new dist is smaller than the neighbors' g then set neighbor to have the new_dist
                neighbor.set_g(new_dist)
                neighbor.set_t(current.get_t() + 1)
                print('updated : current = %s next = %s new_total_cost = %s' % (
                    current.get_id(), neighbor.get_id(), neighbor.get_g()))
                route[neighbor] = current  # update best route

            else:  # else skips
                print('not updated : current = %s next = %s new_total_cost = %s' % (
                    current.get_id(), neighbor.get_id(), neighbor.get_g()))

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_g(), v) for v in graph if not v.visited]
        heapq.heapify(unvisited_queue)  # heapify new queue
    output = []
    m = folium.Map(location=[start.get_lat(), start.get_lon()], zoom_start=17)  # sets starting location of map
    folium.Marker(location=[target.get_lat(), target.get_lon()],
                  icon=folium.Icon(color='red', icon='flag', prefix='fa')).add_to(m)  # sets starting
    return [outputRoute(output, route, start, target, type, m), target.get_g(),
            count]  # returns directions, end distance, and total edegs traversed


def breathFirst(graph, start, target, type):
    count = 0  # count to be used for displaying the amount of edges checked
    route = dict()  # dictionary to store the path

    # Set the level for the start node to zero
    start.set_t(0)
    start.set_g(0)
    # Put tuple pair into the priority queue, for all nodes in graph
    unvisited_queue = [(v.get_t(), v) for v in graph]  # loads all nodes in graph into queue
    heapq.heapify(unvisited_queue)  # heapify the binary tree array

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()  # set current vertex to be visited to prevent infinite looping
        # loops for neighbouring edges in current adjacent:
        for neighbor in current.adjacent:
            count += 1
            # if visited, skip
            if neighbor.visited:
                continue


            # this prevent algorithm to walk from hdb-busstop-hdb-busstop etc
            # vvvvvvv
            if (neighbor.get_id() != start.get_id() and neighbor.get_id() != target.get_id()) and neighbor.get_node_type()=='HDB':
                continue
            if current.get_t() != neighbor.get_t() and current.get_weight(neighbor) < 2000000:

                neighbor.set_g(current.get_g() + current.get_weight(neighbor))
                neighbor.set_t(current.get_t() + 1)
                route[neighbor] = current  # update best route
                print('updated : current = %s next = %s new_total_cost = %s' % (
                    current.get_id(), neighbor.get_id(), neighbor.get_t()))
            if target.get_id() == neighbor.get_id():
                output = []
                m = folium.Map(location=[start.get_lat(), start.get_lon()],
                               zoom_start=17)  # sets starting location of map
                folium.Marker(location=[target.get_lat(), target.get_lon()],
                              icon=folium.Icon(color='red', icon='flag', prefix='fa')).add_to(m)  # sets starting
                return [outputRoute(output, route, start, target, type, m), target.get_g(),
                        count]  # returns directions, end distance, and total edegs traversed

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_t(), v) for v in graph if not v.visited]
        heapq.heapify(unvisited_queue)  # heapify new queue

    return None


def outputRoute(output, route, start, target, type,
                m, xfers=0):  # recursive function to load directions into a array of string to be returned

    if target == start:  # if we reach start node, return string array together with folium map object
        return [output[::-1], m, xfers]
    xfers += 1
    travel_mode = target.get_mode(route[target])  # get travel mode
    travel_service = target.get_name(route[target])  # get travel service
    travel_cost = "{0:.2f}".format((route[target].get_weight(target)))  # gets 'cost' AKA weight
    current_node = route[target].get_id()  # gets current node name
    current_lat = route[target].get_lat()  # gets current node latitude
    current_lon = route[target].get_lon()  # gets current node longitude
    next_node = target.get_id()  # gets next node name
    next_lat = target.get_lat()  # gets next node latitude
    next_lon = target.get_lon()  # gets next node longitude

    folium.PolyLine(locations=([current_lat, current_lon], [next_lat, next_lon])).add_to(
        m)  # draws a line from current node to next node on the map
    m = place_marker(m, current_lat, current_lon, travel_mode, start, route[target])  # places a marker on the map
    if type == 'fastest':  # if type is fastest
        output.append(
            current_node + ' to ' + next_node + ' travel by ' + travel_service + ', ' + travel_mode + ' for ' + travel_cost + ' Min')
    elif type == 'shortest':  # if its shortest
        output.append(
            current_node + ' to ' + next_node + ' travel by ' + travel_service + ', ' + travel_mode + ' for ' + travel_cost + ' Meters')
    return outputRoute(output, route, start, route[target], type,
                       m, xfers)  # calls itself with the next next as its 'target' node


def place_marker(m, lat, lon, mode, start_node, current_node):  # a fucntion to sets marker on transfer nodes
    if start_node == current_node:
        if mode == 'LRT':
            folium.Marker(location=[lat, lon], icon=folium.Icon(color='red', icon='subway', prefix='fa')).add_to(m)
        elif mode == 'Bus':
            folium.Marker(location=[lat, lon], icon=folium.Icon(color='red', icon='bus', prefix='fa')).add_to(m)
        elif mode == 'walk':
            folium.Marker(location=[lat, lon], icon=folium.Icon(color='red', icon='blind', prefix='fa')).add_to(m)
    else:
        if mode == 'LRT':
            folium.Marker(location=[lat, lon], icon=folium.Icon(icon='subway', prefix='fa')).add_to(m)
        elif mode == 'Bus':
            folium.Marker(location=[lat, lon], icon=folium.Icon(icon='bus', prefix='fa')).add_to(m)
        elif mode == 'walk':
            folium.Marker(location=[lat, lon], icon=folium.Icon(icon='blind', prefix='fa')).add_to(m)

    return m
