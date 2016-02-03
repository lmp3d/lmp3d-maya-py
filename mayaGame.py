# mayaGame.py
# Leif Peterson 2016
#
# Implements Input and Game Loop inside Maya Viewport.
import pymel.core as pm
import os
import sys
import time
import math
import ctypes
import random
from ctypes import *
import collections
import sdl2
import sdl2.ext

# define structures to store 2D and 3D floating point values
class FlVector3(Structure):
    _fields_=[("x", c_float), ("y", c_float), ("z", c_float)]

class IntVector3(Structure):
    _fields_=[("x", c_int), ("y", c_int), ("z", c_int)]
    
class IntVector2(Structure):
    _fields_=[("x", c_int), ("y", c_int)]
    
class FlVector2(Structure):
    _fields_=[("x", c_float), ("y", c_float)]    

# Pawn class - has an object and can move
#class Pawn:
    #def __init__(self, speed):
        #fSpeed = speed
        #rColor = 1
        #gColor = 0
        #bColor = 0
        #aColor = 1
        
    #def update(self):
        #pm.xform( mObj[0], r=True, wd=True, t=[ 1.0, 0.0, 1.0] )

def RemapMovement( RawMoveX, RawMoveY ):
    NormX = 0.0
    NormY = 0.0
    NormalMove = FlVector2( NormX, NormY )
    RawX = RawMoveX
    RawY = RawMoveY
    # Dead Zone is between -6000 and 6000
    # Convert the integer a value between -1 and 1
    if abs(RawX) < 6000 :
        NormX = 0.0
    elif abs(RawX) > 6000:
        NormX = ((float(RawX) - (-32768.0)) / (32767.0 - (-32768))) * ( 1.0 - (-1.0)) + (-1.0)       
    if abs(RawY) < 6000 :
        NormY = 0.0
    elif abs(RawY) > 6000:
        NormY = ((float(RawY) - (-32768.0)) / (32767.0 - (-32768))) * ( 1.0 - (-1.0)) + (-1.0)
    # Build the normalized move vector 
    NormalMove.x = NormX
    NormalMove.y = NormY
    return NormalMove

# Vector Functions
def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
    return [ u[i]+v[i] for i in range(len(u)) ]

def sub(u, v):
    return [ u[i]-v[i] for i in range(len(u)) ]

def dot(u, v):
    return sum(u[i]*v[i] for i in range(len(u)))

def normalize(v):
    vmag = magnitude(v)
    return [ v[i]/vmag  for i in range(len(v)) ]           

# AABB Collision Detection Function
def detectCollision( object1, object2 ):
    obj1 = object1
    obj2 = object2
    rawBB1 = pm.xform( obj1, q=True, bb=True )
    rawBB2 = pm.xform( obj2, q=True, bb=True )
    #print rawBB1
    #print rawBB2
    if rawBB1[0] > rawBB2[3]:
        return False
    if rawBB1[2] > rawBB2[5]:
        return False
    if rawBB1[3] < rawBB2[0]:
        return False
    if rawBB1[5] < rawBB2[2]:
        return False
    else:
        return True       

# Invert Vector Function
def reverseV2( movementVector ):
    iV = FlVector2( 0.0, 0.0 )
    Vx = movementVector.x
    Vy = movementVector.y
    iV.x = -1.0*( Vx )
    iV.y = -1.0*( Vy )
    return iV   

# Object Manupliation Functions
def moveObj( Object, MoveX, MoveY, MoveZ ):
    obj = Object
    x = MoveX
    y = 0.0
    z = MoveZ
    pm.move( obj, [ x, y, z ], r=True, wd=True )

class Enemy():
    def __init__(self, minSpawn, maxSpawn):
        colorRGBV = [1,1,0]
        rMax = maxSpawn
        rMin = minSpawn
        spawnMin = rMin + .01
        spawnMax = rMax - .01
        locX = random.uniform(spawnMin, spawnMax)
        locY = random.uniform(spawnMin, spawnMax)
        moveVectorX = random.uniform(-3.0,3.0)
        moveVectorY = random.uniform(-3.0,3.0)
        mayaObj = pm.polyCube( name="Enemy", w=1, h=1, d=1, cuv=0, ax=(0,1,0), sx=1, sy=1, sz=1 )
        moveObj(mayaObj[0], locX, 0, locY)
        pm.selectType( pv=True )
        pm.polySelectConstraint( type=0x0001, mode=3 )
        pm.select()
        pVs = pm.ls( selection=True, fl=True )
        pm.select( cl=True )
        for v in range(len(pVs)):
            pm.polyColorPerVertex( pVs[v], colorRGB=colorRGBV, alpha=1.0, cdo=True, notUndoable=True )
        
        def update( areaMinMaxX, areaMinMaxY ):
            aMinMaxX = areaMinMaxX
            aMinMaxY = areaMinMaxY
            testBoundry = pm.xform( q=True, translation=True, ws=True )
            if testBoundry[0] > aMinMaxX or testBoundry[0] < -(aMinMaxX) or testBoundry[2] > aMinMaxY or testBoundry[2] < -(aMinMaxY):
                moveVectorX = -(moveVectorX)
                moveVectorY - -(moveVectorY)
            moveObj( mayaObj[0], moveVectorX, 0, moveVectorY )

