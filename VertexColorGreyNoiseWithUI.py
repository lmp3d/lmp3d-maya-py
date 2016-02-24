# VertexColorGreyNoiseWithUI.py

##     Version 1.0     ##
## Leif Peterson  2016 ##

# Import Modules
import pymel.core as pm

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
    maxValueField = pm.floatField( value=1.0, minValue=0.0, maxValue=1.0, step=0.01 )
    pm.separator( h=10, style='none' )
    
    # Formatting
    pm.separator( h=10, style='none' )     
    pm.separator( h=10, style='none' )
    pm.separator( h=10, style='none' )
        
    pm.text( label='Noise Type:' )
    
    # Noise Options    
    pm.optionMenu( 'NoiseFunctions' )
    pm.menuItem( label='Simple', parent='NoiseFunctions' )
    pm.menuItem( label='Perlin', parent='NoiseFunctions' )
    pm.menuItem( label='OpenSimplex', parent='NoiseFunctions' )
    pm.separator( h=10, style='none' )
    
    # Formatting
    pm.separator( h=10, style='none' )
    pm.separator( h=10, style='none' )
    pm.separator( h=10, style='none' )
    
    # Buttons 
    pm.separator( h=10, style='none' )   
    pm.button( label='Apply', command=pApplyCallback )
        
    def cancelCallback( *Args ):
        if pm.window( windowID, exists=True ):
            pm.deleteUI( windowID )
        
    pm.button( label='Cancel', command=cancelCallback )
        
    pm.showWindow()
        
def applyCallback( *pArgs ):
    
    print 'Apply button pressed.'
    
createUI( 'NoiseGen', applyCallback )
