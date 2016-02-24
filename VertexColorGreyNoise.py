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

# Set Vertex Color to 0.5 Grey
def SetMiddleGrey( NObject ):
    NObjName = '%s' % NObject.name()
    # Select the Objects Vertices
    pm.selectMode( co=True )
    pm.selectType( pv=True )
    pm.polySelectConstraint( type=0x0001, mode=3 )
    pm.select()
    # List the Objects Vertices
    ObjectVerts = pm.ls( selection=True, fl=True )
    pm.select( cl=True )
    # For Every Vertex on the Object, Set its Vertex Color to 0.5 Grey
    for v in range(len(ObjectVerts)):
        pm.polyColorPerVertex( ObjectVerts[v], colorRGB=(0.5,0.5,0.5), alpha=1.0)
    # Release the Selection Constraints
    pm.polySelectConstraint( mode=0 )
    pm.selectMode( o=True )
    # Select the Object Again
    pm.select( NObjName )

# Class To Hold Noise Functions
#class NoiseFunction:
    
    # Takes Min and Max Float Values
   # def __init__(self, FMin, FMax):
        self.Min = FMin
        self.Max = FMax

    # Generate a Simple Random Noise Gradient 
def SimpleNoise( NObject, FMin, FMax ):
    # Set Local Variables
    NObjName = '%s' % NObject.name()
    min = FMin
    max = FMax    
    # Select the Objects Vertices
    pm.selectMode( co=True )
    pm.selectType( pv=True )
    pm.polySelectConstraint( type=0x0001, mode=3 )
    pm.select()
    # List the Objects Vertices
    ObjectVerts = pm.ls( selection=True, fl=True )
    pm.select( cl=True )
    # For Every Vertex on the Object, Set its Vertex Color to 0.5 Grey
    for v in range(len(ObjectVerts)):
    FValue = random.uniform( min, max )
    pm.polyColorPerVertex( ObjectVerts[v], colorRGB=( FValue, FValue, FValue ), alpha=1.0)
    # Release the Selection Constraints
    pm.polySelectConstraint( mode=0 )
    pm.selectMode( o=True )
    # Select the Object Again
    pm.select( NObjName )           
              
        
# Primary Function
def Main():
    Min = 0.0
    Max = 1.0
    SelectedNoise = NoiseFunction( Min, Max ) 
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
        bIsValidObjType = pm.objectType( SelectionShape, isType='mesh' )
        # If it is Not, Exit the Function and tell the User
        if bIsValidObjType != True:
            return "Selected Object is Not a Polygon Mesh"
        # If Everything in Valid, Execute The Script 
        else:
            # Check Number of Color Sets
            IntNumOfColorSets = NumColorSets()
            if IntNumOfColorSets == 0:
                # Create 2 Color Sets, Set the first one to .5
                # and Run the Noise Function on the Second
                for i in range(2):
                    CreateColorSet(i)
                # If the Current Color Set is colorSet1 set it to 0.5 Grey
                if pm.polyColorSet( query=True, colorSet='colorSet1', currentColorSet=True ) == True:
                    SetMiddleGrey( Selected[0] )
                # Else If it is not the Current Color Set, Set to the Current and Set it's Color to 0.5 Grey
                elif pm.polyColorSet( query=True, colorSet='colorSet1', currentColorSet=True ) == False:
                    pm.polyColorSet( currentColorSet=True, colorSet='colorSet1' )
                    SetMiddleGrey( Selected[0] )
                pm.polyColorSet( currentColorSet=True, colorSet='colorSet2' )
                if pm.polyColorSet( query=True, currentColorSet=True, colorSet='colorSet2' ) != True:
                    return "Unable To Set Current Color Set to colorSet2"
                else:
                    SelectedNoise.SimpleNoise( Selected[0] )
                    return "Random Noise for 'colorSet2' Was Set for %s" % Selected[0].name()
                
            elif IntNumOfColorSets == 1:
                # Create 'colorSet2' 
                CreateColorSet(2)
                # Set 'colorSet2' as the Active Color Set if it's not the Active Color Set
                if pm.polyColorSet( query=True, currentColorSet=True, colorSet='colorSet2' ) != True:
                    pm.polyColorSet( currentColorSet=True, colorSet='colorSet2' )
                # Run Noise Function
                else:
                    SelectedNoise.SimpleNoise( Selected[0] )
                    return "Random Noise for 'colorSet2' Was Set for %s" % Selected[0].name()
                
                
            elif IntNumOfColorSets == 2:
                # List All Color Sets
                AllColorSets = pm.polyColorSet( query=True, allColorSets=True )
                # Replace the Second Color Set with 'colorSet2'
                pm.polyColorSet( rename=True, colorSet= AllColorSets[1], newColorSet='colorSet2' )
                # Set 'colorSet2' as the Active Color Set if it's not the Active Color Set
                if pm.polyColorSet( query=True, currentColorSet=True, colorSet='colorSet2' ) != True:
                    pm.polyColorSet( currentColorSet=True, colorSet='colorSet2' )
                # Run the Noise Function
                else:
                    SelectedNoise.SimpleNoise( Selected[0] )
                    return "Random Noise for 'colorSet2' Was Set for %s" % Selected[0].name()
            
        
        
    else:
        return "Unknown Error Occurred"
