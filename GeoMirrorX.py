# GeoMirrorX.py
# Leif Peterson 2016
#
# LMP3D Python Scripts version 1.0
#
# The Following Maya Python Script is intended to be used to mirror an object across the X Axis

import maya.cmds as cmds
import string

# Get Selected Objects
SelectedObjects = cmds.ls( selection=True )

for Object in SelectedObjects:
    NewObject = string.replace( Object, 'Left', 'Right' )
    cmds.duplicate( Object, name=NewObject, upstreamNodes=True )
    Result = cmds.group( NewObject )
    cmds.xform( Result, pivots=[0,0,0] )
    cmds.scale( -1, x=True)
    cmds.ungroup( Result )
