import networkx as nx
import matplotlib.pyplot as plt
from typing import Final

# type alias
Value = object
Priority = int
Index = int
Node = object
Edge = tuple[Node, Node]
Distance = int
Weight = int

# 상수 정의
INF: Final = float('inf')


class IndexedMinPQ():
    def __init__(self):
        self.N = 0
        self.values: list[Value] = [None]
        self.priorities: list[Priority] = [None]

        # value들을 모은 리스트에 각각의 value들이 해당 
        # 리스트의 어느 인덱스에 존재하는지를 기록하기 위해 
        # 각 value에 해당하는 index를 저장하는 변수.
        # 해당 변수의 존재로, 특정 value를 O(1)만에 찾을 수 있음. 
        # dictionary는 hashtable로 구성되어있기 때문. 
        self.location: dict[Value, Index] = {}

    def getCurrentSize(self) -> (int):
        """
        현재 힙 내에 저장된 데이터의 수 반환
        """
        return self.N
    
    def peek(self) -> (tuple[Value, Priority] | tuple[None, None]):
        """
        제일 먼저 출력될 아이템의 value와 priority를 반환. 
        """
        if self.N == 0:
            return None, None
        v = self.values[1]
        p = self.priorities[1]
        return v, p 
    
    def isEmpty(self) -> (bool):
        """
        우선순위 큐가 비어있는지 확인하는 메서드. 비어있으면 True 반환.
        """
        return self.N == 0

    def __contains__(self, target_value: Value) -> (bool):
        """
        각 value의 리스트 내 인덱스 위치를 기록하는 변수 
        self.location의 존재 덕분에 O(1)이라는 짧은 시간 내에 
        해당 값이 우선순위 큐에 존재하는지 확인할 수 있다. 
        """
        return target_value in self.location
    
    def _less(self, i: Index, j: Index) -> (bool | None):
        """
        두 인덱스에 해당하는 value들의 우선순위를 비교하여 
        i의 우선순위가 j의 것보다 더 작은지를 확인하는 메서드. 
        우선순위의 수치값이 작은 value가 더 우선순위가 높은 구조를 가지는 
        우선순위 큐이기에 i > j이면 True, 그렇지 않으면 False 반환. 
        매개변수로 입력받은 두 인덱스 중 하나라도 None이라면 None을 반환. 
        """
        if (i is None) or (j is None): return None
        return self.priorities[i] > self.priorities[j]
    
    def _swap(self, i: Index, j: Index) -> (None):
        """
        주어진 두 인덱스 i, j에 해당하는 두 개체의 위치를 바꾼다. 
        """
        self.values[i], self.values[j] = self.values[j], self.values[i]
        self.priorities[i], self.priorities[j] = \
        self.priorities[j], self.priorities[i]
        self.location[self.values[i]] = i
        self.location[self.values[j]] = j

    def _getParentIndex(self, child_index: Index) -> (Index | None):
        """
        힙 내 특정 데이터의 부모 데이터의 인덱스 반환. 
        부모 데이터가 존재하지 않으면 None을 반환. 
        """
        parent_index = child_index // 2
        if parent_index >= 1:
            return parent_index
        return None
    
    def _getChildIndex(self, parent_index: Index) \
        -> (tuple[Index | None, Index | None]):
        """
        힙 내의 특정 데이터의 두 (왼쪽, 오른쪽) 자식 데이터의 인덱스 반환. 
        자식 데이터가 존재하지 않을 경우의 반환값) \n
        - 두 자식 데이터 모두 없는 경우: (None, None) \n
        - 왼쪽 자식 데이터만 없는 경우: (None, Index) \n
        - 오른쪽 자식 데이터만 없는 경우: (Index, None) \n
        """
        lchild_index = parent_index * 2
        rchild_index = parent_index * 2 + 1
        if lchild_index > self.N:
            lchild_index = None
        if rchild_index > self.N:
            rchild_index = None
        return lchild_index, rchild_index
    
    def _goUp(self, target_idx: Index) -> (None):
        """
        enqueue를 통해 새 데이터 입력 시 힙 순위 특성에 맞게 재배치하기 위해 
        새 데이터를 우선순위에 따라 더 높은 층으로 이동시킨다. 

        매개변수
        -------
        target_idx: 새로 입력되어 힙 내에서 재배열이 필요한 데이터의 인덱스.
        """
        parent_idx = self._getParentIndex(target_idx)
        while parent_idx:
            if self._less(parent_idx, target_idx):
                self._swap(parent_idx, target_idx)
            else:
                # 이미 경로 내 정렬이 모두 끝났으므로 작업 종료.
                break

    def _goDown(self, target_idx: Index):
        """
        dequeue 작업에 의해 맨 마지막에 있던 데이터가 최상위 층으로 이동한 경우, 
        힙 순서 특성을 맞추기 위해 해당 데이터의 위치를 필요한 만큼 힙 구조의 
        아래로 내려가게끔 하는 메서드. 

        매개변수
        -------
        target_idx: dequeue 작업에 의해 최상위 층으로 이동된 데이터의 인덱스.
        """
        lchild_idx, rchild_idx = self._getChildIndex(target_idx)
        while lchild_idx or rchild_idx:
            if rchild_idx is None and self._less(target_idx, lchild_idx):
                self._swap(target_idx, lchild_idx)
            elif rchild_idx is None and not self._less(target_idx, lchild_idx):
                break

            if (self._less(target_idx, lchild_idx) or 
                  self._less(target_idx, rchild_idx)):
                if self._less(lchild_idx, rchild_idx):
                    self._swap(target_idx, rchild_idx)
                    target_idx = rchild_idx
                else:
                    self._swap(target_idx, lchild_idx)
                    target_idx = lchild_idx
                lchild_idx, rchild_idx = self._getChildIndex(target_idx)
            else: break

    def enqueue(self, v: Value, p: Priority) -> (None):
        self.N += 1
        #self.values[self.N], self.priorities[self.N] = v, p
        self.values.append(v)
        self.priorities.append(p)
        self.location[v] = self.N
        self._goUp(self.N)

    def dequeue(self) -> (Value | None):
        if self.isEmpty(): return

        value_to_be_removed = self.values[1]
        if self.N == 1: 
            self.N -= 1
            return value_to_be_removed
        
        self.values[1] = self.values.pop()
        self.priorities[1] = self.priorities.pop()
        self.location[self.values[1]] = 1
        self.location.pop(value_to_be_removed)
        self.N -= 1
        self._goDown(1)
        return value_to_be_removed

    def decreasePriority(
            self,
            target_value: Value,
            lower_priority: Priority
        ) -> (None):
        """
        target_value 매개변수로 입력받은 값의 우선순위의 수치값을 
        lower_priority 매개변수로 입력받은 우선순위 수치값으로 낮춰서 
        해당 데이터의 우선순위를 키우는 메서드. 
        target_value의 우선순위 수치값은 lower_priority의 값보다 더 
        커야 한다. 
        """
        try:
            target_idx = self.location[target_value]
        except KeyError:
            # target_value가 우선순위 큐에 없는 경우.
            print(f"에러: 값 {target_value}는 우선순위 큐에 존재하지 않습니다.")
            return
        if self.priorities[target_idx] <= lower_priority:
            error_msg = """
            Error from decreasePriority() in class IndexedMinPQ. 
            target_value의 우선순위 값이 lower_priority의 값보다 더 
            작습니다. 
            """
            raise RuntimeError(error_msg)
        
        self.priorities[target_idx] = lower_priority
        self._goUp(target_idx)


