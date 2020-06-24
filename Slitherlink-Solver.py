import os
from tkinter import *

assetPath = os.getcwd() + "/Assets/"

puzzleFile = open(assetPath + "Goal.txt", "r")
puzzleData = puzzleFile.readlines()
puzzleNodes = []
puzzleNumbers = []

class Node:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.possibleConnections = []
        self.connections = []
        self.invalidConnections = []
        canvas.create_oval((x * 30) + 8, (y * 30) + 8, (x * 30) + 12, (y * 30) + 12, fill = "black", tags = "Outline")

    def SetupPossibleConnections(self):
        if (self.x != 0):
            _tempNodes = puzzleNodes[self.y]
            self.possibleConnections.append(_tempNodes[self.x - 1])
        if (self.x != len(puzzleNodes[self.y]) - 1):
            _tempNodes = puzzleNodes[self.y]
            self.possibleConnections.append(_tempNodes[self.x + 1])
        if (self.y != 0):
            _tempNodes = puzzleNodes[self.y - 1]
            self.possibleConnections.append(_tempNodes[self.x])
        if (self.y != len(puzzleNodes) - 1):
            _tempNodes = puzzleNodes[self.y + 1]
            self.possibleConnections.append(_tempNodes[self.x])

    def CutOffExcessConnections(self):
        if (len(self.connections) == 2 and len(self.possibleConnections) != 0):
            for i in self.possibleConnections:
                self.RemoveConnection(i)
        elif (len(self.connections) == 1 and len(self.possibleConnections) == 1):
            self.MakeConnection(self.possibleConnections[0])
        elif (len(self.possibleConnections) == 1 and len(self.connections) == 0):
            self.RemoveConnection(self.possibleConnections[0])

    def MakeConnection(self, node):
        if (node in self.possibleConnections):
            self.possibleConnections.remove(node)
            self.connections.append(node)
            canvas.create_line((self.x * 30) + 10, (self.y * 30) + 10, (node.x * 30) + 10, (node.y * 30) + 10, tags = "Outline")
            node.RespondMakeConnection(self)
            self.CutOffExcessConnections()

    def RespondMakeConnection(self, node):
        self.possibleConnections.remove(node)
        self.connections.append(node)
        self.CutOffExcessConnections()

    def RemoveConnection(self, node):
        if (node in self.possibleConnections):
            self.possibleConnections.remove(node)
            self.invalidConnections.append(node)
            canvas.create_line((self.x * 30) + 10, (self.y * 30) + 10, (node.x * 30) + 10, (node.y * 30) + 10, fill = "gray75", tags = "Outline")
            node.RespondRemoveConnection(self)
            self.CutOffExcessConnections()

    def RespondRemoveConnection(self, node):
        self.possibleConnections.remove(node)
        self.invalidConnections.append(node)
        self.CutOffExcessConnections()

    def GetEnd(self, previousNode):
        if (previousNode == None):
            return self.connections[0].GetEnd(self)
        elif (len(self.connections) == 1):
            return self
        else:
            for i in self.connections:
                if (i != previousNode):
                    return i.GetEnd(self)

