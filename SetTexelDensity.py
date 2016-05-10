# SetTexelDensity.py

########################
##    Version 1.0     ##
## Leif Peterson 2016 ##

# Import Modules
import pymel.core as pm
import functools

## Variable Naming Conventions
## Integers Start with I
## Floats Start with F
## Strings Start with S
## Bools Start with B

## UI Function ##
def createUI( SWindowTitle, pApplyCallback ):
    
    windowID = 'texdenWindowID'
    
    # If Window is Already Open, Delete it and Open a New One
    if pm.window( windowID, exists=True ):
        pm.deleteUI( windowID )
    
    # Init Window
    pm.window( windowID, title=SWindowTitle, sizeable=False, resizeToFitChildren=True )
    
    pm.rowColumnLayout( numberOfColumns=3, columnWidth=[ (1, 95), (2, 75), (3, 75) ], columnOffset=[ (1, 'right', 3) ])
    
    pm.text( label='Texels Per Unit' )
    
    # Field for Desired Texel Density, Default = 1.0, min = 0.0, invisible slider step 1.0
    DensityField = pm.floatField( value=1.0, minValue=0.0, step=1.0, annotation="This is the Desired Texel Density" )
    pm.separator( h=10, style='none' )
    
    pm.text( label='Texture Resolution' )
    
    # Field for Texture Resolution, Default 1
    ResolutionField = pm.intField( value=1, minValue=1, step=1, annotation="This is Texture Resolution" )
    pm.separator(h=10, style='none' )
    
    # Formatting
    pm.separator( h=10, style='none' )     
    pm.separator( h=10, style='none' )
    pm.separator( h=10, style='none' )
    
    pm.separator( h=10, style='none' )   
    pm.button( label='Apply', command=functools.partial(pApplyCallback,
                                                        DensityField,
                                                        ResolutionField) )
    
        
    def cancelCallback( *Args ):
        if pm.window( windowID, exists=True ):
            pm.deleteUI( windowID )
        
    pm.button( label='Cancel', command=cancelCallback )
    
    pm.showWindow()

## Function to Apply Texel Desired Texel Density
## Takes as Inputs FTxlPerUnit (Float Pixels Per Unit), ITexResolution (Integer Texture Resolution), BKeepLayout (Boolean Retain layout, only works on selections with interior polygons)
def setTexelDensity( FTxlPerUnit, ITexResolution ):
    
    FDensity = FTxlPerUnit
    FResolution = float(ITexResolution)
    
    if FResolution < 0.001:
        return "Don't Divide by 0"
    
    FScalar = FDensity/FResolution
    
    SSelection = pm.ls( selection=True, fl=True )
    
    if len(SSelection) == 0:
        return "No Selection"
    else:   
        for i in range(len(SSelection)):
            pm.unfold( SSelection[i], stoppingThreshold=0.001, globalBlend=0.0, globalMethodBlend=1.0, pinUvBorder=False, pinSelected=False, optimizeAxis=0, useScale=True, scale=FScalar )
            return "Texel Density Applied"
        
## Executes when Apply Button is Pressed
def applyCallback( pDensityField, pResolutionField, *pArgs ):
    
    FDensityValue = pm.floatField( pDensityField, query=True, value=True )
    IResolutionValue = pm.intField( pResolutionField, query=True, value=True )
    
    setTexelDensity( FDensityValue, IResolutionValue )
    
createUI( 'Texel Density', applyCallback )
