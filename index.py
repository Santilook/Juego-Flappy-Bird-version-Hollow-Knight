import pygame, sys, random

#Se crea una funcion para que se ejecute el floor picture
def draw_floor():
    scale_factor = 0.2  # Puedes ajustar este valor para el tamaño deseado
    scaled_floor = pygame.transform.scale(floor_surface, (int(floor_surface.get_width() * scale_factor), int(floor_surface.get_height() * scale_factor)))
    floor_y = screen.get_height() - scaled_floor.get_height()
    # Repetir la base para cubrir todo el ancho de la pantalla
    num_tiles = int(screen.get_width() / scaled_floor.get_width()) + 2
    for i in range(num_tiles):
        screen.blit(scaled_floor, (floor_x_pos + i * scaled_floor.get_width(), floor_y))

#Se crea la función para que aparezcan las tuberias
def create_pipe():
    #Se crean los tuberias en diferentes alturas aleatorias
    random_pipe_pos = random.choice(pipe_height)
    #Se crean las tuberias top y bottom 
    bottom_pipe = pipe_surface.get_rect(midtop = (500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (500, random_pipe_pos - 100))
    return bottom_pipe, top_pipe

#Funcion para realizar el movimiento de las tuberias
def move_pipes(pipes):
    for pipe in pipes:
        #Itera a travez de la lista y las va a ir desplazando hacia la izquierda
        pipe.centerx -= 2
    return pipes

#Se dibujan las tuberias
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            #Rota la imagen de la tuberia para que este en la parte superior
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

#Definir la funcion para la colision con el caballerito
def check_collision(pipes):
    global can_score
    # Ajustar el rect del caballerito para hacerlo más pequeño y justo
    caballerito_hitbox = caballerito_rect.inflate(-caballerito_rect.width * 0.8, -caballerito_rect.height * 0.8)
    for pipe in pipes:
        pipe_hitbox = pipe.inflate(-pipe.width * 0.1, -pipe.height * 0.1)
        if caballerito_hitbox.colliderect(pipe_hitbox):
            death_sound.play()
            can_score = True
            return False
    if caballerito_rect.top <= -100 or caballerito_rect.bottom >= 560:
        can_score = True
        return False
    return True

# --- SCORE AL PASAR TUBERIA ---
scored_pipes = [] 

def pipe_score_check():
    global score, can_score, scored_pipes
    for pipe in pipe_list:
        if pipe.bottom >= 512: 
            pipe_id = id(pipe)
            if pipe.centerx < caballerito_rect.left and pipe_id not in scored_pipes:
                score += 1
                score_sound.play()
                scored_pipes.append(pipe_id)
    # Limpiar pipes que ya salieron de pantalla
    scored_pipes = [pid for pid in scored_pipes if any(id(p) == pid and p.right > 0 for p in pipe_list)]

#Crear la funcion para rotar/transicionar la imagen del caballerito
def rotate_caballerito(caballerito):
    new_caballerito = pygame.transform.rotozoom(caballerito, -bird_movement * 3, 1)
    return new_caballerito

#Crear la secuencia y posicion del caballerito
def caballerito_animation():
    new_caballerito = caballerito_frames[caballerito_index]
    # Mantener el centro actual para evitar desfase
    new_caballerito_rect = new_caballerito.get_rect(center = caballerito_rect.center)
    return new_caballerito, new_caballerito_rect

#Crear el score para el juego
def score_display(game_state):
    if game_state == 'main_game':
        #Crear el texto la claridad y el color del score
        score_surface = game_font.render('Puntaje: '+ str(int(score)), True, (255,255,255))
        #La posicion
        score_rect = score_surface.get_rect(center = (100, 50))
        #Se agrega al juego
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Puntaje: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (100, 50))
        screen.blit(score_surface, score_rect)

        #High Score
        high_score_surface = game_font.render(f'Puntaje más alto: {int(score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (160,100))
        screen.blit(high_score_surface, high_score_rect)

#Funcion para actualizar el score 
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.init()

screen = pygame.display.set_mode((510,740))
clock = pygame.time.Clock()
#Establecer el tipo de fuente (letra y el tamaño) para el juego
game_font = pygame.font.SysFont('04B_19.ttf',40)

#Variables del juego
gravity = 0.12
bird_movement = 0
game_active = True
score = 0
high_score = 0
can_score = True

#Se importa la imagen de fondo de la app, lo convierte para ser mas facil de trabajar
bg_surface = pygame.image.load('assets/background-hollow.png').convert()


#Se carga la imagen para el piso
floor_surface = pygame.image.load('assets/base-hollow.png').convert()


#Se fija la posicion inicial para el movimiento de la imagen
floor_x_pos = 0

# Puedes cambiar estas dimensiones para el caballerito
caballerito_width = 70 
caballerito_height = 70  

# Cargar y escalar imágenes de caballerito
caballerito_downflap = pygame.transform.scale(pygame.image.load('assets/caballerito.png').convert_alpha(), (caballerito_width, caballerito_height))
caballerito_midflap = pygame.transform.scale(pygame.image.load('assets/caballerito-alas.png').convert_alpha(), (caballerito_width, caballerito_height))

#Almacena todas las imagenes en una lista para generar una secuencia de movimiento
caballerito_frames = [caballerito_downflap, caballerito_midflap]
caballerito_index = 0
#Se establece la imagen inicial
caballerito_surface = caballerito_frames[caballerito_index]
#Fijar la posicion del caballerito
caballerito_rect = caballerito_surface.get_rect(center = (100,266))

#Se establece el evento para el cambio de imagen y su secuencia
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#Cambiar dimensiones para los pipes
pipe_width = 120 
pipe_height = 400  

# Cargar y escalar la imagen de las tuberías
pipe_surface = pygame.transform.scale(pygame.image.load('assets/pipe-hollow.png'), (pipe_width, pipe_height))
#Se crea una lista para almacenar las tuberias
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 380, 350, 400, 300]

