from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGL.arrays import vbo
import pygame

MTX_TRANSLATE = 0
MTX_SCALE = 1
MTX_ROTATE = 2

F_VERTEX = 0
F_TEXTCOORD = 1
F_NORMAL = 2
F_MATERIAL = 3

class Light:
    def __init__(self, light_id=GL_LIGHT0):
        self.id = light_id
        
        self.ambient = (0.0, 0.0, 0.0)
        self.diffuse = (0.0, 0.0, 0.0)
        self.specular = (0.0, 0.0, 0.0)
        self.position = (0, 0, 0)
        self.enabled = False
        
    def render(self):
        if self.enabled == True:
            glEnable(self.id)
            #Tipo de luz
            glLightfv(self.id, GL_AMBIENT, self.ambient)
            glLightfv(self.id, GL_DIFFUSE, self.diffuse)
            glLightfv(self.id, GL_SPECULAR, self.specular)
            glLightfv(self.id, GL_POSITION, self.position)

        else:
            glDisable(self.id)
            
    @staticmethod
    def Init():
        glEnable(GL_LIGHTING)

class Scene:
    def __init__(self):
        self.models = {}
        self.lights = {}

class TextureMap:
    def __init__(self):
        self.width = None
        self.height = None
        self.texture = None
        
    def loadImage(self, filename):
        textureSurface = pygame.image.load(filename)

        textureData = str(pygame.image.tostring(textureSurface, "RGBA", 1))
        
        self.width = textureSurface.get_width()
        self.height = textureSurface.get_height()
        
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)
    
class Material:
    def __init__(self, name=None):
        self.name = name
        self.ambient = [0.0, 0.0, 0.0, 1.0]
        self.diffuse = [0.0, 0.0, 0.0, 1.0]
        self.specular = [0.0, 0.0, 0.0, 1.0]
        self.shininess = 100
        self.texture = None
        
    def render(self):

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, self.ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, self.diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, self.specular)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, self.shininess)
        glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE);
        glColor3fv(self.diffuse)

        
        
class TriMesh:

    
    def __init__(self):
        self.vc = []        # Vertices
        self.nc = []        # Normales
        self.f = []         # Caras
        self.tc = []        # Coord. texturas
        self.mtl = {}       # Materiales
        self.fcmtl = {}     # Caras asignadas a materiales

        
    def addMaterial(self, material):
        self.mtl[material.name] = material
        self.fcmtl[material.name] = []
        
    def getFaceVertex(self, id):
        face = self.f[id]
        return (self.vc[face[0][F_VERTEX]], self.vc[face[1][F_VERTEX]], self.vc[face[2][F_VERTEX]])
    
    def getFaceNormal(self, id):
        face = self.f[id]
        return (self.vc[face[0][F_NORMAL]], self.vc[face[1][F_NORMAL]], self.vc[face[2][F_NORMAL]])
    
    def getFaceTexcoord(self, face):
        face = self.f[id]
        return (self.vc[face[0][F_TEXTCOORD]], self.vc[face[1][F_TEXTCOORD]], self.vc[face[2][F_TEXTCOORD]])

        
    def render(self):
        #glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        
        lastMaterial = None
        
        for mat_name in self.fcmtl:
            #if mat_name == "MAGGIE_blue_1":
                glColor3f(0, 0, 0)
                self.mtl[mat_name].render()
                glBindTexture(GL_TEXTURE_2D, self.mtl[mat_name].texture.texture)
                #print self.mtl[mat_name].texture
                for face in self.fcmtl[mat_name]:
                    v1 = self.vc[face[0][F_VERTEX]]
                    v2 = self.vc[face[1][F_VERTEX]]
                    v3 = self.vc[face[2][F_VERTEX]]
                    
                    n1 = self.nc[face[0][F_NORMAL]]
                    n2 = self.nc[face[1][F_NORMAL]]
                    n3 = self.nc[face[2][F_NORMAL]]
       
                    t1 = self.tc[face[0][F_TEXTCOORD]]
                    t2 = self.tc[face[1][F_TEXTCOORD]]
                    t3 = self.tc[face[2][F_TEXTCOORD]]
                    
                    glBegin(GL_TRIANGLES)
    
                    glNormal3f(n1[0], n1[1], n1[2])
                    glTexCoord2fv(t1)
                    glVertex3f(v1[0], v1[1], v1[2])
                    
                    glNormal3f(n2[0], n2[1], n2[2])
                    glTexCoord2fv(t2)
                    glVertex3f(v2[0], v2[1], v2[2])
                    
                    glNormal3f(n3[0], n3[1], n3[2])
                    glTexCoord2fv(t3)
                    glVertex3f(v3[0], v3[1], v3[2])
                    
                    glEnd()
        """
        for i in xrange(0, len(self.f)):
            face = self.f[i]
            
            v1 = self.vc[face[0][F_VERTEX]]
            v2 = self.vc[face[1][F_VERTEX]]
            v3 = self.vc[face[2][F_VERTEX]]
            
            n1 = self.nc[face[0][F_NORMAL]]
            n2 = self.nc[face[1][F_NORMAL]]
            n3 = self.nc[face[2][F_NORMAL]]
        
            if not lastMaterial:
                lastMaterial = face[0]    
            glBegin(GL_TRIANGLES)
            
            glNormal3f(n1[0], n1[1], n1[2])
            glVertex3f(v1[0], v1[1], v1[2])
            
            glNormal3f(n2[0], n2[1], n2[2])
            glVertex3f(v2[0], v2[1], v2[2])
            
            glNormal3f(n3[0], n3[1], n3[2])
            glVertex3f(v3[0], v3[1], v3[2])
            
            glEnd()"""
class Model:
    def __init__(self):
        self.mesh = None
        self.material = None
        self.matrix = [0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0]
    
    def getFaceNormal(self, v1, v2, v3):
        v1x = v1[0] - v2[0]
        v1y = v1[1] - v2[1]
        v1z = v1[2] - v2[2]
        v2x = v2[0] - v3[0]
        v2y = v2[1] - v3[1]
        v2z = v2[2] - v3[2]
        
        nx = (v1y * v2z) - (v1z * v2y)
        ny = (v1z * v2x) - (v1x * v2z)
        nz = (v1x * v2y) - (v1y * v2x)
        
        vLen = 1#sqrt((nx * nx) + (ny * ny) + (nz * nz));
    
        return (float(nx / vLen), float(ny / vLen), float(nz / vLen))

    def render(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        for idx_face in xrange(0, len(self.mesh.fc)):
        
            v1 = self.mesh.vx[self.mesh.fc[idx_face][0]]
            v2 = self.mesh.vx[self.mesh.fc.faces[idx_face][1]]
            v3 = self.mesh.vx[self.mesh.fc.faces[idx_face][2]]

            n = self.getFaceNormal(v1, v2, v3)
            
            glNormal3f(n[0], n[1], n[2])
            
            glBegin(GL_TRIANGLES)
            
            glVertex3f(v1[0], v1[1], v1[2])
            glVertex3f(v2[0], v2[1], v2[2])
            glVertex3f(v3[0], v3[1], v3[2])
    
            glEnd()

