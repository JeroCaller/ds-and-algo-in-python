"""
Undirected_graph 시각화. 
미로를 노드와 엣지의 연결로 보고 미로를 제작. 
그 후 해당 미로를 시각화. 
미로 입구에서 출구까지의 경로를 찾는 여러 알고리즘들을 살펴보기 위한 모듈. 
"""

import networkx as nx
import matplotlib.pyplot as plt
from sub_modules.my_stack import DynamicStack
from sub_modules.my_queue import DynamicQueue
from sub_modules.priorityqueue import PriorityQueue

# type alias
# 노드의 (X, Y) 위치
PosX = int
PosY = int
Node = tuple[PosX, PosY]
PriorNode = Node
CurrentNode = Node
PositionInfo = dict[Node, tuple[PosX, PosY]]
NodeTrace = dict[CurrentNode, PriorNode]

def create_retangular_maze(
        g: nx.Graph, 
        width: int = 3,
        height: int = 5,
        walls: list[tuple[tuple[PosX, PosY], tuple[PosX, PosY]]] = [None]
    ) -> (tuple[nx.Graph, PositionInfo]):
    """
    직사각형의 미로를 구현하는 함수. 
    지나갈 수 있는 빈 공간을 노드, 빈 공간에서 빈 공간으로 가는 길을 
    엣지로 표현. 
    """
    def create_nodes(
            g: nx.Graph, 
            width, 
            height
        ) -> (tuple[nx.Graph, PositionInfo]):
        pos = {}
        for j in range(height):
            for i in range(width):
                g.add_node((i, j))
                pos[(i, j)] = (i, j)
        return g, pos
    
    def create_edges(
            g: nx.Graph, 
            width, 
            height, 
            walls: list[tuple[tuple[PosX, PosY], tuple[PosX, PosY]]]
        ) -> (nx.Graph):
        for j in range(height):
            for i in range(width):
                node = (i, j)
                node_h = (i, j+1)
                node_v = (i+1, j)
                if (node, node_h) not in walls and (node_h, node) not in walls:
                    if j != height - 1:
                        g.add_edge(node, node_h)
                if (node, node_v) not in walls and (node_v, node) not in walls:
                    if i != width - 1:
                        g.add_edge(node, node_v)
        return g

    g, pos = create_nodes(g, width, height)
    g = create_edges(g, width, height, walls)
    return g, pos

def draw_maze(
        g: nx.Graph, 
        positions: PositionInfo, 
    ) -> (None):
    """
    미로 시각화 함수. 
    """
    nx.draw_networkx(g, pos=positions)
    plt.show()


