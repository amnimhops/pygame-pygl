from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import *
from OpenGL import arrays

import time
from Model import Light
from Loader import TriMeshLoader



global lightpos
global angle
global ancho
global alto
global profundidad
global fov
global myLight
global ticks
global trimesh

OpenGL.FULL_LOGGING = True

def strin3d(font, string):
    for chr in string:
        
        glutStrokeCharacter(font, ord(chr))
        
def init3D():
    #Si GL_DEPTH_TEST no esta activado, se renderizan todos los poligonos (sin oclusion de caras)
    glEnable(GL_DEPTH_TEST)
    #Esta llamada hace que el poligono se renderize como una malla
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glEnable (GL_BLEND);               
    glBlendFunc (GL_SRC_ALPHA , GL_ONE_MINUS_SRC_ALPHA);
    glEnable(GL_TEXTURE_2D)

    glShadeModel(GL_SMOOTH)
    #Poligonos bonitos y suaves
    glEnable(GL_POLYGON_SMOOTH)
    #A saber, pero habilita los materiales
    glEnable(GL_COLOR_MATERIAL)
    
    glEnable(GL_CULL_FACE);
    glDepthMask(GL_TRUE);

    #Convierte las normales de las caras/vertices a vectores unitarios
    glEnable(GL_NORMALIZE)
    camera()

def camera():
    #print ancho, alto
    glViewport(0, 0, ancho, alto)
    
    #ortho()
    perspective()
    #lookAt()

def ortho():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glTranslatef(0, 0, 0)
    glOrtho(-10, 10, -10, 10, -10, 10)
    
def perspective():
    global fov, ancho, alto
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, ancho * 1.0 / alto, ancho * 1.0 / alto, 100);
    lookAt(0, 10, -45, 0, 0, 0)
    
def lookAt(ox=0, oy=0, oz= -10, x=0, y=0, z=0):
    gluLookAt(ox, oy, oz, x, y, z, 0.0, 1.0, 0.0)

def lights():
    global lightpos
    global angle
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(lightpos[0], lightpos[1], lightpos[2])
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.5 , 0.5 , 0.5 , 1.0));    
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0 , 1.0 , 1.0 , 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0 , 1.0 , 1.0 , 1.0))
    #Posicion de la luz
    glLightfv (GL_LIGHT0, GL_POSITION, lightpos)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, (0, 0, 0))
    glLightfv(GL_LIGHT0, GL_CONSTANT_ATTENUATION, (0.1, 0, 0))
    glutSolidCube(1)
 
def axis():
    glLoadIdentity()
    glTranslatef(0, 0, 0)
    # eje x
    
    glBegin(GL_LINES)
    glColor4f(1, 0, 0, 1)
    glVertex3f(-10, 0, 0)
    glVertex3f(10, 0, 0)
    glEnd()
    # eje y
    glBegin(GL_LINES)
    glColor4f(0, 1, 0, 1)
    glVertex3f(0, -10, 0)
    glVertex3f(0, 10, 0)
    glEnd()
    # eje z
    glBegin(GL_LINES)
    glColor4f(0, 0, 1, 1)
    glVertex3f(0, 0, -10)
    glVertex3f(0, 0, 10)
    glEnd()
    
def draw():
    global myLight, ticks
    
    
    
    #print (ticks - time.clock())*1000
    
    if 1000 * (time.clock() - ticks) > 20:
        ticks = time.clock()
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        lights()
        
        #axis()
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        transform()
        
        modeltrimesh()
        
        
        glutSwapBuffers()

def transform():
    global angle
    glRotatef(angle, 0, 1, 0)

def modeltrimesh():
    global trimesh
    
    glLoadIdentity()
    
    #glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
    #glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, (0.1, 0.1, 0.1, 1.0))
    #glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1, 1, 1, 1.0))
    #glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 120);
    #glScalef(0.1, 0.1, 0.1)
    glScalef(10, 10, 10)
    #glColor(0.2, 0.2, 0.2, 1)
    transform()
    
    trimesh.render()
    
    
def cube():
    # Esto dibuja la malla en lugar del solido
    #glPolygonMode(GL_FRONT, GL_LINE);
    #glPolygonMode(GL_BACK, GL_LINE);
    glLoadIdentity()
    transform()
    
    #glColorMaterial (GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, (0.0, 0.0, 1.0, 1.0))
    #glMaterial(GL_FRONT, GL_DIFFUSE, (0.8, 0.8, 0.8, 1.0))
    #glMaterial(GL_FRONT, GL_SPECULAR, (0.5  , 0.5, 0.5, 1.0))
    #glMaterial(GL_FRONT, GL_EMISSION, (0.1, 0.1, 0.1))
    #glColor4f(0.5, 0.5, 0.5, 1)
    glutSolidCube(2)
    
    
def plane():
    """glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #glNormal(0, 1, 0)
    glClearColor(0, 0, 0, 1)
    glEnable(GL_COLOR_MATERIAL)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.5, 0.5, 0.5, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [0.5, 0.5, 0.5, 1])
        
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1, 1, 1, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 20);
    glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE);
    glColor3fv([0.5, 0.5, 0.5])
    glNormal(0, 1, 0)
    glBegin(GL_QUADS)
    glNormal(0, 1, 0)
    glVertex(-20, -40, -20)
    glNormal(0, 1, 0)
    glVertex(-20, -40, 20)
    glNormal(0, 1, 0)
    glVertex(20, -40, 20)
    glNormal(0, 1, 0)
    glVertex(20, -40, -20)
    glEnd()"""
    
def reshape(width, height):
    global ancho, alto
    ancho = profundidad = width;
    alto = height;
    
    camera()
    
    glutPostRedisplay()
    
    #print "Reshape to : aspect %f %dx%d" % (1.0 * width / height, width, height)
    
def keyboard(key, x, y):
    global angle, fov, lightpos
    #print key, x, y
    if key == 'r':
        angle = angle + 1
        if angle >= 360:
            angle = 0
            
        #print lightpos
    
    
    if key == 'f':
        fov = fov + 1
        camera()
        
    
    if key == 'F':
        fov = fov - 1
        camera()
        
    
    
    if key == 'w': #z+
        lightpos[2] = lightpos[2] + 1
    
    if key == 's': #z-
        lightpos[2] = lightpos[2] - 1
    
    if key == 'a': #x-
        lightpos[0] = lightpos[0] - 1
        
    if key == 'd': #x+
        lightpos[0] = lightpos[0] + 1
    
    
    glutPostRedisplay()
        
        
def mouse(button, state, x, y):
    #print button, state, x, y
    pass
    
def idle():
    global lightpos
    
    pass

ticks = 0

lightpos = [0, 0, -10]    
ancho = profundidad = 400
alto = 400
fov = 60
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGB | GLUT_DEPTH | GLUT_DOUBLE) #GLUT_DOUBLE activa el doble buffer, pero necesita llamar a glutSwapBuffers en lugar de a glFlush
glutInitWindowSize(ancho, alto)
glutCreateWindow("OpenGL PDF")

init3D()

glutKeyboardFunc(keyboard)
glutDisplayFunc(draw)
glutReshapeFunc(reshape)
glutMouseFunc(mouse)
glutIdleFunc(idle)
print glGetString(GL_VERSION)

angle = 0

trimesh = TriMeshLoader().load("../../data/megaman.obj")

glutMainLoop()
