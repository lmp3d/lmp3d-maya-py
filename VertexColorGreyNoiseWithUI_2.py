# VertexColorGreyNoiseWithUI.py

##     Version 2.0     ##
## Leif Peterson  2016 ##

# Import Modules
import pymel.core as pm
import random
import math
import functools

## UI Function ##
def createUI( SWindowTitle, pApplyCallback ):
    
    windowID = 'vcgnWindowID'
    
    # If Window is Already Open, Delete it and Open a New One
    if pm.window( windowID, exists=True ):
        pm.deleteUI( windowID )
        
    # Init Window
    pm.window( windowID, title=SWindowTitle, sizeable=False, resizeToFitChildren=True )
        
    pm.rowColumnLayout( numberOfColumns=3, columnWidth=[ (1, 75), (2, 75), (3,75) ], columnOffset=[ (1,'right', 3) ])
        
    pm.text( label='Min Value:' )
        
    # Minimum Value Field, Default = 0.0, min = 0.0, max = 1.0, invisible slider step = 0.01
    MinValueField = pm.floatField( value=0.0, minValue=0.0, maxValue=1.0, step=0.01 )
    pm.separator( h=10, style='none' )
        
    pm.text( label='Max Value:' )
        
    # Maximum Value Field, Default = 1.0, min = 0.0, max = 1.0, invisible slider step = 0.01
    MaxValueField = pm.floatField( value=1.0, minValue=0.0, maxValue=1.0, step=0.01 )
    pm.separator( h=10, style='none' )
    
    # Formatting
    pm.separator( h=10, style='none' )     
    pm.separator( h=10, style='none' )
    pm.separator( h=10, style='none' )
        
    pm.text( label='Noise Type:' )
    
    # Noise Options - Disabled For Version 1.0 Will Be Enabled in 2.0    
    NoiseOption = pm.optionMenu( 'NoiseFunctions', enable=True )
    pm.menuItem( label='Simple', parent='NoiseFunctions' )
    pm.menuItem( label='3D Weighted', parent='NoiseFunctions' )
    pm.menuItem( label='Triangular', parent='NoiseFunctions' )
    pm.menuItem( label='Gamma', parent='NoiseFunctions' )
    pm.menuItem( label='Perlin', parent='NoiseFunctions' )
    pm.menuItem( label='OpenSimplex', parent='NoiseFunctions' )
    pm.separator( h=10, style='none' )
    
    # Formatting
    pm.separator( h=10, style='none' )
    pm.separator( h=10, style='none' )
    pm.separator( h=10, style='none' )
    
    # Buttons 
    pm.separator( h=10, style='none' )   
    pm.button( label='Apply', command=functools.partial(pApplyCallback,
                                                        NoiseOption,
                                                        MaxValueField,
                                                        MinValueField) )
        
    def cancelCallback( *Args ):
        if pm.window( windowID, exists=True ):
            pm.deleteUI( windowID )
        
    pm.button( label='Cancel', command=cancelCallback )
        
    pm.showWindow()       


## Noise Generation Functions Start Here ##


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

### Noise Functions ##

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
    # For Every Vertex on the Object, Set its Vertex Color to a value between Min and Max
    for v in range(len(ObjectVerts)):
        FValue = random.uniform( min, max )
        pm.polyColorPerVertex( ObjectVerts[v], colorRGB=( FValue, FValue, FValue ), alpha=1.0)
    # Release the Selection Constraints
    pm.polySelectConstraint( mode=0 )
    pm.selectMode( o=True )
    # Select the Object Again
    pm.select( NObjName )           
    
# Generate a Triangular Random Noise Gradient 
def TriangularNoise( NObject, FMin, FMax ):
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
    # For Every Vertex on the Object, Set its Vertex Color to a value between Min and Max
    for v in range(len(ObjectVerts)):
        FValue = random.triangular( min, max, random.uniform( min+0.1, max-0.1 ) )
        pm.polyColorPerVertex( ObjectVerts[v], colorRGB=( FValue, FValue, FValue ), alpha=1.0)
    # Release the Selection Constraints
    pm.polySelectConstraint( mode=0 )
    pm.selectMode( o=True )
    # Select the Object Again
    pm.select( NObjName )  