class FindPathInMazeDFS():
    """
    미로를 탈출하는 경로를 찾는 클래스. 
    깊이 우선 탐색법 (Depth First Search)으로 경로를 찾는다. 
    """
    def __init__(
            self,
            maze_g: nx.Graph,
            maze_nodes_pos: PositionInfo,
            source_node: Node = None,
            target_node: Node = None
        ):
        """
        매개변수
        -------
        maze_g: draw_retangular_maze() 함수를 통해 이미 미로를 구성한 \
        nx.Graph 객체. \n
        source_node: 미로의 출발점 노드. \n
        target_node: 미로의 탈출구 노드. 
        """
        self.G: nx.Graph = maze_g
        self.maze_pos: PositionInfo = maze_nodes_pos
        self.src: Node = source_node
        self._target: Node = target_node

        self.node_trace = self._search()
        #self.node_trace = self._recurSearch()
        self.path = self._constructPathToExit(self.node_trace)

    @property
    def source(self) -> (Node): return self.src

    @source.setter
    def source(self, new_src: Node) -> (None): self.src = new_src

    @property
    def target(self) -> (Node): return self._target

    @target.setter
    def target(self, new_target: Node) -> (None): self._target = new_target

    def getPath(self) -> (list[Node]): return self.path

    def _search(self) -> (NodeTrace):
        """
        깊이 우선 탐색법(Depth-First Search)을 통해 미로의 입구부터 
        출구까지의 경로를 탐색. 

        탐색 방법
        ---
        1. 소스 노드(미로 입구)에 플레이어가 발을 디뎠다고 가정하고 해당 노드를 
        이미 방문한 노드로 표시한다. 
        2. 현재 노드에서 인접하고 접근 가능한 (즉, 벽에 막히지 않은 = 엣지가 존재하는) 
        노드들 중 아직 방문하지 않은 노드들 중 하나를 골라 그 곳으로 내딛어 탐색한다. 
        3. 만약 막다른 길(dead end)에 도착하면, 앞서 아직 방문하지 않은 노드들이 
        있는 곳으로 돌아가 아직 방문하지 않은 노드들을 차례대로 다시 방문하고, 
        앞선 과정 2번을 반복한다. 
        4. 이 과정을 모든 접근 가능한(reachable) 노드들에 모두 방문했을 때까지 반복한다. 
        """
        # visited: 이미 방문한 노드들을 기록하는 딕셔너리 변수. 
        # 이미 방문한 노드의 value를 True로 설정한다. 
        # 아직 방문하지 않은 노드들은 해당 변수에 기록되지 않은 상태일 것이다. 
        visited: dict[Node, bool] = {}

        # cp_nodes: current-prior nodes의 줄임말. 
        # 현재 노드와 그 현재 노드에 닿기 위해 접근했던 바로 이전 노드를
        # 딕셔너리 형태로 기록한다. 
        cp_nodes: NodeTrace = {}

        stack: DynamicStack[Node] = DynamicStack()
        visited[self.src] = True
        stack.push(self.src)

        while not stack.is_empty():
            node = stack.pop()
            for adjacent_node in self.G[node]:
                if adjacent_node not in visited:
                    cp_nodes[adjacent_node] = node
                    visited[adjacent_node] = True
                    stack.push(adjacent_node)
        return cp_nodes
    
    def _recurSearch(self) -> (NodeTrace):
        """
        재귀 호출을 이용한 DFS 검색법. 
        """
        def recurDFS(
                node: Node, 
                visited: dict[Node, bool],
                node_trace: NodeTrace
            ) -> (NodeTrace):
            visited[node] = True
            for adjacent_node in self.G[node]:
                if adjacent_node not in visited:
                    node_trace[adjacent_node] = node
                    recurDFS(adjacent_node, visited, node_trace)
            return node_trace
        
        visited: dict[Node, bool] = {}
        cp_nodes: NodeTrace = {}

        cp_nodes = recurDFS(self.src, visited, cp_nodes)
        return cp_nodes
    
    def drawAllPath(self) -> (None):
        """
        DFS_Search 메서드를 통해 얻은 cp_nodes를 통해 
        특정 노드와 그 노드로 향하는 이전 노드간의 관계를 모두 
        direct graph로 나타냄.
        """
        dg = nx.DiGraph()
        positions: PositionInfo = {}
        for cnode, pnode in self.node_trace.items():
            dg.add_nodes_from([cnode, pnode])
            dg.add_edge(cnode, pnode)
            positions[cnode] = cnode
            positions[pnode] = pnode
        nx.draw_networkx(dg, pos=positions)
        plt.show()
    
    def _constructPathToExit(self, cp_nodes: NodeTrace) -> (list[Node]):
        """
        DFS_Search 메서드를 통해 찾은 모든 경로 중, 
        미로 입구(self.src)에서 미로 출구(self.target)로 이어지는 
        경로를 구성한다. 
        """
        if self.src is None:
            print("소스 노드(출발점)를 먼저 설정해주세요.")
            print("source 속성을 통해 설정 가능.")
            return
        if self._target is None:
            print("타겟 노드(탈출구)를 먼저 설정해주세요.")
            print("target 속성을 통해 설정 가능.")
            return
        if self._target not in cp_nodes:
            print("해당 탈출구에 도달할 수 없습니다.")
            return
        
        path: list[Node] = []
        node = self._target
        while node != self.src:
            path.append(node)
            node = cp_nodes[node]
        path.append(self.src)
        path.reverse()
        return path
    
    def drawAnswer(self) -> (None):
        """
        constructPathToExit 메서드를 통해 얻은 
        입구부터 출구까지의 경로를 시각화.
        """
        dg = nx.DiGraph()
        dg.add_node(self.path[0])
        positions = {self.path[0]: self.path[0]}
        for i in range(1, len(self.path)):
            dg.add_node(self.path[i])
            dg.add_edge(self.path[i-1], self.path[i])
            positions[self.path[i]] = self.path[i]
        nx.draw_networkx(dg, pos=positions)
        plt.show()

    def drawBothMazeAndPath(self) -> (None):
        """
        전체 미로와 입구에서 출구로 향하는 경로를 동시에 그려 이를 보여줌. 
        """
        maze_color = 'blue'
        path_color = 'green'
        path_trace = {}
        for i in range(len(self.path)-1):
            path_trace[self.path[i]] = self.path[i+1]
        path_trace = list(path_trace.items())

        edge_colors = []
        for u, v in self.G.edges():
            if (u, v) in path_trace:
                edge_colors.append(path_color)
            else:
                edge_colors.append(maze_color)

        node_colors = []
        for node in self.G.nodes():
            if node in self.path:
                node_colors.append(path_color)
            else:
                node_colors.append(maze_color)
        nx.drawing.nx_pylab.draw_networkx(
            self.G, 
            pos=self.maze_pos, 
            edge_color=edge_colors, 
            node_color=node_colors)
        plt.show()


