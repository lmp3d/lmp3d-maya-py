#import pymel.core as pm
import os
import sys
import ctypes
from ctypes import *
import collections
import sdl2
import sdl2.ext

# define structures to store 2D and 3D floating point values
class Vector3(Structure):
    _fields_=[("x", c_float), ("y", c_float), ("z", c_float)]
    
class Vector2(Structure):
    _fields_=[("x", c_int), ("y", c_int)]
    
#def normalize_axis( ):
        

def run():
    
    RawMovementVector = Vector2( 0, 0 )
    
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
    
    # Start Game Loop
    running = True    
    while running:
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
                        
        print RawMovementVector.x, RawMovementVector.y, ButtonPressed
        
        sdl2.SDL_Delay(20)
         
            
    sdl2.SDL_DestroyWindow(ctrlWindow)
    sdl2.SDL_Quit()
    return 0
        
#ticks = sdl2.SDL_GetTicks()
#print ticks
#sdl2.SDL_WINDOW_HIDDEN

run()


sdl2.SDL_Quit()
