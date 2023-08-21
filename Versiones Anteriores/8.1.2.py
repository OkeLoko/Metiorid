import pygame
import sys
import math
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
# Resolucion de Pantalla = 1366 × 768
screen_width = 1366  # Ancho de la pantalla
screen_height = 768  # Alto de la pantalla
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Metroid 8.1.2")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Posición, ángulo y velocidad inicial de la nave
ship_x = screen_width // 2
ship_y = screen_height // 2
ship_angle = 0
ship_speed = 0
deceleration = 0.1001  # Deceleración aún más gradual
acceleration = 0.1001  # Aceleración hacia adelante
max_speed = 12  # Velocidad máxima permitida
mini_speed = -4   # Velocidad mínima permitida de reversa


# Triángulo representando la nave (punta hacia adelante)
ship_points = [(0, 10), (-8, -10), (8, -10)]

# Lista para almacenar los disparos
bullets = []

# Lista para almacenar los meteoritos
meteorites = []

# Fuente para mostrar los FPS y la velocidad
font = pygame.font.Font(None, 36)

# Puntaje Inicial
score = 0

# Fuente para mostrar el puntaje
score_font = pygame.font.Font(None,36)

# Reloj para controlar el framerate
clock = pygame.time.Clock()

def create_meteorite():
    side = random.randint(1, 4)  # Elegir un lado (1: arriba, 2: derecha, 3: abajo, 4: izquierda)
    # angle = random.uniform(0, 2*math.pi)  # Elegir un ángulo aleatorio en radianes
    angle = random.uniform(10,30)
    speed = random.uniform(1, 3)  # Elegir una velocidad aleatoria
    if side == 1:  # Arriba
        x = random.randint(0, screen_width)
        y = 0
    elif side == 2:  # Derecha
        x = screen_width
        y = random.randint(0, screen_height)
    elif side == 3:  # Abajo
        x = random.randint(0, screen_width)
        y = screen_height
    else:  # Izquierda
        x = 0
        y = random.randint(0, screen_height)
    meteorites.append((x, y, angle, speed))

# Función para mostrar los FPS y la velocidad en la pantalla
def show_info():
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, green)
    speed_text = font.render(f"Speed: {ship_speed:.2f}", True, green)
    screen.blit(fps_text, (10, 10))
    screen.blit(speed_text, (120, 10))
    score_text = score_font.render(f"Score: {score}", True, green)
    screen.blit(score_text, (280, 10))

    # Mostrar vidas restantes y puntaje en la pantalla
    lives_text = score_font.render(f"Lives: {rocket_lives}", True, green)
    screen.blit(lives_text, (480, 10))


# Vidas iniciales del cohete
rocket_lives = 3
rocket_respawn_delay = 180  # 3 segundos (60 frames por segundo)
rocket_invulnerable_duration = 120  # 2 segundos (60 frames por segundo)

# Tiempo de invulnerabilidad
rocket_invulnerable_timer = 1

