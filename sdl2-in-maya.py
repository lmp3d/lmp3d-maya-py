#import pymel.core as pm
import os
import sys
import ctypes
import sdl2
import sdl2.ext

def init():
    
    if sdl2.SDL_Init(sdl2.SDL_INIT_TIMER|sdl2.SDL_INIT_GAMECONTROLLER|sdl2.SDL_INIT_EVENTS) != 0:
        print(sdl2.SDL_GetError())
        return -1
        
    ctrlWindow = sdl2.SDL_CreateWindow( b"Control", sdl2.SDL_WINDOWPOS_UNDEFINED, sdl2.SDL_WINDOWPOS_UNDEFINED, 200, 150, sdl2.SDL_WINDOW_INPUT_FOCUS )
    if not ctrlWindow:
        print(sdl2.SDL_GetError())
        return -1
    #sdl2.SDL_Delay(10)    
    sdl2.SDL_DestroyWindow(ctrlWindow)
    sdl2.SDL_Quit()
    return ctrlWindow
        
#ticks = sdl2.SDL_GetTicks()
#print ticks
#sdl2.SDL_WINDOW_HIDDEN

init()

sdl2.SDL_DestroyWindow(ctrlWindow)

sdl2.SDL_Quit()
