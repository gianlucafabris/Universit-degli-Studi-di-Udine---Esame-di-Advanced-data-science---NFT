import os
import csv
import json
import numpy as np
import matplotlib.pyplot as plt
import random

from perlin_noise import *

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]

def rgb_to_hex(rgb_color):
    return "#{:02x}{:02x}{:02x}".format(int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255))

def generateArt(nodes, color="6B9EE1"):
    #normalization
    maxlat = max([max([n[1] for n in node]) for node in nodes])
    minlat = min([min([n[1] for n in node]) for node in nodes])
    maxlon = max([max([n[0] for n in node]) for node in nodes])
    minlon = min([min([n[0] for n in node]) for node in nodes])
    maxlatlon = max(maxlat, maxlon)
    for node in nodes:
        for i in range(len(node)):
            node[i][1] = node[i][1]/maxlatlon*1000 #lat
            node[i][0] = node[i][0]/maxlatlon*1000 #lon
            if maxlon > maxlat:
                node[i][1] += (1000-(maxlat/maxlatlon*1000))/2 #lat
            else:
                node[i][0] += (1000-(maxlon/maxlatlon*1000))/2 #lon
    #art
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    gradient = [rgb_to_hex(c) for c in np.linspace(hex_to_rgb(color), hex_to_rgb("6B9EE1"), 6)]
    for i in range(6):
        x_offset = random.random()*1000000
        y_offset = random.random()*1000000
        for node in nodes:
            x = [n[0] for n in node]
            y = [n[1] for n in node]
            if i == 0:
                z = [i for n in node]
            else:
                # exp
                # scale = (1/(2**i))*10000
                # z = [i+perlin_noise(int(n[0]+x_offset), int(n[1]+y_offset), int(scale))/(int(scale)) for n in node]
                # lin
                scale = 1/i*1000
                z = [i+i*perlin_noise(int(n[0]+x_offset), int(n[1]+y_offset), int(scale))/(int(scale)*5) for n in node]
            ax.plot(x,y,z, color=gradient[i])
    ax.grid(False)
    ax.set_axis_off()
    ax.view_init(elev=25, azim=-45)
    ax.set_box_aspect([1, 1, 1.5])
    plt.show()

def main():
    with open("f1.csv", mode = "r") as file:
        f1_csv = csv.reader(file)
        for index, row in enumerate(f1_csv):
            if index == 0:
                continue
            with open(os.path.join("output", row[1]+".json"), "r") as file2:
                nodes = json.load(file2)
            c = row[3]
            if c == "na":
                c = "000000"
            print(str(index) + "_" + row[0] + " - " + row[1])
            generateArt(nodes, c)

if __name__ == '__main__':
    main()