# Generate a Gamma Distribution Random Noise Gradient 
def GammaNoise( NObject, FMin, FMax ):
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
    # For Every Vertex on the Object, Set its Vertex Color to a value between Min and Max
    for v in range(len(ObjectVerts)):
        FValue = random.gammavariate( min+.001, max )
        pm.polyColorPerVertex( ObjectVerts[v], colorRGB=( FValue, FValue, FValue ), alpha=1.0)
    # Release the Selection Constraints
    pm.polySelectConstraint( mode=0 )
    pm.selectMode( o=True )
    # Select the Object Again
    pm.select( NObjName )               

# Generate a Random Noise Gradient Weighted by the 3D Location
def f3DNoise( NObject, FMin, FMax ):
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
    RandomVerts = list(ObjectVerts)
    random.shuffle(RandomVerts)
    pm.select( cl=True )
    # For Every Vertex on the Object, Set its Vertex Color to a random value weighted by the sum of its location
    for v in range(len(ObjectVerts)):
        loc = pm.xform( RandomVerts[v], query=True, translation=True, worldSpace=True )
        locValue = math.sqrt(abs(random.choice(loc)))
        RValue = random.uniform( min, max )
        FValue = (locValue + RValue)/2
        pm.polyColorPerVertex( ObjectVerts[v], colorRGB=( FValue, FValue, FValue ), alpha=1.0)
    # Release the Selection Constraints
    pm.polySelectConstraint( mode=0 )
    pm.selectMode( o=True )
    # Select the Object Again
    pm.select( NObjName ) 
        
