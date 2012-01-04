
class ObjLoader():
    
    def __init__(self, filename):
        
        self.vertex = []
        self.faces = [] #Cada cara tiene 3vx, 3tx y 3vn. En este orden
        self.normals = []
        self.textcoords = []
        
        method_map = {"s":self.parse_unmapped, "mtllib":self.parse_unmapped, "g":self.parse_group, "v":self.parse_vertexcoords, "#":self.parse_comment, "vt":self.parse_texcoords, "vn":self.parse_vertex_normals, "f":self.parse_faces, "usemtl":self.parse_usematerial}
        
        file = open(filename, "r")
        
        for line in file:
            if line[0] != "\n" and line[0] != "#":
                data_offset = line.index(' ')
                action = line[:data_offset]
                #print "'%s'" % action
                #print line[:-1]
                method_map[action](line[data_offset:].strip())
            
            
            
        file.close()
        
    def parse_unmapped(self, line):
        pass
    
    def parse_vertexcoords(self, line):
        data = line.split(" ")
        vertex = (float(data[0]), float(data[1]), float(data[2]))
        self.vertex.append(vertex)
        
        pass
    
    def parse_group(self, line):
        pass
    
    def parse_comment(self, line):
        pass
    
    def parse_texcoords(self, line):
        pass
    
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
            
        self.faces.append(face)
        
    def parse_vertex_normals(self, line):
        data = line.split(" ")
        normal = (float(data[0]), float(data[1]), float(data[2]))
        self.normals.append(normal)
        
    
    def parse_usematerial(self, line):
        pass
    
    
        
    ''' Iterador de los vertices de la cara index '''
    def getFaceVertex(self, index):
        for vertex_id in self.faces[index]:
            #print "Cara", index, "(%d,%d,%d)" % self.vertex[vertex_id]
            
            yield self.vertex[vertex_id]
