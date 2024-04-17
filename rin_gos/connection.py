from node import *

class Connection:
	def __init__(self, node1, node2):
		self.node1 = node1
		self.node2 = node2
		self.name = 'Соединение'
		self.bandwidth = 0 # Пропуская способность

	def getNode1(self):
		return self.node1

	def getNode2(self):
		return self.node2

	def getBandwidth(self):
		return self.bandwidth

	def setBandwidth(self, new_bandwidth):
		self.bandwidth = new_bandwidth

	def __eq__(self, otherConnection):
		if self.getNode1() == otherConnection.getNode1() and self.getNode2() == otherConnection.getNode2():
			return True