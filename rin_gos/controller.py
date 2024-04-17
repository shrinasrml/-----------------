from PyQt6.QtCore import QModelIndex
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QPen, QColor
from PyQt6.QtWidgets import QMainWindow, QGraphicsView, QGraphicsScene, QPushButton, QDialog, QTableView, QLineEdit, \
    QGraphicsLineItem, QGraphicsTextItem, QGraphicsEllipseItem, QTableWidget, QTableWidgetItem, QVBoxLayout

from connection import Connection
# Импортируем дизайн окон
from main_window import Ui_mw_mainWindow
from add_node import Ui_d_addNodeWindow
from change_node import Ui_d_changeNodeWindow
from delete_node import Ui_d_deleteNodeWindow
from add_connection import Ui_d_addConnectionWindow
from load_matrix import Ui_d_loadMatrixWindow
from shortest_path import Ui_d_shortestWaysWindow

from graph import *
from node import *

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mw_mainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Семестровая работа по компьютерным сетям")

        global graph
        graph = Graph()

        # Работаем со сценой
        self.field = self.findChild(QGraphicsView, "gv_field")
        global scene
        scene = QGraphicsScene()
        self.field.setScene(scene)
        addAxes()

        # Работаем с редактором узлов
        self.addNode = self.findChild(QPushButton, "pb_main_addNode")
        self.addNode.clicked.connect(self.showAddNodeWindow)
        self.changeNode = self.findChild(QPushButton, "pb_main_changeNode")
        self.changeNode.clicked.connect(self.showChangeNodeWindow)
        self.deleteNode = self.findChild(QPushButton, "pb_main_deleteNode")
        self.deleteNode.clicked.connect(self.showDeleteNodeWindow)

        # Работаем с редактором каналов
        self.addConnection = self.findChild(QPushButton, "pb_main_addConnection")
        self.addConnection.clicked.connect(self.showAddConnectionWindow)

        # Работаем с матрицей нагурзки
        self.loadMatrix = self.findChild(QPushButton, "pb_main_loadMatrix")
        self.loadMatrix.clicked.connect(self.showLoadMatrixWindow)

        # Работаем с матрциами вывода
        self.adjacencyMatrix = self.findChild(QPushButton, "pb_main_adjacencyMatrix")
        self.adjacencyMatrix.clicked.connect(self.showAdjacencyMatrix)
        self.incidenceMatrix = self.findChild(QPushButton, "pb_main_incidenceMatrix")
        self.incidenceMatrix.clicked.connect(self.showIncidenceMatrix)

        self.BFS = self.findChild(QPushButton, "pb_shortestPath")
        self.BFS.clicked.connect(self.BFS_clicked)



    def BFS_clicked(self):
        self.BFSMenu = BFSMenu()
        self.BFSMenu.show()

    def showAddNodeWindow(self):
        self.addNodeMenu = AddNodeMenu()
        self.addNodeMenu.show()

    def showChangeNodeWindow(self):
        self.changeNodeMenu = ChangeNodeMenu()
        self.changeNodeMenu.show()

    def showDeleteNodeWindow(self):
        self.deleteNodeMenu = DeleteNodeMenu()
        self.deleteNodeMenu.show()

    def showAddConnectionWindow(self):
        self.addConnectionMenu = AddConnectionMenu()
        self.addConnectionMenu.show()

    def showLoadMatrixWindow(self):
        self.loadMatrix = LoadMatrixMenu()
        self.loadMatrix.show()

    def showAdjacencyMatrix(self):
        AdjacencyMatrix_widget = QTableWidget()
        AdjacencyMatrix = graph.getAdjacencyMatrix()

        if AdjacencyMatrix:
            AdjacencyMatrix_widget.setRowCount(len(AdjacencyMatrix))
            AdjacencyMatrix_widget.setColumnCount(len(AdjacencyMatrix[0]))
            names = graph.getNodeNames()
            AdjacencyMatrix_widget.setVerticalHeaderLabels(names)
            AdjacencyMatrix_widget.setHorizontalHeaderLabels(names)

            for row in range(AdjacencyMatrix_widget.rowCount()):
                for column in range(AdjacencyMatrix_widget.columnCount()):
                    tableItem = QTableWidgetItem()
                    tableItem.setText(str(AdjacencyMatrix[row][column]))

                    AdjacencyMatrix_widget.setItem(row, column, tableItem)

            dialog = QDialog()
            dialog.setWindowTitle("Матрица смежности")
            layout = QVBoxLayout()
            layout.addWidget(AdjacencyMatrix_widget)

            # Установка макета для диалогового окна
            dialog.setLayout(layout)

            # Отображение диалогового окна
            dialog.exec()

    def showIncidenceMatrix(self):
        IncidenceMatrix_widget = QTableWidget()
        IncidenceMatrix = graph.getIncidenceMatrix()

        if IncidenceMatrix:
            IncidenceMatrix_widget.setRowCount(len(IncidenceMatrix))
            IncidenceMatrix_widget.setColumnCount(len(IncidenceMatrix[0]))
            names = graph.getNodeNames()
            IncidenceMatrix_widget.setVerticalHeaderLabels(names)
            IncidenceMatrix_widget.setHorizontalHeaderLabels(names)

            for row in range(IncidenceMatrix_widget.rowCount()):
                for column in range(IncidenceMatrix_widget.columnCount()):
                    tableItem = QTableWidgetItem()
                    tableItem.setText(str(IncidenceMatrix[row][column]))

                    IncidenceMatrix_widget.setItem(row, column, tableItem)

            dialog = QDialog()
            dialog.setWindowTitle("Матрица инценденций")
            layout = QVBoxLayout()
            layout.addWidget(IncidenceMatrix_widget)

            # Установка макета для диалогового окна
            dialog.setLayout(layout)

            # Отображение диалогового окна
            dialog.exec()


class AddNodeMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_d_addNodeWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Добавление узлов")

        # Делаем красивую табличку
        nodeList = self.findChild(QTableView, "tv_nodeList")
        global nodeListModel
        nodeListModel = QStandardItemModel()
        nodeListModel.setHorizontalHeaderItem(0, QStandardItem("Название"))
        nodeListModel.setHorizontalHeaderItem(1, QStandardItem("X"))
        nodeListModel.setHorizontalHeaderItem(2, QStandardItem("Y"))
        nodeList.setModel(nodeListModel)
        nodeList.setColumnWidth(0, 300)
        nodeList.setColumnWidth(1, 50)
        nodeList.setColumnWidth(2, 50)
        for i, node in enumerate(graph.getNodeArray()):
            nameItem = QStandardItem(node.getName())
            xItem = QStandardItem(str(node.getX()))
            yItem = QStandardItem(str(node.getY()))
            nodeListModel.setItem(i, 0, nameItem)
            nodeListModel.setItem(i, 1, xItem)
            nodeListModel.setItem(i, 2, yItem)

        # Работаем с кнопкой добавления узла. Тут ещё поля для нового узла смотрим
        self.le_name = self.findChild(QLineEdit, "le_nodeName")
        self.le_x = self.findChild(QLineEdit, "le_x")
        self.le_y = self.findChild(QLineEdit, "le_y")
        addNode = self.findChild(QPushButton, "pb_addNode")
        addNode.clicked.connect(self.addNode)

    def addNode(self):
        name = self.le_name.text()
        x = self.le_x.text()
        y = self.le_y.text()

        # Добавляем узел в граф
        node = Node(name, int(x), int(y))
        graph.addNode(node)

        # Добавляем узел в таблицу
        nameItem = QStandardItem(name)
        xItem = QStandardItem(x)
        yItem = QStandardItem(y)
        row = graph.nodeCount() - 1
        nodeListModel.setItem(row, 0, nameItem)
        nodeListModel.setItem(row, 1, xItem)
        nodeListModel.setItem(row, 2, yItem)

        refreshScene()


class ChangeNodeMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_d_changeNodeWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Изменение узлов")

        self.le_newName = self.findChild(QLineEdit, "le_newNodeName")
        self.le_newX = self.findChild(QLineEdit, "le_newX")
        self.le_newY = self.findChild(QLineEdit, "le_newY")

        # Работаем с таблицей узлов
        nodeList = self.findChild(QTableView, "tv_nodeList")
        global nodeListModel
        nodeList.setModel(nodeListModel)
        nodeList.setColumnWidth(0, 300)
        nodeList.setColumnWidth(1, 50)
        nodeList.setColumnWidth(2, 50)
        nodeList.clicked.connect(self.nodeList_clicked)

        # Работаем с кнопкой изменения узлов
        changeNode = self.findChild(QPushButton, "pb_changeNode")
        changeNode.clicked.connect(self.changeNode)

    def nodeList_clicked(self, index: QModelIndex):
        self.currentRow = index.row()

        global graph, nodeListModel
        currentNode = graph.getNode(self.currentRow)
        self.le_newName.setText(currentNode.getName())
        self.le_newX.setText(str(currentNode.getX()))
        self.le_newY.setText(str(currentNode.getY()))

    def changeNode(self):
        newName = self.le_newName.text()
        newX = self.le_newX.text()
        newY = self.le_newY.text()

        graph.getNode(self.currentRow).setName(newName)
        graph.getNode(self.currentRow).setX(int(newX))
        graph.getNode(self.currentRow).setY(int(newY))

        nameItem = QStandardItem(newName)
        xItem = QStandardItem(newX)
        yItem = QclassStandardItem(newY)

        nodeListModel.setItem(self.currentRow, 0, nameItem)
        nodeListModel.setItem(self.currentRow, 1, xItem)
        nodeListModel.setItem(self.currentRow, 2, yItem)

        refreshScene()


class DeleteNodeMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_d_deleteNodeWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Удаление узлов")

        # Работаем с таблицей узлов
        nodeList = self.findChild(QTableView, "tv_nodeList")
        global nodeListModel
        nodeList.setModel(nodeListModel)
        nodeList.setColumnWidth(0, 300)
        nodeList.setColumnWidth(1, 50)
        nodeList.setColumnWidth(2, 50)
        nodeList.clicked.connect(self.nodeList_clicked)

        # Кнопка удаления узла
        deleteNode = self.findChild(QPushButton, "pb_deleteNode")
        deleteNode.clicked.connect(self.deleteNode)

        self.currentRow = None

    def nodeList_clicked(self, index: QModelIndex):
        self.currentRow = index.row()

    def deleteNode(self):
        if self.currentRow is not None:
            nodeListModel.removeRow(self.currentRow)

            global graph

            graph.removeNodeIndex(self.currentRow)

            self.currentRow = None

            refreshScene()


class AddConnectionMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_d_addConnectionWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Добавление каналов")

        # Делаем красивую табличку
        global connectionListModel, connectionList
        connectionList = self.findChild(QTableWidget, "tv_connectionList")
        connectionList.setRowCount(graph.nodeCount())
        connectionList.setColumnCount(graph.nodeCount())
        nodeNames = graph.getNodeNames()
        connectionList.setHorizontalHeaderLabels(nodeNames)
        connectionList.setVerticalHeaderLabels(nodeNames)
        nodeCount = graph.nodeCount()
        for i in range(nodeCount):
            for j in range(nodeCount):
                if i == j:
                    blackColorItem = QTableWidgetItem()
                    connectionList.setItem(i, j, blackColorItem)
                    blackColorItem.setBackground(QColor("black"))
                else:
                    if graph.getConnectionFromAM(i, j):
                        greenColorItem = QTableWidgetItem()
                        greenColorItem.setBackground(QColor("Green"))
                        graph.refreshAdjacencyMatrix()
                        greenColorItem.setText(str(graph.getConnectionFromAM(i, j).getBandwidth()))
                        connectionList.setItem(i, j, greenColorItem)
        connectionList.clicked.connect(self.connectionList_clicked)

        # Пропускная способность
        self.bitCount = self.findChild(QLineEdit, "le_bitCount")
        self.bitCount.editingFinished.connect(self.bitCountChanged)

    def connectionList_clicked(self):
        global graph

        self.row = connectionList.currentRow()
        self.column = connectionList.currentColumn()
        connectionList.setCurrentCell(-1, -1)

        if self.row == self.column:
            return

        node1 = graph.getNode(self.row)
        node2 = graph.getNode(self.column)

        for connection in graph.getConnectionArray():
            if Connection(node1, node2) == connection or Connection(node2, node1) == connection:
                whiteColorItem = QTableWidgetItem()
                whiteColorItem.setBackground(QColor("White"))
                connectionList.setItem(self.row, self.column, whiteColorItem)
                whiteColorItem = QTableWidgetItem()
                whiteColorItem.setBackground(QColor("White"))
                connectionList.setItem(self.column, self.row, whiteColorItem)
                graph.removeConnection(connection)
                refreshScene()
                return
        graph.addConnection(Connection(node1, node2))

        bit = graph.getConnectionFromAM(self.row, self.column).getBandwidth()

        greenColorItem = QTableWidgetItem()
        greenColorItem.setBackground(QColor("Green"))
        graph.refreshAdjacencyMatrix()
        greenColorItem.setText(str(bit))
        connectionList.setItem(self.row, self.column, greenColorItem)

        greenColorItem = QTableWidgetItem()
        greenColorItem.setText(str(bit))
        greenColorItem.setBackground(QColor("Green"))
        connectionList.setItem(self.column, self.row, greenColorItem)
        refreshScene()

    def bitCountChanged(self):
        bits = self.bitCount.text()
        graph.getConnectionFromAM(self.row, self.column).setBandwidth(bits)

        #self.bitCount.setText('')

        bitItem = QTableWidgetItem()
        bitItem.setBackground(QColor("Green"))
        bitItem.setText(str(bits))
        connectionList.setItem(self.column, self.row, bitItem)

        bitItem = QTableWidgetItem()
        bitItem.setBackground(QColor("Green"))
        bitItem.setText(str(bits))
        connectionList.setItem(self.row, self.column, bitItem)

class LoadMatrixMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_d_loadMatrixWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Матрциа нагрузки")


        # Делаем красивую табличку
        global loadMatrixList
        loadMatrixList = self.findChild(QTableWidget, "tw_loadMatrix")
        loadMatrixList.setRowCount(graph.nodeCount())
        loadMatrixList.setColumnCount(graph.nodeCount())
        nodeNames = graph.getNodeNames()
        loadMatrixList.setHorizontalHeaderLabels(nodeNames)
        loadMatrixList.setVerticalHeaderLabels(nodeNames)
        nodeCount = graph.nodeCount()
        for i in range(nodeCount):
            for j in range(nodeCount):
                if i == j:
                    blackColorItem = QTableWidgetItem()
                    blackColorItem.setBackground(QColor("black"))
                    loadMatrixList.setItem(i, j, blackColorItem)
                else:
                    zeroItem = QTableWidgetItem()
                    if graph.getLoadMatrix()[i][j] != 0:
                        zeroItem.setText(str(graph.getLoadMatrix()[i][j]))
                    else:
                        zeroItem.setText('0')
                    loadMatrixList.setItem(i, j, zeroItem)
        loadMatrixList.cellChanged.connect(self.loadMatrixListCellChanged)

    def loadMatrixListCellChanged(self, row, col):
        item = loadMatrixList.item(row, col)
        if item is not None:
            graph.getLoadMatrix()[row][col] = int(item.text())

class BFSMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_d_shortestWaysWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Отображение кратчайших путей")

        # Делаем красивую табличку
        global shortestPathList
        shortestPathList = self.findChild(QTableWidget, "tw_shortestPath")
        shortestPathList.setRowCount(graph.nodeCount())
        shortestPathList.setColumnCount(3)
        shortestPathList.setHorizontalHeaderLabels(['Название', 'X', 'Y'])
        nodeNames = graph.getNodeNames()
        NodeArray = graph.getNodeArray()
        nodeXs = [node.getX() for node in NodeArray]
        nodeYs = [node.getY() for node in NodeArray]
        for i in range(graph.nodeCount()):
            tableItem1 = QTableWidgetItem()
            tableItem1.setText(nodeNames[i])
            tableItem2 = QTableWidgetItem()
            tableItem2.setText(str(nodeXs[i]))
            tableItem3 = QTableWidgetItem()
            tableItem3.setText(str(nodeYs[i]))
            shortestPathList.setItem(i, 0, tableItem1)
            shortestPathList.setItem(i, 1, tableItem2)
            shortestPathList.setItem(i, 2, tableItem3)

        shortestPathList.clicked.connect(self.loadMatrixListClicked)

        self.node1 = None
        self.node2 = None

    def loadMatrixListClicked(self):
        row = shortestPathList.currentRow()
        item = shortestPathList.item(row, 0)
        print(item.text())
        for node in graph.getNodeArray():
            if node.getName() == item.text():
                if not self.node1:
                    refreshScene()
                    self.node1 = node
                elif not self.node2:
                    self.node2 = node
        if self.node1 and self.node2:
            path = graph.BFS(self.node1, self.node2)

            for i in range(len(path) - 1):
                knot1 = path[i]
                knot2 = path[i + 1]

                x1 = knot1.getX()
                y1 = knot1.getY()
                x2 = knot2.getX()
                y2 = knot2.getY()
                line = QGraphicsLineItem(x1, -y1, x2, -y2)
                line.setPen(QColor("Red"))
                scene.addItem(line)

            self.node1 = None
            self.node2 = None


def addAxes():
    axis_x = QGraphicsLineItem(-1500, 0, 1500, 0)
    axis_y = QGraphicsLineItem(0, -500, 0, 500)
    scene.addItem(axis_x)
    scene.addItem(axis_y)

    # Добавляем пометки на оси x
    for x in range(-1500, 1501, 300):
        mark = QGraphicsTextItem(str(x))
        mark.setPos(x, 5)  # 5 - расстояние от оси x
        scene.addItem(mark)

    # Добавляем пометки на оси y
    for y in range(-500, 501, 300):
        mark = QGraphicsTextItem(str(-y))
        mark.setPos(-15, y)  # -15 - расстояние от оси y
        scene.addItem(mark)

def refreshScene():
    scene.clear()
    addAxes()
    xynamesArray = [(node.getName(), node.getX(), node.getY()) for node in graph.getNodeArray()]
    circle_radius = 9
    for name, x, y in xynamesArray:
        name_label = QGraphicsTextItem(name)
        name_label.setPos(x + circle_radius, -y - circle_radius - 10)
        circle = QGraphicsEllipseItem(x - circle_radius, -y - circle_radius, 2 * circle_radius, 2 * circle_radius)
        circle.setBrush(QColor(255, 0, 0))  # Красный цвет заливки
        scene.addItem(circle)
        scene.addItem(name_label)

    for connection in graph.getConnectionArray():
        x1 = connection.getNode1().getX()
        y1 = connection.getNode1().getY()
        x2 = connection.getNode2().getX()
        y2 = connection.getNode2().getY()

        line = QGraphicsLineItem(x1, -y1, x2, -y2)
        line.setPen(QColor("Blue"))
        scene.addItem(line)