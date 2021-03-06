import math
import time

import Tkinter as tk

class RushVisualization:
    def __init__(self, boards, dimension, size, speed):
        "Initializes a visualization with the specified parameters."

        self.boards = boards
        self.speed = speed
        self.dimension = dimension
        self.tileSize = size / self.dimension

        self.width = self.dimension
        self.height = self.dimension

        # Initialize a drawing surface
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, width=size, height=size)
        self.canvas.pack()
        self.window.update()
        
        # Draw gridlines
        for i in range(self.dimension + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, self.dimension)
            self.canvas.create_line(x1, y1, x2, y2)
        for i in range(self.dimension + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(self.dimension, i)
            self.canvas.create_line(x1, y1, x2, y2)

        #runs the simulation
        self.runBoardsSimulation(self.boards)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        xmapped = x * self.tileSize
        ymapped = y * self.tileSize
        return (xmapped, ymapped)

    def runBoardsSimulation(self, boards):
        """
        Runs a tkinter simulation of all the boards in a path
        :param boards: all the boards that belong the the path that needs to be visualized
        :return: a tkinter visualisation
        """

        # sets a color range for the cars to be colored
        colors = ['#ff99cc', '#99ccff', '#4dff4d', '#ffff4d', '#ff8533', '#b366ff', '#248f24', '#0059b3', '#4dffdb', '#ff1a8c', '#b3ff66', '#660000', '#800040', '#b3d9ff', '#558000', '#003366', '#ffff00', '#ccccff', '#ff6699', '#ff6600', '#008080', '#66ffff', '#009933', '#99ff33']

        # loops over the all the boards
        for board in boards:
            # for each board remove the previous one
            self.canvas.delete(tk.ALL)

            # loop over al board coordinates
            for y in range (len(board)):
                for x in range (len(board[y])):

                    #switch x and y to get right orientation
                    boardValue = board[y][x]
                    # sets the default tilecolor to white
                    tileColor = 'white'

                    # colors the red car red
                    if boardValue == 1:
                        tileColor = 'red'

                    # for al other cars a color from the color range is taken to color it
                    elif boardValue > 1:
                        tileColor = colors[boardValue%len(colors)]

                    # maps the board coordinated to the canvas size
                    x1, y1 = self._map_coords(x, y)
                    x2, y2 = self._map_coords(x + self.tileSize, y + self.tileSize)

                    # creates rectangles on the canvas for all the cars
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=tileColor)
            # updates the canvas with the new board
            self.canvas.update()
            # sets the speed of the animation
            time.sleep(self.speed)

    def done(self):
        # starts the animation loop
        tk.mainloop()