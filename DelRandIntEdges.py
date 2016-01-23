# This code can be used for deleting random interior edges on a Maya PolyObject
import maya.cmds as cmds
import random

# Get the Current Selection
selObjs = cmds.ls( sl = True ) 

# For each object in the selection
for Obj in range(len(selObjs)):
    # Select only the interior edges
    cmds.selectType( pe=True )
    cmds.polySelectConstraint( mode=3, type=0x8000, where=2 )
    
    # List the selected edges
    iEdges = cmds.ls( selection=True, fl=True )
    
    # For each edge in the list, delete it if the random int is greater than 5
    for edge in range(len(iEdges)):
        if random.randrange( 0, 9 ) > 5:
            #print iEdges[edge]
            cmds.delete( iEdges[edge] )
            
    # Release the Selection Constraint when finished       
    cmds.polySelectConstraint( where=0 )