class SingleNodeShortestPath():
    """
    weighted graph에서 가중치를 고려하여 source 노드에서 특정 노드까지의 
    최단 거리 및 해당 경로를 찾는 알고리즘 모음.
    """
    def __init__(
        self, 
        graph_inst: nx.Graph | nx.DiGraph,
        source_node: Node,
        target_node: Node
        ):
        self.graph = graph_inst
        self.src = source_node
        self.tar = target_node
        self.dist_to: dict[Node, Distance] = {}
        self.edge_to: dict[Node, Edge] = {}

    def dijkstraAlgorithm(self) -> (None):
        """
        weighted graph에서 가중치를 고려하여 source 노드로부터 특정 노드까지의 
        최단 거리와 그 경로를 구하는 함수. 해당 함수는 모든 가중치가 양수여야만 
        제대로 작동한다. 
        undirected graph에서도 잘 작동할 지 테스트 필요.
        """
        # source node는 거리를 0으로 초기화하고, 나머지 노드들에 대해서는 
        # 모두 무한대(inf)로 지정한다. 
        dist_to: dict[Node, Distance] = {v:INF for v in self.graph.nodes()}
        dist_to[self.src] = 0

        impq = IndexedMinPQ()   #2
        impq.enqueue(self.src, dist_to[self.src])
        for v in self.graph.nodes():
            if v != self.src:
                impq.enqueue(v, INF)

        def relax(e) -> (None):
            """
            source 노드에서 target 노드까지의 최단 거리를 탐색하는 함수.
            """
            # edge (n, v)에서 노드 n, v와 가중치 weight를 추출.
            n, v, weight = e[0], e[1], e[2]['weight']   #5

            # 특정 노드로부터 n까지의 거리와 그 노드에서  
            # 노드 v로 향하는 edge weight 가중치 값을 더한 값이 
            # v로 직접 향하는 경로보다 더 짧으면 더 짧은 경로를 찾았다는 뜻. 
            # 따라서 해당 값을 새로 dist_to[v]에 갱신한다.
            if dist_to[n] + weight < dist_to[v]:   #6
                dist_to[v] = dist_to[n] + weight   #7

                # Dijkstra 알고리즘을 통해 노드 v로 향하는 짧은 경로에 해당하는
                # edge (n, v)를 기록.
                edge_to[v] = e    #8

                # 노드 v의 우선순위 수치값을 새로 발견한 최단 거리값으로 낮춘다. 
                # 이를 통해 후에 while 문에서 최단 경로를 가지는 노드 추출이 
                # 가능해진다. 
                impq.decreasePriority(v, dist_to[v])   #9

        # edge_to: 탐색 동안 찾은 v 노드로 향하는 edge를 기록.
        edge_to: dict[Node, Edge] = {}    #3
        while not impq.isEmpty():
            n = impq.dequeue()   #4

            # G.edges(data=True): edge의 가중치(weight) 추출을 위해 
            # data=True로 설정해줘야 함.
            # n과 연결된 edge들을 반환.
            for e in self.graph.edges(n, data=True):
                relax(e)
        self.dist_to = dist_to.copy()
        self.edge_to = edge_to.copy()

    def bellmanFordAlgorithm(self) -> (None):
        """
        Directed weighted graph에 대해서, 전체 가중치 중 하나라도 음수가 있는 
        경우 source 노드에서 특정 노드까지의 최단 거리 및 경로를 탐색하고 이를 
        반환하는 함수. 
        """
        dist_to: dict[Node, Distance] = {v:INF for v in self.graph.nodes()}    #1
        dist_to[self.src] = 0
        edge_to: dict[Node, Edge] = {}    #2

        def relax(e):
            u, v, weight = e[0], e[1], e[2]['weight']
            if dist_to[u] + weight < dist_to[v]:    #5
                dist_to[v] = dist_to[u] + weight    #6
                edge_to[v] = e    #7
                return True    #8  # 노드 v로 향하는 최단 경로를 찾았다는 뜻.
            return False
        
        # 모든 edge들에 대해 전체 노드 N개에 대해 작업 수행.
        for i in range(self.graph.number_of_nodes()):    #3
            for e in self.graph.edges(data=True):    #4
                if relax(e):
                    # 주어진 전체 노드 개수 N에 대해, 가장 긴 경로를 구성하는 
                    # edge의 개수는 적어도 N-1을 넘지는 않는다. 
                    # 마지막 노드에 대해서도 src 노드로부터 특정 노드 v로
                    # 향하는 최단 경로를 새로 발견한다면 (즉, 거리값이 줄었다면)
                    # 이는 negative cycle에 갇힘을 의미.
                    if i == self.graph.number_of_nodes() - 1:    #9
                        raise RuntimeError("Negative cycle exists in graph.")
        self.dist_to = dist_to.copy()
        self.edge_to = edge_to.copy()

    def reconstructShortestPath(self) -> (list[Node]):
        """
        dijkstra 또는 bellman-ford 알고리즘을 통해 얻은 각 노드와 
        각 노드로 향하는 최단 거리 edge 정보를 담은 edge_to를 통해 
        source 노드로부터 target 노드까지의 최단 거리를 
        이루는 경로를 재구성하여 이를 반환하는 함수.
        """
        if self.tar not in self.edge_to:
            error_msg = f"""Error from function shortest_path(). 
            target node {self.tar} is unreachable."""
            raise ValueError(error_msg)
        
        path: list[Node] = []
        current_node = self.tar
        while current_node != self.src:
            path.append(current_node)
            current_node = self.edge_to[current_node][0]
        path.append(self.src)
        path.reverse()
        return path
    
    def getShortestDistance(self) -> (Distance):
        """
        source node로부터 target node로 가는 최단 거리를 반환.
        """
        return self.dist_to[self.tar]


