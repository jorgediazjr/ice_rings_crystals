#!/Users/jdiaz/miniconda3/bin/python

import time
from matplotlib.pyplot import show
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import os
import collections
import math


def read_spot_file(file_name):
    ''' gets all (x,y) coordinates
    Parameters
    ----------
    file_name: str
        a path to SPOT.XDS where the first
        two columns are x and y coordinates respectively

    Returns
    -------
    xy_pairs: dict
        each KEY is an x_coord and
        each VALUE is a list of y_coordinate(s)
    '''
    xy_pairs = {}
    with open(file_name, 'r') as f:
        for line in f:
            x = float(line.split()[0])
            y = float(line.split()[1])
            if x in xy_pairs:
                xy_pairs[round(x, 4)].append(y)
            else:
                xy_pairs[round(x, 4)] = [y]
    return xy_pairs


def add_index_to_dict(ordered_pairs):
    ''' adds an index to all ordered pairs
    Parameters
    ----------
    ordered_pairs: dict
        a dict with (x,y) coordinates extracted
        from read_spot_file()

    Returns
    -------
    dict:
        a nested dict with OUTER KEY = index
        INNER KEY = X VALUES
        VALUE = Y VALUES
    '''
    new_dict = {}
    for i, key in enumerate(ordered_pairs):
        new_dict[i] = {key: ordered_pairs[key]}
    return new_dict


def find_distance(p, q):
    '''Calculates the distance between two points
    using the Euclidean distance formula

    Paramters
    ---------
    p: list
        (x, y) pair
    q: list
        (x, y) pair

    Returns
    -------
    float:
        distance between two points
    '''
    dist = math.sqrt(((p[0] - q[0])*(p[0] - q[0])) +
                     ((p[1] - q[1])*(p[1] - q[1])))
    return dist


def check_ice_rings(p, radius=1600):
    ''' checks for point close to ice ring

    Parameters
    ----------
    p: list
        (x, y) pair
    radius: int
        can either be user-specified and
        is used for calculation of circle
        circumference

    Returns
    -------
    close_to_circ: 2D list
        the first list/row is the point being checked &
        the second list/row is the point on circumference
    points_from_circle: list
        all the points on the circumference that are connected
        to the points close to itself
    '''
    points_from_circle = []
    close_to_circ = [[0, 0], [0, 0]]
    min_distance_1 = 100
    center = [1600, 1600]
    points_on_circ = [[radius * math.sin(i) + center[0],
                       radius * math.cos(i) + center[1]] for i in range(0, 361)]
    for i, point in enumerate(points_on_circ):
        dist_1 = find_distance(p, point)
        print("{} {:.2f}".format(i, dist_1))
        if dist_1 < min_distance_1:
            min_distance_1 = dist_1
            close_to_circ = [p, point]
            points_from_circle.append(point)
    print("{}\t<---->\t{}".format(close_to_circ[0],
                                  close_to_circ[1]))
    return close_to_circ, points_from_circle


def find_ice_rings(ordered_pairs, radius=1400):
    '''
    Parameters
    ----------
    ordered_pairs: dict
        all of the xy pairs extarcted from read_spot_file()
        and updated with add_index_to_dict()
    radius: int, optional
        the radius of the circle for checking ice ring

    Returns
    -------
    close_to_circ: 2D list
        each element in this list is itself a list with
        x-coord as first index and y-coord as second index
    points_from_circle: 2D list
        each element in this list is itself a list with
        xy pair from points on the circumference of the
        circle with default or given radius
    '''
    close_to_circ = []
    points_from_circle = []
    for index in ordered_pairs:
        for x_coord in ordered_pairs[index]:
            for y_coord in ordered_pairs[index][x_coord]:
                p1, circle_points = check_ice_rings([x_coord, y_coord], radius)
                print(p1)
                if(p1[0][0] == 0 and p1[0][1] == 0 and
                   p1[1][0] == 0 and p1[1][1]):
                    continue
                else:
                    close_to_circ.append(p1)
                    points_from_circle.extend(circle_points)
    return close_to_circ, points_from_circle