class Number:
    def __init__(self, x, y, number):
        self.x = float(x)
        self.y = float(y)
        self.number = number
        self.colour = None
        canvas.create_text((x * 30) + 10, (y * 30) + 10, text = number, tags = "Outline")           

    def SetupNodes(self):
        self.nodes = []
        _tempNodes = puzzleNodes[int(self.y - 0.5)]
        self.nodes.append(_tempNodes[int(self.x - 0.5)])
        self.nodes.append(_tempNodes[int(self.x + 0.5)])
        _tempNodes = puzzleNodes[int(self.y + 0.5)]
        self.nodes.append(_tempNodes[int(self.x + 0.5)])
        self.nodes.append(_tempNodes[int(self.x - 0.5)])

    def SetupAdjacentNumbers(self):
        if (self.number == "3"):
            for i in range(int(self.x - 0.5)):
                if ((self.y - 1.5) - i >= 0):
                    _tempNumbers = puzzleNumbers[int(((self.y - 1.5) - i))]
                    if (_tempNumbers[int((self.x - 1.5) - i)].number == "3"):
                        _tempNumber = _tempNumbers[int((self.x - 1.5) - i)]
                        _tempNumber.nodes[0].MakeConnection(_tempNumber.nodes[1])
                        _tempNumber.nodes[0].MakeConnection(_tempNumber.nodes[3])
                        self.nodes[1].MakeConnection(self.nodes[2])
                        self.nodes[2].MakeConnection(self.nodes[3])
                        break
                    elif (_tempNumbers[int((self.x - 1.5) - i)].number != "2"):
                        break
            if (self.y != 0.5):
                _tempNumbers = puzzleData[int(self.y - 1.5)]
                if (_tempNumbers[int(self.x - 0.5)] == "3"):
                    _tempNumbers = puzzleNumbers[int(self.y - 1.5)]
                    _tempNumber = _tempNumbers[int(self.x - 0.5)]
                    _tempNumber.nodes[0].MakeConnection(_tempNumber.nodes[1])
                    self.nodes[0].MakeConnection(self.nodes[1])
                    self.nodes[2].MakeConnection(self.nodes[3])
            for i in range(int(len(puzzleData[0]) - (self.x + 0.5))):
                if ((self.y - 1.5) - i >= 0):
                    _tempNumbers = puzzleNumbers[int(((self.y - 1.5) - i))]
                    if (_tempNumbers[int((self.x + 0.5) + i)].number == "3"):
                        _tempNumber = _tempNumbers[int((self.x + 0.5) + i)]
                        _tempNumber.nodes[0].MakeConnection(_tempNumber.nodes[1])
                        _tempNumber.nodes[1].MakeConnection(_tempNumber.nodes[2])
                        self.nodes[0].MakeConnection(self.nodes[3])
                        self.nodes[2].MakeConnection(self.nodes[3])
                        break
                    elif (_tempNumbers[int((self.x + 0.5) + i)].number != "2"):
                        break
            if (self.x != 0.5):
                _tempNumbers = puzzleData[int(self.y - 0.5)]
                if (_tempNumbers[int(self.x - 1.5)] == "3"):
                    _tempNumbers = puzzleNumbers[int(self.y - 0.5)]
                    _tempNumber = _tempNumbers[int(self.x - 1.5)]
                    _tempNumber.nodes[0].MakeConnection(_tempNumber.nodes[3])
                    self.nodes[0].MakeConnection(self.nodes[3])
                    self.nodes[1].MakeConnection(self.nodes[2])

    def ConnectionTest(self):
        _tempNode = self.nodes[0]
        nodeConnections = 0
        if (self.nodes[3] in _tempNode.connections):
            nodeConnections = nodeConnections + 1
        if (self.nodes[1] in _tempNode.connections):
            nodeConnections = nodeConnections + 1
        _tempNode = self.nodes[2]
        if (self.nodes[3] in _tempNode.connections):
            nodeConnections = nodeConnections + 1
        if (self.nodes[1] in _tempNode.connections):
            nodeConnections = nodeConnections + 1
        return nodeConnections

    def ConnectionFulfillment(self):
        if (self.number != " "):
            _tempNode = self.nodes[0]
            nodeConnections = 0
            if (self.nodes[3] in _tempNode.possibleConnections or self.nodes[3] in _tempNode.connections):
                nodeConnections = nodeConnections + 1
            if (self.nodes[1] in _tempNode.possibleConnections or self.nodes[1] in _tempNode.connections):
                nodeConnections = nodeConnections + 1
            _tempNode = self.nodes[2]
            if (self.nodes[3] in _tempNode.possibleConnections or self.nodes[3] in _tempNode.connections):
                nodeConnections = nodeConnections + 1
            if (self.nodes[1] in _tempNode.possibleConnections or self.nodes[1] in _tempNode.connections):
                nodeConnections = nodeConnections + 1
            if (self.number == str(nodeConnections)):
                _tempNode = self.nodes[0]
                if (self.nodes[3] in _tempNode.possibleConnections):
                    _tempNode.MakeConnection(self.nodes[3])
                if (self.nodes[1] in _tempNode.possibleConnections):
                    _tempNode.MakeConnection(self.nodes[1])
                _tempNode = self.nodes[2]
                if (self.nodes[3] in _tempNode.possibleConnections):
                    _tempNode.MakeConnection(self.nodes[3])
                if (self.nodes[1] in _tempNode.possibleConnections):
                    _tempNode.MakeConnection(self.nodes[1])

    def ConnectionCutOff(self):
        _tempNode = self.nodes[0]
        nodeConnections = self.ConnectionTest()
        if ((self.number == " " and nodeConnections == 3) or self.number == str(nodeConnections)):
            _tempNode = self.nodes[0]
            if (self.nodes[3] in _tempNode.possibleConnections):
                _tempNode.RemoveConnection(self.nodes[3])
            if (self.nodes[1] in _tempNode.possibleConnections):
                _tempNode.RemoveConnection(self.nodes[1])
            _tempNode = self.nodes[2]
            if (self.nodes[3] in _tempNode.possibleConnections):
                _tempNode.RemoveConnection(self.nodes[3])
            if (self.nodes[1] in _tempNode.possibleConnections):
                _tempNode.RemoveConnection(self.nodes[1])

    def MiscellaneousConnections(self):
        if (self.number == "3"):
            for i in range(len(self.nodes)):
                if (len(self.nodes[i].possibleConnections) == 2 and len(set(self.nodes[i].possibleConnections).intersection(self.nodes)) == 2 and len(self.nodes[i].connections) == 0):
                    self.nodes[i].MakeConnection(self.nodes[NodeAdjustment(i, 1)])
                    self.nodes[i].MakeConnection(self.nodes[NodeAdjustment(i, -1)])
                elif (len(self.nodes[i].connections) == 1):
                    if (self.nodes[i].connections[0] not in self.nodes):
                        self.nodes[NodeAdjustment(i, 1)].MakeConnection(self.nodes[NodeAdjustment(i, 2)])
                        self.nodes[NodeAdjustment(i, -2)].MakeConnection(self.nodes[NodeAdjustment(i, -1)])
                if (len(set(self.nodes[i].connections).intersection(self.nodes)) == 2):
                    self.TwoConnectionTest(NodeAdjustment(i, 2))
        elif (self.number == "1"):
            for i in range(len(self.nodes)):
                if (len(self.nodes[i].possibleConnections) == 2 and len(set(self.nodes[i].possibleConnections).intersection(self.nodes)) == 2 and len(self.nodes[i].connections) == 0):
                    self.nodes[i].RemoveConnection(self.nodes[NodeAdjustment(i, 1)])
                    self.nodes[i].RemoveConnection(self.nodes[NodeAdjustment(i, -1)])
                elif (len(self.nodes[i].connections) == 1 and len(set(self.nodes[i].possibleConnections).intersection(self.nodes)) == len(self.nodes[i].possibleConnections)):
                    self.nodes[NodeAdjustment(i, 1)].RemoveConnection(self.nodes[NodeAdjustment(i, 2)])
                    self.nodes[NodeAdjustment(i, -2)].RemoveConnection(self.nodes[NodeAdjustment(i, -1)])
                if (len(set(self.nodes[i].invalidConnections).intersection(self.nodes)) == 2):
                    self.TwoConnectionTest(NodeAdjustment(i, 2))
        elif (self.number == "2"):
            for i in range(len(self.nodes)):
                if (len(set(self.nodes[i].connections).intersection(self.nodes)) == len(self.nodes[i].connections) - 1 and len(set(self.nodes[i].possibleConnections).intersection(self.nodes)) == len(self.nodes[i].possibleConnections)):
                    self.TwoConnectionTest(NodeAdjustment(i, 2))
                elif (len(self.nodes[i].possibleConnections) == 2 and len(set(self.nodes[i].possibleConnections).intersection(self.nodes)) == 2 and len(self.nodes[i].connections) == 0):
                    self.InverseTwoConnectionTest(NodeAdjustment(i, 2))
                elif (len(set(self.nodes[i].connections).intersection(self.nodes)) == len(self.nodes[i].connections) - 1 and len(set(self.nodes[NodeAdjustment(i, 2)].connections).intersection(self.nodes)) == len(self.nodes[NodeAdjustment(i, 2)].connections) - 1):
                    self.TwoConnectionTest(i)
                    self.TwoConnectionTest(NodeAdjustment(i, 2))
        else:
            _deadEndNodes = 0
            for i in range(len(self.nodes)):
                if (len(set(self.nodes[i].possibleConnections).intersection(self.nodes)) == 2 and len(self.nodes[i].possibleConnections) == 2 and len(self.nodes[i].connections) == 0):
                    _deadEndNodes = _deadEndNodes + 1
            if (_deadEndNodes == 3):
                for i in range(len(self.nodes)):
                    if (len(set(self.nodes[i].possibleConnections).intersection(self.nodes)) == 2 and len(self.nodes[i].possibleConnections) == 2 and len(self.nodes[i].connections) == 0):
                        for j in self.nodes[i].possibleConnections:
                            self.nodes[i].RemoveConnection(j)
            for i in range(len(self.nodes)):
                if (len(set(self.nodes[i].possibleConnections).intersection(self.nodes)) == 2 and len(self.nodes[i].possibleConnections) == 2 and len(self.nodes[i].connections) == 1):
                    if ((len(set(self.nodes[NodeAdjustment(i, 1)].possibleConnections).intersection(self.nodes)) == 2 and len(self.nodes[NodeAdjustment(i, 1)].possibleConnections) == 2 and len(self.nodes[NodeAdjustment(i, 1)].connections) == 1)):
                        for j in range(len(self.nodes)):
                            if (len(set(self.nodes[j].possibleConnections).intersection(self.nodes)) == 2 and len(self.nodes[j].possibleConnections) == 3 and len(self.nodes[j].connections) == 1):
                                for k in range(len(self.nodes)):
                                    if (len(set(self.nodes[k].possibleConnections).intersection(self.nodes)) == 2 and len(self.nodes[k].possibleConnections) == 2 and len(self.nodes[k].connections) == 0):
                                        self.nodes[i].MakeConnection(self.nodes[NodeAdjustment(i, 1)])
                                        break
                    else:
                        break

    def TwoConnectionTest(self, nodeNumber):
        _xMov = self.nodes[nodeNumber].x - self.x
        _yMov = self.nodes[nodeNumber].y - self.y
        if (_xMov == 0.5):
            _range = len(puzzleData[0]) - (self.x - 0.5)
        else:
            _range = self.x + 0.5
        for i in range(int(_range)):
            if ((self.y - 0.5) + i * _yMov * 2 >= 0 and (self.y - 0.5) + i * _yMov * 2 < len(puzzleData) and (self.x - 0.5) + i * _xMov * 2 >= 0 and (self.x - 0.5) + i * _xMov * 2 < len(puzzleData[0])):
                _tempNumbers = puzzleNumbers[int((self.y - 0.5) + i * _yMov * 2)]
                _tempNumber = _tempNumbers[int((self.x - 0.5) + i * _xMov * 2)]
                if (_tempNumber.number == "2" or _tempNumber == self):
                    if (len(_tempNumber.nodes[nodeNumber].possibleConnections) - len(set(_tempNumber.nodes[nodeNumber].possibleConnections).intersection(_tempNumber.nodes)) == 1 and len(_tempNumber.nodes[nodeNumber].connections) - len(set(_tempNumber.nodes[nodeNumber].connections).intersection(_tempNumber.nodes)) == 0):
                        for j in _tempNumber.nodes[nodeNumber].possibleConnections:
                            if (j not in _tempNumber.nodes):
                                _tempNumber.nodes[nodeNumber].MakeConnection(j)
                    elif (len(_tempNumber.nodes[nodeNumber].possibleConnections) - len(set(_tempNumber.nodes[nodeNumber].possibleConnections).intersection(_tempNumber.nodes)) == 1 and len(_tempNumber.nodes[nodeNumber].connections) - len(set(_tempNumber.nodes[nodeNumber].connections).intersection(_tempNumber.nodes)) == 1):
                        for j in _tempNumber.nodes[nodeNumber].possibleConnections:
                            if (j not in _tempNumber.nodes):
                                _tempNumber.nodes[nodeNumber].RemoveConnection(j)
                elif (_tempNumber.number == "1"):
                    _tempNumber.nodes[NodeAdjustment(nodeNumber, 1)].RemoveConnection(_tempNumber.nodes[nodeNumber])
                    _tempNumber.nodes[NodeAdjustment(nodeNumber, -1)].RemoveConnection(_tempNumber.nodes[nodeNumber])
                    break
                elif (_tempNumber.number == "3"):
                    _tempNumber.nodes[NodeAdjustment(nodeNumber, 1)].MakeConnection(_tempNumber.nodes[nodeNumber])
                    _tempNumber.nodes[NodeAdjustment(nodeNumber, -1)].MakeConnection(_tempNumber.nodes[nodeNumber])
                    break
                else:
                    break

    def InverseTwoConnectionTest(self, nodeNumber):
        _xMov = self.nodes[nodeNumber].x - self.x
        _yMov = self.nodes[nodeNumber].y - self.y
        if (_xMov == 0.5):
            _range = len(puzzleData[0]) - (self.x - 0.5)
        else:
            _range = self.x + 0.5
        for i in range(int(_range)):
            if ((self.y - 0.5) + i * _yMov * 2 >= 0 and (self.y - 0.5) + i * _yMov * 2 < len(puzzleData) and (self.x - 0.5) + i * _xMov * 2 >= 0 and (self.x - 0.5) + i * _xMov * 2 < len(puzzleData[0])):
                _tempNumbers = puzzleNumbers[int((self.y - 0.5) + i * _yMov * 2)]
                _tempNumber = _tempNumbers[int((self.x - 0.5) + i * _xMov * 2)]
                if (_tempNumber.number == "2"):
                    _tempNumber.TwoConnectionTest(NodeAdjustment(nodeNumber, 1))
                    _tempNumber.TwoConnectionTest(NodeAdjustment(nodeNumber, -1))
                elif (_tempNumber.number == "1"):
                    _tempNumber.nodes[NodeAdjustment(nodeNumber, 1)].RemoveConnection(_tempNumber.nodes[NodeAdjustment(nodeNumber, 2)])
                    _tempNumber.nodes[NodeAdjustment(nodeNumber, -1)].RemoveConnection(_tempNumber.nodes[NodeAdjustment(nodeNumber, 2)])
                    break
                elif (_tempNumber.number == "3"):
                    _tempNumber.nodes[NodeAdjustment(nodeNumber, 1)].MakeConnection(_tempNumber.nodes[NodeAdjustment(nodeNumber, 2)])
                    _tempNumber.nodes[NodeAdjustment(nodeNumber, -1)].MakeConnection(_tempNumber.nodes[NodeAdjustment(nodeNumber, 2)])
                    break
                else:
                    break

    def ColourCode(self):
        if (self.y == 0.5):
            self.BoundaryColours(0, 1)
            self.AdjacentColourCheck(2, 3, -0.5, 0.5)
        elif (self.y == len(puzzleNumbers) - 0.5):
            self.BoundaryColours(2, 3)
            self.AdjacentColourCheck(0, 1, -0.5, -1.5)
        else:
            self.AdjacentColourCheck(0, 1, -0.5, -1.5)
            self.AdjacentColourCheck(2, 3, -0.5, 0.5)
        if (self.x == 0.5):
            self.BoundaryColours(0, 3)
            self.AdjacentColourCheck(1, 2, 0.5, -0.5)
        elif (self.x == len(puzzleNumbers[0]) - 0.5):
            self.BoundaryColours(1, 2)
            self.AdjacentColourCheck(0, 3, -1.5, -0.5)
        else:
            self.AdjacentColourCheck(0, 3, -1.5, -0.5)
            self.AdjacentColourCheck(1, 2, 0.5, -0.5)
        canvas.lift("Outline")

    def BoundaryColours(self, nodeNumber, nodeNumberTwo):
        if (self.nodes[nodeNumber] in self.nodes[nodeNumberTwo].connections):
            canvas.create_rectangle((self.nodes[0].x * 30) + 10, (self.nodes[0].y * 30) + 10, ((self.nodes[0].x + 1) * 30) + 10, ((self.nodes[0].y + 1) * 30) + 10, tags = "Shape", fill = "gray50", outline = "gray50")
            self.colour = "gray50"
        elif (self.nodes[nodeNumber] in self.nodes[nodeNumberTwo].invalidConnections):
            canvas.create_rectangle((self.nodes[0].x * 30) + 10, (self.nodes[0].y * 30) + 10, ((self.nodes[0].x + 1) * 30) + 10, ((self.nodes[0].y + 1) * 30) + 10, tags = "Shape", fill = "gray90", outline = "gray90")
            self.colour = "gray90"

    def AdjacentColourCheck(self, nodeNumber, nodeNumberTwo, xMod, yMod):
        if (self.nodes[nodeNumber] not in self.nodes[nodeNumberTwo].possibleConnections):
            _tempArray = puzzleNumbers[int(self.y + yMod)]
            if (_tempArray[int(self.x + xMod)].colour != None):
                if (self.nodes[nodeNumber] in self.nodes[nodeNumberTwo].connections):
                    self.colour = ColourSwitch(_tempArray[int(self.x + xMod)].colour)
                    canvas.create_rectangle((self.nodes[0].x * 30) + 10, (self.nodes[0].y * 30) + 10, ((self.nodes[0].x + 1) * 30) + 10, ((self.nodes[0].y + 1) * 30) + 10, tags = "Shape", fill = self.colour, outline = self.colour)
                elif (self.nodes[nodeNumber] in self.nodes[nodeNumberTwo].invalidConnections):
                    self.colour = _tempArray[int(self.x + xMod)].colour
                    canvas.create_rectangle((self.nodes[0].x * 30) + 10, (self.nodes[0].y * 30) + 10, ((self.nodes[0].x + 1) * 30) + 10, ((self.nodes[0].y + 1) * 30) + 10, tags = "Shape", fill = self.colour, outline = self.colour)

    def ColourCompare(self):
        if (self.y == 0.5):
            #self.BoundaryColours(0, 1)
            self.AdjacentColourCompare(2, 3, -0.5, 0.5)
        elif (self.y == len(puzzleNumbers) - 0.5):
            #self.BoundaryColours(2, 3)
            self.AdjacentColourCompare(0, 1, -0.5, -1.5)
        else:
            self.AdjacentColourCompare(0, 1, -0.5, -1.5)
            self.AdjacentColourCompare(2, 3, -0.5, 0.5)
        if (self.x == 0.5):
            #self.BoundaryColours(0, 3)
            self.AdjacentColourCompare(1, 2, 0.5, -0.5)
        elif (self.x == len(puzzleNumbers[0]) - 0.5):
            #self.BoundaryColours(1, 2)
            self.AdjacentColourCompare(0, 3, -1.5, -0.5)
        else:
            self.AdjacentColourCompare(0, 3, -1.5, -0.5)
            self.AdjacentColourCompare(1, 2, 0.5, -0.5)

    def AdjacentColourCompare(self, nodeNumber, nodeNumberTwo, xMod, yMod):
        if (self.nodes[nodeNumber] in self.nodes[nodeNumberTwo].possibleConnections):
            _tempArray = puzzleNumbers[int(self.y + yMod)]
            if (_tempArray[int(self.x + xMod)].colour != None):
                if (self.colour == _tempArray[int(self.x + xMod)].colour):
                    self.nodes[nodeNumber].RemoveConnection(self.nodes[nodeNumberTwo])
                elif (self.colour == ColourSwitch(_tempArray[int(self.x + xMod)].colour)):
                    self.nodes[nodeNumber].MakeConnection(self.nodes[nodeNumberTwo])
                    
