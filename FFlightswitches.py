#Silas Clymer 4/8/21

#Ex 7.6 -- Complete. Works with test cases. Returns True if the given system is ergonomic.
#Now updated to show certificates for non-ergonomic systems.

Walls = [(1,2),(1,5),(8,5),(8,3),(11,3),(11,1),(5,1),(5,3),(4,3),(4,1),(1,1),(1,2)]
Lights, Switches =  [(2,4),(2,2),(5,4)], [(4,4),(6,3),(6,2)] #Daniel, ergonomic {{(2,2),(4,4)},{(2,4),(6,3)},{(5,4),(6,2)}}


#Provided by Daniel - code to check whether a given light and switch are visible from each other
def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
# Return true if line segments AB and CD intersect
# Source: http://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)
def visible(pt1,pt2,Walls):
    x1,y1 = pt1
    x2,y2 = pt2
    for i,wall in enumerate(Walls[:-1]):
        x3,y3 = wall
        x4,y4 = Walls[i+1]
        if intersect((x1,y1),(x2,y2),(x3,y3),(x4,y4)):
            return False
    return True


#G is a graph stored as an adjacency list
def build_graph(Walls, Lights, Switches):
    G = {'s': {}, 't': {}}
    for L in Lights:
        G['s'][L] = 1
        for S in Switches:
            G[S] = {'t': 1}
            if visible(L,S,Walls):
                if L not in G:
                    G[L] = {S: 1}
                else:
                    G[L][S] = 1
    return G

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
    b = min(c)   #here's our bottleneck
    for i in range(len(P)-1):
        Gf[P[i]][P[i+1]] = max(0, Gf[P[i]][P[i+1]] - b) #subtract bottleneck from forward edges
        if P[i] not in Gf[P[i+1]]: #update backward edges
            Gf[P[i+1]][P[i]] = b
        else:
            Gf[P[i+1]][P[i]] += b 
    return(b, Gf)


#flow algorithm based on p.344 pseudocode
def Max_Flow(Gf):
    f = 0           #initialize flow
    while find_paths(Gf, 's', 't'): 
        P = find_paths(Gf, 's', 't').pop()  #P is some existing s-t path
        f += augment(P, Gf)[0]          #add P's bottleneck to flow
        Gf = augment(P, Gf)[1]          #update residual graph
    return f,Gf


G = build_graph(Walls, Lights, Switches)
flow = Max_Flow(G)

def DFS(G, s):
    S = [s]
    R = []
    while S:
        u = S.pop()
        if u not in R:
            R.append(u)
            if u in G:
                for v in G[u]:
                    if G[u][v] != 0:
                        S.append(v)
    return R
        

A = [u for u in DFS(flow[1], 's') if u in Lights]
B = [G[v] for v in A if v in G]

if flow[0] == len(Lights): #True if maximum flow matches the number of lights
    print('Ergonomic.')
else:
    print('Not ergonomic. Lights at',A,'are only visible from Switches at',B)





















#-------------------------------------------------------------------------------------------
#Old "scratch" work


'''   
    

G = {
    's': {'A': 1, 'B': 1, 'C': 1},
    'A': {'E': 1},
    'B': {'E': 1},
    'C': {'D': 1, 'F': 1},
    'D': {'t': 1},
    'E': {'t': 1},
    'F': {'t': 1},
    't': {}
    }

#optional way to print graphs using English
def describe(G):
    for node in G:
        for neighbor in G[node]:
            print(node,'points to',neighbor,'with capacity',G[node][neighbor])



    #old = []
    #paths = find_paths(Gf, 's', 't')
        if P not in old:
            old.append(P)
        paths = find_paths(Gf, 's', 't')
        for p in old:
            if p in paths:
                paths.remove(p)


def min_cut(Gf):
    A = DFS(Gf, 's')
    B = [u for u in Gf if u not in A]
    return A,B
        '''
