import math
import os
import json
import matplotlib.pyplot as plt
import requests
import csv

def visualizeRoad(nodes):
    fig, ax = plt.subplots()
    for node in nodes:
        x = [n[0] for n in node]
        y = [n[1] for n in node]
        ax.plot(x, y)
        # ax.scatter(x,y)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('roads')
    ax.set_aspect('equal')
    plt.show()

def downloadOSM(ids, file, debug=False):
    #ids
    #   array of numbers
    #file
    #   string - file name
    #debug
    #   bool - for debuging visualization of roads
    responseRoads = []
    print("Loading road data...")
    for id in ids:
        #import road from osm
        query = {'data': f"""
        [out:json];
        way({id});
        out geom;
        """}
        responseRoads.append(requests.post("https://overpass-api.de/api/interpreter", data = query).json())
    nodes = []
    for i in range(len(responseRoads)):
        nodes += [[[geometry["lon"],geometry["lat"]] for geometry in element["geometry"]] for element in responseRoads[i]["elements"]]
    #equirectangular projection - see https://en.wikipedia.org/wiki/Equirectangular_projection
    maxlat = max([max([n[1] for n in node]) for node in nodes])
    minlat = min([min([n[1] for n in node]) for node in nodes])
    maxlon = max([max([n[0] for n in node]) for node in nodes])
    minlon = min([min([n[0] for n in node]) for node in nodes])
    for node in nodes:
        for i in range(len(node)):
            node[i][1] = 6372.797*(math.radians(node[i][1]) - math.radians((minlat+maxlat)/2))/100 #lat
            node[i][0] = 6372.797*(math.radians(node[i][0])-math.radians((minlon+maxlon)/2))*math.cos(math.radians((minlat+maxlat)/2))/100 #lon
    #to meters - see https://en.wikipedia.org/wiki/Geographic_coordinate_system#Latitude_and_longitude
    for node in nodes:
        for i in range(len(node)):
            lat = node[i][1]
            node[i][1] = node[i][1]*(111132.92 - 559.82*math.cos(2*math.radians(node[i][1])) + 1.175*math.cos(4*math.radians(node[i][1])) - 0.0023*math.cos(6*math.radians(node[i][1]))) #lat
            node[i][0] = node[i][0]*(111412.84*math.cos(math.radians(lat)) - 93.5*math.cos(2.0*math.radians(lat)) + 0.118*math.cos(4.0*math.radians(lat))) #lon
    #normalization
    maxlat = max([max([n[1] for n in node]) for node in nodes])
    minlat = min([min([n[1] for n in node]) for node in nodes])
    maxlon = max([max([n[0] for n in node]) for node in nodes])
    minlon = min([min([n[0] for n in node]) for node in nodes])
    for node in nodes:
        for i in range(len(node)):
            node[i][1] = round(node[i][1]-minlat,3) #lat
            node[i][0] = round(node[i][0]-minlon,3) #lon
    if debug:
        visualizeRoad(nodes)
    #save json
    if not os.path.exists("output"):
        os.makedirs("output")
    with open(os.path.join("output", file + ".json"), "w") as file:
        file.write(json.dumps(nodes, indent=4))

def main():
    with open("f1.csv", mode = "r") as file:
        f1_csv = csv.reader(file)
        for index, row in enumerate(f1_csv):
            if index == 0:
                continue
            #import road from OpenStreetMap
            downloadOSM(row[2].split(";"), row[1], True)

if __name__ == '__main__':
    main()