def ColourSwitch(colour):
    if (colour == "gray50"):
        return "gray90"
    elif (colour == "gray90"):
        return "gray50"

def NodeAdjustment(nodeNumber, increase):
    nodeNumber = nodeNumber + increase
    if (nodeNumber < 0):
        nodeNumber = nodeNumber + 4
    elif (nodeNumber > 3):
        nodeNumber = nodeNumber - 4
    return nodeNumber

def RunThroughNumbers(event):
    for i in range(len(puzzleNumbers)):
        _tempNumbers = puzzleNumbers[i]
        for j in _tempNumbers:
            j.ConnectionCutOff()
            j.ConnectionFulfillment()
            j.MiscellaneousConnections()
            j.ColourCompare()
    for i in range(len(puzzleNodes) - 1):
        _tempNodes = puzzleNodes[i]
        _tempNodesUnder = puzzleNodes[i + 1]
        _possibleCCounter = 0
        _connectionCounter = 0
        for j in range(len(_tempNodes)):
            if (_tempNodes[j] in _tempNodesUnder[j].possibleConnections):
                if (_possibleCCounter > 1):
                    break
                else:
                    _possibleCCounter = _possibleCCounter + 1
            elif (_tempNodes[j] in _tempNodesUnder[j].connections):
                _connectionCounter = _connectionCounter + 1
        if (_possibleCCounter == 1):
            for j in range(len(_tempNodes)):
                if (_tempNodes[j] in _tempNodesUnder[j].possibleConnections):
                    if (_connectionCounter % 2 == 0):
                        _tempNodes[j].RemoveConnection(_tempNodesUnder[j])
                    else:
                        _tempNodes[j].MakeConnection(_tempNodesUnder[j])
    for i in range(len(puzzleNodes[0]) - 1):
        _possibleCCounter = 0
        _connectionCounter = 0
        for j in range(len(puzzleNodes)):
            _tempNodes = puzzleNodes[j]
            if (_tempNodes[i] in _tempNodes[i + 1].possibleConnections):
                if (_possibleCCounter > 1):
                    break
                else:
                    _possibleCCounter = _possibleCCounter + 1
            elif (_tempNodes[i] in _tempNodes[i + 1].connections):
                _connectionCounter = _connectionCounter + 1
        if (_possibleCCounter == 1):
            for j in range(len(puzzleNodes)):
                _tempNodes = puzzleNodes[j]
                if (_tempNodes[i] in _tempNodes[i + 1].possibleConnections):
                    if (_connectionCounter % 2 == 0):
                        _tempNodes[i].RemoveConnection(_tempNodes[i + 1])
                    else:
                        _tempNodes[i].MakeConnection(_tempNodes[i + 1])
    for i in puzzleNodes:
        for j in i:
            if (len(j.connections) == 1):
                _node = j.GetEnd(None)
                if (_node in j.possibleConnections):
                    _makeConnection = True
                    for k in puzzleNumbers:
                        for l in k:
                            nodeConnections = l.ConnectionTest()
                            if (str(nodeConnections) != l.number):
                                _makeConnection = False
                    if (_makeConnection == False):
                        _node.RemoveConnection(j)
                    else:
                        _node.MakeConnection(j)

