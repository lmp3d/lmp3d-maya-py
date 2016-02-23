## VertexColorGreyNoise.py ##
##     Version 1.0     ##
## Leif Peterson  2016 ##

## This Script Creates a Second Vertex Color Set on the Selected Object named "colorSet2"
## and adds a Noise Gradient on which the user can select a Minimum and Maximum Value.

# Import Modules
import pymel.core as pm
import random



# Check The Objects Number of Vertex Color Sets
def NumColorSets():
    ColorSets = pm.polyColorSet( query=True, allColorSets=True )
    # If there are No Color Sets, Return 0, if there is Exactly 1, Return 1, if there are at least 2, Return 2.
    if ColorSets == None:
        return 0
    elif len(ColorSets) == 1:
        return 1
    elif len(ColorSets) > 1:
        return 2
        
# Create Second Vertex Color Set
def CreateColorSet( IntIndex ):
    i = IntIndex
    colorSetName = 'colorSet%d' % i
    print colorSetName
    pm.polyColorSet( create=True, colorSet = colorSetName )
        
        
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
    # If there is a Valid Selection
    elif len(Selected) == 1:
        # Get the Selection's Shape
        SelectionShape = Selected[0].getShape()
        # Check if the Object Type is a Polygon Mesh
        IsValidObjType = pm.objectType( SelectionShape, isType='mesh' )
        # If it is Not, Exit the Function and tell the User
        if IsValidObjType != True:
            return "Selected Object is Not a Polygon Mesh"
        # If Everything in Valid, Execute The Script 
        else:
            # Check Number of Color Sets
            NumOfColorSets = NumColorSets()
            if NumOfColorSets == 0:
                # Create 2 Color Sets, Set the first one to .5
                # and Run the Noise Function on the Second
                print "TODO"
                
            elif NumOfColorSets == 1:
                # Create colorSet2 and Run Noise Function
                print "TODO"
                
            elif NumColorSets == 2:
                # Replace the Second Color Set with colorSet2
                # and Run the Noise Function
                print "TODO"
            
        
        
    else:
        return "Unknown Error Occurred"
