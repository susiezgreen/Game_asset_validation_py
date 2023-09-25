


class sgLODValues(object):

    def __init__(self):
        
        self.name = "Default values for LOD Info Report"       
        
        #Global Values
        self.DC = 5.0    # defaultClosest: default value for the closest we ever get to this object in m
        self.GAS = 1000  # gameArenaSize: default value for the game Arena Size in m (furthest we might see this object if it doesn't lod out)
        self.RES = 1.3   # resolution (set this at highest likely to be achieved)
        self.MAP = 1.0   # minAreaPix: minimum acceptable face size in pixels (probably one)
        self.DAP = 9.0   # denseAreaPix: faces smaller than this are considered overly dense
        
        #Prop
        #Min Values for warning
        self.TC = [100000,] #Triangle Count 
        self.ZAF = [0,]     #Zero Area Faces
        self.VSE = [50]     #percentage vertex sharing efficiency (in game)
        
        #Min Values for [v poor > n0 > poor > n1 > good]
        self.SPN = [2,1]     # percent of sub pixel faces at LOD start
        self.SPF = [5,2]     # percent of sub pixel faces at LOD end
        self.MC = [20,5]    #  Number of Materials
        self.TEC = [50,15]    #  Number of Textures
        
        
        #Min Values for [v poor > n0 >poor > n1 >acceptable > n2 >good > n3 > v good]
        self.TDN = [20,10,2,1]     # percent of overly dense pixel faces at LOD start
        self.TDF = [50,25,10,2]     # percent of overly dense pixel faces at LOD end
        self.TTS = [100,50,10,2]    # Total Texture Size in MB
        
        
        self.TOTS = [100,75,50,5] #tweak to give good values for the overall score. This is made up of adding all the previous scores.
        
        
        
        

        
        
        
        
        