import math as math
import os as os
import pymel.core as pm

####TESTING AREA######  
# import os as os
# import pymel.core as pm
# import sgLODInfo
# reload(sgLODInfo)

# resolution = 1.3 #game resolution to test against
# minAreaPix = 1.0 #smallest acceptable face area in pixels
# denseAreaPix = 9.0 #overly dense face area in pixels
# distance = 50

# lgs = pm.ls(sl=True, type = 'transform')
# if len(lgs)> 0:
    # lod = sgLODInfo.sgLODInfo(lgs[0],1.3)
    
    # print "\n________________________________________________________________"
    # print "\nlod is ",lod.name
    
    # print "________________________________________________________________\n"
    # print "TRIANGLES\n"
    # print "                         number of visible shapes: ", lod.countVisibleShapes()
    # print "                            Largest BBX face area: ", lod.getBBXArea()
    # print " smallest visible face size at ",distance, "m (1 pixel) is: ",round(lod.getMinAreaM(distance,minAreaPix),4), "m2"
    # print "                                  number of faces: ",lod.countFaces()
    # print "                        number of Zero Area Faces: ", lod.countZeroAreaFaces()
    # #pm.select(lod.listZeroAreaFaces())
    # print "                             bottom 50% face area: ", lod.getPercentileFaceArea(0,50)
    # print "                                top 50% face area: ", lod.getPercentileFaceArea(50,100)
    # print "                                      smallest 1%: ", lod.getPercentileFaceArea(0,1)
    # print "                                   mean face area: ", lod.getMeanFaceArea()
    # print "                                 median face area: ", lod.getMedianFaceArea()
    # print "                 at 50m number of faces under 1px: ", lod.countSmallFaces(distance,minAreaPix)  
    # print "                     at 50m 1% of faces under 1px: ", lod.getPercentSmallFaces(distance,minAreaPix)
    # #print lod.listSmallFaces(distance,minAreaPix)
    # print "                 at 50m number of faces under 9px: ", lod.countSmallFaces(distance,denseAreaPix)  
    # print "                     at 50m 1% of faces under 9px: ", lod.getPercentSmallFaces(distance,denseAreaPix)
    # #print lod.listSmallFaces(distance,denseAreaPix)
    # print "________________________________________________________________\n"
    # lod.printAreaCurve(10)
    # print "face area consistancy: ",  lod.getFaceAreaConsistancy(), "   (Values under 0.01 have some disproportionately small faces)"
    # print "________________________________________________________________\n"
    # print "MATERIALS & TEXTURES\n"
    # print "Number of Materials: ", lod.countATGMaterials()
    # print "Number of Textures:  ", lod.countTextures()
    # print "Total Texture Size:  ", round(lod.getTotalTexSize())," MB"
    # print "\nMATERIALS"
    # for ATGMat in lod.listATGMaterials():
        # print ATGMat
    # print "\nTEXTURES and SIZES (in game)"
    # for i, tex in enumerate(lod.listTexPaths()):
        # print round(lod.listTexSizes()[i],2)," MB \t",tex
    # print "________________________________________________________________\n"


    # countUniqueVtx,sharedVertEff,normEff,colEff,uvEff,UniqueValueEff = lod.getVtxDataEfficiency()

    # print "Number of unique vertices",countUniqueVtx
    # print "Shared Vertex efficiency:",sharedVertEff,"%"
    # print "\nNormal efficiency: ",normEff,"%"
    # print "Colour efficiency: ",colEff,"%"
    # print "UV map efficiency: ",uvEff,"%"
    # print "\nVtx data efficiency: ",UniqueValueEff,"%"


