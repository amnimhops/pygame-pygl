import Model
import os
from Model import Material, TextureMap


class TriMeshLoader():    
    def __init__(self):
        #trimesh
        self.trimesh = Model.TriMesh()
        #material
        
        self.trimesh.vc = []
        self.trimesh.nc = []
        self.trimesh.tc = []
        self.trimesh.f = []
        self.materialHash = {}
        self.currentMaterial = None
        
        self.path = "./"
        self.method_map = {"o":self.parse_unmapped, "s":self.parse_unmapped, "mtllib":self.parse_materiallib, "g":self.parse_group, "v":self.parse_vertexcoords, "#":self.parse_comment, "vt":self.parse_texcoords, "vn":self.parse_vertex_normals, "f":self.parse_faces, "usemtl":self.parse_usematerial}
    
    def load(self, filename):
        # Aqui buscaremos los .mtl definidos en el .obj
        self.path = os.path.dirname(filename)
        
        file = open(filename, "r")
        
        for line in file:
            if line[0] != "\n" and line[0] != "#":
                data_offset = line.index(' ')
                action = line[:data_offset]
                #print "'%s'" % action
                #print line[:-1]
                self.method_map[action](line[data_offset:].strip())
            
        file.close()
        
        return self.trimesh
    
    def parse_materiallib(self, line):
        mtlList = MaterialLoader().load(os.path.join(self.path, line))
        print os.path.join(self.path, line)
        c = 0
        for k, v in mtlList.items():
            self.materialHash[k] = v
            self.trimesh.addMaterial(v)
            
    def parse_unmapped(self, line):
        pass
    
    def parse_vertexcoords(self, line):
        data = line.split(" ")
        vertex = (float(data[0]), float(data[1]), float(data[2]))
        self.trimesh.vc.append(vertex)
        
        pass
    
    def parse_group(self, line):
        pass
    
    def parse_comment(self, line):
        pass
    
    def parse_texcoords(self, line):
        data = line.split(" ")
        txcoord = (float(data[0]), float(data[1]))
        self.trimesh.tc.append(txcoord)
    
    def parse_faces(self, line):
        data = line.split(" ")
        face = []
        for i in data:
            f = i.split("/")
            #f[0]=numvertice|f[1]=numtexcoord|f[2]=numvnormal
            
            vxid = (int(f[0]) - 1)
            #El indice de textura o de normal puede no venir especificado (el del vertice tiene que venir por cojones)
            txid = None
            if f[1] != '':
                txid = (int(f[1]) - 1)
            
            vnid = None
            if f[2] != '':
                vnid = (int(f[2]) - 1)
            
            face.append((vxid, txid, vnid))
            
        self.trimesh.f.append(face)
        self.trimesh.fcmtl[self.currentMaterial.name].append(face)
        
    def parse_vertex_normals(self, line):
        data = line.split(" ")
        normal = (float(data[0]), float(data[1]), float(data[2]))
        self.trimesh.nc.append(normal)
        
    
    def parse_usematerial(self, line):
        self.currentMaterial = self.materialHash[line]
        print "usando material %s" % line

class MaterialLoader:
    def __init__(self):
        self.mtlList = {}
        self.currentMaterial = None
        self.path = None
        self.method_map = {"map_Kd":self.parse_texturefile, "newmtl":self.parse_newmaterial, "Ka":self.parse_ambient, "Kd":self.parse_diffuse, "Ks":self.parse_specular, "Ns":self.parse_shininess, "d":self.parse_unmapped, "Tr":self.parse_unmapped, "Ni":self.parse_unmapped, "illum":self.parse_unmapped}
    
    def load(self, filename):
        self.path = os.path.dirname(filename)
        file = open(filename, "r")
        c = 0
        for line in file:
            print "Procesando linea %d" % c
            c += 1
            if line[0] != "\n" and line[0] != "#":
                data_offset = line.index(' ')
                action = line[:data_offset]
                #print "'%s'" % action
                #print line[:-1]
                self.method_map[action](line[data_offset:].strip())
            
        file.close()
        
        return self.mtlList
        
    def parse_newmaterial(self, line):
        print "Nuevo material %s" % line
        material = Material(line)
        self.mtlList[line] = material
        self.currentMaterial = material
    
    def parse_texturefile(self, line):
        self.currentMaterial.texture = TextureMap()
        self.currentMaterial.texture.loadImage(os.path.join(self.path, line))

    def parse_ambient(self, line):
        data = line.split(" ")
        self.currentMaterial.ambient = [float(data[0]), float(data[1]), float(data[2])]

    def parse_diffuse(self, line):
        data = line.split(" ")
        self.currentMaterial.diffuse = [float(data[0]), float(data[1]), float(data[2])]
    
    def parse_specular(self, line):
        data = line.split(" ")
        self.currentMaterial.specular = [float(data[0]), float(data[1]), float(data[2])]
    
    def parse_shininess(self, line):
        data = line.split(" ")
        
        self.currentMaterial.shininess = float(data[0])
    
    def parse_unmapped(self, line):
        print "Funcion no mapeada:%s" % line
    
    
if __name__ == "__main__":
    trimesh = TriMeshLoader().load("c:/model3d/megaman/megaman.obj")


    
    for v in trimesh.mtl:
        print trimesh.mtl[v].texture.texture