class AllPairShortestPath():
    """
    weighted graph에서 가중치를 고려하여 임의의 두 노드 u, v에 대해 
    u에서 v로 향하는 최단 거리와 그 경로를 구하는 알고리즘 클래스. 
    Single node shortest path 문제에서는 source 노드라는 시작점이 정해진 
    것에 비해, 이 문제는 어떤 두 노드를 임의로 고르더라도 두 노드 간 최단 
    거리 및 경로를 구한다는 차이점이 존재. 
    """
    def __init__(
            self, 
            graph_inst: nx.Graph | nx.DiGraph,
            source_node: Node,
            target_node: Node
        ):
        self.graph = graph_inst
        self.src = source_node
        self.tar = target_node
        self.dist_to: dict[Node, dict[Node, Distance]] = {}
        self.node_from: dict[Node, dict[Node, Node | None]] = {}

    def resetAttr(self) -> (None):
        """
        self.dist_to, self.node_from 등의 인스턴스 속성들을 리셋한다. 
        """
        self.dist_to.clear()
        self.node_from.clear()

    def floydWarshallAlgorithm(self) -> (None):
        self.resetAttr()
        for u in self.graph.nodes():
            self.dist_to[u] = {v:INF for v in self.graph.nodes()}  #2
            self.node_from[u] = {v:None for v in self.graph.nodes()}  #3
            self.dist_to[u][u] = 0  #4  # 자기 자신 노드로의 거리는 0으로 설정.
            for e in self.graph.edges(u, data=True):  #5
                v = e[1]
                # 처음 u -> v 거리는 두 노드 사이의 edge의 가중치로 초기화.
                self.dist_to[u][v] = e[2]["weight"]
                # u -> v로 최단 거리로 향할 때 v 노드로 향하는 이전
                # 노드를 u로 초기화.
                self.node_from[u][v] = u  #6
        
        for k in self.graph.nodes():
            for u in self.graph.nodes():
                for v in self.graph.nodes():
                    shortest_dist = self.dist_to[u][k] + self.dist_to[k][v] #7
                    if shortest_dist < self.dist_to[u][v]:
                        # u -> v로 곧장 가는 것보다 u -> k -> v로 가는 것이 
                        # 더 빠를 경우. 
                        self.dist_to[u][v] = shortest_dist  #8
                        # u -> v로 향할 때 v로 향하는 이전 노드를 
                        # k -> v로 향할 때 v로 향하는 이전 노드로 업데이트.
                        # 예) u -> k -> v일 경우,
                        # node_from[u][v] = node_from[k][v] = k
                        self.node_from[u][v] = self.node_from[k][v]

    def reconstructAllPairsPath(self) -> (list[Node]):
        """
        floydWarshallAlgorithm을 통해 얻은 정보를 통해 
        source 노드로부터 target 노드까지의 최단 경로를 구하고 이를 반환. 
        """
        if self.node_from[self.src][self.tar] is None:
            error_msg = f"""Error from the instance method 
            reconstructAllPairsPath() in class AllPairShortestPath. 
            the path from source node {self.src} to target node {self.tar} is 
            unreachable."""
            raise ValueError(error_msg)
        path = []
        v = self.tar
        while v != self.src:
            path.append(v)
            v = self.node_from[self.src][v]
        path.append(self.src)
        path.reverse()
        return path

    def getShortestDistance(self) -> (Distance):
        """
        src 노드부터 tar 노드로 향하는 최단 경로의 거리를 반환.
        """
        return self.dist_to[self.src][self.tar]
    