# Primary Function
def GenerateVertexColor( StrNoiseOpt, FMax, FMin ):
    NoiseFunction = StrNoiseOpt
    Min = FMin
    Max = FMax 
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
                    CreateColorSet(i+1)
                # If the Current Color Set is colorSet1 set it to 0.5 Grey
                if pm.polyColorSet( query=True, colorSet=True, currentColorSet=True ) == 'colorSet1':
                    SetMiddleGrey( Selected[0] )
                # Else If it is not the Current Color Set, Set to the Current and Set it's Color to 0.5 Grey
                elif pm.polyColorSet( query=True, colorSet=True, currentColorSet=True ) != 'colorSet1':
                    pm.polyColorSet( currentColorSet=True, colorSet='colorSet1' )
                    SetMiddleGrey( Selected[0] )
                pm.polyColorSet( currentColorSet=True, colorSet='colorSet2' )
                if pm.polyColorSet( query=True, currentColorSet=True, colorSet=True ) == 'colorSet1':
                    return "Unable To Set Current Color Set to colorSet2"
                else:
                    if NoiseFunction == 'Simple':
                        SimpleNoise( Selected[0], Min, Max )
                        return "Random Noise for 'colorSet2' Was Set for %s" % Selected[0].name()
                    elif NoiseFunction == 'Triangular':
                        TriangularNoise( Selected[0], Min, Max )
                        return "Triangular Noise was used for 'colorSet2' for %s" % Selected[0].name()
                    elif NoiseFunction == 'Gamma':
                        GammaNoise( Selected[0], Min, Max )
                        return "Gamma Noise Distribution was used for 'colorSet2' for %s" % Selected[0].name()
                    elif NoiseFunction == '3D Weighted':
                        f3DNoise( Selected[0], Min, Max )
                        return "3D Weighted Noise was used for 'colorSet2' for %s" % Selected[0].name()
                    else:
                        return "Invalid Noise Function Sepcified"
                        
            elif IntNumOfColorSets == 1:
                # Create 'colorSet2' 
                CreateColorSet(2)
                # Set 'colorSet2' as the Active Color Set if it's not the Active Color Set
                if pm.polyColorSet( query=True, currentColorSet=True, colorSet=True ) != 'colorSet2':
                    pm.polyColorSet( currentColorSet=True, colorSet='colorSet2' )
                    # Run Noise Function
                    if NoiseFunction == 'Simple':
                        SimpleNoise( Selected[0], Min, Max )
                        return "Random Noise for 'colorSet2' Was Set for %s" % Selected[0].name()
                    elif NoiseFunction == 'Triangular':
                        TriangularNoise( Selected[0], Min, Max )
                        return "Triangular Noise was used for 'colorSet2' for %s" % Selected[0].name()
                    elif NoiseFunction == 'Gamma':
                        GammaNoise( Selected[0], Min, Max )
                        return "Gamma Noise Distribution was used for 'colorSet2' for %s" % Selected[0].name()
                    elif NoiseFunction == '3D Weighted':
                        f3DNoise( Selected[0], Min, Max )
                        return "3D Weighted Noise was used for 'colorSet2' for %s" % Selected[0].name()
                    else:
                        return "Invalid Noise Function Sepcified"
                
            elif IntNumOfColorSets == 2:
                # List All Color Sets
                AllColorSets = pm.polyColorSet( query=True, allColorSets=True )
                # Check for 'colorSet2" 
                if 'colorSet2' in AllColorSets:
                    if pm.polyColorSet( query=True, currentColorSet=True, colorSet=True ) != 'colorSet2':
                        pm.polyColorSet( currentColorSet=True, colorSet='colorSet2' )
                        # Run the Noise Function
                        if NoiseFunction == 'Simple':
                            SimpleNoise( Selected[0], Min, Max )
                            return "Random Noise for 'colorSet2' Was Set for %s" % Selected[0].name()
                        elif NoiseFunction == 'Triangular':
                            TriangularNoise( Selected[0], Min, Max )
                            return "Triangular Noise was used for 'colorSet2' for %s" % Selected[0].name()
                        elif NoiseFunction == 'Gamma':
                            GammaNoise( Selected[0], Min, Max )
                            return "Gamma Noise Distribution was used for 'colorSet2' for %s" % Selected[0].name()
                        elif NoiseFunction == '3D Weighted':
                            f3DNoise( Selected[0], Min, Max )
                            return "3D Weighted Noise was used for 'colorSet2' for %s" % Selected[0].name()
                        else:
                            return "Invalid Noise Function Sepcified"
                           
                # if it does not exist Create 'colorSet2'
                CreateColorSet(2)
                # Set 'colorSet2' as the Active Color Set if it's not the Active Color Set
                if pm.polyColorSet( query=True, currentColorSet=True, colorSet=True ) != 'colorSet2':
                    pm.polyColorSet( currentColorSet=True, colorSet='colorSet2' )
                    # Run the Noise Function
                    if NoiseFunction == 'Simple':
                        SimpleNoise( Selected[0], Min, Max )
                        return "Random Noise for 'colorSet2' Was Set for %s" % Selected[0].name()
                    elif NoiseFunction == 'Triangular':
                        TriangularNoise( Selected[0], Min, Max )
                        return "Triangular Noise was used for 'colorSet2' for %s" % Selected[0].name()
                    elif NoiseFunction == 'Gamma':
                        GammaNoise( Selected[0], Min, Max )
                        return "Triangular Noise was used for 'colorSet2' for %s" % Selected[0].name()
                    elif NoiseFunction == '3D Weighted':
                        f3DNoise( Selected[0], Min, Max )
                        return "3D Weighted Noise was used for 'colorSet2' for %s" % Selected[0].name()
                    else:
                        return "Invalid Noise Function Sepcified"
            
                
    else:
        return "Unknown Error Occurred"
        
        
def applyCallback( pNoiseOption, pMaxValueField, pMinValueField, *pArgs ):
    
    NoiseOptionState = pm.optionMenu( pNoiseOption, query=True, value=True )
    MaxValue = pm.floatField( pMaxValueField, query=True, value=True )
    MinValue = pm.floatField( pMinValueField, query=True, value=True )
    
    GenerateVertexColor( NoiseOptionState, MaxValue, MinValue )   
    
    
createUI( 'NoiseGen', applyCallback )
