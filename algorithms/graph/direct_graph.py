import networkx as nx
import matplotlib.pyplot as plt

# type alias
# 노드의 (X, Y) 위치
PosX = int
PosY = int

Node = tuple[PosX, PosY]
Edge = list[tuple[Node, Node]]
PositionInfo = dict[Node, tuple[PosX, PosY]]
#PriorNode = Node
#CurrentNode = Node
#NodeTrace = dict[CurrentNode, PriorNode]


def draw_directed_graph(dg: nx.DiGraph, pos: PositionInfo) -> (None):
    """
    방향성 그래프 시각화. 
    """
    nx.draw_networkx(dg, pos=pos)
    plt.show()

def topological_sort(dg: nx.DiGraph):
    """
    위상 정렬. 
    cycle이 존재하지 않는 방향성 그래프를 선형으로 정렬한다. 
    이 때 노드 간 edge의 방향은 항상 오른쪽으로 향하도록 한다. 
    
    문제점)
    edge가 하나도 없는 노드에 대해서도 결과에 포함되어서 
    마치 해당 노드에 edge가 있는 것처럼 착각할 수도 있다. 
    """
    visited: dict[Node, bool] = {}
    result: list[Node] = []

    def dfs(u: Node):
        visited[u] = True
        for v in dg[u]:
            if v not in visited:
                dfs(v)
        # out-degree = 0인 마지막 노드를 먼저 리스트에 삽입.
        result.append(u)

    for u in dg.nodes():
        if u not in visited:
            dfs(u)
    result.reverse() # out-degree = 0인 노드를 맨 오른쪽 끝에 오도록 함.
    return result


class DrawRectGraph():
    """
    방향성 그래프를 직사각형 형태로 생성 및 그리는 클래스. 
    """
    def __init__(
            self,
            start_node: Node = (0, 0),
            end_node: Node = (5, 5), 
            edges: list[tuple[Node, Node]] = []
        ):
        """
        매개변수
        -------
        start_node: 직사각형 형태의 방향성 그래프의 시작 노드. \n 
        end_node: 직사각형 형태의 방향성 그래프의 끝 노드. \n
        start_node부터 end_node까지의 범위 내에 모든 노드들을 자동 형성한다. 
        """
        self._dg = nx.DiGraph()
        self._start_node = start_node
        self._end_node = end_node
        self._edges = edges
        self._positions: PositionInfo = {}

    @property
    def edges(self) -> (list[tuple[Node, Node]]): return self._edges

    @edges.setter
    def edges(self, new_edges: list[tuple[Node, Node]]) -> (None): 
        self._edges = new_edges

    @property
    def startNode(self) -> (Node): return self._start_node

    @startNode.setter
    def startNode(self, new_start_node: Node) -> (None):
        self._start_node = new_start_node

    @property
    def endNode(self) -> (Node): return self._end_node

    @endNode.setter
    def endNode(self, new_end_node: Node) -> (None):
        self._end_node = new_end_node

    @property
    def DG(self) -> (nx.DiGraph):
        self._createDirectedGraph()
        return self._dg

    def removeNodes(self, target_nodes: list[Node]):
        return self._dg.remove_nodes_from(target_nodes)
    
    def removeEdges(self, target_edges: list[Edge]):
        return self._dg.remove_edges_from(target_edges)

    def _createNodes(self):
        for i in range(self._start_node[0], self._end_node[0]+1):
            for j in range(self._start_node[1], self._end_node[1]+1):
                self._dg.add_node((i, j))
                self._positions[(i, j)] = (i, j)

    def _createEdges(self):
        for u, v in self._edges:
            self._dg.add_edge(u, v)

    def _createDirectedGraph(self):
        self._createNodes()
        self._createEdges()

    def drawDirectedGraph(self):
        self._createDirectedGraph()
        draw_directed_graph(self._dg, self._positions)


