from geopy.geocoders import Nominatim
from geopy import distance
import gmplot
import time

start = time.time()
import webbrowser
from itertools import combinations

origin = 'Kuala Lumpur'
geolocator = Nominatim(user_agent="Algo Assignment")
KL_location = geolocator.geocode(origin, timeout=100)
KL_latitude = KL_location.latitude
KL_longitude = KL_location.longitude
cities = ['Kuala Lumpur', 'Jakarta', 'Bangkok', 'Taipei', 'HongKong', 'Beijing', 'Tokyo', 'Seoul']
cities_latitude = [None] * len(cities)
cities_longitude = [None] * len(cities)
for i in range(len(cities)):
    location = geolocator.geocode(cities[i], timeout=150)
    cities_latitude[i] = location.latitude
    cities_longitude[i] = location.longitude

gmap3 = gmplot.GoogleMapPlotter(KL_latitude, KL_longitude, 13)
gmap3.scatter(cities_latitude, cities_longitude, '#FF0000', 20, True)

cities_latitude.append(KL_latitude)
cities_longitude.append(KL_longitude)
cities_location = {}
cities_coords = {}
geolocator = Nominatim(user_agent="Algo Assignment", timeout=30)
cities_distance = {}
comb_distance = list(
    combinations(['Kuala Lumpur', 'Jakarta', 'Bangkok', 'Taipei', 'HongKong', 'Beijing', 'Tokyo', 'Seoul'], 6))

for i in range(len(cities)):
    cities_location[cities[i]] = geolocator.geocode(cities[i])
    cities_coords[cities[i]] = {}

for i in range(len(cities)):
    cities_coords[cities[i]]['latitude'] = cities_location[cities[i]].latitude
    cities_coords[cities[i]]['longitude'] = cities_location[cities[i]].longitude


def calcdistance(start):
    for i in range(0, len(cities)):
        cities_distance[cities[start]][cities[i]] = int(
            distance.distance((cities_coords[cities[start]]['latitude'], cities_coords[cities[start]]['longitude']),
                              (cities_coords[cities[i]]['latitude'], cities_coords[cities[i]]['longitude'])).kilometers)


for i in range(len(cities)):
    cities_distance[cities[i]] = {}
    calcdistance(i)

from sys import maxsize
import copy


class TravellingSalesman():
    def __init__(self, graph, s, t):
        # store all vertex apart from source vertex
        self.route = [s]
        dummy_graph = copy.deepcopy(graph)
        dummy_country = copy.deepcopy(cities)

        for i in range(len(dummy_country)):
            dummy_graph[i].append(0)
            if i == s:
                dummy_graph[i].append(0)
            else:
                dummy_graph[i].append(maxsize)

        dummy_country.append("All")
        dummy_country.append("StartEnd")
        dummy_graph.append([0] * len(dummy_country))
        dummy_graph.append([0])
        for i in range(len(dummy_country) - 2):
            dummy_graph[len(dummy_country) - 1].append(maxsize)
        dummy_graph[len(dummy_country) - 1].append(0)

        vertex = []
        for i in range(len(dummy_graph)):
            if i != s:
                vertex.append(i)

                # store minimum weight Hamiltonian Cycle
        min_path = maxsize

        while True:

            # store current Path weight(cost)
            current_pathweight = 0

            # compute current path weight
            k = s
            current_route = dummy_country[s]
            test_route = [dummy_country[s]]

            for i in range(len(vertex)):
                current_pathweight += dummy_graph[k][vertex[i]]
                k = vertex[i]
                if (dummy_country[k] != "StartEnd") and (dummy_country[k] != "All"):
                    current_route += "-->" + dummy_country[k]
                    test_route.append(dummy_country[k])
            current_pathweight += dummy_graph[k][s]

            # update minimum
            if current_pathweight < min_path:
                shortest_route = current_route
                self.route = test_route
            min_path = min(min_path, current_pathweight)

            if not next_permutation(vertex):
                break

        print("Distance Travelled:", min_path, "km\nRoute Taken:", shortest_route,"\n")
        l = shortest_route.split('-->')
        t += l

        storeLatCor = []
        storeLongCor = []
        mark = 0

        for i in range(len(cities)):
            mark = geolocator.geocode(l[i])
            storeLatCor.append(mark.latitude)
            storeLongCor.append(mark.longitude)

        gmap3 = gmplot.GoogleMapPlotter(KL_latitude, KL_longitude, 13)

        gmap3.scatter(cities_latitude, cities_longitude, '#FF0000', size=100, marker=True)
        gmap3.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"
        gmap3.marker(cities_latitude[0], cities_longitude[0], 'cornflowerblue')

        for j in range(len(cities) + 1):
            for i in range(len(cities) + 1):
                gmap3.plot(storeLatCor[j:i], storeLongCor[j:i], 'red', edge_width=2.5)

        gmap3.apikey = "AIzaSyCFSPRV9xJNrjPuUKGO9FKtqhH2go4Hmao"

        gmap3.draw("gmap.html")

        end = time.time()

        print("Running Time: ", (end - start))
        url = "Path.html"
        webbrowser.open(url, new=2)

        return None

    def get_route(self):
        return self.route


# next_permutation implementation
def next_permutation(L):
    n = len(L)

    i = n - 2
    while i >= 0 and L[i] >= L[i + 1]:
        i -= 1

    if i == -1:
        return False

    j = i + 1
    while j < n and L[j] > L[i]:
        j += 1
    j -= 1

    L[i], L[j] = L[j], L[i]

    left = i + 1
    right = n - 1

    while left < right:
        L[left], L[right] = L[right], L[left]
        left += 1
        right -= 1

    return True

# Driver Code
if __name__ == "__main__":
    import cumma
    t = []
    # matrix representation of graph
    adj = [[0 for i in range(len(cities))] for j in range(len(cities))]
    for i in range(len(cities)):
        for j in range(len(cities)):
            adj[i][j] = cities_distance[cities[i]][cities[j]]
    s = 0
    print(TravellingSalesman(adj, s, t))
    print(t)
    cumma.data(t)
