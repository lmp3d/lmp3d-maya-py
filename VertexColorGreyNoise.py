## VertexColorGreyNoise.py ##
##     Version 1.0     ##
## Leif Peterson  2016 ##

## This Script Creates a Second Vertex Color Set on the Selected Object named "colorSet2"
## and adds a Noise Gradient on which the user can select a Minimum and Maximum Value.

# Import Modules
import pymel.core as pm
import random



# Check if Object has Multiple Vertex Color Sets
def HasMultipleColorSets():
    ColorSets = pm.polyColorSet( query=True, allColorSets=True )
    if len(ColorSets) > 1:
        return True
    elif len(ColorSets) == 1:
        return False
        
# Create Second Vertex Color Set
def CreateSecondColorSet( SelectedObject ):
    if HasMultipleColorSets() == True:
        return 0
        
        
#selected = pm.ls( selection=True )        
#print len(selected)       
        
# Primary Function
def Main():
    # Check that a Valid Selection has been made
    Selected = pm.ls( selection = True ) 
    if len(Selected) == 0:
        return "No Objects Selected"
    elif len(Selected) > 1:
        return "More Than One Object Selected"
    # If there is a Valid Selection, Execute the script
    elif len(Selected) == 1:
        # Get the Selection's Shape
        SelectionShape = Selected[0].getShape()
        # Check if the Object Type is a Polygon Mesh
        IsValidObjType = pm.objectType( SelectionShape, isType='mesh' )
        # If it is Not, Exit the Function and tell the User
        if IsValidObjType != True:
            return "Selected Object is Not a Polygon Mesh"
        else:
            print "is valid"
        
        
    else:
        return "Unknown Error Occurred"