def plot(*args):
    ''' displays the circumference of the circles
    with given radii and the connections between
    points close to circumference and points on
    circumference

    Parameters
    ----------
    args: list
        check main() for specific names on each element in args
    '''
    fig, ax = plt.subplots()

    if args[1]:
        lc_1 = mc.LineCollection(args[1],
                                 colors=[(0, 1, 0, 1)],
                                 linewidths=0.50)
        ax.add_collection(lc_1)

    if args[1]:
        lc_2 = mc.LineCollection(args[2],
                                 colors=[(0, 1, 0, 1)],
                                 linewidths=0.50)
        ax.add_collection(lc_2)

    if args[2]:
        lc_3 = mc.LineCollection(args[3],
                                 colors=[(0, 1, 0, 1)],
                                 linewidths=0.50)
        ax.add_collection(lc_3)

    if args[3]:
        lc_4 = mc.LineCollection(args[4],
                                 colors=[(0, 1, 0, 1)],
                                 linewidths=0.50)
        ax.add_collection(lc_4)

    x_vals = []
    y_vals = []
    for index in args[0]:  # all ordered pairs
        for x_coord in args[0][index]:
            for y_coord in args[0][index][x_coord]:
                x_vals.append(x_coord)
                y_vals.append(y_coord)
    ax.scatter(x_vals, y_vals, s=0.2, color='blue')

    x_vals = []
    y_vals = []
    for point in args[5]:
        x_vals.append(point[0])
        y_vals.append(point[1])
    ax.scatter(x_vals, y_vals, s=0.2, color='red')

    x_vals = []
    y_vals = []
    for point in args[6]:
        x_vals.append(point[0])
        y_vals.append(point[1])
    ax.scatter(x_vals, y_vals, s=0.2, color='red')

    x_vals = []
    y_vals = []
    for point in args[7]:
        x_vals.append(point[0])
        y_vals.append(point[1])
    ax.scatter(x_vals, y_vals, s=0.2, color='red')

    x_vals = []
    y_vals = []
    for point in args[8]:
        x_vals.append(point[0])
        y_vals.append(point[1])
    ax.scatter(x_vals, y_vals, s=0.2, color='red')

    circle_1 = plt.Circle((1600, 1600), 1000, lw=0.3,
                          color='black', fill=False)
    ax.add_artist(circle_1)

    circle_2 = plt.Circle((1600, 1600), 1200, lw=0.3,
                          color='black', fill=False)
    ax.add_artist(circle_2)

    circle_3 = plt.Circle((1600, 1600), 1400, lw=0.3,
                          color='black', fill=False)
    ax.add_artist(circle_3)

    circle_4 = plt.Circle((1600, 1600), 1600, lw=0.3,
                          color='black', fill=False)
    ax.add_artist(circle_4)

    circle_5 = plt.Circle((1600, 1600), 1800, lw=0.3,
                          color='black', fill=False)
    ax.add_artist(circle_5)
    ax.set_title(args[9])
    show()


def main():
    files = []
    with open(os.getcwd() + '/spot_files', 'r') as f:
        for line in f:
            files.append(line.replace('\n', ''))
    for f in files:
        message = '''
        *-----------------------*
        *\tPROCESSING\t*
        *\t{}\t\t*
        *-----------------------*
        '''
        print(message.format(f.split('/')[4].upper()))
        start_time = time.time()
        pairs = read_spot_file(f)
        ordered_pairs = collections.OrderedDict(sorted(pairs.items()))
        ordered_pairs = add_index_to_dict(ordered_pairs)
        close_to_circ_1, circle_pts_1 = find_ice_rings(ordered_pairs,
                                                       radius=1200)
        close_to_circ_2, circle_pts_2 = find_ice_rings(ordered_pairs,
                                                       radius=1400)
        close_to_circ_3, circle_pts_3 = find_ice_rings(ordered_pairs,
                                                       radius=1600)
        close_to_circ_4, circle_pts_4 = find_ice_rings(ordered_pairs,
                                                       radius=1800)
        end_time = time.time()
        print("TIME TAKEN: {:.3f}".format(end_time-start_time))
        plot(ordered_pairs,
             close_to_circ_1,
             close_to_circ_2,
             close_to_circ_3,
             close_to_circ_4,
             circle_pts_1,
             circle_pts_2,
             circle_pts_3,
             circle_pts_4,
             f.split('/')[4].upper())


if __name__ == '__main__':
    main()