def Render(event):
    for i in range(len(puzzleNumbers)):
        _tempNumbers = puzzleNumbers[i]
        for j in _tempNumbers:
            if (j.colour == None):
                j.ColourCode()

root = Tk()

xScroll = Scrollbar(root, orient = HORIZONTAL)
xScroll.pack(fill = X, side = BOTTOM)

yScroll = Scrollbar(root)
yScroll.pack(fill = Y, side = RIGHT)

canvas = Canvas(root, xscrollcommand = xScroll.set, yscrollcommand = yScroll.set)
canvas.pack(expand = True, fill = BOTH)

root.bind("u", RunThroughNumbers)
root.bind("r", Render)

for i in range(len(puzzleData)):
    puzzleData[i] = puzzleData[i].replace("\n", "")
    _tempDataArray = puzzleData[i]
    _tempNodes = []
    _tempNumbers = []
    _tempNodes.append(Node(0, i))
    for j in range(len(_tempDataArray)):
        _tempNodes.append(Node(j + 1, i))
        if (_tempDataArray[j] != " "):
            _tempNumbers.append(Number(j + 0.5, i + 0.5, _tempDataArray[j]))
        else:
            _tempNumbers.append(Number(j + 0.5, i + 0.5, " "))
    puzzleNodes.append(_tempNodes)
    puzzleNumbers.append(_tempNumbers)
    if (i == len(puzzleData) - 1):
        _tempNodes = []
        for k in range(len(puzzleData[i]) + 1):
            _tempNodes.append(Node(k, i + 1))
        puzzleNodes.append(_tempNodes)

canvas.config(scrollregion = (0, 0, len(puzzleData[0]) * 30 + 15, len(puzzleData) * 30 + 15))

xScroll.config(command = canvas.xview)
yScroll.config(command = canvas.yview)

for i in puzzleNodes:
    for j in i:
        j.SetupPossibleConnections()

for i in puzzleNumbers:
    for j in i:
        j.SetupNodes()
        j.SetupAdjacentNumbers()

root.mainloop()
