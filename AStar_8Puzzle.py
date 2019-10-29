from copy import deepcopy

case = [[2, 4, 3],
        [1, 0, 5],
        [7, 8, 6]]

# [ [2 , 4 , 3],
#[1 , 0 , 5],
# [7 , 8 , 6]]

# [ [8 , 6 , 7],
#[2 , 5 , 4],
# [3 , 0 , 1]]

goal = [[1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]]


def getHammingValue(case):
    global goal
    hammingValue = 0
    for i in range(len(case)):
        for j in range(len(case[i])):
            if case[i][j] != goal[i][j] and goal[i][j] != 0:
                hammingValue += 1

    return hammingValue


def getManhattanDistance(case):

    manhattanSum = 0
    for i in range(len(case)):
        for j in range(len(case[i])):
            value = case[i][j]
            if value != 0:
                targetX = (value - 1) / 3
                targetY = (value - 1) % 3
                deviationX = i - targetX
                deviationY = j - targetY
                if deviationX < 0:
                    deviationX *= -1
                elif deviationY < 0:
                    deviationY *= -1

                manhattanSum += (deviationX + deviationY)

    return manhattanSum


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.queue])

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == []

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def delete(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i].getPriorityValue() <= self.queue[max].getPriorityValue():
                    max = i
            item = deepcopy(self.queue[max])
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()


class States:

    def __init__(self, state, heuristic, dist, priorityValue, directionPath, lastIndex):
        self.heuristic = heuristic
        self.dist = dist
        self.priorityValue = priorityValue
        self.state = state
        self.directionPath = directionPath
        self.lastIndex = lastIndex

    def getPriorityValue(self):
        return self.priorityValue

    def getState(self):
        return self.state

    def getDist(self):
        return self.dist

    def getPath(self):
        return self.directionPath

    def getLastIndex(self):
        return self.lastIndex

    def printList(self):
        print ("dist : ", self.dist)
        print ("state : ", self.state)


def find_index_0(case):
    for i in range(len(case)):
        for j in range(len(case[i])):
            if case[i][j] == 0:
                return i, j


def swap(state, firstIndex, secondIndex):
    temp = state[firstIndex[0]][firstIndex[1]]
    state[firstIndex[0]][firstIndex[1]] = state[secondIndex[0]][secondIndex[1]]
    state[secondIndex[0]][secondIndex[1]] = temp
    return state


if __name__ == '__main__':
    moves = [[-1, 0], [1, 0], [0, 1], [0, -1]]
    currentHeuristic = getHammingValue(case) + getManhattanDistance(case)
    priorityValue = currentHeuristic
    lastZeroIndex = [-1, -1]
    currentState = States(case, currentHeuristic, 0,
                          priorityValue, "Start", lastZeroIndex)
    zero_index = find_index_0(currentState.getState())
    openList = PriorityQueue()
    closeList = []

    # closeList.append(currentState)
    start = deepcopy(currentState)

    while True:

        # currentState.printList()

        if currentState.getState() == goal:
            print ("Found Solution!!")
            # currentState.printList()
            print ("Move = ", currentState.getDist())
            break

        for move in moves:
            predictedMove = zero_index[0] + move[0], zero_index[1] + move[1]
            if predictedMove[0] >= 0 and predictedMove[0] < 3 and predictedMove[1] >= 0 and predictedMove[1] < 3 and predictedMove != currentState.getLastIndex():

                originalState = deepcopy(currentState.getState())
                nextState = swap(originalState, predictedMove, zero_index)
                nextHeuristic = getHammingValue(
                    nextState) + getManhattanDistance(nextState)
                nextDist = currentState.getDist() + 1
                nextPriority = nextHeuristic + nextDist
                lastZeroIndex = deepcopy(zero_index)

                if move == [-1, 0]:
                    tracePath = "Up"
                elif move == [1, 0]:
                    tracePath = "Down"
                elif move == [0, 1]:
                    tracePath = "Right"
                elif move == [0, -1]:
                    tracePath = "Left"

                expandState = States(
                    nextState, nextHeuristic, nextDist, nextPriority, tracePath, lastZeroIndex)
                # expandState.printList()
                openList.insert(expandState)

        backState = deepcopy(currentState)
        currentState = openList.delete()
        zero_index = find_index_0(currentState.getState())

        if currentState.getDist() <= backState.getDist():
            stop = False
            while stop == False:
                stop = True
                for state in closeList:
                    if state.getDist() > currentState.getDist():
                        stop = False
                        # print "Remove"
                        # state.printList()
                        closeList.remove(state)
                        break
                    if state.getDist() == currentState.getDist():
                        closeList.remove(state)
                        stop = False
                        break

        closeList.append(currentState)

    # print len(closeList)
    print (start.getPath())
    start.printList()

    for state in closeList:
        print (state.getPath())
        state.printList()

    # print len(closeList)

    # for state in closeList:
     #   state.printList()