def weighted_digraph_set(
        dataset: list[tuple[Node, Node, Weight]]
    ) -> (nx.DiGraph):
    """
    directed, weighted 그래프 설정 및 DiGraph 인스턴스 반환.
    """
    dg = nx.DiGraph()
    dg.add_weighted_edges_from(dataset)
    # 가중치 엣지 추가하는 다른 방법들.
    # dg.add_edge('a', 'b', weight=12)
    # dg.add_edges_from(
    # [('a', 'b', {'weight': 12}), ('b', 'a', {'weight': 5})])
    return dg

def draw_weighted_directed_graph(graph: nx.DiGraph):
    # 각각의 node와 edge들을 그리기 위한 위치 정보.
    # layout 모듈에는 다양한 모양의 그래프 출력을 지원한다.
    draw_pos = nx.layout.spring_layout(graph)

    # 가중치만 따로 그리기 위해 가중치 정보만 추출.
    weight_info: dict[Edge, Weight] = nx.classes.function.get_edge_attributes(graph, 'weight')

    # 두 노드 사이의 엣지가 양방향으로 연결된 경우, 
    # 두 가중치 값이 그래프 상에서 겹쳐서 하나만 보인다. 
    # 이를 해결하기 위해, 양방향 엣지의 가중치들만 따로 추출하여 따로 그리도록 함.
    one_way_weight: dict[Edge, Weight] = {}
    u_to_v_weight: dict[Edge, Weight] = {}
    v_to_u_weight: dict[Edge, Weight] = {}
    for n1, n2 in graph.edges():
        if (n2, n1) in graph.edges():
            u_to_v_weight[(n1, n2)] = weight_info[(n1, n2)]
            v_to_u_weight[(n2, n1)] = weight_info[(n2, n1)]
        else:
            one_way_weight[(n1, n2)] = weight_info[(n1, n2)]
    
    # node, edge 그리기
    nx.drawing.nx_pylab.draw_networkx(graph, pos=draw_pos, with_labels=True)

    # edge 정보 (가중치) 그리기
    nx.drawing.nx_pylab.draw_networkx_edge_labels(
        graph, pos=draw_pos, edge_labels=one_way_weight)
    nx.drawing.nx_pylab.draw_networkx_edge_labels(
        graph, pos=draw_pos, edge_labels=u_to_v_weight, label_pos=0.7)
    nx.drawing.nx_pylab.draw_networkx_edge_labels(
        graph, pos=draw_pos, edge_labels=v_to_u_weight, label_pos=0.3)
    plt.show()

