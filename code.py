import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

squaresize = 32
GridSize = 16
windowSize = squaresize * GridSize
px = windowSize/2
py = windowSize/2

def drawMap2D(map) :
    for y in range(len(map)) :
        for x in range(len(map[y])):
            if map[y][x]==1 :
                glColor3f(1.0,1.0,1.0)
            else :
                glColor3f(1.0,0.0,3.0)
            x0 = x*squaresize
            y0 = y*squaresize
            glBegin(GL_QUADS)
            glVertex2i(x0+1,y0+1)
            glVertex2i(x0+1,y0+squaresize-1)
            glVertex2i(x0+squaresize-1,y0+squaresize-1)
            glVertex2i(x0+squaresize-1,y0+1)
            glEnd()


def iterate() :
    glViewport(0,0,windowSize,windowSize)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0,windowSize,0.0,windowSize,0.0,1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

class Grid:
    def __init__(self) :
        self.SIZE = GridSize
        self.grille = [[0 for k in range(self.SIZE)] for j in range(self.SIZE)]

    def gen(self) :
        for y in range(self.SIZE) :
            for x in range(self.SIZE) :
                if x==0 or y==0 or x==self.SIZE-1 or y==self.SIZE-1 or random.randint(0,100)>85:
                    self.grille[y][x] =1


grille = Grid()
grille.gen()

class Inputs:
    def keyboard(key, x, y):
        print(key, x, y)

# The display() method does all the work; it has to call the appropriate
# OpenGL functions to actually display something.
def display():
    # Clear the color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # ... render stuff in here ...
    # It will go to an off-screen frame buffer.
    glLoadIdentity()
    iterate()
    glColor3f(1.0,0.0,3.0)
    #square()
    drawMap2D(grille.grille)
    # Copy the off-screen buffer to the screen.
    glutSwapBuffers()

glutInit(sys.argv)

# Create a double-buffer RGBA window.   (Single-buffering is possible.
# So is creating an index-mode window.)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

glutInitWindowSize(windowSize,windowSize)
glutInitWindowPosition(0,0)

# Create a window, setting its title
glutCreateWindow('Doomineur-3D')

# Set the display callback.  You can set other callbacks for keyboard and
# mouse events.
glutDisplayFunc(display)
glutIdleFunc(display)
glutKeyboardFunc(Inputs.keyboard)

# Run the GLUT main loop until the user closes the window.
glutMainLoop()

