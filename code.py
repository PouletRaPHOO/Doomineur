#-------------------- Imports -------------------------#
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import pi, cos, sin, tan, sqrt, inf, log2, floor, ceil
import random
#-------------------------------------------------------#

#--------------------- SETTINGS ------------------------#
SIZE = 2
#-------------------------------------------------------#

#--------------------- Constants -----------------------#
squaresize = int(4/SIZE)*16
ratio = int(64/squaresize)
GridSize = 8*ratio

windowSize = squaresize * GridSize
DR = 0.0174533

colors = [[0,0,1],[0,1,0],[1,0,0]]

cursorw = 3
cursorl = 15
resolution = 2
playerSpeed = 0.1

fps = 0.0
frame1 = 0.0
frame2 = 0.0

nb_bombes = int(((GridSize-1)**2)/5)

UNBREAKABLE = 1
BOMB=2
NONBOMB = 3

CONFIRMFLAG = 1
TEMPFLAG = 2
#-------------------------------------------------------#



#--------------------- Functions -----------------------#
def dist(dx,dy,ax,ay) :
    return sqrt((dx-ax)**2+(dy-ay)**2)

def getRay3D(ra,px,py) :
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
        if 0<=my<GridSize and 0<=mx<GridSize and grille.grille[my][mx].type >= 1 :
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
        if 0<=my<GridSize and 0<=mx<GridSize and grille.grille[my][mx].type >= 1 :
            dof = GridSize
            distV = dist(px,py,rx,ry)
        else :
            rx += x0
            ry += y0
            dof += 1

    if distH < distV :
        rx = Hx
        ry = Hy
        mx = int(rx) >> 6
        my = int(ry) >> 6

    return (distH,distV,min(distH,distV),rx,ry,mx,my)

def drawRays3D() :
    px= grille.x
    py = grille.y
    ra = (grille.yau -(-32*DR)) % (2*pi)

    for r in range(resolution*64):
        
        distH,distV,distMin,rx,ry,mx,my = getRay3D(ra,px,py)


        c = [1.0,0.0,0.0]

        if 0<=my<GridSize and 0<=mx<GridSize :
            c = colors[grille.grille[my][mx].type-1][0:]


        if distH < distV :
            c[0] = c[0] * 0.7
            c[1] = c[1] * 0.7
            c[2] = c[2] * 0.7
        else :
            c[0] = c[0] * 0.9
            c[1] = c[1] * 0.9
            c[2] = c[2] * 0.9


        glColor3f(c[0],c[1],c[2])

        glLineWidth(2)
        glBegin(GL_LINES)
        glVertex2f(px/ratio,py/ratio)
        glVertex2f(rx/ratio,ry/ratio)
        glEnd()


        ca = (grille.yau -ra)%(2*pi)
        distMin = distMin * cos(ca)*0.2
        lineh=((GridSize*windowSize)/distMin)
        glLineWidth((8/resolution)) 
        glBegin(GL_LINES)
        tempx =(r+1)*(8/resolution)+windowSize
        lineO = (windowSize/2)-lineh/2
        glVertex2f(tempx,lineO)
        glVertex2f(tempx, lineh+lineO)
        glEnd()

        ra= (ra-(DR/resolution))% (2*pi)

def drawMap2D(grille) :
    for y in range(len(grille)) :
        for x in range(len(grille[y])):
            if grille[y][x].type>=1 :
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

def drawCursor():
    glColor3f(0,1,0)
    glBegin(GL_QUADS)
    x0 = windowSize + windowSize/2
    y0 = windowSize/2
    glVertex2f(x0-cursorl/2,y0+cursorw/2)
    glVertex2f(x0+cursorl/2,y0+cursorw/2)
    glVertex2f(x0+cursorl/2,y0-cursorw/2)
    glVertex2f(x0-cursorl/2,y0-cursorw/2)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(x0-cursorw/2,y0+cursorl/2)
    glVertex2f(x0+cursorw/2,y0+cursorl/2)
    glVertex2f(x0+cursorw/2,y0-cursorl/2)
    glVertex2f(x0-cursorw/2,y0-cursorl/2)
    glEnd()
    
def destroy():
    px= grille.x
    py = grille.y
    ra = grille.yau
    distH,distV,distMin,rx,ry,mx,my = getRay3D(ra,px,py)
    if 0<=my<GridSize and 0<=mx<GridSize and not grille.grille[my][mx].type == UNBREAKABLE:
        grille.grille[my][mx].type = 0

def construct() :
    px= grille.x
    py = grille.y
    ra = grille.yau
    distH,distV,distMin,rx,ry,mx,my = getRay3D(ra,px,py)

    if distH==distMin :
        if 0<=ra<pi:
            my-=1
        else :
            my+= 1
    else :
        if pi/2<=ra<3*pi/2:
            mx+=1
        else :
            mx-= 1

    if 0<=my<GridSize and 0<=mx<GridSize and grille.grille[my][mx].type == 0:
        grille.grille[my][mx].type = NONBOMB

def iterate() :
    glViewport(0,0,windowSize*2,windowSize)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0,windowSize*2,0.0,windowSize,0.0,1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
#-------------------------------------------------------#



