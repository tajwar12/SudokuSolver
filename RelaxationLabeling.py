
from random import randint

import numpy as np
import queue


numberofcells = 9
totalcells = 81

#Below two codes is used for the probabities and Creating Rij Matric
p = np.ones((totalcells * numberofcells, 1)) / numberofcells
rij = np.zeros((totalcells * numberofcells, totalcells * numberofcells))

#so we create a CSV file to fill it with Rij values

def CreatingRijMatrix():

#looping all over the cells and ckecking compatibility Matrix
    for i in range(totalcells):
        for lb in range(numberofcells):
            for j in range(totalcells):
                for mu in range(numberofcells):
                    rij[i * numberofcells + lb][j * numberofcells + mu] = CompatibilityMatrix(i, j, lb, mu)
    np.savetxt('rij.csv', rij, delimiter=',')

def VectorInitialization(board):
#for initilizing the board
    BoardVectorInitialization(board)

def BoardVectorInitialization(board):


    board = StateOfCurrentCell(board)
    numberofcells = board.blockSize

    for i in range(numberofcells):
        for j in range(numberofcells):
            domainSet = board.getDomainSet(i,j)
            n = len(domainSet)
            prob = np.zeros((1, numberofcells))[0]
            if not board.isEmpty(i,j):# values are just assigned if not empty
                val = int(board.getValue(i,j))
                prob[val-1] = 1
            else:
                for k in domainSet:
                    prob[int(k) - 1] = 1/n + randint(0,20)/100.0
            prob = prob/np.sum(prob)
            p.reshape(numberofcells, numberofcells, numberofcells)[i][j] = prob

#here we will show compatibility matrix of a Sudoku
def CompatibilityMatrix(i, j, l, m):
    if i == j:
        return 0
    if l != m:
        return 1
    if SameRow(i, j) or SameColumn(i, j) or SameBox(i, j): #checking the constraints
        return 0
    return 1
# it will only return 0 or 1 to show if assignment is valid or not


#if in a same column return cell
def SameColumn(i, j):

    return i % numberofcells == j % numberofcells
#if in a same row return cell
def SameRow(i, j):

    return i // numberofcells == j // numberofcells

#if in a same box return cell
def SameBox(i, j):


    i_x = i // numberofcells
    i_y = i % numberofcells
    j_x = j // numberofcells
    j_y = j % numberofcells
    start_i_x = i_x - i_x%3
    start_i_y = i_y - i_y%3
    start_j_x = j_x - j_x%3
    start_j_y = j_y - j_y%3
    return start_i_x == start_j_x and start_i_y == start_j_y

#according to formula we compute average consistency
def FindingAverageConsistency(q):
    return np.sum(p*q)

#Main Algorithm
def RelaxationLabelingOnSudoku():
    global rij, p #rij coefficient
    diff = 1
    avg_b = 0
    t = 0

    while diff > 0.001: #stopping criteria
        q = np.dot(rij, p) #dot product of coefficient and probability
        num = p * q
        row_sums = num.reshape(numberofcells * numberofcells, numberofcells).sum(axis=1)
        p = (num.reshape(numberofcells * numberofcells, numberofcells) / row_sums[:, np.newaxis]).reshape(729, 1)
        avg = FindingAverageConsistency(q)
        diff = avg - avg_b
        avg_b = avg
        t += 1
        #above three line are actually related to convergence
    p = p.reshape(totalcells, numberofcells)


