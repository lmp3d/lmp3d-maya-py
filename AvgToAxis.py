# AvgToAxis.py
# Leif Peterson 2016
#
# LMP3D Maya Python Scripts version 1.0
#
# The Following Maya Python Script is intended to be used to average a selection along a world space axis.

import maya.cmds as cmds

# Function Declaration for X Axis
def AvgToX( *pArgs ):
    Selected = cmds.ls(selection = True, fl = True) # Gets Selection, Returns Flattened
    print Selected                                  
    
    PosX = []      # Declare a List to store X location values for each vertex  
    
    for component in Selected:
        SelectedPosition = cmds.xform(component, q = True, ws = True, t = True) # Get the Location of each Vertex
        PosX.append(SelectedPosition[0])                                 # Add the Location to to the List 
        #print SelectedPosition
    
    #print PosX[0:len(PosX)] # Prints the list, for debugging purposes
    
    AvgXPos = sum(PosX) / len(PosX)
    
    print AvgXPos
    
    for vertex in Selected:
        cmds.move(  AvgXPos, x = True, ws = True)
    return

# Function Declaration for Y Axis
def AvgToY( *pArgs ):
    Selected = cmds.ls(selection = True, fl = True) # Gets Selection, Returns Flattened
    print Selected                                  
    
    PosY = []      # Declare a List to store Y location values for each vertex  
    
    for component in Selected:
        SelectedPosition = cmds.xform(component, q = True, ws = True, t = True) # Get the Location of each Vertex
        PosY.append(SelectedPosition[1])                                 # Add the Location to to the List 
        #print SelectedPosition
    
    #print PosY[0:len(PosY)] # Prints the list, for debugging purposes
    
    AvgYPos = sum(PosY) / len(PosY)
    
    print AvgYPos
    
    for vertex in Selected:
        cmds.move(  AvgYPos, y = True, ws = True)
    return
 
# Function Declaration for Z Axis 
def AvgToZ( *pArgs ):
    Selected = cmds.ls(selection = True, fl = True) # Gets Selection, Returns Flattened
    print Selected                                  
    
    PosZ = []      # Declare a List to store Z location values for each vertex  
    
    for component in Selected:
        SelectedPosition = cmds.xform(component, q = True, ws = True, t = True) # Get the Location of each Vertex
        PosZ.append(SelectedPosition[2])                                 # Add the Location to to the List 
        #print SelectedPosition
    
    #print PosZ[0:len(PosZ)] # Prints the list, for debugging purposes
    
    AvgZPos = sum(PosZ) / len(PosZ)
    
    print AvgZPos
    
    for vertex in Selected:
        cmds.move(  AvgZPos, z = True, ws = True)
    return
    
def createUI (pWindowTitle):
    
    windowID = 'AvgWindowID'
    
    if cmds.window( windowID, exists = True ):
        cmds.deleteUI( windowID )
        
    cmds.window( windowID, title=pWindowTitle, sizeable = False, resizeToFitChildren = True )
    
    cmds.rowColumnLayout( numberOfColumns = 1, columnWidth = [ (1, 100) ], columnOffset = [ (1, 'both', 6) ] )
    
    cmds.text( label='Average to Axis' )
    
    cmds.separator( h=10, style='none' )
    
    cmds.button( label='Average to X', bgc=[1.0,0.3,0.3], command=AvgToX )
    
    cmds.separator( h=5, style='none' )
    
    cmds.button( label='Average to Y', bgc=[0.3,1.0,0.3], command=AvgToY )
    
    cmds.separator( h=5, style='none' )
    
    cmds.button( label='Average to Z', bgc=[0.3,0.3,1.0], command=AvgToZ )
    
    cmds.separator( h=10, style='none' )
    
    def cancelAvg( *pArgs ):
        if cmds.window(windowID, exists=True ):
            cmds.deleteUI( windowID )
            
    cmds.button( label='Cancel', command=cancelAvg )
    
    cmds.showWindow()
    
createUI( 'Average to Axis' )
