"""
직사각형 미로를 랜덤으로 만드는 알고리즘 모음. 
networkx 모듈을 사용하여 미로의 빈 방을 노드로 표현하고, 인접한 두 빈 방이 
벽에 막혀있지 않고 연결되어 있으면 두 노드를 edge로 연결한다. 
만약 벽에 막혀있다면 두 노드 사이에 edge를 형성하지 않는다. 
노드는 2차원 미로에서의 위치 (X, Y)를 노드로 표현한다. 

랜덤 미로 생성 알고리즘 관련 참고자료들 목록) 
1. https://en.wikipedia.org/wiki/Maze_generation_algorithm
2. https://www.baeldung.com/cs/maze-generation
"""
import networkx as nx
import matplotlib.pyplot as plt
import random
from sub_modules.my_stack import DynamicStack
import draw_maze as dm

# type aliases
PosX, PosY = int, int
Node = tuple[PosX, PosY]
Edge = tuple[Node, Node]
NodePositions = dict[Node, tuple[PosX, PosY]]
NextNode = Node
PriorNode = Node
AdjacentDict = dict[NextNode, PriorNode]

def create_rect_initial_maze(
        graph: nx.Graph, 
        width: int, 
        height: int,
    ) -> (tuple[nx.Graph, NodePositions]):
    """
    직사각형 모양의 미로를 생성한다. 
    초기 미로는 4방향 모두 벽이 존재하지 않는 형태로 만든다.
    
    매개변수
    -------
    width: 전체 미로의 가로 길이.
    height: 전체 미로의 세로 길이.
    """
    def create_nodes() -> (NodePositions):
        pos: NodePositions = {}
        for y in range(height):
            for x in range(width):
                node = (x, y)
                graph.add_node(node)
                pos[node] = (x, y)
        return pos
    
    def connect_all_adjacent_nodes() -> (None):
        """
        모든 인접한 노드끼리 edge로 연결한다. 
        """
        for y in range(height):
            for x in range(width):
                node = (x, y)
                node_w, node_h = (x+1, y), (x, y+1)
                if x != width - 1:
                    graph.add_edge(node, node_w)
                if y != height - 1:
                    graph.add_edge(node, node_h)

    pos = create_nodes()
    connect_all_adjacent_nodes()
    return graph, pos

def draw_maze(graph: nx.Graph, pos: NodePositions):
    """
    미로 출력.
    """
    nx.drawing.nx_pylab.draw_networkx(graph, pos=pos)
    plt.show()


