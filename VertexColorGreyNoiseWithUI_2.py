# VertexColorGreyNoiseWithUI.py

##     Version 2.0     ##
## Leif Peterson  2016 ##

# Import Modules
import pymel.core as pm
import sys
import os
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
    pm.menuItem( label='Perlin', parent='NoiseFunctions' )
    pm.menuItem( label='3D Weighted', parent='NoiseFunctions' )
    pm.menuItem( label='Triangular', parent='NoiseFunctions' )
    pm.menuItem( label='Gamma', parent='NoiseFunctions' )
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


## Perlin Noise Base Functions and Globals ##

# Hash table to assist in generation
hashMask = 22

gradientMask3D = 15

hash = (151,160,137, 91, 90, 15,131, 13,201, 95, 96, 53,194,233,  7,225,
        140, 36,103, 30, 69,142,  8, 99, 37,240, 21, 10, 23,190,  6,148,
        247,120,234, 75,  0, 26,197, 62, 94,252,219,203,117, 35, 11, 32,
         57,177, 33, 88,237,149, 56, 87,174, 20,125,136,171,168, 68,175,
         74,165, 71,134,139, 48, 27,166, 77,146,158,231, 83,111,229,122,
         60,211,133,230,220,105, 92, 41, 55, 46,245, 40,244,102,143, 54,
         65, 25, 63,161,  1,216, 80, 73,209, 76,132,187,208, 89, 18,169,
        200,196,135,130,116,188,159, 86,164,100,109,198,173,186,  3, 64,
         52,217,226,250,124,123,  5,202, 38,147,118,126,255, 82, 85,212,
        207,206, 59,227, 47, 16, 58, 17,182,189, 28, 42,223,183,170,213,
        119,248,152,  2, 44,154,163, 70,221,153,101,155,167, 43,172,  9,
        129, 22, 39,253, 19, 98,108,110, 79,113,224,232,178,185,112,104,
        218,246, 97,228,251, 34,242,193,238,210,144, 12,191,179,162,241,
         81, 51,145,235,249, 14,239,107, 49,192,214, 31,181,199,106,157,
        184, 84,204,176,115,121, 50, 45,127,  4,150,254,138,236,205, 93,
        222,114, 67, 29, 24, 72,243,141,128,195, 78, 66,215, 61,156,180 )

sizeX = len(hash)
sizeY = len(hash)

# Smooth function
def Smooth(t):
    return t*t*t*(t*(t*float(6.0) - float(15)) + float(10.0)) 

# Lerp function
def Lerp(t,a,b):
 
    return a + t*(b - a)
    
# Gradient   
def Grad(hashMask,x,y,z):

    if hashMask < 8:
        u=x
    else:
        u=y
    if hashMask < 4:
        v=y
    else:
        if hashMask == 12 or hashMask == 14:
            v=x
        else:
            v=z
    if hashMask&1 == 0:
        first = u
    else:
        first = -u
    if hashMask&2 == 0:
        second = v
    else:
        second = -v
    return first + second


#Dot product of the 3D gradient
def DotGridGradient(ix, iy,iz, x, y, z): 
 
     #Precomputed (or otherwise) gradient vectors at each grid point X,Y
     Grad(hashMask,x,y,z)
 
     dx = float(x) - ix
     dy = float(y) - iy
     dz = float(z) - iz
     #Compute the dot-product
     return dx*Grad(hashMask,ix,0,0) + dy*Grad(hashMask,0,iy,0) + dz*Grad(hashMask,0,0,iz)

