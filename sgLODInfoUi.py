import pymel.core as pm
import sgLODInfo
import sgLODValues
reload(sgLODInfo)
reload(sgLODValues)

v = sgLODValues.sgLODValues()

def sgReturnFirstSelectedLODGroup(node):


    while True:
        if node.nodeType()== 'lodGroup':return node
        if node.getParent()== None:return None
        node = node.getParent()


def sgReturnLODsInLODGroup(LODGroup):
    lods = LODGroup.getChildren()   
    print "\n\nLods are:  ",lods,"\n\n"
    return lods

def make_float(s):
    try:
        return float(s)
    except ValueError:
        return False

def sgLODInfoUiUpdate(defaultClosestFF,gameArenaSizeFF, resolutionFF,minAreaPixFF,denseAreaPixFF,obj,*args):
    defaultClosest = defaultClosestFF.getValue()
    gameArenaSize = gameArenaSizeFF.getValue()
    resolution = resolutionFF.getValue()
    minAreaPix = minAreaPixFF.getValue()
    denseAreaPix = denseAreaPixFF.getValue()
    sgLODInfoUi(defaultClosest,gameArenaSize,resolution,minAreaPix,denseAreaPix,obj)
    
def sgButtonColourWarning(value,compare):
    red = (1.0,0.0,0.0)
    orange = (1.0,0.55,0.0)
    yellow = (1.0,1.0,0.0)
    greenYellow = (0.6,1.0,0.17)
    lightGreen = (0.45,0.70,0.45)
    green = (0.3,0.50,0.3)
    grey = (0.5,0.5,0.5)
    

    print "compare 0 = ",compare[0]
    print "len compare = ",len(compare)
    print "compare = ",compare
    print "value = ", value
    
    value = make_float(value)
    if value == False:
        score = [3,grey,"UNKNOWN"]
    
    else:
        score = [0,green,"VERY GOOD"]
        if len(compare) == 1:
            if float(value) > float(compare[0]):score = [3,orange,"ACCEPTABLE"]

        
        elif len(compare) == 2:
            if float(value) > float(compare[1]):score = [3,orange,"ACCEPTABLE"]
            if float(value) > float(compare[0]):score = [5,red,"VERY BAD"]
                
        elif len(compare) == 4:
            if float(value) > float(compare[3]):score = [1,greenYellow,"OK"]
            if float(value) > float(compare[2]):score = [2,yellow,"ACCEPTABLE"]
            if float(value) > float(compare[1]):score = [3,orange,"POOR"]
            if float(value) > float(compare[0]):score = [5,red,"VERY BAD"]
        
    return score
        
def sgButtonSelection(target):
    pm.select(target)
    
def sgButtonSelectionList2(target, list1,list2):
    #lists must be equal
    pm.select(target)
    if len(list1)==len(list2):
        print "\n"
        for i,x in enumerate(list1):
            print list1[i]," --- ",list2[i]

def sgGetVertexData(lods,vertexButtonLayout,vCountLayout,vEfficLayout):

    #vertexButtonLayout.reset()
    pm.deleteUI(vCountLayout,vEfficLayout,layout=True)
    
    countUniqueVtx = []
    UniqueValueEff = []
    for lod in lods:
        countUniqueVtx.append(lod.getVtxDataEfficiency()[0])
        UniqueValueEff.append(lod.getVtxDataEfficiency()[5])
     
    print "\n\nUniqueValueEff: ",UniqueValueEff
    
    with vertexButtonLayout:
                            
        with pm.verticalLayout():
            v3 = pm.text(label='Vertices\nin\nGame')
            for i, lod in enumerate(lods):            
                pm.button(label= countUniqueVtx[i], enable = True)
        with pm.verticalLayout():
            v4 = pm.text(label='Vertex\nSharing\nEfficiency')
            for i, lod in enumerate(lods):
                pm.button(label= str(int(UniqueValueEff[i]))+" %", backgroundColor = sgButtonColourWarning((100 - UniqueValueEff[i]),v.VSE)[1], enable = True)
    score = sgButtonColourWarning((100 - UniqueValueEff[i]),v.VSE)[0]
    return score
        