#Creating and Writing in Rij Matrix
#Creating the board
#solving the board
def solve_relaxationLabeling(SudokuBoard, create = False):
    global p, rij
    if create: CreatingRijMatrix() # creating Rij Matrix if its not created for the first time
    VectorInitialization(SudokuBoard)

    rij = np.loadtxt("rij.csv", delimiter=",") # createRij()

    #applying the algorithm on the Sudoku Board
    RelaxationLabelingOnSudoku()


    # After algorithm is finished it will again print the Board
    for i in range(len(SudokuBoard)):
        if i % 3 == 0 and i != 0:
            print("-----------------------")

        for j in range(len(SudokuBoard[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(SudokuBoard[i][j])
            else:
                print(str(SudokuBoard[i][j]) + " ", end="")



#this class is used and the basic purpose of this class is to the assigments of values
class AssignmentQueue:
    assign_queue = queue.Queue(0)

    @staticmethod
    def push(value):
        AssignmentQueue.assign_queue.put(value)
        return True

    @staticmethod
    def pop():
        value = AssignmentQueue.assign_queue.get()
        return value

    @staticmethod
    def empty():
        return AssignmentQueue.assign_queue.empty()

#Find the values of the cells
class ValueOfCells:
    def __init__(self, value, x, y):
        self.val = value
        self.x = x
        self.y = y

#Class State is used to find what is the state of the cell
class StateOfCurrentCell:

    def __init__(self, sudokuboard):
        ncells = len(sudokuboard)
        self.blockSize = ncells  # blocks have dimension ncells x ncells
        self.counter = 0
        self.BoardInitialization(sudokuboard)


#Have to initialize th board for finding the states
    def BoardInitialization(self, board):
        ncells = self.blockSize
        self.cells = []
        for i in range(0, ncells*ncells):
            self.cells.append(['0',[str(i) for i in range(1,ncells+1)]])

        for i in range(0,self.blockSize):
            for j in range(0, self.blockSize):
                if board[i][j] != '0':
                    value = ValueOfCells(str(board[i][j]), i, j)
                    if not self.AssignValueToCells(value):
                        return False
        return True

#assignment of the values
    def AssignValueToCells(self, value):
        if self.SatisfyingAllConstraints(value):
            self.cells[value.x * self.blockSize + value.y] = [str(value.val),[]]
            self.counter = self.counter + 1
            return True

        return False


#when assigning need to transverse the whole Sudoku board
    def SatisfyingAllConstraints(self, value):
        return self.isEmpty(value.x,value.y) and self.BoxConstraint(value) and self.TransverseColumn(value) and self.TransverseRow(value)

    def TransverseColumn(self, value):
        columns = list(range(0, self.blockSize))

        for j in columns:
            if not self.removeConstraintValue(value.x, j, value):
                return False
        return True

    def TransverseRow(self, value):
        rows = list(range(0, self.blockSize))
        for i in rows:
            if not self.removeConstraintValue(i, value.y, value):
                return False
        return True

    def BoxConstraint(self, value):
        start_x = value.x - value.x%3
        start_y = value.y - value.y%3

        for i in range(start_x, start_x +3):
            for j in range(start_y, start_y + 3):
                if not self.removeConstraintValue(i,j,value):
                    return False
        return True

    def indirectConstraint(self):
        indirect = False
        for i in [0,3,6]:
            for j in [0,3,6]:
                occ = [ValueOfCells(0, 0, 0)] * self.blockSize
                for x in range(i,i+3):
                    for y in range(j,j+3):
                        domainSet = self.cells[x * self.blockSize + y][1]
                        for k in domainSet:
                            k = int(k)
                            occ[k-1] = ValueOfCells(occ[k - 1].val + 1, x, y)
                u = 0
                valid = False
                while u < self.blockSize and not valid:
                    if occ[u].val == 1:
                        self.AssignValueToCells(ValueOfCells(str(u + 1), occ[u].x, occ[u].y))
                        valid = indirect = True
                    u = u + 1
        return indirect

# and if the constraints are not compatible remove that constraint and checks for others

    def removeConstraintValue(self, i, j, value):
        domainSet = self.cells[i * self.blockSize + j][1]
        val = self.cells[i * self.blockSize + j][0]

        if val == value.val:
            return False

        if value.val in domainSet:
            domainSet.remove(value.val)

        if len(domainSet) == 1:
            assign = ValueOfCells(domainSet[0], i, j)
            AssignmentQueue.push(assign)
        return True


#Some functions regarding constraints checking
    def isUnique(self, i,j):
        return len(self.cells[i * self.blockSize + j][1])== 1

    def getDomainSet(self, i,j):
        return self.cells[i * self.blockSize + j][1]

    def getValue(self,i,j):
        return self.cells[i * self.blockSize + j][0]

    def isEmpty(self, i,j):
        return (self.cells[i * self.blockSize + j][0] == '0')

    def isFinish(self):
        return self.counter == 81