# Main Game Function
def run():
    
    RawMovementVector = IntVector2( 0, 0 )
    numEnemies = 15
    playSpaceMinMaxX = 50
    playSpaceMinMaxY = 50
    enemyList = []
    
    # Init SDL
    if sdl2.SDL_Init(sdl2.SDL_INIT_TIMER|sdl2.SDL_INIT_GAMECONTROLLER|sdl2.SDL_INIT_EVENTS) != 0:
        print(sdl2.SDL_GetError())
        return -1
    
    # Init Controller
    controller = sdl2.SDL_GameController()
   
    for i in range(sdl2.SDL_NumJoysticks()):
        if sdl2.SDL_IsGameController(i):
            controller = sdl2.SDL_GameControllerOpen(i)
    
    # Create SDL Window    
    ctrlWindow = sdl2.SDL_CreateWindow( b"Control", sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED, 200, 150, sdl2.SDL_WINDOW_INPUT_FOCUS )#|sdl2.SDL_WINDOW_HIDDEN )
    if not ctrlWindow:
        print(sdl2.GetError())
        return -1
    
    # Init Player
    player = pm.polyCube( name="Player", w=1, h=1, d=1, cuv=0, ax=(0,1,0), sx=1, sy=1, sz=1 )
    if player is None:
        print "ERROR! Player not created!"
        return -1
    else:
        pm.selectType( pv=True )
        pm.polySelectConstraint( type=0x0001, mode=3 )
        pm.select()
        pVs = pm.ls( selection=True, fl=True )
        pm.select( cl=True )
        for v in range(len(pVs)):
            pm.polyColorPerVertex( pVs[v], colorRGB=(1.0,0.0,0.0), alpha=1.0, cdo=True, notUndoable=True )
    pSpeed = 10.0
    
    for i in range(numEnemies):
        thisE = Enemy(-(playSpaceMinMaxX), playSpaceMinMaxX)
        enemyList.append(thisE)
    print enemyList
    
    # Start Ticks
    lastTime = 0
    cTime = sdl2.SDL_GetTicks()
    
    # Start Game Loop
    running = True    
    while running:
        #Calculate Delta Time
        lastTime = cTime
        cTime = sdl2.SDL_GetTicks()
        dTime = cTime - lastTime
        if dTime > 16:
            dTime = 16
        
        deltaM = float(dTime)/float(1000)
              
        ButtonPressed = False
        # Process Input
        evnt = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(ctypes.byref(evnt)) != 0:
            if evnt.type == sdl2.SDL_QUIT:
                running = False
                break
            elif evnt.type == sdl2.SDL_CONTROLLERAXISMOTION:
                if evnt.caxis.axis == sdl2.SDL_CONTROLLER_AXIS_LEFTX:
                    RawMovementVector.x = evnt.caxis.value
                    break
                elif evnt.caxis.axis == sdl2.SDL_CONTROLLER_AXIS_LEFTY:
                    RawMovementVector.y = evnt.caxis.value
                    break
            elif evnt.type == sdl2.SDL_CONTROLLERBUTTONDOWN:
                if evnt.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_A:
                    ButtonPressed = True
                    break
            elif evnt.type == sdl2.SDL_CONTROLLERBUTTONUP:
                if evnt.cbutton.button == sdl2.SDL_CONTROLLER_BUTTON_A:
                    ButtonPressed = False
                    break
            elif evnt.type == sdl2.SDL_KEYDOWN:
                if evnt.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    sdl2.SDL_DestroyWindow(ctrlWindow)
                    sdl2.SDL_Quit()
                    break
                        
        #print RawMovementVector.x, RawMovementVector.y, ButtonPressed
        # Remap Raw Movement to -1 to 1 in float
        Movement = RemapMovement( RawMovementVector.x, RawMovementVector.y )
        #print Movement.x, Movement.y
        pMoveX = Movement.x * (deltaM*pSpeed)
        pMoveY = Movement.y * (deltaM*pSpeed)
        moveObj( player[0], pMoveX, 0.0, pMoveY)
        for i in range(len(enemyList))
            enemylist[i].update( playSpaceMinMaxX, playSpaceMinMaxY )
        pm.refresh( cv=True )
             
            
    sdl2.SDL_DestroyWindow(ctrlWindow)
    sdl2.SDL_Quit()
    return 0