#imagen game over
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
# Escalar el mensaje a un tamaño más pequeño
message_scale = 0.3  # Ajusta este valor para el tamaño deseado
scaled_message = pygame.transform.scale(game_over_surface, (int(game_over_surface.get_width() * message_scale), int(game_over_surface.get_height() * message_scale)))
game_over_rect = scaled_message.get_rect(center = (250,326))

#Se agregan los sonidos del juego
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

# Control de volumen global
VOLUMEN_JUEGO = 0.3  # Cambia este valor entre 0.0 (mute) y 1.0 (máximo)

# Establecer el volumen de todos los sonidos
flap_sound.set_volume(VOLUMEN_JUEGO)
death_sound.set_volume(VOLUMEN_JUEGO)
score_sound.set_volume(VOLUMEN_JUEGO)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            #Se realiza la funcionalidad de salto para la tecla space
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 3
                flap_sound.play()
            #Se establece la funcionalidad para reactivar el juego
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
                #Se reinicia la tuberia y se centra el caballerito
                pipe_list.clear()
                caballerito_rect.center = (100,266)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            #Cuando surja el evento se crea una nueva tuberia y se almacena en la lista
            pipe_list.extend(create_pipe())
        
        #Se establece el evento para realizar la secuencia de movimiento
        if event.type == BIRDFLAP:
            if caballerito_index < len(caballerito_frames) - 1:
                caballerito_index += 1
            #Cuando llega a la ultima imagen se reiniciaria la secuencia
            else:
                caballerito_index = 0
            # Actualizar el rect manteniendo el centro
            caballerito_surface, caballerito_rect = caballerito_animation()

    # Dibujar el background cubriendo toda la ventana
    screen.blit(pygame.transform.scale(bg_surface, (screen.get_width(), screen.get_height())), (0,0))
    if game_active:

        bird_movement += gravity
        #Se fija la imagen del caballerito con la funcion rotate_caballerito
        rotated_caballerito = rotate_caballerito(caballerito_surface)
        caballerito_rect.centery

        # Actualizar el rect después de moverlo
        caballerito_rect.centery += bird_movement
        caballerito_surface, caballerito_rect = caballerito_animation()
        #Se fija el caballerito
        screen.blit(rotated_caballerito, caballerito_rect)
        game_active = check_collision(pipe_list)

        #Las Tuberias
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        pipe_score_check()

        # Limpiar pipes viejos y su atributo scored
        pipe_list = [pipe for pipe in pipe_list if pipe.right > 0]

        #Aumenta el score
        score_display('main_game')
    else:
        screen.blit(scaled_message, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    
    #Se itera imagen del suelo
    floor_x_pos -= 1
    #Se establece el suelo
    draw_floor()

    #Se realiza la continuidad de la imagen con un if
    if floor_x_pos <= -pygame.transform.scale(floor_surface, (int(floor_surface.get_width() * 0.2), int(floor_surface.get_height() * 0.2))).get_width():
        floor_x_pos = 0
    
    pygame.display.update()
    clock.tick(120)