#--------------------- Classes -------------------------#
class Draw:
    def plot_points(x, y):
        glColor3f(0.0,1.0,0.0)
        glPointSize(5.0)
        glBegin(GL_POINTS)
        glVertex2f(x/ratio, y/ratio)
        glEnd()
        glFlush()

    def plot_trait(x, y, angle):
        glPointSize(5.0)
        glBegin(GL_LINES)        # GL_POINTS -> GL_LINES
        glVertex2f(x, y)
        glVertex2f(x+cos(angle)*40, y+sin(angle)*40)         # Added another Vertex specifying end coordinates of line
        glEnd()

class Case:
    def __init__(self,arg):
        self.type=arg
        self.number = 0
        self.flagged = 0
        self.color = (1.0, 1.0, 1.0)

class Grid:
    def __init__(self) :
        self.SIZE = GridSize
        self.grille = [[Case(0) for k in range(self.SIZE)] for j in range(self.SIZE)]
        self.x, self.y, self.yau = squaresize*4+squaresize/2,squaresize*4+squaresize/2, 0.0001

    def gen(self) :
        cos_bombes_grille = []
        for j in range(1, self.SIZE-1):
            for k in range(1, self.SIZE-1):
                cos_bombes_grille.append((j,k))
        random.shuffle(cos_bombes_grille)

        i= nb_bombes
        a = 0
        while i>0 and a < len(cos_bombes_grille):
            print("a")
            j,k = cos_bombes_grille[a]
            if abs(j-(self.y/(squaresize*ratio)))>1 or abs(k-(self.x/(squaresize*ratio)))>1 :
                self.grille[j][k].type = BOMB
                for v in range(j-1,j+2) :
                    for w in range(k-1,k+2) :
                        self.grille[v][w].number +=1
                i -= 1
            a+=1

        for y in range(self.SIZE) :
            for x in range(self.SIZE) :
                if x==0 or y==0 or x==self.SIZE-1 or y==self.SIZE-1:
                    self.grille[y][x].type = UNBREAKABLE
                elif (abs(y-(self.y/(squaresize*ratio)))>1 or abs(x-(self.x/(squaresize*ratio)))>1) and not self.grille[y][x].type == BOMB :
                    self.grille[y][x].type = NONBOMB
                # elif random.randint(0,100)>85:
                #     self.grille[y][x].type =random.randint(1,3)

    def __str__(self) :
        st = ""
        for k in self.grille[::-1] :
            for i in k:
                if i.type == BOMB:
                    st+="??? "
                else :
                    st+=f"{i.number} "
            st+="\n"
        return st

grille = Grid()
grille.gen()

class Inputs:
    z = 0
    s = 0
    q = 0
    d = 0
    def keyboard(key, x, y):
        if key == b"e":
            destroy()
        if key == b"a":
            #construct()
            print("En construction")
            print(grille)

    def keyboardDown(key, x, y):
        if key==b"z":
            Inputs.z = 1
        if key==b"s":
            Inputs.s = 1
        if key==b"q":
            Inputs.q = 1
        if key==b"d":
            Inputs.d = 1
        Inputs.keyboard(key, x , y)

    def keyboardUp(key, x, y):
        if key==b"z":
            Inputs.z = 0
        if key==b"s":
            Inputs.s = 0
        if key==b"q":
            Inputs.q = 0
        if key==b"d":
            Inputs.d = 0
    
    def actionsOnPress(fps):
        px = grille.x
        py = grille.y
        ra = grille.yau
        if Inputs.z:
            distH,distV,distMin,rx,ry,mx,my = getRay3D(ra,px,py)
            if distMin >= playerSpeed*fps:
                grille.x += cos(grille.yau) * playerSpeed * fps
                grille.y += sin(grille.yau) * playerSpeed * fps
        if Inputs.s:
            distH,distV,distMin,rx,ry,mx,my = getRay3D( (ra+pi)%(2*pi),px,py)
            if distMin >= playerSpeed*fps:
                grille.x -= cos(grille.yau) * playerSpeed * fps
                grille.y -= sin(grille.yau) * playerSpeed * fps
        if Inputs.q:
            grille.yau = (grille.yau+0.003*fps) %(2*pi)
        if Inputs.d:
            grille.yau = (grille.yau-0.003*fps) %(2*pi)

    def mouseDown(button, state, x,y):
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            destroy()
        if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            construct()
#-------------------------------------------------------#



#--------------------- Main Loop -----------------------#
def display():
    global frame1
    frame2 = glutGet(GLUT_ELAPSED_TIME)
    fps = frame2 - frame1
    frame1 = glutGet(GLUT_ELAPSED_TIME)
    Inputs.actionsOnPress(fps)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glutSetCursor(GLUT_CURSOR_NONE)

    iterate()

    
    drawMap2D(grille.grille)

    glColor3f(1.0,0.0,3.0)
    Draw.plot_points(grille.x, grille.y)

    drawRays3D()

    drawCursor()
    # print(grille)


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
glutKeyboardFunc(Inputs.keyboardDown)
glutKeyboardUpFunc(Inputs.keyboardUp)
glutMouseFunc(Inputs.mouseDown)

# Run the GLUT main loop until the user closes the window.
glutMainLoop()

print("a")
# vim:set foldmethod=indent:
#-------------------------------------------------------#