class MazeRandomizedDFS():
    """
    recursive backtracker algorithm이라고도 불린다. 
    미로를 구성하는 여러 노드들 중 하나를 선택한 후, DFS를 이용하여 
    현재 선택된 노드에서 인접한 노드와의 벽을 허무는 
    방식을 통해 미로를 만들어간다. 
    """
    def __init__(
            self, 
            width: int, 
            height: int, 
            multiple_path: bool = True
        ):
        """
        매개변수
        -------
        width: 미로의 가로 길이. \n
        height: 미로의 세로 길이. \n
        multiple_path: 출구로 향하는 경로를 여러 개로 할 지에 대한 변수. \
        True -> 여러 개의 경로 개발. False -> 단 하나의 경로.
        """
        self._graph, self._init_graph = nx.Graph(), nx.Graph()
        self._width = width
        self._height = height
        self._multiple_path = multiple_path
        self._init_graph, self._node_pos = create_rect_initial_maze(self._init_graph, width, height)
        self._source_node, self._target_node = self.chooseSourceAndTargetNode()
        self.removeWalls()

    @property
    def graph(self) -> (nx.Graph): return self._graph

    @property
    def sourceNode(self) -> (Node): return self._source_node

    @property
    def targetNode(self) -> (Node): return self._target_node

    @property
    def mazePos(self) -> (NodePositions): return self._node_pos

    def chooseSourceAndTargetNode(self) -> (tuple[Node, Node]):
        """
        미로를 생성하기 위해 필요한 미로 입구 노드 (source node)와 
        출구 노드 (target node)의 위치를 결정 후 반환. 
        미로 입구, 출구 모두 미로의 변에 위치하도록 함. 
        N, E, W, S: 각각 미로의 북, 동, 서, 남쪽 변. 
        target_node의 위치는 (width-src_x, height-src_y)으로 하여 
        두 노드가 서로 정반대에 위치하도록 함. 
        """
        N, E, W, S = 1, 2, 3, 4
        choose = random.choice([1, 2, 3, 4])
        if choose == N:
            src_x = random.randint(0, self._width-1)
            src_y = self._height - 1
        elif choose == S:
            src_x = random.randint(0, self._width-1)
            src_y = 0
        elif choose == E:
            src_x = self._width - 1
            src_y = random.randint(0, self._height-1)
        else:
            # if choose == W
            src_x = 0
            src_y = random.randint(0, self._height-1)
        tar_x = (self._width - 1) - src_x
        tar_y = (self._height - 1) - src_y
        source_node = src_x, src_y
        target_node = tar_x, tar_y
        return source_node, target_node
    
    def removeWalls(self) -> (None):
        """
        초기 미로를 탐색하면서 일부 벽들을 삭제함으로써 
        복잡한 미로를 형성한다. 
        """
        visited: dict[Node, bool] = {}
        adjacent_dict: AdjacentDict = {}
        stack = DynamicStack()

        stack.push(self._source_node)
        visited[self._source_node] = True
        # 두 빈 방 사이의 벽을 없앤다 = 두 노드를 edge로 잇는다.
        walls_to_be_removed: list[Edge] = []
        while not stack.is_empty():
            u = stack.pop()
            adjacent_nodes = list(self._init_graph[u])
            random.shuffle(adjacent_nodes)
            for v in adjacent_nodes:
                if v not in visited:
                    walls_to_be_removed.append((u, v))
                    adjacent_dict[v] = u
                    visited[v] = True
                    stack.push(v)
        self._graph.add_nodes_from(self._init_graph.nodes())
        self._graph.add_edges_from(walls_to_be_removed)
        if self._multiple_path:
            num_chances = 20  # 기존 미로를 수정할 기회 횟수.
            for i in range(num_chances):
                x = random.randint(0, self._width-1)
                y = random.randint(0, self._height-1)
                u = (x, y)
                adjacent_nodes = list(self._init_graph[u])
                for v in adjacent_nodes:
                    if (u, v) or (v, u) not in self._graph.edges():
                        self._graph.add_edge(u, v)
                        # 특정 노드에 연결되지 않은 edge 수가 둘 이상일 경우
                        # 그 중 하나의 edge만 생성한다.
                        break


def test_randomizedDFS():
    initializer = MazeRandomizedDFS(10, 10)
    print(f"Entrance position: {initializer.sourceNode}")
    print(f"Exit position: {initializer.targetNode}")
    draw_maze(initializer.graph, initializer.mazePos)

def test_find_exit():
    initializer = MazeRandomizedDFS(10, 10)
    print(f"Entrance position: {initializer.sourceNode}")
    print(f"Exit position: {initializer.targetNode}")
    dfs_solver = dm.FindPathInMazeDFS(
        initializer.graph, 
        initializer.mazePos, 
        initializer.sourceNode, 
        initializer.targetNode
    )
    bfs_solver = dm.FindPathInMazeBFS(
        initializer.graph,
        initializer.mazePos,
        initializer.sourceNode,
        initializer.targetNode
    )
    guided_solver = dm.FindPathInMazeGuided(
        initializer.graph,
        initializer.mazePos,
        initializer.sourceNode,
        initializer.targetNode
    )
    # 기본 미로 출력.
    draw_maze(initializer.graph, initializer.mazePos)

    # 정답 출력.
    dfs_solver.drawBothMazeAndPath()
    bfs_solver.drawBothMazeAndPath()
    guided_solver.drawBothMazeAndPath()

if __name__ == '__main__':
    #test_randomizedDFS()
    test_find_exit()
    pass
    