def test_dijkstra(
        dataset: list[tuple[Node, Node, Weight]],
        src: Node,
        tar: Node
    ) -> (None):
    # 초기 그래프.
    dg = weighted_digraph_set(dataset)
    draw_weighted_directed_graph(dg)

    solver = SingleNodeShortestPath(dg, src, tar)
    solver.dijkstraAlgorithm()
    path = solver.reconstructShortestPath()
    print(path)
    print(solver.getShortestDistance())

def test_bellman_ford(
        dataset: list[tuple[Node, Node, Weight]],
        src: Node,
        tar: Node
    ) -> (None):
    dg = weighted_digraph_set(dataset)
    draw_weighted_directed_graph(dg)

    solver = SingleNodeShortestPath(dg, src, tar)
    solver.bellmanFordAlgorithm()
    path = solver.reconstructShortestPath()
    print(path)
    print(solver.getShortestDistance())

def test_floyd_warshall(
        dataset: list[tuple[Node, Node, Weight]],
        src: Node,
        tar: Node
    ) -> (None):
    dg = weighted_digraph_set(dataset)
    draw_weighted_directed_graph(dg)

    solver = AllPairShortestPath(dg, src, tar)
    solver.floydWarshallAlgorithm()
    path = solver.reconstructAllPairsPath()
    print(path)
    print(solver.getShortestDistance())

if __name__ == '__main__':
    test_dataset = [
        ('a', 'b', 4), ('b', 'a', 2),
        ('a', 'c', 3), ('b', 'd', 5), 
        ('d', 'b', 1), ('d', 'c', 7), 
        ('c', 'b', 6),
    ]
    test_dataset2 = [
        ('a', 'b', 4), ('b', 'a', -2),
        ('a', 'c', -3), ('b', 'd', 5), 
        ('d', 'b', -1), ('d', 'c', 7), 
        ('c', 'b', 6),
    ]
    test_dataset3 = [
        ('a', 'b', 3), ('a', 'c', 1),
        ('b', 'd', -2), ('c', 'd', 1),
    ]
    test_dataset4 = [
        ('a', 'b', -3), ('b', 'c', 1),
        ('c', 'd', 1), ('d', 'e', 1),
    ]  # no negative cycle
    test_dataset5 = [
        ('a', 'b', -3), ('b', 'c', 1),
        ('c', 'd', 1), ('d', 'e', 1),
        ('e', 'a', -1),
    ] # negative cycle
    #test_dijkstra(test_dataset3, 'a', 'd')
    #test_bellman_ford(test_dataset2, 'a', 'c')
    #test_floyd_warshall(test_dataset, 'a', 'd')
    test_floyd_warshall(test_dataset2, 'd', 'c')

    #test_dijkstra(test_dataset4, 'a', 'e')
    #test_bellman_ford(test_dataset4, 'a', 'e')
    #test_bellman_ford(test_dataset5, 'a', 'e')
    pass
    