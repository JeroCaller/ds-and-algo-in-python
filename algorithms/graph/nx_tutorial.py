import networkx as nx

G = nx.Graph()  # undirected graph 생성.

# 노드는 None을 제외한 해시 가능한 파이썬 객체라면 
# 모두 가능하다. 여기선 문자열로 채택하였다. 
G.add_node('A2') 
G.add_nodes_from(['A3', 'A4', 'A5'])  # 여러 노드들을 list로 동시에 추가.

G.add_edge('A2', 'A3') # 두 노드 사이의 edge 추가.

# 여러 edge들을 동시에 추가.
G.add_edges_from([('A3', 'A4'), ('A4', 'A5')])

for i in range(2, 6):
    # 만약 존재하지도 않는 노드 사이에 엣지를 추가하려고 시도하면 
    # 해당 노드들이 먼저 자동으로 추가되고 그 후에 엣지가 추가된다. 
    G.add_edge(f"B{i}", f"C{i}")
    if 2 < i < 5:
        G.add_edge(f"B{i}", f"B{i+1}")
    if i < 5:
        G.add_edge(f"C{i}", f"C{i+1}")

print(G.number_of_nodes(), "nodes.")  # 노드의 개수를 반환하는 메서드.
print(G.number_of_edges(), 'edges.')  # 엣지 개수 반환 메서드. 

# 'C3'과 인접한 노드를 반환.
print("adjacent nodes to C3: ", list(G['C3']))

# 'C3'과 인접한 엣지 반환. 
print("edges adjacent to C3: ", list(G.edges('C3')))
