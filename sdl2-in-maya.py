import os
import sys
import ctypes
import sdl2

def run():
    sdl2.SDL_Init(sdl2.SDL_INIT_TIMER|sdl2.SDL_INIT_GAMECONTROLLER|sdl2.SDL_INIT_EVENTS)

ticks = sdl2.SDL_GetTicks()

print ticks

run()

sdl2.SDL_Quit()