class FindPathInMazeBFS(FindPathInMazeDFS):
    """
    너비 우선 탐색법(Breadth First Search)으로 미로의 입구부터 출구까지의 
    모든 경로 중 가장 짧은 경로를 찾는 클래스.
    """
    def __init__(
            self, 
            maze_g: nx.Graph, 
            maze_nodes_pos: PositionInfo,
            source_node: Node = None, 
            target_node: Node = None
        ):
        super().__init__(maze_g, maze_nodes_pos, source_node, target_node)
    
    def _search(self) -> (NodeTrace):
        """
        넓이 우선 탐색법(Breadth-First Search)을 통해 미로의 입구부터 
        출구까지의 경로를 탐색. 
        스택 대신 큐를 사용하는 것을 제외하면 _DFS_Search 메서드에 사용된 
        방법, 코드가 거의 일치한다. 
        """
        visited: dict[Node, bool] = {}
        cp_nodes: NodeTrace = {}

        queue: DynamicQueue[Node] = DynamicQueue()
        visited[self.src] = True
        queue.enqueue(self.src)

        while not queue.isEmpty():
            node = queue.dequeue()
            for adjacent_node in self.G[node]:
                if adjacent_node not in visited:
                    cp_nodes[adjacent_node] = node
                    visited[adjacent_node] = True
                    queue.enqueue(adjacent_node)
        return cp_nodes
    