class sgLODInfo(object):
    """getting information about lods for optimisation"""
    
    def __init__(self, lod, resolution):
        """Create a LOD Object"""
        self.name = str(lod)
        self.lod = lod
        self.res = resolution
        self.dataPath = "/data/ps4_common/"

        #get a list of all the submeshes and faces in sub meshes except physics and navmesh
        self.shapes = []
        self.faces = []
        self.vtx = []
        self.areas = [] 
        self.tri = pm.polyEvaluate(self.lod, t=True )
        
        allShapes = pm.listRelatives(self.lod, allDescendents=True, shapes=True)
        for shape in allShapes:
            if "rigidbody" not in str(shape).lower() and "navmesh" not in str(shape).lower():
                self.shapes.append(shape)
                for f in shape.f:
                    self.faces.append(f)
                    self.areas.append(f.getArea()/10000.0) #convert area from cm to m
                for v in shape.vtx:
                    self.vtx.append(v)
        self.orderedAreas = sorted(self.areas)

        bbx = self.lod.getBoundingBox()
        self.bbx = max([bbx.depth()*bbx.height(),bbx.depth()*bbx.width(), bbx.height()*bbx.width()][:]) 

   
        


    ##GENERAL FUNCTIONS##    
        
    def listVisibleShapes(self):
        """returns a list of all (non physics) submeshes"""
        return self.shapes  
    
    def countVisibleShapes(self):
        """returns the number of (non physics) submeshes"""
        return len(self.shapes)        

    def isRemove(self):
        """returns True if LOD is a remove LOD"""
        if len(self.lod.getChildren()) == 0:
            return True  
        else:return False
        
    def niceName(self):
        return self.name.replace("_"," ")
        
    ##AREA FUNCTIONS##       
        
    def getBBXArea(self):
        """get the BBX area in m for the largest side"""
        bbx = self.lod.getBoundingBox()
        return max([bbx.depth()*bbx.height(),bbx.depth()*bbx.width(), bbx.height()*bbx.width()][:])   
    
    
    def getMinAreaM(self,distance,minArea):
        """ Calculate the height of a pixel in meters at given distance and square this for the equivalent area,     
        multiply by the given minimum area in pixels (probably 1)"""
        FOV = 100.0
        screensize = 1080.0 * self.res
        #pixelsize = (((diameter/distance)*180/pi) * screensize )/FOV#
        pixelsize = (((1.0/distance)*57.3)*screensize)/FOV
        return pow(1.0/pixelsize,2) *minArea
    
    def listVertices(self):
        """returns a list of all (non physics) submesh faces"""
        return self.vtx
    
    def countVertices(self):
        """Returns number of (non physics) submesh faces"""
        return len(self.vtx)
        
        
    def listFaces(self):
        """returns a list of all (non physics) submesh faces"""
        return self.faces
        
    def countFaces(self):
        """Returns number of (non physics) submesh faces"""
        return len(self.faces)
        
    
        
    def listFaceAreas(self):
        """returns list of face areas"""
        return self.areas
        
    def oListFaceAreas(self):
        """returns list of face areas in size order"""
        return self.orderedAreas
        
    def listZeroAreaFaces(self):
        """returns a list of zero area faces -slower"""
        zf = []
        minLength = 0.0001
        threshold = self.bbx * pow(minLength,2)
        for i,a in enumerate(self.areas):
            if a < threshold:
                zf.append(self.faces[i])
        return zf

    def countZeroAreaFaces(self):
        """returns the number of zero area faces"""
        minLength = 0.0001
        threshold = self.bbx * pow(minLength,2)
        if self.countFaces() > 0:
            n = 0
            while self.orderedAreas[n] < threshold and n < len(self.orderedAreas)- 1:
                #print "n = ",n, " area = ",self.orderedAreas[n]," length = ", len(self.orderedAreas)
                n+=1
            return n
        else: return 0
        
    def getMeanFaceArea(self):
        """calculate mean average area across all faces"""
        return sum(self.areas)/len(self.faces)
 
    def getMedianFaceArea(self):
        """return the value in the middle of the data"""
        return self.areas[len(self.faces)/2]
               
    def getPercentileFaceArea(self,start,end):
        """calculate average area across specified percentile
        start and end should be integers between 0 and 100"""
        #check for divide by zeros        
        if start != 0:start = (len(self.faces)*start)/100
        if end != 0:end = (len(self.faces)*end)/100
        #if start is same as end return just that faces value
        if start == end:return self.orderedAreas[start] 
        return sum(self.orderedAreas[start:end])/math.fabs(float(start-end))

    def getFaceAreaConsistancy(self):
        """ return a value for the difference between the median face size and the smallest 1%-
        1 is all faces equal area, values towards zero are more unequal"""        
        return self.getPercentileFaceArea(0,1)/self.getMedianFaceArea()


    def printAreaCurve(self,spacing):
        """print out each percentile in rows to show size distribution"""
        print "\nCurve showing average area for each ",spacing,"% of total faces\n"
        p = 0
        while p <= (100-spacing):
            p += spacing
            s = self.getPercentileFaceArea(p-spacing,p)
            
            print round(s/self.getMeanFaceArea(),2)*100, ":","*" * int((s*10)/self.getMeanFaceArea())
        print "\n"
        
    def countSmallFaces(self,distance,minArea):
        """return the number of faces with an area smaller than the given value in pixels"""
        area = self.getMinAreaM(distance,minArea)
        #print area
        n = 0
        while self.orderedAreas[n] < area and n < len(self.orderedAreas)- 1:
            #print "n = ",n, " area = ",self.orderedAreas[n]," length = ", len(self.orderedAreas)
            n+=1
        return n
        
    def getPercentSmallFaces(self,distance,minArea):
        """return the % of faces with an area smaller than the given value"""
        n = self.countSmallFaces(distance,minArea)
        return (n * 100)/len(self.orderedAreas)
        
        
    def listSmallFaces(self,distance,minArea):
        """return the faces with an area smaller than the given value in pixels- slower"""
        area = self.getMinAreaM(distance,minArea)
        #print area
        smallFaces = []
        for i,f in enumerate(self.faces):
            if self.areas[i] < area:
                smallFaces.append(f)
        return smallFaces
    
    ##MATERIAL FUNCTIONS##        
    
    def listShadingGroups(self):
        """returns a set of all Shading Groups containing LOD's (non physics) submeshes"""
        allSGs = set()
        for shape in self.shapes:
            shEng = shape.outputs(type = "shadingEngine")
            for sh in shEng:
                allSGs.add(sh)
            
        return allSGs    

    def listATGMaterials(self):
        """returns a list of all ATGMaterials attached to the LOD"""
        allSGs = self.listShadingGroups()
        atgMat = []
        for sg in allSGs:
            m = sg.inputs(type = "ATGMaterial")
            if len(m)>0:
                atgMat.append(m[0])            
        return atgMat    

    def countATGMaterials(self):
        """returns the number of unique ATG Materials attached to the LOD"""           
        return len(self.listATGMaterials())   

        
    def listTexNodes(self):
        """returns a list of all texture nodes attached to the LOD"""           
        allATGMat = self.listATGMaterials()
        textNodes = []        
        #get the unique connected file nodes
        for mat in allATGMat:
            for file in pm.listConnections(mat,type="file"):
                    textNodes.append(file)
        return textNodes
        
    def listTexPaths(self):
        """returns a list of all unique texture paths attached to the LOD"""           
        allATGMat = self.listATGMaterials()
        paths = set()        
        #get the unique connected file nodes
        for mat in allATGMat:
            for file in pm.listConnections(mat,type="file"):
                    path = pm.getAttr(file.fileTextureName)
                    paths.add(path)                
        return list(paths)

    def listTextures(self):
        """returns a list of unique textures attached to the LOD"""     
        textures = []
        for path in self.listTexPaths():
            textures.append(os.path.basename(path))
        return textures
        
    def countTextures(self):
        """returns the number of unique textures attached to the LOD""" 
        return len(self.listTextures())
        
    def listTexSizes(self):
        """returns a list of the size on disk in MB of all data side textures connected to the LOD's Materials"""           
        allTexturePaths = self.listTexPaths()
        texSizes = []
        for path in allTexturePaths:
            path = path.lower()
            dataTexPath = os.path.splitext(path.replace("/assets/", self.dataPath))[0]+".texture" 
            size = float(os.path.getsize(dataTexPath))/1048576
            texSizes.append(size)
        return texSizes
        
    def listTexSizesString(self):
        strings = []
        for t in self.listTexSizes():
            strings.append(str(round(t,1))+" MB")
            
        return strings
    

        
    def getTotalTexSize(self):
        """returns the combined size on disk in MB of all data side textures connected to the LOD's Materials"""   
        return sum(self.listTexSizes())

    def listTotalTexSizesString(self):
        return str(round(self.getTotalTexSize(),1))+" MB"
        
        
    ##VERTEX DATA EFFICIENCY##
    
    
    def getVtxDataEfficiency(self):
        """ Looks at how efficiently Vertex data is sent to the game 
        Returns a value between 0 and 1 for normals, colour, UVs, faces and overall
        Note 1. this is SLOW especially on big objects
        Note 2. If the Shared Vertex Efficiency is > 1, there are lambda faces"""
        countVtx = 0
        countNormValues = 0
        countColValues = 0
        countUvValues = 0 
        countUniqueVtx = 0        
        
        for shape in self.shapes:
            for v in shape.vtx:
                #get normal values and remove duplicates- return number
                setN=set()
                for n in v.getNormals():setN.add(str(n))
                #get colour values and remove duplicates- return number
                setC=set()
                for c in v.getColors():setC.add(str(c))                  
                uniqueNs = len(setN)
                uniqueCs = len(setC)
                uniqueUvs = v.numUVs()   
                #print "n:",uniqueNs, " uv:",uniqueUvs, " col:",uniqueCs
                countNormValues += uniqueNs
                countColValues += uniqueCs
                countUvValues += uniqueUvs
                countUniqueVtx += max(uniqueNs,uniqueUvs,uniqueCs)
                countVtx += 1                
                
        normEff = round(float(countVtx)/float(countNormValues),2)*100
        colEff = round(float(countVtx)/float(countColValues),2)*100
        uvEff = round(float(countVtx)/float(countUvValues),2)*100
        sharedVertEff = round(float(self.countFaces()+2)/float(countVtx),2)*100
        UniqueValueEff = round(float(countVtx)/float(countUniqueVtx),2)*100
        
        return [countUniqueVtx, sharedVertEff, normEff, colEff, uvEff, UniqueValueEff]
        
        
        