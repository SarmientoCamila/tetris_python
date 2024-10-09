import pygame
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la ventana y del grid
win_width = 300
win_height = 600
grid_width = 10
grid_height = 20
grid_size = 30
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Tetris")

# Colores
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)]

# Formas
shapes = [
    [[1, 1, 1, 1]],  # Línea larga
    [[1, 1], [1, 1]],  # Cuadrado
    [[1, 1, 0], [0, 1, 1]],  # forma Z
    [[0, 1, 1], [1, 1, 0]],  # forma S
    [[1, 1, 1], [0, 1, 0]],  # forma T
    [[1, 1, 1], [1, 0, 0]],  # forma L
    [[1, 1, 1], [0, 0, 1]]  # forma J o espejo L
]

# Posición inicial de la forma
current_shape = random.choice(shapes)
current_x = grid_width // 2 - len(current_shape[0]) // 2
current_y = 0

# Grid vacío
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

# Función para dibujar el grid
def draw_grid():
    for y in range(grid_height):
        for x in range(grid_width):
            rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
            pygame.draw.rect(win, colors[grid[y][x]], rect, 0)
            pygame.draw.rect(win, (255, 255, 255), rect, 1)

# Función para dibujar la forma
def draw_shape(shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect((offset_x + x) * grid_size, (offset_y + y) * grid_size, grid_size, grid_size)
                pygame.draw.rect(win, (0, 255, 0), rect, 0)

# Comprobar la colisión 
def check_collision(shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if (
                    offset_x + x < 0 or
                    offset_x + x >= grid_width or
                    offset_y + y >= grid_height or
                    grid[offset_y + y][offset_x + x]
                ):
                    return True
    return False

# Añadir forma al grid
def merge_shape_to_grid(shape, offset_x, offset_y):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[offset_y + y][offset_x + x] = 1

# Eliminar las líneas completas 
def clear_lines():
    lines_cleared = 0
    for y in range(grid_height):
        if all(grid[y]):
            del grid[y]  # Elimina la fila completa
            grid.insert(0, [0 for _ in range(grid_width)])  # Inserta una fila vacía en la parte superior
            lines_cleared += 1
    return lines_cleared

# Bucle principal del juego
clock = pygame.time.Clock()
running = True
while running:
    win.fill((0, 0, 0))
    draw_grid()
    draw_shape(current_shape, current_x, current_y)

    # Mover la pieza hacia abajo
    current_y += 1
    if check_collision(current_shape, current_x, current_y):
        current_y -= 1
        merge_shape_to_grid(current_shape, current_x, current_y)
        clear_lines()  # Elimina líneas completas después de fusionar la pieza con el grid
        current_shape = random.choice(shapes)
        current_x = grid_width // 2 - len(current_shape[0]) // 2
        current_y = 0

        # Verificar si se perdió
        if check_collision(current_shape, current_x, current_y):
            print("¡Perdiste!")
            running = False

    # Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_x -= 1
                if check_collision(current_shape, current_x, current_y):
                    current_x += 1
            if event.key == pygame.K_RIGHT:
                current_x += 1
                if check_collision(current_shape, current_x, current_y):
                    current_x -= 1
            if event.key == pygame.K_DOWN:
                current_y += 1
                if check_collision(current_shape, current_x, current_y):
                    current_y -= 1
            if event.key == pygame.K_UP:
                # Rotar la forma
                rotated_shape = list(zip(*current_shape[::-1]))
                
                # Comprobar colisión tras rotar
                if not check_collision(rotated_shape, current_x, current_y):
                    current_shape = rotated_shape
                else:
                    # Intentar ajustar hacia la izquierda o derecha si hay colisión en los bordes
                    if current_x + len(rotated_shape[0]) > grid_width:  # Si sale por la derecha
                        current_x = grid_width - len(rotated_shape[0])
                    elif current_x < 0:  # Si sale por la izquierda
                        current_x = 0

    # Actualizar pantalla y controlar velocidad
    pygame.display.flip()
    clock.tick(2)

pygame.quit()
