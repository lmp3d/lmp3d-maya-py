# noiseGen.py
# Leif Peterson 2016
#
#LMP3D Python Scripts version 1.0
#
# The Following Maya Python Script is intended to be used to generate Simple Noise

import maya.cmds as cmds
import functools
import random

def addNoise( xD = 1.0, yD = 1.0, zD = 1.0, nF = 1.0 ):
    xDisplace = xD # Placeholder until UI is implemented
    yDisplace = yD # Placeholder until UI is implemented
    zDisplace = zD # Placeholder until UI is implemented
    
    noiseFactor = nF # Placeholder until UI is implemented - will range from 0.0 to 1.0
    
    # Get Selection, Convert to Vertices 
    Selection = cmds.ls( selection = True, fl=True )
    convertedSel = cmds.polyListComponentConversion( Selection, tv = True )
    vtxSelection = cmds.ls( convertedSel, fl=True )
    
    for index in range(len(vtxSelection)):
        cmds.move( random.uniform(-noiseFactor*xDisplace, noiseFactor*xDisplace), random.uniform(-noiseFactor*yDisplace, noiseFactor*yDisplace), random.uniform(-noiseFactor*zDisplace, noiseFactor*zDisplace), vtxSelection[index], r=True )
       
def createNoiseUI(pWindowTitle, pApplyCallback):

    windowID = 'NoiseWindowID'
    
    if cmds.window( windowID, exists = True ):
        cmds.deleteUI( windowID )
        
    cmds.window( windowID, title=pWindowTitle, sizeable = False, resizeToFitChildren = True )
    
    cmds.rowColumnLayout( numberOfColumns = 3, columnWidth = [ (1, 75), (2, 60), (3, 60) ], columnOffset = [ (1, 'right', 3) ] )
    
    cmds.text( label='X Amount:' )
    
    xAmountField = cmds.floatField( value=1.0, step=0.1, min=-100, max=100, bgc=(1.0,0.8,0.8) )
    
    cmds.separator( h=10, style='none' )
    
    cmds.text( label='Y Amount:' )
    
    yAmountField = cmds.floatField( value=1.0, step=0.1, min=-100, max=100, bgc=(0.8,1.0,0.8) )
    
    cmds.separator( h=10, style='none' )
    
    cmds.text( label='Z Amount:' )
    
    zAmountField = cmds.floatField( value=1.0, step=0.1, min=-100, max=100, bgc=(0.8,0.8,1.0) )
    
    cmds.separator( h=10, style='none' )
    
    cmds.text( label='Noise Factor:' )
    
    NoiseFactorField = cmds.floatField( value=1.0, step=0.1, min=0, max=2, precision=3 )
    
    cmds.separator( h=10, style='none' )
    
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    cmds.separator( h=10, style='none' )
    
    cmds.separator( h=10, style='none' )
    
    cmds.button( label='Apply', command=functools.partial( pApplyCallback, xAmountField, yAmountField, zAmountField, NoiseFactorField ) )
    
    def cancelCallback( *pArgs ):
        if cmds.window(windowID, exists=True ):
            cmds.deleteUI( windowID )
            
    cmds.button( label='Cancel', command=cancelCallback )
    
    cmds.showWindow()
    
def applyCallback( pxAmountField, pyAmountField, pzAmountField, pNoiseFactorField, *pArgs ):
    
    xAmount = cmds.floatField( pxAmountField, query=True, value=True )
    yAmount = cmds.floatField( pyAmountField, query=True, value=True )
    zAmount = cmds.floatField( pzAmountField, query=True, value=True )
    NoiseFactor = cmds.floatField( pNoiseFactorField, query=True, value=True )
    
    addNoise( xAmount, yAmount, zAmount, NoiseFactor )
    
createNoiseUI( 'Noise', applyCallback )
