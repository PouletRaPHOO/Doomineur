import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import pi, cos, sin

size = 64
def drawMap2D(map) :
    for y in range(len(map)) :
        for x in range(len(map[y])):
            if map[y][x]==1 :
                glColor3f(1.0,1.0,1.0)
            else :
                glColor3f(1.0,0.0,3.0)
            x0 = x*size
            y0 = y*size
            glBegin(GL_QUADS)
            glVertex2i(x0,y0)
            glVertex2i(x0,y0+size)
            glVertex2i(x0+size,y0+size)
            glVertex2i(x0+size,y0)
            glEnd()


def iterate() :
    glViewport(0,0,500,500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0,500,0.0,500,0.0,1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def square() :
    glBegin(GL_QUADS)
    glVertex2f(100,100)
    glVertex2f(100,200)
    glVertex2f(200,200)
    glVertex2f(200,100)
    glEnd()

class Draw:
    def plot_points(x, y):
        glColor3f(0.0,1.0,0.0)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        glVertex2f(x*size, y*size)
        glEnd()
        glFlush()

    def plot_trait(x, y):
        glColor3f(1.0,0.0,0.0)
        glPointSize(5.0)
        glBegin(GL_LINES)        # GL_POINTS -> GL_LINES
        glVertex2f(0.0, 0.0)
        glVertex2f(1.0, 1.0)         # Added another Vertex specifying end coordinates of line
        glEnd()
        glFlush()






class Grid:
    def __init__(self) :
        self.SIZE = 8
        self.grille = [
                [1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,1],
                [1,0,0,0,1,0,0,1],
                [1,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,1],
                [1,0,0,1,0,0,0,1],
                [1,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1]
            ]
        self.x, self.y = 4,4 
        self.yau = 0

grille = Grid()

class Inputs:
    def keyboard(key, x, y):
        if key == b"z":
            grille.x += cos(grille.yau) * 0.2
            grille.y += sin(grille.yau) * 0.2
        if key == b"s":
            grille.x -= cos(grille.yau) * 0.2
            grille.y -= sin(grille.yau) * 0.2
        if key == b"q":
            grille.yau += 0.2
        if key == b"d":
            grille.yau -= 0.2

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
    glColor3f(1.0,0.0,3.0)
    Draw.plot_points(grille.x, grille.y)
    Draw.plot_trait(grille.x, grille.y)
    # Copy the off-screen buffer to the screen.
    glutSwapBuffers()

glutInit(sys.argv)

# Create a double-buffer RGBA window.   (Single-buffering is possible.
# So is creating an index-mode window.)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

glutInitWindowSize(500,500)
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

