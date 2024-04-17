from queue import Queue


class Graph:
    def __init__(self):
        self.nodeArray = []
        self.connectionArray = []

        self.loadMatrix = []
        self.adjacencyMatrix = None
        self.incidenceMatrix = None

    def addNode(self, node):
        self.nodeArray.append(node)
        self.refreshLoadMatrix()

    def addConnection(self, connection):
        self.connectionArray.append(connection)

    def getNodeArray(self):
        return self.nodeArray

    def getNodeIndex(self, node):
        return self.nodeArray.index(node)

    def getNodeNames(self):
        nodeNames = []
        for node in self.nodeArray:
            nodeNames.append(node.getName())
        return nodeNames

    def getConnectionArray(self):
        return self.connectionArray

    def getNode(self, index):
        return self.nodeArray[index]

    def getLoadMatrix(self):
        return self.loadMatrix

    def getAdjacencyMatrix(self):
        self.refreshAdjacencyMatrix()
        return self.adjacencyMatrix

    def getIncidenceMatrix(self):
        self.refreshIncidenceMatrix()
        return self.incidenceMatrix

    def nodeCount(self):
        return len(self.nodeArray)

    def removeNode(self, node):
        for conn in self.connectionArray:
            if conn.getNode1() == node or conn.getNode2() == node:
                self.removeConnection(conn)
        self.nodeArray.remove(node)

    def removeNodeIndex(self, index):
        self.removeNode(self.nodeArray[index])


    def removeConnection(self, connection):
        self.connectionArray.remove(connection)


    def neighbors(self, node):
        neighbors = list()
        for connection in self.connectionArray:
            if str(connection.getNode1()) == str(node):
                neighbors.append(connection.getNode2())
            elif str(connection.getNode2()) == str(node):
                neighbors.append(connection.getNode1())
        return neighbors

    def BFS(self, startNode, endNode): # Обход в глубину
        if startNode == endNode:
            return [startNode]

        visited = set()
        queue = Queue()
        parent_map = {}

        queue.put(self.getNodeIndex(startNode))
        visited.add(self.getNodeIndex(startNode))

        while not queue.empty():
            currentNode = self.nodeArray[queue.get()]

            for neighbor in self.neighbors(currentNode):

                if self.getNodeIndex(neighbor) not in visited:
                    queue.put(self.getNodeIndex(neighbor))
                    visited.add(self.getNodeIndex(neighbor))
                    parent_map[self.getNodeIndex(neighbor)] = currentNode

                    if neighbor == endNode:
                        path = [endNode]
                        while path[-1] != startNode:
                            path.append(parent_map[self.getNodeIndex(path[-1])])
                        path.reverse()
                        return path
        return None

    def refreshLoadMatrix(self):
        self.loadMatrix.append(list([0] * (self.nodeCount() - 1)))
        for i in range(self.nodeCount()):
            self.loadMatrix[i].append(0)
        return

    def refreshAdjacencyMatrix(self):
        self.adjacencyMatrix = [[0 for _ in range(self.nodeCount())] for _ in range(self.nodeCount())]
        for connection in self.getConnectionArray():
            index1 = self.getNodeIndex(connection.getNode1())
            index2 = self.getNodeIndex(connection.getNode2())
            self.adjacencyMatrix[index1][index2] = 1
            self.adjacencyMatrix[index2][index1] = 1
        for i in range(self.nodeCount()):
            self.adjacencyMatrix[i][i] = -1

    def refreshIncidenceMatrix(self):
        self.incidenceMatrix = [[0 for _ in range(self.nodeCount())] for _ in range(self.nodeCount())]

        edge_index = 0
        for i in range(self.nodeCount()):
            for j in range(i + 1, self.nodeCount()):  # Перебираем только верхний треугольник матрицы
                if self.adjacencyMatrix[i][j] == 1:
                    # Вершина i инцидентна ребру
                    self.incidenceMatrix[i][edge_index] = 1
                    # Вершина j инцидентна тому же ребру (если граф неориентированный)
                    self.incidenceMatrix[j][edge_index] = 1
                    edge_index += 1

    def getConnectionFromAM(self, i, j):
        self.refreshAdjacencyMatrix()
        if self.adjacencyMatrix[i][j]:
            node1 = self.nodeArray[i]
            node2 = self.nodeArray[j]
            for connection in self.connectionArray:
                if (connection.getNode1() == node1 and connection.getNode2() == node2) or (
                        connection.getNode1() == node2 and connection.getNode2() == node1):
                    return connection