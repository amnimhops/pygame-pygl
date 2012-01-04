import pygame

from sys import exit 
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.raw.GLUT import glutSolidIcosahedron, glutWireTeapot

import random
def initializeDisplay(w, h):
    pygame.display.set_mode((w, h), pygame.OPENGL | pygame.DOUBLEBUF)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluOrtho2D(0, w, 0, h);
    glMatrixMode(GL_MODELVIEW);
    
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    

#La textura ha de ser multiplo de 16!!!
def loadImage(image):
    textureSurface = pygame.image.load(image)
    
    textureData = str(pygame.image.tostring(textureSurface, "RGBA", 1))
    
    width = textureSurface.get_width()
    height = textureSurface.get_height()
    
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    
    return texture, width, height

def delTexture(texture):
    glDeleteTextures(texture)    

def createTexDL(texture, width, height):
    newList = glGenLists(1)
    glNewList(newList, GL_COMPILE);
    glBindTexture(GL_TEXTURE_2D, texture)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(-width / 2, -height / 2)    # Bottom Left Of The Texture and Quad
    #glColor4f(255.0,255.0,1.0,1.0)
    glTexCoord2f(0, 1); glVertex2f(-width / 2, height / 2)    # Top Left Of The Texture and Quad
    glTexCoord2f(1, 1); glVertex2f(width / 2, height / 2)    # Top Right Of The Texture and Quad
    glTexCoord2f(1, 0); glVertex2f(width / 2, -height / 2)    # Bottom Right Of The Texture and Quad
    glEnd()
    glEndList()
    return newList
def delDL(list):
    glDeleteLists(list, 1)
    
if __name__ == "main":
    pygame.init()
    initializeDisplay(800, 600)
    glColor4f(255.0, 1.0, 1.0, 1.0)
    
    textura1, w1, h1 = loadImage("mario-small.png")
    cosa1 = createTexDL(textura1, w1, h1)
    
    textura2, w2, h2 = loadImage("pacman.png")
    cosa2 = createTexDL(textura2, w2, h2)
    
    angulo = 0.0
    
    clock = pygame.time.Clock()
    
    """glNewList(3,GL_COMPILE)
    
    glutSolidIcosahedron()
    glEndList"""
    
    while True:
        clock.tick()
        #glClear(GL_COLOR_BUFFER_BIT)
        #glRotate(angulo,0,0,-1)
        #glTranslate(320,240,0)
        #glTranslate(0,0,0)
        x = random.random()*800
        y = random.random()*600
        
        for c in xrange(1, 1000):
            glLoadIdentity()
            glTranslate(c * 10, y + c, 0) #donde lo dibujamos
            glCallList(cosa1)
            
        
        #glCallList(3)
        #angulo+=0.5
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit()
        #print pygame.time.Clock().get_fps()
        print clock.get_fps()
        
        pygame.display.flip()
        
        
