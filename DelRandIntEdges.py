# DelRandIntEdges.py
#
# Leif Peterson 2016
#
# This code deletes random interior edges and cleans up winged vertices, while maintaing corners

import pymel.core as pm
import random

# create a list of all selected objects
SelectedObjects = pm.ls( selection=True, o=True )

# for each object delete its interior edges randomly 
for Object in range(len(SelectedObjects)):
    # select only border edges
    pm.selectType( pe=True )
    pm.hilite( SelectedObjects[Object] )
    pm.polySelectConstraint( mode=3, type=0x8000, where=1 )
    pm.select()
    borderEdges = pm.ls( selection=True, fl=True )
    
    # select all edges
    pm.polySelectConstraint( where=0 )
    pm.select()
    allEdges = pm.ls( selection=True, fl=True )
    
    # initilize the inside edges list
    insideEdges = []
    
    # remove border edges
    for edge in range(len(borderEdges)):
        allEdges.remove( borderEdges[edge] )
    
    # create a list of interior edges from the list of all edges with the border edges removed    
    for edge in range(len(allEdges)):
        insideEdges.append(allEdges[edge])
    
    # clear selection
    pm.select( cl=True )  
    
    # randomly select and delete an interior edge   
    for iEdge in range(len(insideEdges)):
        if random.randrange( 0, 9 ) > 5:
            pm.select( insideEdges[iEdge] )
            pm.polyDelEdge( cv=False )
    
    # Clean up the winged vertices that are along straight edges, preserving corners        
    pm.selectType( pv=True )
    pm.polySelectConstraint( angle=1, type=0x0001, mode=3, anglebound=[ 91.0, 181.0 ] )
    pm.select()
    pm.polyDelVertex()
    pm.polySelectConstraint( angle=0 )