# Modify surface with Perlin Noise
def PerlinNoise(x,y,z, bound):
    BoundingDimention = bound
    X0 = int(x)&(BoundingDimention - 1)
    Y0 = int(y)&(BoundingDimention - 1)
    Z0 = int(z)&(BoundingDimention - 1)
    
    X0 &= hashMask
    Y0 &= hashMask
    Z0 &= hashMask
    
    X1 = X0 + 1
    Y1 = Y0 + 1
    Z1 = Z0 + 1
    
    x -= int(x)
    y -= int(y)
    z -= int(z)
    
    u = Smooth(x)
    v = Smooth(y)
    w = Smooth(z)
    
    h0 = hash[X0]
    h1 = hash[Y0]
    h00 = hash[h0 + Y0]
    h10 = hash[h1 + Y0]
    h01 = hash[h0 + Y1]
    h11 = hash[h1 + Y1]
    
    
    A = Grad(hash[h00 + Z0] & gradientMask3D,x,y,z)
    B = Grad(hash[h10 + Z0] & gradientMask3D,x,y,z)
    C = Grad(hash[h01 + Z0] & gradientMask3D,x,y,z)
    D = Grad(hash[h11 + Z0] & gradientMask3D,x,y,z)
    E = Grad(hash[h00 + Z1] & gradientMask3D,x,y,z)
    F = Grad(hash[h10 + Z1] & gradientMask3D,x,y,z)
    G = Grad(hash[h01 + Z1] & gradientMask3D,x,y,z)
    H = Grad(hash[h11 + Z1] & gradientMask3D,x,y,z)
    
    v000 = DotGridGradient(A,X0,Y0,Z0, y, z)
    v100 = DotGridGradient(B,X1,Y0,Z0, y, z)
    v010 = DotGridGradient(C,X0,Y1,Z0, y, z)
    v110 = DotGridGradient(D,X1,Y1,Z0, y, z)
    v001 = DotGridGradient(E,X0,Y0,Z1, y, z)
    v101 = DotGridGradient(F,X1,Y0,Z1, y, z)
    v011 = DotGridGradient(G,X0,Y1,Z1, y, z)
    v111 = DotGridGradient(H,X1,Y1,Z1, y, z)
   
    
    tx = Smooth(x)
    ty = Smooth(y)
    tz = Smooth(z)
    
    return Lerp(Lerp(Lerp(v000, v100, tx), Lerp(v010, v110, tx), ty), Lerp(Lerp(v001, v101, tx),Lerp(v011, v111, tx), ty), tz)

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
    
# Generate a Random Noise Gradient Weighted by the 3D Location
def PerlinNoiseFiller( NObject, FMin, FMax ):
    # Set Local Variables
    NObjName = '%s' % NObject.name()
    Divisions = 15
    min = FMin
    max = FMax    
    # Select the Objects Vertices
    pm.selectMode( co=True )
    pm.selectType( pv=True )
    pm.polySelectConstraint( type=0x0001, mode=3 )
    pm.select()
    # List the Objects Vertices
    ObjectVerts = pm.ls( selection=True, fl=True )
    random.shuffle(RandomVerts)
    pm.select( cl=True )
    # For Every Vertex on the Object, Set its Vertex Color to a random value weighted by the sum of its location
    for v in range(len(ObjectVerts)):
        loc = pm.xform( ObjectVerts[v], query=True, translation=True, worldSpace=True )
        RawValue = PerlinNoise((loc[0]*200),(loc[1]*300),(loc[2]*250), Divisions)
        ModValue = math.sqrt(abs(RawValue))/100000.0 
        if ModValue < 0.5:
            FValue = (ModValue * min)/2.0
        elif ModValue > 0.5:
            FValue = (ModValue * max)/2.0  
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
                    elif NoiseFunction == 'Perlin':
                        PerlinNoiseGen( Selected[0], Min, Max )
                        return "Perlin Noise was used for 'colorSet2' for %s" % Selected[0].name()
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
                    elif NoiseFunction == 'Perlin':
                        PerlinNoiseGen( Selected[0], Min, Max )
                        return "Perlin Noise was used for 'colorSet2' for %s" % Selected[0].name()
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
                        elif NoiseFunction == 'Perlin':
                            PerlinNoiseGen( Selected[0], Min, Max )
                            return "Perlin Noise was used for 'colorSet2' for %s" % Selected[0].name()
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
                    elif NoiseFunction == 'Perlin':
                        PerlinNoiseGen( Selected[0], Min, Max )
                        return "Perlin Noise was used for 'colorSet2' for %s" % Selected[0].name()
                    elif NoiseFunction == 'Triangular':
                        TriangularNoise( Selected[0], Min, Max )
                        return "Triangular Noise was used for 'colorSet2' for %s" % Selected[0].name()
                    elif NoiseFunction == 'Gamma':
                        GammaNoise( Selected[0], Min, Max )
                        return "Gamma Noise was used for 'colorSet2' for %s" % Selected[0].name()
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
