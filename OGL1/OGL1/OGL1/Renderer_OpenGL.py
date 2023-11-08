import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pygame
from pygame.locals import *
from gl import Renderer
from model import Model
from shaders import *

width = 1000
height = 1000

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.OPENGL | pygame.DOUBLEBUF)
clock = pygame.time.Clock()

rend = Renderer(screen)

# Inicialmente, establecemos el shader "rainbow" al inicio
rend.setShader(vertexShader=rainbow_vertex_shader, fragmentShader=rainbow_fragment_shader)

model = Model("modelos/cala.obj")
model.loadTexture("texturas/ola.bmp")
model.position.z = -5.5
model.scale = glm.vec3(2, 2, 2)
model.rotation.x = 45

rend.scene.append(model)

isRunning = True

current_shader = 1  # 1 for rainbow, 2 for grid, 3 for waves

while isRunning:
    deltaTime = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False

            # Cambia el shader al presionar teclas 1, 2 o 3
            if event.key == pygame.K_1:
                if current_shader != 1:
                    rend.setShader(vertexShader=rainbow_vertex_shader, fragmentShader=rainbow_fragment_shader)
                    current_shader = 1
            elif event.key == pygame.K_2:
                if current_shader != 2:
                    rend.setShader(vertexShader=grid_vertex_shader, fragmentShader=grid_fragment_shader)
                    current_shader = 2
            elif event.key == pygame.K_3:
                if current_shader != 3:
                    rend.setShader(vertexShader=waves_vertex_shader, fragmentShader=waves_fragment_shader)
                    current_shader = 3

    if keys[K_d]:
        rend.camPosition.x -= 5 * deltaTime
    if keys[K_a]:
        rend.camPosition.x += 5 * deltaTime
    if keys[K_w]:
        rend.camPosition.y -= 5 * deltaTime
    if keys[K_s]:
        rend.camPosition.y += 5 * deltaTime
    if keys[K_q]:
        rend.camPosition.z -= 5 * deltaTime
    if keys[K_e]:
        rend.camPosition.z += 5 * deltaTime

    if rend.activeShader == waves_vertex_shader:
        glUniform1f(glGetUniformLocation(rend.activeShader, "time"), rend.elapsedTime)

    rend.elapsedTime += deltaTime
    rend.render()
    pygame.display.flip()

pygame.quit()
