'''
Created on 07/02/2011

@author: amninhops
'''
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import pygame

def initializeDisplay(w, h):
    pygame.display.set_mode((w, h), pygame.OPENGL | pygame.DOUBLEBUF)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, w, 0, h);
    glMatrixMode(GL_MODELVIEW);
    
    #glEnable(GL_TEXTURE_2D) # ATENCION: NO se puede texturizar y colorear a la vez
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def initialize3D(w,h):
    pygame.display.set_mode((w,h), pygame.OPENGL | pygame.DOUBLEBUF)
    # set viewing projection
    light_diffuse = [1.0, 1.0, 1.0, 1.0]
    light_position = [1.0, 1.0, 1.0, 0.0]

    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClearDepth(1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, 1.0, 1.0, 30.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, 10.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)


class Textura:
    idx_textura = 1
    def __init__(self):
        self.data = None
        self.w = None
        self.h = None
        self.texid = None
        
    def from_image(self, imagen):
        image = pygame.image.load(imagen)
        self.w = image.get_width()
        self.h = image.get_height()
        
        self.texid = Textura.idx_textura
        self.texture = glGenTextures(1) # Devuelve 1 nombre de textura???
        
        print self.texture
        Textura.idx_textura += 1
        
        glBindTexture(GL_TEXTURE_2D, self.texture)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.w, self.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, str(pygame.image.tostring(image, "RGBA", 1)))
        
    def from_surface(self, surface):
        self.w = surface.get_width()
        self.h = surface.get_height()
        
        self.texid = Textura.idx_textura
        self.texture = glGenTextures(1) # Devuelve 1 nombre de textura???
        
        print self.texture
        Textura.idx_textura += 1
        
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.w, self.h, 0, GL_RGBA, GL_UNSIGNED_BYTE, str(pygame.image.tostring(surface, "RGBA", 1)))
        
       
class Plano:
    idx_plano = 1
    def __init__(self):
        self.glList = None
        self.planoid = None
        pass
    
    def create(self, textura):
        self.glList = glGenLists(Plano.idx_plano)
        self.planoid = Plano.idx_plano
        
        Plano.idx_plano += 1
        
        glNewList(self.glList, GL_COMPILE);
        glBindTexture(GL_TEXTURE_2D, textura.texture)
        glBegin(GL_QUADS)
        """glTexCoord2f(0, 0); glVertex2f(-textura.w / 2, -textura.h / 2)    # Bottom Left Of The Texture and Quad
        #glColor4f(255.0,255.0,1.0,1.0)
        glTexCoord2f(0, 1); glVertex2f(-textura.w / 2, textura.h / 2)    # Top Left Of The Texture and Quad
        glTexCoord2f(1, 1); glVertex2f(textura.w / 2, textura.h / 2)    # Top Right Of The Texture and Quad
        glTexCoord2f(1, 0); glVertex2f(textura.w / 2, -textura.h / 2)    # Bottom Right Of The Texture and Quad"""
        
        glEnd()
        glEndList()
    
    def flydraw(self, textura, c):
        
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textura.texture)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f((-textura.w / 2), -textura.h / 2)    # Bottom Left Of The Texture and Quad
        glTexCoord2f(0, 2); glVertex2f((-textura.w / 2), textura.h / 2)    # Top Left Of The Texture and Quad
        glTexCoord2f(2, 2); glVertex2f(textura.w / 2, textura.h / 2)    # Top Right Of The Texture and Quad
        glTexCoord2f(2, 0); glVertex2f(textura.w / 2, -textura.h / 2)    # Bottom Right Of The Texture and Quad
        glEnd()
        
        glDisable(GL_TEXTURE_2D)
    
    def draw(self):
        glCallList(self.planoid) 
        
pygame.init()
#initializeDisplay(800, 600)
initialize3D(800, 600)


#glColor4f(255.0, 1.0, 1.0, 1.0)

"""
anim = pygame.image.load("anim.png")
tx = []
for c in range(0, 3):
    t = Textura()
    t.from_surface(anim.subsurface(c * 256, 0, 256, 256))
    tx.append(t)
    

pl = []
for idtx in range(len(tx)):
    p = Plano()
    p.create(tx[idtx])
    pl.append(p)


clock = pygame.time.Clock()


"""
c = 0
while True:
    

    c += 1
    if c == 500:
        c = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            exit()

    
    #Plano.flydraw(pl[0], tx[0], c)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    color = [1.0,1.,0.,1.]
    glMaterialfv(GL_FRONT,GL_DIFFUSE,color)
    glutSolidSphere(2,20,20)
    glPopMatrix()
    
    pygame.display.flip()
    
