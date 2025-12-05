import time
import random
import math
import numpy as np
import argparse

#import graph
def import_graph(path):
    with open(path, 'r') as f:
        n = int(f.readline().strip()) # # nodes
        f.readline() # skip the header line

        dist = np.zeros((n, n), dtype=float)

        for line in f:
            a,b,d = line.split()
            i = int(a) - 1 # convert to 0-based
            j = int(b) - 1
            dij = float(d)
            dist[i][j] = dij
            dist[j][i] = dij
    return n, dist

#tour cost calculator
def tour_cost(tour, dist):
    cost = 0.0
    n = len(tour)
    for i in range(n):
        cost += dist[tour[i]][tour[(i+1)%n]]
    return cost

#nearest neighbor
def nn(n, dist): #n nodes, dist distance, start starting node
    start = random.randint(0,n-1)
    unvisited = set(range(n)) 
    unvisited.remove(start)

    tour = [start]
    current = start
    
    while unvisited: #while there are unvisited nodes
        nxt = min(unvisited, key = lambda j: dist[current][j]) #pick nearest neigbor
        tour.append(nxt)
        unvisited.remove(nxt)
        current = nxt

    return tour


#2-opt

def two_opt(tour, dist, start_time, time_limit, cycles):
    n = len(tour)
    improved = True

    while improved and (time.time() - start_time < time_limit):
        improved = False
        for i in range(n - 1):

            # if time limit
            if time.time() - start_time >= time_limit:
                return tour
            for j in range(i + 2, n):
                if time.time() - start_time >= time_limit:
                    return tour, cycles
                if i == 0 and j == n - 1:
                    continue
                a, b = tour[i], tour[i+1]
                c, d = tour[j], tour[(j+1) % n]
                cycles +=1
                old_cost = dist[a][b] + dist[c][d]
                new_cost = dist[a][c] + dist[b][d]
                if new_cost < old_cost:
                    tour[i+1:j+1] = reversed(tour[i+1:j+1])
                    improved = True
                    break
            if improved:
                break
    return tour, cycles


#solver
def solve_tsp(n, dist):
    start_time = time.time()
    time_limit = 60.0
    max_no_improve = 1000

    best_tour = None
    best_cost = float('inf')
    cycles = 0
    lstImprove = 0 #time since last improvement

    while time.time() - start_time < time_limit and (lstImprove < max_no_improve):
        tour = nn(n, dist)
        cost = tour_cost(tour, dist)
        cycles += 1

        tour, cycles = two_opt(tour, dist, start_time, time_limit, cycles)

        cost = tour_cost(tour, dist)
        cycles += 1

        if cost < best_cost:
            best_cost = cost
            best_tour = tour[:]
            lstImprove = 0      # improvement reset
        else:
            lstImprove += 1

    return best_tour, round(best_cost, 2), "{:.1e}".format(cycles)


def write_solution(tour,filename):
    # convert back to 1 based
    t = [node + 1 for node in tour]
    t.append(t[0])  # close the cycle
    
    with open(filename, "w") as f:
        f.write(",".join(str(x) for x in t))
    

if __name__ == "__main__":
  
    n, dist = import_graph("TSP_1000_euclidianDistance.txt")

    # solve
    tour, cost, cycles = solve_tsp(n, dist)

    print("Euclidian best cost:", cost)
    print("Cycles:", cycles)
    print("best tour:", tour)

    write_solution(tour, "solution_920047428_euclidean.txt")

    n, dist = import_graph("TSP_1000_randomDistance.txt")

    # solve
    tour, cost, cycles = solve_tsp(n, dist)

    print("Random best cost:", cost)
    print("Cycles:", cycles)
    print("best tour:", tour)

    write_solution(tour,"solution_920047428_random.txt")
