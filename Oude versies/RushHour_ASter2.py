# Rush Hour
# Name: Nicol Heijtbrink (10580611), Nicole Silverio (10521933) & Sander de Wijs (10582134)
# Course: Heuristieken
# University of Amsterdam
# Time: November-December, 2016

import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import pylab
import math
import Queue as QueueClass
import copy
import time
import csv
import sys

class PQueueItem(object):
    def __init__(self, priority, cars, grid):
        self.priority = priority
        self.cars = cars
        self.grid = grid
        return
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

class Car(object):
    """
    An object which can move around the board.
    """
    def __init__(self, x, y, length, orientation, id):
        """
        Initializes a car with a position with coordinates [x, y] on a board, with a given orientation and id.
        :param x, y, length, orientation, id: All parameters are defined in a separate list.
        """
        self.x = x
        self.y = y
        self.orientation = orientation
        self.length = length
        self.id = id

class Game(object):
    """
    The state of the board (grid), which changes after each movement of a car.
    """
    def __init__(self, dimension, cars):
        """
        Initializes the given grid and creates an empty array, to be filled with cars.
        :param playboard: The given empty grid.
        """
        self.cars = cars
        self.dimension = dimension

        # create a 2d grid consisting of zeros with type integer
        self.grid = np.zeros(shape=(dimension, dimension), dtype=np.int)

        # add each car in self.cars to the grid
        for car in self.cars:
            self.addCarToGrid(car)

        # create a priority queue
        self.queue = QueueClass.PriorityQueue()

        # set the standard priority on 500
        self.priority = 500

        # create a queueItem with the start parameters and put it in the priority queue
        queueItem = PQueueItem(self.priority, copy.deepcopy(self.cars), self.grid.copy())
        self.queue.put(queueItem)

        # create set to store board states
        self.stateSet = set()
        # create list to store single board state
        self.stateList = []

        # create key of starting grid state
        start = self.gridToString()

        # create dictionary of grid state (key) paired to
        # corresponding number of performed moves (value)
        self.moves = {}

        # set start key value
        self.moves[start] = 0

        # create dictionary to be able to deduce the fastest path from the winning board
        self.path = {}

        # list that will be filled with all the board states of the fastest path
        self.all_boards_path = []

        # create a start state to check for the end of the path
        self.start_state = start

    def addCarToGrid(self, car):
        """
        Fill the board with a given car.
        Checks orientation and starting coordinates of car,
        then fills in the rest according to the given length.

        :param car: object with given x, y, length, orientation and idcar
        :return: a filled grid.
        """
        x = car.x
        y = car.y
        # first check orientation of car
        if car.orientation == "H":
            # then replace 0 with idcar integer for length of car
            for i in range(0, car.length):
                if self.grid[x,y] == 0:
                    self.grid[x,y] = car.id
                    x += 1
                else:
                    print car.id
                    print "Error, car cannot be placed on a tile that contains another car"

        elif car.orientation == "V":
            for i in range(0, car.length):
                if self.grid[x,y] == 0:
                    self.grid[x,y] = car.id
                    y += 1
                else:
                    print car.id
                    print "Error, car cannot be placed on a tile that contains another car"
                    # return self.grid

    def canMoveRight(self, car):
        """
        Checks if the location on the right of the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not horizontal, moving to the right is not possible
        if car.orientation == "V":
            return False

        # check if movement to the right would place Car outside of the grid
        if car.x < (self.dimension - car.length):

            # check if movement to the right would cause collision between Cars
            if self.grid[car.x + car.length, car.y] == 0:
                return True
        return False

    def canMoveLeft(self, car):
        """
        Checks if the location on the left of the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not horizontal, moving to the left is not possible
        if car.orientation == "V":
            return False

        # check if movement to the left would place Car outside of the grid
        if car.x > 0:

            # check if movement to the left would cause collision between Cars
            if self.grid[car.x - 1, car.y] == 0:
                return True
        return False

    def canMoveUp(self, car):
        """
        Checks if the location above the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not vertical, moving upwards is not possible
        if car.orientation == "H":
            return False

        # check if upward movement would place Car outside of the grid
        if car.y > 0:

            # check if upward movement would cause collision between Cars
            if self.grid[car.x, car.y - 1] == 0:
                return True
        return False

    def canMoveDown(self, car):
        """
        Checks if the location underneath the car is within the grid and empty.
        :param car: Car object
        :return: True or False
        """

        # if orientation is not vertical, moving downwards is not possible
        if car.orientation == "H":
            return False

        # check if downward movement would place Car outside of the grid
        if car.y < (self.dimension - car.length):

            # check if downward movement would cause collision between Cars
            if self.grid[car.x, car.y + car.length] == 0:
                return True
        return False

    def moveRight(self, carId):

        """
        'Moves' a given car 1 place to the right on the grid.
        Replaces the 0 on the right side next to the car with integer idcar
        and replaces the left side of the car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given car out of list of cars
        car = self.cars[carId.id - 1]

        # replace right side next to the car with integer idcar
        self.grid[car.x + car.length, car.y] = car.id

        # replace the left side of the car with a 0 (empty)
        self.grid[car.x, car.y] = 0

        # update x coordinate
        car.x = car.x + 1

        # update the list of cars with the moved car
        self.cars[car.id - 1] = car

    def moveLeft(self, carId):

        """
        'Moves' a given car 1 place to the left on the grid.
        Replaces the 0 on the left side next to the car with integer idcar
        and replaces the right side of the car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given car out of list of cars
        car = self.cars[carId.id - 1]

        # replace left side next to the car with integer idcar
        self.grid[car.x - 1, car.y] = car.id

        # replace the right side of the car with a 0 (empty)
        self.grid[car.x + (car.length - 1), car.y] = 0

        # update x coordinate
        car.x = car.x - 1

        # update list of cars with moved car
        self.cars[car.id - 1] = car

    def moveDown(self, carId):

        """
        'Moves' a given car 1 place down on the grid.
        Replaces the 0 one place underneath the car with integer idcar
        and replaces the top of the car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given car out of list of cars
        car = self.cars[carId.id - 1]

        # replace one tile underneath the car with integer idcar
        self.grid[car.x, car.y + car.length] = car.id

        # replace the top of the car with a 0 (empty)
        self.grid[car.x, car.y] = 0

        # update y coordinate
        car.y = car.y + 1

        # update list of cars with the moved car
        self.cars[car.id - 1] = car

    def moveUp(self, carId):

        """
        'Moves' a given car 1 place up on the grid.
        Replaces the 0 one place above the car with integer idcar
        and replaces the bottom of the car with a 0.
        :return: grid (with 1 moved car compared to previous state of grid).
        """

        # obtain given car out of list of cars
        car = self.cars[carId.id - 1]

        # replace one tile above the car with integer idcar
        self.grid[car.x, car.y - 1] = car.id

        # replace the bottom of the car with a 0 (empty)
        self.grid[car.x, car.y + (car.length - 1)] = 0

        # update y coordinate
        car.y = car.y - 1

        # update list of cars with moved cars
        self.cars[car.id - 1] = car

    def calculateCost(self, car, gridstring):

        """
        Calculates the cost for a given car in order to give it priority in the queue or not.
        """

        # initial cost for all cars
        cost = 500

        # get the amount of moves made to get to current board state
        moves = self.moves[gridstring]

        # add the cost of the moves to the initial cost
        cost += moves * 10

        # checks if any part of a vertical car is in line and in front of the red car, if so subtract 100 from cost
        if car.orientation == "V" and car.x > self.cars[0].x:
            if car.y == self.cars[0].y:
                cost -= 100
            if car.y - 1 == self.cars[0].y:
                cost -= 100
            if car.length == 3:
                if car.y - 2 == self.cars[0].y:
                    cost -= 100

        # if given car is the red car, give priority
        if car.id == 1:
            cost -= 200

        # gives trucks priority
        if car.length == 3:
            cost -= 500

        # gives cars at the left of the board lower priority
        if car.x < self.dimension/2:
            cost += 100

        # gives the state with the red car at the winning position huge priority
        if self.grid[self.dimension - 1, self.cars[0].y] == 1:
            cost -= 400

        return cost

    def putinQueue(self, car, gridstring):

        """
        Creates a queueItem with the current parameters and puts it in the priority queue
        """

        # call calculateCost to return the priority
        self.priority = self.calculateCost(car, gridstring)

        # create a queueItem with the current priority, a deepcopy of the cars and a copy of the grid
        queueItem = PQueueItem(self.priority, copy.deepcopy(self.cars), self.grid.copy())

        # put the queueItem in the queue
        self.queue.put(queueItem)

    def checkMove(self):

        """
        Checks if a move can be made by trying to put in a set. If the length of the set does not change it means
        this is a duplicate. Returns the length of the set after trying to put the board state in the set
        """

        grid_string = self.gridToString()
        self.stateSet.add(grid_string)
        return len(self.stateSet)

    def gridToString(self):

        """
        Transforms the grid into a string of numbers, representing the state of the board.
        :return: String representing state of board.
        """

        # create variable to store string in
        hash = ""

        # iterate through the grid and place every integer in the hash as a char followed by a comma, creating a string
        for i in range(len(self.grid.T)):
            for j in range(len(self.grid[i])):
                hash += str(self.grid.T[i][j])
                hash += ","
        return hash

    def addToPath(self, car, parentString):

        """
        Links parent board with their child board in dictionaries children and path.
        Then inserts the current grid in the queue.
        Adds 1 to the value of moves with child_string as key.
        """

        # create and set variable to current state as string
        child_string = self.gridToString()

        # set value of child_string key to parentString in path dictionary
        self.path[child_string] = parentString

        # set number of moves paired with child state to number of moves from parent state + 1
        self.moves[child_string] = 1 + self.moves[parentString]

        # create a queueItem and put this in the queue
        self.putinQueue(car, child_string)

    def queueAllPossibleMoves(self):

            """
            For every car all directions are checked. If a car can move in a certain direction it is checked if it is
            already in the archive, if so the board state will not be added to the queue. If it is a new unique board
            state after a move, setNewParent will be called to create a queueItem and put this in the priority queue
            and the move will be reset, also to be able to check the opposite direction.
            """

            # set parent_string to the string of the current board state
            parent_string = self.gridToString()

            # iterate through all the cars in self.cars and check for each direction if a move is possible
            for car in self.cars:

                # check if car can move up
                if self.canMoveUp(car):

                    # length of set before moving car
                    a = Game.checkMove(self)

                    # move the car
                    self.moveUp(car)

                    # length of set after moving car
                    b = Game.checkMove(self)

                    # if the length of the set has changed after a move
                    if a != b:

                        # call addToPath
                        self.addToPath(car, parent_string)

                    #reset move
                    self.moveDown(car)

                # do the same as for moving up
                if self.canMoveDown(car):
                    a = Game.checkMove(self)
                    self.moveDown(car)
                    b = Game.checkMove(self)
                    if a != b:
                        self.addToPath(car, parent_string)
                    self.moveUp(car)

                # do the same as for moving up
                if self.canMoveRight(car):
                    a = Game.checkMove(self)
                    self.moveRight(car)
                    b = Game.checkMove(self)
                    if a != b:
                        self.addToPath(car, parent_string)


                        # check if winning position has been reached in this state
                        if self.grid[self.dimension - 1, self.cars[0].y] == 1:
                            # if winning state has been reached, exit the for loop
                            return False
                    self.moveLeft(car)

                # do the same as for moving up
                if Game.canMoveLeft(self, car):
                    a = Game.checkMove(self)
                    self.moveLeft(car)
                    b = Game.checkMove(self)
                    if a != b:
                        self.addToPath(car, parent_string)
                    self.moveRight(car)

    def makeBestPath(self):

        """
        Makes a list of every board state in strings of the fastest path from the final state to the start state.
        Then each board state, from start to finish, will be converted from a string into a 2d array and saved in a
        list, to be able to visualize the path.
        """

        # make a string of the winning board
        path_state = self.gridToString()

        # initialise an empty list to fill with all the board states of the fastest path in strings
        fastest_path = []

        # add the winning state to the list
        fastest_path.append(path_state)

        # while path_state is not the start state
        while path_state != self.start_state:

            # the previous board state is the value of the current board state key in self.path
            path_previous = self.path.get(path_state)

            # add this state to the list
            fastest_path.append(path_previous)

            # set the current board state to the previous board state
            path_state = path_previous

        # add the start state to the list
        fastest_path.append(self.start_state)

        # for all board states of the fastest path, but from start to finish
        for board_string in reversed(fastest_path):

            # initialise an empty list to fill with the rows of the board
            board_path = []

            # initialise y to zero
            y = 0

            # split the board state by commas
            board_split = board_string.split(",")

            # create as many rows as the dimension
            for i in range(1, self.dimension + 1):

                x = self.dimension * i

                # a row of the board is the split string, index y to x
                board_row = board_split[y:x]

                # append this row to the list
                board_path.append(board_row)

                # set y to x
                y = x

            # make a 2d array of all the rows
            board_path = np.vstack(board_path)

            # make the 2d array into an numpy array with integers
            board_path = np.array(board_path, dtype=int)

            # add this board to the list of all the boards in the path
            self.all_boards_path.append(board_path)

    def writeFile(self, filename):
        # Generate some test data
        data = self.all_boards_path

        # Write the array to disk
        with file(filename, 'w') as outfile:
            # I'm writing a header here just for the sake of readability
            # Any line starting with "#" will be ignored by numpy.loadtxt
            # outfile.write('# Array shape: {0}\n'.format(self.dimension))

            # Iterating through a ndimensional array produces slices along
            # the last axis. This is equivalent to data[i,:,:] in this case
            for data_slice in data:

                # The formatting string indicates that I'm writing out
                # the values in left-justified columns 7 characters in width
                # with 2 decimal places.
                np.savetxt(outfile, data_slice, fmt='%d')

                # Writing out a break to indicate different slices...
                #outfile.write('\n')

    def deque(self):

        """
        Prints starting grid and initiates algorithm to solve the board.
        Prints end state of grid, number of moves, number of iterations and time needed to solve board.
        Afterwards the path to the fastest solution is deduced and saved in a list.
        """

        # start time of the algorithm
        startTime = time.clock()

        print "Starting grid:\n"
        print self.grid.T
        print "\n"

        # set iteration to zero
        iteratrions = 0

        # while the red car is not on the winning position
        while self.grid[self.dimension - 1, self.cars[0].y] != 1:

            # get the first item out of the priority queue
            queueItem = self.queue.get()

            # set self.grid to the grid of queueItem
            self.grid = queueItem.grid

            # set self.cars to the cars of queueItem
            self.cars = queueItem.cars

            # call queueAllPossibleMoves
            self.queueAllPossibleMoves()

            # add one to the iterations
            iteratrions += 1

        # calculate duration of the algorithm
        timeDuration = time.clock() - startTime

        print "End of loop"
        print self.grid.T
        print "Number of moves needed to finish game: ", self.moves[self.gridToString()]
        print "finished in", iteratrions, "iterations"
        print timeDuration

        # save the path to the best solution by calling makeBestPath
        self.makeBestPath()

def loadDataset(filename, cars):
    with open(filename, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)

        dimension = dataset[0][0]
        for carLine in dataset[1:]:
            car = Car(int(carLine[0]), int(carLine[1]), int(carLine[2]), carLine[3], int(carLine[4]))
            cars.append(car)

        return int(dimension)

if (len(sys.argv) == 3):
    cars = []
    filename = str(sys.argv[1])
    dimension = loadDataset(filename, cars)
    game = Game(dimension, cars)
    game.deque()
    game.writeFile(str(sys.argv[2]))
elif (len(sys.argv) != 2):
    print('Error, usage: program.py boardfile.csv')
else:
    cars = []
    filename = str(sys.argv[1])
    dimension = loadDataset(filename, cars)
    game = Game(dimension, cars)
    game.deque()