def sgLODInfoUi(defaultClosest= v.DC,gameArenaSize =  v.GAS,resolution =  v.RES,minAreaPix =  v.MAP,denseAreaPix=  v.DAP, obj=None, *args):

    # print defaultClosest
    print "gameArenaSize ",gameArenaSize
    # print resolution
    # print minAreaPix
    # print denseAreaPix
    
    totalScore  = 0


    if pm.window("LODInfoWindow", exists = True):
        pm.deleteUI("LODInfoWindow")
     
    # define some colours
    lightGrey = (0.5,0.5,0.52)
    grey = (0.38,0.38,0.4)
    darkGreyBg = (0.25,0.25,0.28)
    vDarkGrey = (0.15,0.15,0.18)
    darkGreyField = (0.23,0.23,0.25)
    darkGreySection = (0.29,0.29,0.32)
    red = (1.0,0.0,0.0)
    orange = (1.0,0.55,0.0)
    yellow = (1.0,1.0,0.0)
    greenYellow = (0.6,1.0,0.17)
    lightGreen = (0.45,0.70,0.45)
    green = (0.3,0.50,0.3)
    darkGreen = (0.15,0.40,0.15)
    darkGreenGrey = (0.18, 0.2,0.2)
    lightGreenGrey = (0.36, 0.4,0.4)
    
    lightBlueGrey = (0.5,0.65,0.9)
    blueGrey = (0.4,0.45,0.7)
    darkBlueGrey = (0.2, 0.2,0.5)
    lightBlue = (0.4,0.55,1.0)
    blue = (0.2,0.45,1.0)
    darkBlue = (0.1,0.3,0.8)
    
    #attach colours to UI
    bgColours = vDarkGrey
    boxColours = darkGreySection
    updateButtonColours = grey
    ffColours = lightGrey
    metricsColours = grey
    metricsSectionsColours = darkGreySection
    metricsLOD0sButtonColours = lightGrey
    metricsButtonColours = grey
    
    
    #display value rounding
    overViewRounding = 1
    
    #define some sizes
    borderSize = 10
    lodRowSize = 20
    buttonSpacing = 5
    lodSpacing = 2
    textHeight = 17
    metricsMenuHeight = 36
    metricsButtonHeight = 42
    metricsButtonWidth = 50

    templateA = pm.uiTemplate('ExampleTemplate', force=True)
    templateA.define(pm.button, align='left')
    templateA.define(pm.floatField, precision = 1,backgroundColor= darkGreyField)
    templateA.define(pm.rowLayout)
    templateA.define(pm.columnLayout,backgroundColor=darkGreyBg)

    
    
    selected = pm.ls(sl=True, type = 'transform')

    #####################################################
    #CREATE A SMALL WINDOW WARNING IF THERE IS NOTHING VALID SELECTED#        

    if len(selected)== 0 and obj == None:
        with pm.window("LODInfoWindow",menuBar=False,menuBarVisible=False, w = 200, h = 150, resizeToFitChildren =True , backgroundColor=darkGreyBg) as win:
            with pm.verticalLayout(): 
                pm.text(label="No valid Model or LOD group selected")
                pm.button(label='Try Again', command = pm.Callback(sgLODInfoUi),backgroundColor= darkGreyField )
                win.setHeight(150)
                win.setWidth(200)
    
    ##################################################### 
    #SET UP LOD GROUPS#
    
    else:
        if obj == None:
            obj = sgReturnFirstSelectedLODGroup(selected[0])

        lods = []
        lodDist = [defaultClosest]
        
        lodGrp = True
        
        if obj == None:
            obj = selected[0]
            lodGrp = False            
        else:
            lods = sgReturnLODsInLODGroup(obj)
            for threshold in obj.threshold.get():
                lodDist.append(threshold/100)
        
        if lodGrp:
            print "lod group is :", str(obj)            
            for i  in range(len(lods)):       
                lods[i] = sgLODInfo.sgLODInfo(lods[i],resolution)
                
            
            if lods[-1].isRemove():lods.pop(-1)
            else: lodDist.append(gameArenaSize)
            
            print "\n"
            for lod in lods:
                print lod
            for dist in lodDist:
                print dist
            print "\n"
            if len(lods) != len(lodDist)-1:
                pm.error("Number of LODs do not match LOD Thresholds")
            for i,lod in enumerate(lods):
                print lod.name," is visible from ", lodDist[i], " to ",lodDist[i+1]
      
            
        else:  print "Object (not a lod group) is :", str(obj) 
        pm.select(obj)
        
                   
            
        scoreText = "GOOD"
        scoreColour = green    
        
        
    ####### TEMPLATES #######################################
        overviewTemplate = pm.uiTemplate('overviewTemplate', force=True)
        overviewTemplate.define(pm.floatField, backgroundColor = ffColours)    
        metricsTemplate = pm.uiTemplate('MetricsTemplate', force=True)
        metricsTemplate.define(pm.button, backgroundColor = metricsButtonColours, w=metricsButtonWidth)    
    #########################################################
    #CREATE WINDOW
        with pm.window("LODInfoWindow",menuBar=True,menuBarVisible=True, resizeToFitChildren =True , backgroundColor=darkGreyBg) as win:
            with pm.formLayout(backgroundColor=bgColours) as frame: #border
                ######################################################################################################################## OVERVIEW BOX
                with pm.formLayout(backgroundColor=boxColours) as overview: 
                    with overviewTemplate:
                        ov1 = pm.text(label=str(obj).replace("_"," "))
                        ov2 = pm.text(label = scoreText, backgroundColor = scoreColour,h=100, font = "boldLabelFont")
                        with pm.horizontalLayout() as ovFFLayout:
                                with pm.verticalLayout():
                                    pm.text(label='Set Closest Distance in Game in m', align = "right")
                                    pm.text(label='Set Game Arena size in m', align = "right")
                                    pm.text(label='Set Resolution', align = "right")
                                    pm.text(label='Set Minimum Face Area in Pixels', align = "right")
                                    pm.text(label='Set Dense Face Area in Pixels', align = "right")
                                with pm.verticalLayout():                                       
                                    defaultClosestFF =  pm.floatField(value = round(defaultClosest,overViewRounding))
                                    gameArenaSizeFF =   pm.floatField(value = round(gameArenaSize,overViewRounding))
                                    ResolutionFF =      pm.floatField(value = round(resolution,overViewRounding))
                                    minAreaPixFF =      pm.floatField(value = round(minAreaPix,overViewRounding))
                                    denseAreaPixFF =    pm.floatField(value = round(denseAreaPix,overViewRounding))
                                                
                        ovFFLayout.redistribute(2,1)
                        ovUpdateBut = pm.button(label='Update After Model Changes',backgroundColor=updateButtonColours) 

                
                ########################################################################################################################## SUGGESTIONS BOX
                with pm.formLayout(backgroundColor=boxColours) as suggestions: 
                    pm.text(label="suggestions")
                    
                                    
                ########################################################################################################################## METRICS BOX
                with pm.formLayout(backgroundColor=boxColours) as metrics:
                    with metricsTemplate:
                        ##
                        with pm.formLayout(backgroundColor=metricsSectionsColours) as LODColumn:
                            l1 = pm.text(label="LODs\n",font = "obliqueLabelFont",h=metricsMenuHeight)
                            
                            with pm.verticalLayout(backgroundColor=metricsSectionsColours) as LODButtonLayout:########################### LODS
                                l2 = pm.text(label=' \n \n ')
                                for i, lod in enumerate(lods):
                                    pm.button(label='LOD'+str(i))
                        ##
                        with pm.formLayout(backgroundColor=metricsSectionsColours) as distColumn:################################### DISTANCES
                            d1 = pm.text(label="Distance\n",font = "obliqueLabelFont",h=metricsMenuHeight)
                            
                            with pm.horizontalLayout(backgroundColor=metricsSectionsColours) as distButtonLayout:
                                
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours) as distNearLayout:
                                    d2 = pm.text(label=' \n \nNear')
                                    for i, lod in enumerate(lods):
                                        pm.button(label= str(lodDist[i]))
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours) as distFarLayout:
                                    d3 = pm.text(label=' \n \nFar')
                                    for i, lod in enumerate(lods):
                                        pm.button(label=str(lodDist[i+1]))
                                        
                        ##
                        with pm.formLayout(backgroundColor=metricsSectionsColours) as faceColumn:#################################### FACE AREAS
                            f1 = pm.text(label="Faces\n",font = "obliqueLabelFont",h=metricsMenuHeight)
                            
                            with pm.horizontalLayout(backgroundColor=metricsSectionsColours) as FaceButtonLayout:
                                
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours):
                                    f2 = pm.text(label=' \nTriangle\nCount')
                                    for lod in lods:
                                        score = sgButtonColourWarning(lod.tri,v.TC)
                                        pm.button(label= str(lod.tri),backgroundColor = score[1])
                                        totalScore += score[0]
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours):
                                    f3 = pm.text(label='Zero\nArea\nFaces')
                                    for i, lod in enumerate(lods):
                                        score = sgButtonColourWarning(lod.countZeroAreaFaces(),v.ZAF)
                                        pm.button(label= lod.countZeroAreaFaces(), backgroundColor = score[1], command = pm.Callback( sgButtonSelection, lod.listZeroAreaFaces() ) )
                                        totalScore += score[0]
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours) as FaceSSN:
                                    f4 = pm.text(label='Sub\nPixel\nNear')
                                    for i, lod in enumerate(lods):
                                        score = sgButtonColourWarning(lod.getPercentSmallFaces(lodDist[i],minAreaPix),v.SPN)
                                        pm.button(label= str(lod.getPercentSmallFaces(lodDist[i],minAreaPix)) + " %", backgroundColor = score[1], command = pm.Callback( sgButtonSelection, lod.listSmallFaces(lodDist[i],minAreaPix) ))
                                        totalScore += score[0]
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours):
                                    f5 = pm.text(label='Sub\nPixel\nFar')
                                    for i, lod in enumerate(lods):
                                        score = sgButtonColourWarning(str(lod.getPercentSmallFaces(lodDist[i+1],minAreaPix)),v.SPF)
                                        pm.button(label= str(lod.getPercentSmallFaces(lodDist[i+1],minAreaPix)) + " %", backgroundColor = score[1],command = pm.Callback( sgButtonSelection, lod.listSmallFaces(lodDist[i+1],minAreaPix) ))
                                        totalScore += score[0]
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours):
                                    f6 = pm.text(label='Too\nDense\nNear')
                                    for i, lod in enumerate(lods):
                                        score = sgButtonColourWarning(lod.getPercentSmallFaces(lodDist[i],denseAreaPix),v.TDN)
                                        pm.button(label= str(lod.getPercentSmallFaces(lodDist[i],denseAreaPix)) + " %", backgroundColor = score[1], command = pm.Callback( sgButtonSelection, lod.listSmallFaces(lodDist[i],denseAreaPix) ))
                                        totalScore += score[0]
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours) as FaceDF:
                                    f7 = pm.text(label='Too\nDense\nFar ')
                                    for i, lod in enumerate(lods):
                                        score = sgButtonColourWarning(lod.getPercentSmallFaces(lodDist[i+1],denseAreaPix),v.TDF)
                                        pm.button(label= str(lod.getPercentSmallFaces(lodDist[i+1],denseAreaPix)) + " %", backgroundColor = score[1], command = pm.Callback( sgButtonSelection, lod.listSmallFaces(lodDist[i+1],denseAreaPix) ))
                                        totalScore += score[0]

                        
                        with pm.formLayout(backgroundColor=metricsSectionsColours) as materialColumn: #################################### MATERIALS AND TEXTURES
                            m1 = pm.text(label="Materials & Textures\n",font = "obliqueLabelFont",h=metricsMenuHeight)
                            
                            with pm.horizontalLayout(backgroundColor=metricsSectionsColours) as materialButtonLayout:
                            
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours):
                                    m2 = pm.text(label=' \nMaterial\nCount')
                                    for lod in lods:
                                        score = sgButtonColourWarning(lod.countATGMaterials(),v.MC)
                                        pm.button(label= lod.countATGMaterials(), backgroundColor = score[1], command = pm.Callback( sgButtonSelection, lod.listATGMaterials() ) )
                                        totalScore += score[0]
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours):
                                    m3 = pm.text(label='\nTexture\nCount')
                                    for i, lod in enumerate(lods):
                                        score = sgButtonColourWarning(lod.countTextures(),v.TEC)
                                        pm.button(label= lod.countTextures(), backgroundColor = score[1], command = pm.Callback( sgButtonSelectionList2, lod.listTexNodes(),lod.listTextures(),lod.listTexSizesString() ) )
                                        totalScore += score[0]
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours):
                                    m4 = pm.text(label='Total\nTexture\nSize')
                                    for i, lod in enumerate(lods):
                                        score = sgButtonColourWarning(lod.getTotalTexSize(),v.TTS)
                                        pm.button(label= lod.listTotalTexSizesString(), backgroundColor = score[1], command = pm.Callback( sgButtonSelectionList2, lod.listTexNodes(),lod.listTextures(),lod.listTexSizesString()  ) )
                                        totalScore += score[0]
                        
                        
                        
                        with pm.formLayout(backgroundColor=metricsSectionsColours) as vertexColumn:              
                            #v1 = pm.text(label="Vertex Data",font = "obliqueLabelFont")
                            vertexDataButton = pm.button(label = "Calculate Vertex\n Data (slow)")
                            
                            with pm.horizontalLayout(backgroundColor=metricsSectionsColours) as vertexButtonLayout:
                            
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours)as vCountLayout:
                                    v2 = pm.text(label='Vertices\nin\nMaya')
                                    for i, lod in enumerate(lods):
                                        pm.button(label= lod.countVertices(), enable = True)
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours)as vCountLayout:
                                    v3 = pm.text(label='Vertices\nin\nGame')
                                    for i, lod in enumerate(lods):
                                        pm.button(label= "-", enable = False)
                                with pm.verticalLayout(backgroundColor=metricsSectionsColours)as vEfficLayout:
                                    v4 = pm.text(label='Vertex\nSharing\nEfficiency')
                                    for i, lod in enumerate(lods):
                                        pm.button(label= "-", enable = False)

                
                
                
                
                
                ##FRAME LAYOUT
                pm.formLayout( frame, e=True, attachForm=[(overview,'top',borderSize),(overview,'left',borderSize)])
                pm.formLayout( frame, e=True, attachForm=[(suggestions,'top',borderSize),(suggestions,'right',borderSize)], attachControl=[(suggestions,'left',borderSize,overview)])
                pm.formLayout( frame, e=True, attachForm=[(metrics,'left',borderSize),(metrics,'right',borderSize),(metrics,'bottom',borderSize)], attachControl=[(metrics,'top',borderSize,overview)])

                #OVERVIEW LAYOUT
                pm.formLayout( overview, e=True, attachForm=[(ov1,'top',buttonSpacing),(ov1,'left',buttonSpacing),(ov1,'right',buttonSpacing)])
                pm.formLayout( overview, e=True, attachControl=[(ov2,'top',buttonSpacing,ov1)], attachForm=[(ov2,'left',buttonSpacing*8),(ov2,'right',buttonSpacing*8)])
                pm.formLayout( overview, e=True, attachControl=[(ovFFLayout,'top',buttonSpacing,ov2)], attachForm=[(ovFFLayout,'left',buttonSpacing),(ovFFLayout,'right',buttonSpacing)])
                pm.formLayout( overview, e=True, attachControl=[(ovUpdateBut,'top',buttonSpacing,ovFFLayout)], attachForm=[(ovUpdateBut,'left',buttonSpacing),(ovUpdateBut,'right',buttonSpacing),(ovUpdateBut,'bottom',buttonSpacing)])
                
                #SUGGESTIONS LAYOUT
                

                #METRICS LAYOUT
                pm.formLayout( metrics, e=True, attachForm=[(LODColumn,'top',0),(LODColumn,'left',0),(LODColumn,'bottom',0)])
                pm.formLayout( metrics, e=True, attachForm=[(faceColumn,'top',0),(faceColumn,'bottom',0)],attachControl=[(faceColumn,'left',borderSize,distColumn)])
                pm.formLayout( metrics, e=True, attachForm=[(materialColumn,'top',0),(materialColumn,'bottom',0)],attachControl=[(materialColumn,'left',borderSize,faceColumn)])
                pm.formLayout( metrics, e=True, attachForm=[(vertexColumn,'top',0),(vertexColumn,'bottom',0),(vertexColumn,'right',0)],attachControl=[(vertexColumn,'left',borderSize,materialColumn)])
                pm.formLayout( metrics, e=True, attachForm=[(distColumn,'top',0),(distColumn,'bottom',0)],attachControl=[(distColumn,'left',borderSize,LODColumn)])
                
                    #LODs COLUMN
                pm.formLayout( LODColumn, e=True, attachForm=[(l1,'top',lodSpacing),(l1,'left',lodSpacing),(l1,'right',lodSpacing)])  
                pm.formLayout( LODColumn, e=True, attachForm=[(LODButtonLayout,'left',lodSpacing),(LODButtonLayout,'right',lodSpacing),(LODButtonLayout,'bottom',lodSpacing)], attachControl = [(LODButtonLayout,'top',lodSpacing,l1)]) 
                    
                
                    #DIST COLUMN
                pm.formLayout( distColumn, e=True, attachForm=[(d1,'top',lodSpacing),(d1,'left',lodSpacing),(d1,'right',lodSpacing)])  
                pm.formLayout( distColumn, e=True, attachForm=[(distButtonLayout,'left',lodSpacing),(distButtonLayout,'right',lodSpacing),(distButtonLayout,'bottom',lodSpacing)], attachControl = [(distButtonLayout,'top',lodSpacing,d1)])                     
                   

                   #FACE AREA COLUMN
                pm.formLayout( faceColumn, e=True, attachForm=[(f1,'top',lodSpacing),(f1,'left',lodSpacing),(f1,'right',lodSpacing)])  
                pm.formLayout( faceColumn, e=True, attachForm=[(FaceButtonLayout,'left',lodSpacing),(FaceButtonLayout,'right',lodSpacing),(FaceButtonLayout,'bottom',lodSpacing)], attachControl = [(FaceButtonLayout,'top',lodSpacing,f1)])    
                    
                
                    #MATERIAL & TEXTURE COLUMN
                pm.formLayout( materialColumn, e=True, attachForm=[(m1,'top',lodSpacing),(m1,'left',lodSpacing),(m1,'right',lodSpacing)])  
                pm.formLayout( materialColumn, e=True, attachForm=[(materialButtonLayout,'left',lodSpacing),(materialButtonLayout,'right',lodSpacing),(materialButtonLayout,'bottom',lodSpacing)], attachControl = [(materialButtonLayout,'top',lodSpacing,m1)])    
                  
                    #VERTEX COLUMN
                pm.formLayout( vertexColumn, e=True, attachForm=[(vertexDataButton,'top',lodSpacing),(vertexDataButton,'left',lodSpacing),(vertexDataButton,'right',lodSpacing)])  
                pm.formLayout( vertexColumn, e=True, attachForm=[(vertexButtonLayout,'left',lodSpacing),(vertexButtonLayout,'right',lodSpacing),(vertexButtonLayout,'bottom',lodSpacing)], attachControl = [(vertexButtonLayout,'top',lodSpacing,vertexDataButton)])  
                
                
        suggestions.setHeight(overview.getHeight())
        win.setWidthHeight([((metricsButtonWidth+6)*15)+(14*4)+borderSize*3+5,overview.getHeight()+borderSize*3+metricsMenuHeight+textHeight*3+(metricsButtonHeight)*len(lods)])

        ovUpdateBut.setCommand(pm.Callback(sgLODInfoUiUpdate,defaultClosestFF,gameArenaSizeFF, ResolutionFF, minAreaPixFF, denseAreaPixFF,obj))
        vertexDataButton.setCommand(pm.Callback(sgGetVertexData,lods,vertexButtonLayout,vCountLayout,vEfficLayout))
        print "totalScore =", totalScore
        totalScoreValues = sgButtonColourWarning(totalScore,v.TOTS)
        ov2.setLabel("Score "+ str(totalScore)+ "\n" + totalScoreValues[2])
        ov2.setBackgroundColor(totalScoreValues[1])