# Bucle principal del juego
running = True
while running:

    x = random.randint(1,30)
    y = random.randint(1,30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Detectar si se presiona la barra espaciadora para disparar
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet_x = ship_x + math.cos(math.radians(ship_angle)) * 20
            bullet_y = ship_y - math.sin(math.radians(ship_angle)) * 20
            bullets.append((bullet_x, bullet_y, ship_angle))
    
    # Capturar las teclas presionadas
    keys = pygame.key.get_pressed()
    
    # Cambiar el ángulo de la nave según las teclas presionadas
    if keys[pygame.K_LEFT]:
        ship_angle += 2.5
    elif keys[pygame.K_RIGHT]:
        ship_angle -= 2.5
        
    # Acelerar hacia adelante con la flecha hacia arriba
    if keys[pygame.K_UP]:
        ship_speed += acceleration
        ship_speed = min(ship_speed, max_speed)  # Limitar velocidad máxima
    else:
        ship_speed *= .955  # Deceleración gradual cuando no se presiona la tecla de aceleración
    
    # Frenar y avanzar hacia atrás con la flecha hacia abajo
    if keys[pygame.K_DOWN]:
        ship_speed -= deceleration
        ship_speed = max(ship_speed, mini_speed)
    
    # Verificar si la nave está fuera del encuadre y ajustar su posición
    if ship_x < 0:
        ship_x = screen_width
    elif ship_x > screen_width:
        ship_x = 0
    if ship_y < 0:
        ship_y = screen_height
    elif ship_y > screen_height:
        ship_y = 0
    
    # Limpiar la pantalla
    screen.fill(black)
    
    # Calcular la posición de los puntos del triángulo rotado
    rotated_ship_points = [
        (x * math.cos(math.radians(ship_angle)) - y * math.sin(math.radians(ship_angle)),
         x * math.sin(math.radians(ship_angle)) + y * math.cos(math.radians(ship_angle)))
        for x, y in ship_points
    ]
    
    # Verificar si una bala impacta a un meteorito
    hit = False
    for bullet in bullets:
            bullet_x, bullet_y, _ = bullet
            distance = math.sqrt((meteorite_x - bullet_x) ** 2 + (meteorite_y - bullet_y) ** 2)
            if distance < x:
                hit = True
                break

    # Verificar si el cohete chocó con un meteorito y aún tiene vidas
    if rocket_lives > 0:
            for meteorite in meteorites:
                meteorite_x, meteorite_y, _, _ = meteorite
                distance = math.sqrt((meteorite_x - ship_x) ** 2 + (meteorite_y - ship_y) ** 2)
                if distance < x and rocket_invulnerable_timer <= 0:
                    rocket_lives -= 1
                    rocket_invulnerable_timer = rocket_respawn_delay
                    if rocket_lives > 0:
                        ship_x = screen_width // 2
                        ship_y = screen_height // 2
                    break
    
    # Actualizar el temporizador de invulnerabilidad
    if rocket_invulnerable_timer > 0:
        rocket_invulnerable_timer -= 1
   
    # Mostrar "Game Over" y puntaje si se quedan sin vidas
    if rocket_lives <= 0:
        game_over_text = score_font.render("Game Over", True, green)
        screen.blit(game_over_text, (screen_width // 2 - 60, screen_height // 2))
        final_score_text = score_font.render(f"Final Score: {score}", True, green)
        screen.blit(final_score_text, (screen_width // 2 - 70, screen_height // 2 + 40))
        # game_over_text = score_font.render("Rene Oke", True, green)
        # screen.blit(game_over_text, (screen_width // 2 - 65 , screen_height // 2 + 60))
        
    else:
        
         # Mostrar los controles en la esquina inferior derecha
        controls_text = font.render("Controls:", True, green)
        controls_up_text = font.render("Up: Accelerate", True, green)
        controls_down_text = font.render("Down: Decelerate", True, green)
        controls_left_text = font.render("Left: Turn Left", True, green)
        controls_right_text = font.render("Right: Turn Right", True, green)
        screen.blit(controls_text, (screen_width - 220, screen_height - 120))
        screen.blit(controls_up_text, (screen_width - 220, screen_height - 90))
        screen.blit(controls_down_text, (screen_width - 220, screen_height - 60))
        screen.blit(controls_left_text, (screen_width - 220, screen_height - 30))
        screen.blit(controls_right_text, (screen_width - 220, screen_height))

        # Mostrar la tecla de disparo en la esquina inferior izquierda
        shoot_text = font.render("Space: Shoot", True, green)
        screen.blit(shoot_text, (20, screen_height - 30))


        # Dibujar el triángulo hueco en la pantalla con la rotación
        pygame.draw.polygon(screen, green, [(y + ship_x, x + ship_y) for x, y in rotated_ship_points], 1)

        # Actualizar la posición de la nave
        ship_x += math.cos(math.radians(ship_angle)) * ship_speed
        ship_y -= math.sin(math.radians(ship_angle)) * ship_speed
        
        # Actualizar la posición y dibujar los disparos
        new_bullets = []
        for bullet in bullets:
            bullet_x, bullet_y, bullet_angle = bullet
            bullet_x += math.cos(math.radians(bullet_angle)) * 20  # Disminuir velocidad de las balas
            bullet_y -= math.sin(math.radians(bullet_angle)) * 20  # Disminuir velocidad de las balas
            pygame.draw.circle(screen, green, (int(bullet_x), int(bullet_y)), 3)
            if 0 <= bullet_x < screen_width and 0 <= bullet_y < screen_height:
                new_bullets.append((bullet_x, bullet_y, bullet_angle))
        bullets = new_bullets

        # Crear meteoritos aleatoriamente
        if random.random() < 0.1:
            create_meteorite()
        
        # Actualizar y dibujar meteoritos
        new_meteorites = []

        for meteorite in meteorites:
            meteorite_x, meteorite_y, angle, speed = meteorite
            
            # Calcular los cambios en x e y usando el ángulo y la velocidad
            delta_x = math.cos(angle) * speed
            delta_y = math.sin(angle) * speed
            
            # Aplicar los cambios a la posición del meteorito
            meteorite_x += delta_x
            meteorite_y += delta_y
            
            # Dibujar el meteorito
            # pygame.draw.circle(screen, white, (int(meteorite_x), int(meteorite_y)), 10, 2)
            pygame.draw.circle(screen, green, (int(meteorite_x), int(meteorite_y)),x,y)
            
            # Verificar si una bala impacta a un meteorito
            hit = False
            for bullet in bullets:
                bullet_x, bullet_y, _ = bullet
                distance = math.sqrt((meteorite_x - bullet_x) ** 2 + (meteorite_y - bullet_y) ** 2)
                if distance < x:
                    hit = True
                    if hit:
                        score += random.randint(1,10)
                        meteorite = None
                    break
            # Si no hubo impacto, agregar el meteorito a la lista de nuevos meteoritos
            if not hit:
                new_meteorites.append((meteorite_x, meteorite_y, angle, speed))
        meteorites = new_meteorites

        # Mostrar los FPS y la velocidad en la esquina superior izquierda
        show_info()
    
    # Actualizar la pantalla
    pygame.display.flip()
    
    # Limitar el framerate
    clock.tick(60)

# Salir del juego
pygame.quit()
sys.exit()