class CycleDetector():
    """
    방향성 그래프(directed graph)에 cycle(순환 루트)이 존재하는지 검사하는 클래스. 
    """
    def __init__(self, directed_graph: nx.DiGraph):
        self._dg = directed_graph
    
    @property
    def DG(self) -> (nx.DiGraph): return self._dg

    @DG.setter
    def DG(self, new_dg: nx.DiGraph): self._dg = new_dg

    def hasCycle(self) -> (bool):
        """
        그래프에 cycle (순환 노드)이 있는지 확인하는 메서드. 
        존재하면 True, 그렇지 않으면 False 반환. 
        """
        visited: dict[Node, bool] = {}
        in_stack: dict[Node, bool] = {}

        def dfs(u: Node):  #1
            visited[u] = True  #3

            # 재귀 호출 스택에 포함되어 있는 노드들을 기록. 
            # 해당 노드가 재귀 호출 스택에 있다면 해당 노드의 값을 
            # True로 설정. 
            # 만약 해당 노드가 더 이상 재귀 호출 스택에 없다면 
            # 해당 노드의 값을 False로 설정.
            in_stack[u] = True  #2

            for v in self._dg[u]:
                if v not in visited:
                    if dfs(v):  #4
                        # 한 루트만 파고든다. 
                        # 현재 탐색하고 있는 루트가 순환 루트를 이루는지 검사. 
                        # 순환 루트인 경우 True 반환. 
                        return True
                else:
                    if v in in_stack and in_stack[v]:  #5
                        # 노드 v가 이미 방문한 것으로 표시되어 있을 때
                        # (visited[v] = True), 
                        # 해당 노드가 아직 재귀 호출 스택에 존재할 수도 있다. 
                        # 만약 그러한 경우, cycle이다. 
                        return True
            in_stack[u] = False  #6
            return False
        
        # nx.Digraph.nodes() -> list[Node]
        for u in self._dg.nodes():  #7
            if u not in visited:
                if dfs(u):  #8
                    return True
        return False
    
    def findCycle(self) -> (list[Node] | list):
        """
        그래프에서 cycle을 찾고 해당 cycle의 경로를 반환. 
        """
        visited: dict[Node, bool] = {}
        in_stack: list[Node] = []

        def dfs(u: Node):
            visited[u] = True
            in_stack.append(u)
            for v in self._dg[u]:
                if v not in visited:
                    result = dfs(v)
                    if result != []:
                        return result
                elif v in (visited and in_stack):
                    start_idx = in_stack.index(v)
                    end_idx = len(in_stack) - 1
                    cycle_list = in_stack[start_idx:end_idx+1]
                    cycle_list.append(v)
                    return cycle_list
            in_stack.remove(u)
            return []
        
        for u in self._dg.nodes():
            if u not in visited:
                result = dfs(u)
                if result != []:
                    return result
        return []


def test_edges():
    def test_draw_rect_directed_graph(edges):
        s_node, e_node = (0, 0), (2, 2)
        graph_inst = DrawRectGraph(
            start_node=s_node, end_node=e_node, edges=edges
            )
        graph_inst.drawDirectedGraph()

        cycle = CycleDetector(graph_inst.DG)
        print(cycle.hasCycle())
        print(cycle.findCycle())
    
    edges = [
        ((0, 0), (0, 1)),
        ((0, 0), (1, 0)),
        ((0, 1), (0, 2)),
        ((0, 1), (1, 1)),
        ((0, 2), (1, 2)),
        ((1, 0), (2, 0)),
        ((2, 0), (2, 1)),
        ((1, 2), (2, 2)),
    ]
    edges2 = [
        ((1, 1), (2, 1)),
        ((2, 1), (2, 2)),
        ((2, 2), (1, 2)),
        ((1, 2), (1, 1))
    ]
    edges3 = [
        ((1, 1), (2, 1)),
        ((1, 1), (1, 2)),
        ((2, 1), (2, 2)),
        ((1, 2), (2, 2)),
    ]
    edges4 = [
        ((0, 0), (1, 1)),
        ((1, 1), (0, 2)),
        ((0, 2), (0, 1)),
        ((0, 1), (0, 0))
    ]
    edges5 = [
        ((0, 0), (1, 1)),
        ((1, 1), (0, 1)),
        ((0, 1), (0, 0))
    ]
    edges6 = []
    edges6.extend(edges)
    edges6.extend(edges2)
    edges6.remove(((1, 2), (2, 2)))
    test_draw_rect_directed_graph(edges6)

def test_topological_sort():
    def draw_rect_directed_graph(
            s_node: Node, 
            e_node: Node, 
            edges: list[Edge]
        ) -> (nx.DiGraph):
        graph_inst = DrawRectGraph(s_node, e_node, edges)
        graph_inst.drawDirectedGraph()
        cycle = CycleDetector(graph_inst.DG)
        print(cycle.hasCycle())
        return graph_inst.DG
    
    s_node, e_node = (0, 0), (2, 2)
    edges1 = [
        ((0, 0), (0, 1)),
        ((0, 0), (1, 0)),
        ((0, 1), (0, 2)),
        ((0, 1), (1, 1)),
        ((0, 2), (1, 2)),
        ((1, 0), (2, 0)),
        ((2, 0), (2, 1)),
        ((1, 2), (2, 2)),
    ]  # non-cycle
    edges2 = [
        ((1, 1), (2, 1)),
        ((2, 1), (2, 2)),
        ((2, 2), (1, 2)),
        ((1, 2), (1, 1))
    ]  # cycle
    edges3 = [
        ((1, 1), (2, 1)),
        ((1, 1), (1, 2)),
        ((2, 1), (2, 2)),
        ((1, 2), (2, 2)),
    ]  # non-cycle
    edges4 = []
    edges4.extend(edges1)
    edges4.extend(edges2)
    result_dg = draw_rect_directed_graph(s_node, e_node, edges1)
    print(topological_sort(result_dg))

if __name__ == '__main__':
    #test_edges()
    test_topological_sort()
    pass
    