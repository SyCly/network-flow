#Silas Clymer 4/1/21


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
    b = min(c)
    for i in range(len(P)-1):
        Gf[P[i]][P[i+1]] -= b #subtract bottleneck from forward edges
        if P[i] not in Gf[P[i+1]]: #update backward edges
            Gf[P[i+1]][P[i]] = b
        else:
            Gf[P[i+1]][P[i]] += b 
    return(b, Gf)


#flow algorithm based on p.344 pseudocode
def max_flow(Gf):
    f = 0           #initialize flow
    while find_paths(Gf, 's', 't'): 
        P = find_paths(Gf, 's', 't').pop()  
        f += augment(P, Gf)[0]          #update flow
        Gf = augment(P, Gf)[1]          #update residual graph
    return f

#example of G stored as dictionary of dictionaries
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
def describe(G):
    for node in G:
        for neighbor in G[node]:
            print(node,'points to',neighbor,'with capacity',G[node][neighbor])
            
describe(G)
print(max_flow(G))
