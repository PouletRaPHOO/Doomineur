import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import pi, cos, sin, tan, sqrt, inf, log2
import random

squaresize = 64
GridSize = 8
windowSize = squaresize * GridSize
DR = 0.0174533

def dist(dx,dy,ax,ay) :
    return sqrt((dx-ax)**2+(dy-ay)**2)

def drawRays3D() :
    px= grille.x*64
    py = grille.y*64
    dof=0
    ra = (grille.yau -(-30*DR)) % (2*pi)

    for r in range(120):
        
        distH = inf
        Hy = py
        Hx =px
        dof =0
        aTan =(-1)/tan(ra)
        if ra>pi :
            ry = ((int(py) >> 6) << 6) -0.00001
            rx = (py-ry) * aTan + px
            y0 = -64
            x0 = (-y0) * aTan
        elif ra<pi :
            ry = ((int(py) >> 6) << 6) + 64
            rx = (py-ry) * aTan + px
            y0 = 64
            x0 = (-y0) * aTan
        else :
            rx = px
            ry = py
            dof = GridSize
        while dof<GridSize:
            mx = int(rx) >> 6
            my = int(ry) >> 6
            if 0<=my<GridSize and 0<=mx<GridSize and grille.grille[my][mx] == 1 :
                dof = GridSize
                Hx= rx
                Hy = ry
                distH = dist(px,py,Hx,Hy)
            else :
                rx += x0
                ry += y0
                dof += 1

        



        distV= inf
        dof =0
        nTan =-tan(ra)
        if ra>pi/2 and ra<(3*pi)/2 :
            rx = ((int(px) >> 6) << 6) -0.00001
            ry = (px-rx) * nTan + py
            x0 = -64
            y0 = (-x0) * nTan
        elif ra<pi/2 or ra>(3*pi)/2 :
            rx = ((int(px) >> 6) << 6) + 64
            ry = (px-rx) * nTan + py
            x0 = 64
            y0 = (-x0) * nTan
        else :
            rx = px
            ry = py
            dof = GridSize
        while dof<GridSize:
            mx = int(rx) >> 6
            my = int(ry) >> 6
            if 0<=my<GridSize and 0<=mx<GridSize and grille.grille[my][mx] == 1 :
                dof = GridSize
                distV = dist(px,py,rx,ry)
            else :
                rx += x0
                ry += y0
                dof += 1

        glColor3f(0.9,0,0)

        if distH < distV :
            rx = Hx
            ry = Hy
            distV = distH
            glColor3f(0.7,0,0)


        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2f(px,py)
        glVertex2f(rx,ry)
        glEnd()


        ca = (grille.yau -ra)%(2*pi)
        distV = distV * cos(ca)*0.2
        lineh=((GridSize*windowSize)/distV)
        glLineWidth(4)
        glBegin(GL_LINES)
        tempx =(r+1)*4+windowSize
        lineO = (windowSize/2)-lineh/2
        glVertex2f(tempx,lineO)
        glVertex2f(tempx, lineh+lineO)
        glEnd()

        ra= (ra-(DR/2))% (2*pi)


def drawMap2D(grille) :
    for y in range(len(grille)) :
        for x in range(len(grille[y])):
            if grille[y][x]==1 :
                glColor3f(1.0,1.0,1.0)
            else :
                glColor3f(1.0,0.0,3.0)
            x0 = x*squaresize
            y0 = (y)*squaresize
            glBegin(GL_QUADS)
            glVertex2i(x0+1,y0+1)
            glVertex2i(x0+1,y0+squaresize-1)
            glVertex2i(x0+squaresize-1,y0+squaresize-1)
            glVertex2i(x0+squaresize-1,y0+1)
            glEnd()


def iterate() :
    glViewport(0,0,windowSize*2,windowSize)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0,windowSize*2,0.0,windowSize,0.0,1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


class Draw:
    def plot_points(x, y):
        glColor3f(0.0,1.0,0.0)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        glVertex2f(x*squaresize, y*squaresize)
        glEnd()
        glFlush()

    def plot_trait(x, y, angle):
        glPointSize(5.0)
        glBegin(GL_LINES)        # GL_POINTS -> GL_LINES
        glVertex2f(x, y)
        glVertex2f(x+cos(angle)*40, y+sin(angle)*40)         # Added another Vertex specifying end coordinates of line
        glEnd()


class Grid:
    def __init__(self) :
        self.SIZE = GridSize
        self.grille = [[0 for k in range(self.SIZE)] for j in range(self.SIZE)]
        self.x, self.y, self.yau = 4,4, 0.0001

    def gen(self) :
        for y in range(self.SIZE) :
            for x in range(self.SIZE) :
                if x==0 or y==0 or x==self.SIZE-1 or y==self.SIZE-1 or random.randint(0,100)>85:
                    self.grille[y][x] =1

    def __str__(self) :
        st = ""
        for k in self.grille :
            for i in k :
                if i==1 :
                    st+="■ "
                else :
                    st+="0 "
            st+="\n"
        return st


grille = Grid()
grille.gen()

class Inputs:
    def keyboard(key, x, y):
        if key == b"z":
            grille.x += cos(grille.yau) * 0.1
            grille.y += sin(grille.yau) * 0.1
        if key == b"s":
            grille.x -= cos(grille.yau) * 0.1
            grille.y -= sin(grille.yau) * 0.1
        if key == b"q":
            grille.yau = (grille.yau+0.1) %(2*pi)
        if key == b"d":
            grille.yau = (grille.yau-0.1) %(2*pi)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    iterate()

    
    drawMap2D(grille.grille)

    glColor3f(1.0,0.0,3.0)
    Draw.plot_points(grille.x, grille.y)

    drawRays3D()


    # Draw.plot_trait(grille.x*squaresize, grille.y*squaresize, grille.yau+(pi/6))
    # Draw.plot_trait(grille.x*squaresize, grille.y*squaresize, grille.yau-(pi/6))
    # Copy the off-screen buffer to the screen.
    glutSwapBuffers()

glutInit(sys.argv)

# Create a double-buffer RGBA window.   (Single-buffering is possible.
# So is creating an index-mode window.)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

glutInitWindowSize(windowSize*2,windowSize)
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

print("a")