class FindPathInMazeGuided(FindPathInMazeDFS):
    """
    Guided Search 방법을 이용하여 미로의 입구에서부터 출구로 이르는 경로를 
    찾는 클래스.
    """
    def __init__(
            self, 
            maze_g: nx.Graph, 
            maze_nodes_pos: PositionInfo,
            source_node: Node = None, 
            target_node: Node = None
        ):
        super().__init__(maze_g, maze_nodes_pos, source_node, target_node)

    def _calculateDistance(
            self, 
            start_node: Node,
            end_node: Node
        ) -> (int):
        """
        시작 노드에서 도착 노드까지의 거리를 구하고 반환하는 메서드. 
        시작 노드와 도착 노드의 각각 X좌표와 Y좌표끼리 뺀 값들을 더한 값이 
        거리이다. 
        """
        dx = abs(start_node[0] - end_node[0])
        dy = abs(start_node[1] - end_node[1])
        return dx + dy

    def _search(self) -> (NodeTrace):
        """
        Guided Search 방법을 이용하여 모든 가능한 경로를 구하는 메서드. 
        DFS, BFS의 _search 메서드 내 코드 구조가 거의 동일하나, 여기서는 
        max binary heap에 기반한 priority queue를 사용한다. 
        우선순위는 각 노드마다 시작 노드에서 도착 노드까지의 거리(행 + 열)를 
        구한 값에 마이너스 기호를 붙인 값을 우선순위 값으로 함.  
        이러한 방식을 통해 최대한 거리가 짧은 경로를 추적하게끔 함. 
        (하지만 그렇다고해서 항상 최단 경로만을 찾는 것을 보장하지는 않는다고 함)
        """
        visited: dict[Node, bool] = {}
        cp_nodes: NodeTrace = {}

        pq: PriorityQueue[Node] = PriorityQueue()
        visited[self.src] = True
        distance = self._calculateDistance(self.src, self._target)
        pq.enqueue((self.src, -distance))

        while not pq.isEmpty():
            node = pq.dequeue()
            for adjacent_node in self.G[node.value]:
                if adjacent_node not in visited:
                    cp_nodes[adjacent_node] = node.value
                    visited[adjacent_node] = True
                    distance = self._calculateDistance(
                        adjacent_node, self._target
                    )
                    pq.enqueue((adjacent_node, -distance))
        return cp_nodes
    

def test_dfs(g: nx.Graph, pos: PositionInfo, src: Node, target: Node):
    solution_dfs = FindPathInMazeDFS(g, pos, src, target)
    solution_dfs.drawAllPath()
    solution_dfs.drawAnswer()
    print(solution_dfs.getPath())

def test_bfs(g: nx.Graph, pos: PositionInfo, src: Node, target: Node):
    solution_bfs = FindPathInMazeBFS(g, pos, src, target)
    solution_bfs.drawAllPath()
    solution_bfs.drawAnswer()

def test_guided(g: nx.Graph, pos: PositionInfo, src: Node, target: Node):
    solution_guided = FindPathInMazeGuided(g, pos, src, target)
    solution_guided.drawAllPath()
    solution_guided.drawAnswer()

def test_dfs_show_all(g: nx.Graph, pos: PositionInfo, src: Node, target: Node):
    """
    전체 미로와 입구에서 출구로 향하는 경로를 모두 한 그래프로 나타냄. 
    """
    solution_dfs = FindPathInMazeDFS(g, pos, src, target)
    solution_dfs.drawBothMazeAndPath()
    print(solution_dfs.getPath())

def test_bfs_show_all(g: nx.Graph, pos: PositionInfo, src: Node, target: Node):
    solution_bfs = FindPathInMazeBFS(g, pos, src, target)
    solution_bfs.drawBothMazeAndPath()
    print(solution_bfs.getPath())

def test_guided_show_all(g: nx.Graph, pos: PositionInfo, src: Node, target: Node):
    solution_guided = FindPathInMazeGuided(g, pos, src, target)
    solution_guided.drawBothMazeAndPath()
    print(solution_guided.getPath())

if __name__ == '__main__':
    graph = nx.Graph()
    walls = [
        ((0, 1), (1, 1)), ((1, 1), (1, 2)), ((1, 2), (1, 3)),
        ((1, 3), (1, 4)), ((1, 3), (2, 3)), ((2, 0), (2, 1)),
    ]
    g, pos = create_retangular_maze(graph, walls=walls)
    draw_maze(g, pos)

    entrance_node = (0, 2)
    exit_node = (2, 2)

    # 다음의 주석처리된 코드들 중 원하는 테스트만 
    # 골라서 해당 코드만 주석 해제하여 실행하면 된다.

    test_dfs(g, pos, entrance_node, exit_node)
    #test_bfs(g, pos, entrance_node, exit_node)
    #test_guided(g, pos, entrance_node, exit_node)

    #test_dfs_show_all(g, pos, entrance_node, exit_node)
    #test_bfs_show_all(g, pos, entrance_node, exit_node)
    #test_guided_show_all(g, pos, entrance_node, exit_node)
    #print(g.nodes())
