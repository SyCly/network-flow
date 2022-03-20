#Silas Clymer 4/14/21

#Ch 7 Exercise 9 -- Complete. Works with randomly generated test cases.
#Returns True if the given locations provide a possible matching
#of all people to balanced hospitals. Otherwise, False

import math
from timeit import timeit
import random

'''
#Example
people = [(1,0),(2,0),(11,0),(12,0)]   n = 4
hospitals = [(-20,0), (40,0)]          k = 2
#G is an adjacency list (a dictionary of dictionaries)
G = {'s': {(1, 0): 1, (2, 0): 1, (11, 0): 1, (12, 0): 1},
     't': {},
     (-20, 0): {'t': 2},
     (1, 0): {(-20, 0): 1},
     (40, 0): {'t': 2},
     (2, 0): {(-20, 0): 1},
     (11, 0): {(40, 0): 1},
     (12, 0): {(40, 0): 1}}
'''

def check_hospitals(n):
    
    def testcase(n):
        k = math.ceil(n/5)  #number of hospitals
        p = [(random.randint(0, 50), random.randint(0, 50)) for i in range(n)] #places random coordinates in a 50x50 square
        h = [(random.randint(0, 50), random.randint(0, 50)) for i in range(k)]
        return p,h

    
    #for this problem, p[i] has an bipartite edge with h[j] if dist(p[i],h[j]) <= 30
    def build_graph(p, h):
        G = {'s': {}, 't': {}}
        for a in p:
            G['s'][a] = 1
            for b in h:
                G[b] = {'t': math.ceil(len(p)/len(h))}   #edges from hospitals to sink have capacity n/k. All other capacities start as 1
                d = math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)   
                if d <= 30:
                    if a not in G:
                        G[a] = {b: 1}
                    else:
                        G[a][b] = 1
        return G

    people = testcase(n)[0]
    hospitals = testcase(n)[1]
    G = build_graph(people, hospitals)

    #Source: https://www.python.org/doc/essays/graphs/
    def find_paths(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in graph:
            return []
        paths = []
        for node in graph[start]:
            if graph[start][node] != 0:  #I added this line to disqualify paths with edges of capacity zero
                if node not in path:
                    newpaths = find_paths(graph, node, end, path)
                    for newpath in newpaths:
                        paths.append(newpath)
        return paths
    
    #determines the bottleneck for a given path and also modifies residual graph edges
    def augment(P, Gf):
        c = []
        for i in range(len(P)-1):
            c.append(Gf[P[i]][P[i+1]])
        b = min(c)  #here's our bottleneck
        for i in range(len(P)-1):
            Gf[P[i]][P[i+1]] -= b #subtract bottleneck from forward edges
            if P[i] not in Gf[P[i+1]]: #update backward edges
                Gf[P[i+1]][P[i]] = b
            else:
                Gf[P[i+1]][P[i]] += b 
        return(b, Gf)

    #flow algorithm based on Tardos p.344 pseudocode
    def max_flow(Gf):
        f = 0                                   #initialize flow
        while find_paths(Gf, 's', 't'):       #until all s-t paths are exhausted:  
            P = find_paths(Gf, 's', 't').pop()  #P is some existing s-t path
            f += augment(P, Gf)[0]              #add P's bottleneck to flow
            Gf = augment(P, Gf)[1]              #update residual graph
        return f

    Gf = G
    flow = max_flow(Gf)
    print('People are located at', people)
    print('Hospitals are located at', hospitals)
    print('Maximum flow =', flow)
    print('Did everyone get to a balanced hospital?', flow == n)
    return flow == n     #if max flow matches number of people, then everyone has found a hospital


#Let's time it! Thanks to Brandon Chupp, who deciphered all this
def wrapper(func, *args): #wraps a function to allow the timeit function to use it
    def wrapped():
        return func(*args)
    return wrapped

n = 15   #number of people
a = wrapper(check_hospitals, n) #passes our function through the wrapper
x = 1
print("size:", n, "time:", timeit(a, number = x)/x) #average runtime of x trials of size n
