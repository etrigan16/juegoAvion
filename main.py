import pygame
import random

# Inicializa Pygame y el modulo de sonido
pygame.init()
pygame.mixer.init()

# Cargar sonidos y música
pygame.mixer.music.load('sound/2016_ Clement Panchout_ Life is full of Joy.wav')
pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen al 50%
pygame.mixer.music.play(-1)  # Reproduce en bucle
sonido_explosion = pygame.mixer.Sound('sound/Retro Explosion Short 01.wav') # Sonido de explosión

# Dimensiones de la pantalla
ANCHO_PANTALLA = 1024
ALTO_PANTALLA = 768
# Configuración de la pantalla
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Juego de Avión")

# Colores
#BLANCO = (255, 255, 255)
#NEGRO = (0, 0, 0)

# Cargar imágenes
imagen_fondo = pygame.image.load("assets/background.png")
imagen_game_over = pygame.image.load("assets/textGameOver.png")
imagen_avion = pygame.image.load("assets/planeRed1.png")
imagen_explosion = pygame.image.load("assets/tank_explosion3.png")

# Cargar imágenes de la cuenta regresiva y "Get Ready"
imagenes_numeros = [
    pygame.image.load("assets/number3.png"),
    pygame.image.load("assets/number2.png"),
    pygame.image.load("assets/number1.png")
]
imagen_texto_preparado = pygame.image.load("assets/textgetready.png")


# Escalar imágenes si es necesario
imagen_avion = pygame.transform.scale(imagen_avion, (80, 60))
imagen_explosion = pygame.transform.scale(imagen_explosion, (100, 80))
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO_PANTALLA, ALTO_PANTALLA))
imagen_game_over = pygame.transform.scale(imagen_game_over, (400, 200))

# Cargar y escalar la imagen de las vidas pequeñas
imagen_avion_pequeno = pygame.transform.scale(imagen_avion, (40, 30))

# Posición inicial del avión
avion_x = 100
avion_y = ALTO_PANTALLA // 2

#Convertir la imagen del avion a un rectangulo para la deteccion de colisiones
rectangulo_avion = imagen_avion.get_rect(topleft=(avion_x, avion_y))

# Velocidad del avión
velocidad_avion = 5
velocidad_avion_x = 10

# Lista de obstáculos
obstaculos = []
nubes = []

# Frecuencia de aparición de obstáculos
frecuencia_obstaculos = 2000  # en milisegundos
ultimo_obstaculo = pygame.time.get_ticks()

ultimo_tiempo_generacion_nube = pygame.time.get_ticks()
intervalo_proxima_generacion_nube = random.randint(0, 5000)

# Inmovilización de nubes
inmovilizado = False
tiempo_inmovilizado = 0
posicion_explosion = (0, 0)

# Inicializar variable para mostrar explosión
mostrar_explosion = False
tiempo_inicio_explosion = 0

# Inicializar variable para ignorar colisión con nubes
ignorar_colision_nube = False
tiempo_ignorar_colision_nube = 0

# Inicializar el contador de vidas
vidas = 3

# Función para generar nuevos obstáculos
def generar_obstaculo():
    x = ANCHO_PANTALLA
    ruta_imagen = random.choice([
        "assets/rockDown.png",
        "assets/rockSnowDown.png",
        "assets/rockGrass.png",
        "assets/rockGrassDown.png"])
    imagen = pygame.image.load(ruta_imagen).convert_alpha()
    imagen = pygame.transform.scale(imagen, (220, 220))
    if ruta_imagen == "assets/rockGrass.png":
        y = ALTO_PANTALLA - imagen.get_height()  # Posición en el límite inferior
    else:
        y = 0  # Posición en el límite superior
    rectangulo_obstaculo = imagen.get_rect(topleft=(x, y)) #Convertir la imagen del obstaculo a un rectangulo para la deteccion de colisiones
    return [x, y, imagen, rectangulo_obstaculo]

#Funcion generar nubes
def generar_nube():
    x = ANCHO_PANTALLA
    ruta_imagen = random.choice([
        "assets/cloud1.png",
        "assets/cloud2.png",
        "assets/cloud3.png",
        "assets/cloud4.png",
        "assets/cloud5.png",
        "assets/cloud6.png",
        "assets/cloud7.png",
        "assets/cloud8.png",
        "assets/cloud9.png"])
    imagen = pygame.image.load(ruta_imagen).convert_alpha()
    imagen = pygame.transform.scale(imagen, (100, 100))
    y = random.randint(0, ALTO_PANTALLA - imagen.get_height())
    rectangulo_nube = imagen.get_rect(topleft=(x, y))
    return [x, y, imagen, rectangulo_nube]


# Funcion Mostrar cuenta regresiva y "Get Ready"
def mostrar_cuenta_regresiva():
    for imagen_numero in imagenes_numeros:
        pantalla.blit(imagen_fondo, (0, 0))
        pantalla.blit(imagen_numero, (ANCHO_PANTALLA // 2 - imagen_numero.get_width() // 2, ALTO_PANTALLA // 2 - imagen_numero.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(1000)  # Esperar 1 segundo

    pantalla.blit(imagen_fondo, (0, 0))
    pantalla.blit(imagen_texto_preparado, (ANCHO_PANTALLA // 2 - imagen_texto_preparado.get_width() // 2, ALTO_PANTALLA // 2 - imagen_texto_preparado.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(1000)  # Esperar 1 segundo

# Función para mostrar "Game Over"
def mostrar_game_over():
    pantalla.blit(imagen_fondo, (0, 0))
    pantalla.blit(imagen_game_over, (ANCHO_PANTALLA // 2 - imagen_game_over.get_width() // 2, ALTO_PANTALLA // 2 - imagen_game_over.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Esperar 2 segundos

# Función para reiniciar el juego
def reiniciar_juego():
    global avion_x, avion_y, obstaculos, nubes, mostrar_explosion, inmovilizado, vidas
    #pygame.time.wait(2000)  # Esperar 2 segundos
    avion_x = 100
    avion_y = ALTO_PANTALLA // 2
    obstaculos = []
    nubes = []
    mostrar_explosion = False
    inmovilizado = False
    vidas -= 1
    if vidas > 0:
        mostrar_cuenta_regresiva()  # Mostrar cuenta regresiva antes de reiniciar el juego
    else:
        mostrar_game_over()  # Mostrar "Game Over" si no hay vidas restantes
    pygame.time.wait(2000)  # Esperar 2 segundos

# Bucle principal del juego
ejecutando = True
reloj = pygame.time.Clock()

# Mostrar cuenta regresiva antes de iniciar el juego
mostrar_cuenta_regresiva()

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Movimiento del avión
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP] and avion_y > 0:
        avion_y -= velocidad_avion
    if teclas[pygame.K_DOWN] and avion_y < ALTO_PANTALLA - imagen_avion.get_height():
        avion_y += velocidad_avion
    if teclas[pygame.K_RIGHT] and avion_x < ANCHO_PANTALLA - imagen_avion.get_width():
        avion_x += velocidad_avion_x
    if teclas[pygame.K_LEFT] and avion_x > 0:
        avion_x -= velocidad_avion_x



    # Generar nuevos obstáculos y nubes
    tiempo_actual = pygame.time.get_ticks()
    if tiempo_actual - ultimo_obstaculo > frecuencia_obstaculos:
        obstaculos.append(generar_obstaculo())
        ultimo_obstaculo = tiempo_actual

    # Comprobar si es momento de generar una nueva nube
    if tiempo_actual - ultimo_tiempo_generacion_nube > intervalo_proxima_generacion_nube:
        nubes.append(generar_nube())
        ultimo_tiempo_generacion_nube = tiempo_actual
        intervalo_proxima_generacion_nube = random.randint(0, 5000)

    # Mover obstáculos y nubes
    for obstaculo in obstaculos:
        obstaculo[0] -= velocidad_avion
    for nube in nubes:
        nube[0] -= velocidad_avion

    # Eliminar obstáculos que salen de la pantalla
    obstaculos = [obstaculo for obstaculo in obstaculos if obstaculo[0] > -50]

    # Eliminar nubes que salen de la pantalla
    nubes = [nube for nube in nubes if nube[0] > -50]

    # Actualizar la posición del rectángulo del avión
    rectangulo_avion.topleft = (avion_x, avion_y)

    # Actualizar la posición de los rectángulos de los obstáculos y nubes
    for obstaculo in obstaculos:
        obstaculo[3].topleft = (obstaculo[0], obstaculo[1]) # Actualizar la posición x del rectángulo del obstáculo
    for nube in nubes:
        nube[3].topleft = (nube[0], nube[1])  # Actualizar la posición x del rectángulo de la nube


    # Detección de colisiones
    for obstaculo in obstaculos:
        if rectangulo_avion.colliderect(obstaculo[3]):  # Usar el rectángulo del obstáculo para la detección de colisiones
            mostrar_explosion = True  # Mostrar la explosión
            tiempo_inicio_explosion = pygame.time.get_ticks()
            posicion_explosion = (avion_x, avion_y)
            sonido_explosion.play() # Reproducir el sonido de explosión


    # Detectar colisión con nubes e inmovilizar avión
    for nube in nubes:
        if rectangulo_avion.colliderect(nube[3]) and not inmovilizado:
            inmovilizado = True
            tiempo_inmovilizado = pygame.time.get_ticks()
            nube_seguida = nube  # Guardar la nube que el avión está siguiendo

    # Inmovilizar avión por 2 segundos
    if inmovilizado:
        if pygame.time.get_ticks() - tiempo_inmovilizado < 2000:
            avion_x = nube_seguida[0]  # Hacer que el avión siga la posición x de la nube
            avion_y = nube_seguida[1]  # Hacer que el avión siga la posición y de la nube
        else:
            velocidad_avion = 5  # Restablecer velocidad del avión
            inmovilizado = False
            nubes.remove(nube_seguida)  # Eliminar la nube seguida
            nube_seguida = None  # Dejar de seguir la nube
            ignorar_colision_nube = True  # Ignorar colisión con nubes por 500 ms
            tiempo_ignorar_colision_nube = pygame.time.get_ticks()

    # Restablecer detección de colisión con nubes después de 500 ms
    if ignorar_colision_nube and pygame.time.get_ticks() - tiempo_ignorar_colision_nube > 2000:
        ignorar_colision_nube = False

    # Dibujar fondo
    pantalla.blit(imagen_fondo, (0, 0))

    # Dibujar avión
    pantalla.blit(imagen_avion, (avion_x, avion_y))

    # Dibujar obstáculos y nubes
    for obstaculo in obstaculos:
        pantalla.blit(obstaculo[2], (obstaculo[0], obstaculo[1]))
    for nube in nubes:
        pantalla.blit(nube[2], (nube[0], nube[1]))

    # Dibujar vidas
    for i in range(vidas):
        pantalla.blit(imagen_avion_pequeno, (ANCHO_PANTALLA - (i + 1) * 40, 10))

    # Mostrar explosión si es necesario
    if mostrar_explosion:
        pantalla.blit(imagen_explosion, posicion_explosion)
        if pygame.time.get_ticks() - tiempo_inicio_explosion > 500:  # Mostrar la explosión por 500 ms
            mostrar_explosion = False
            reiniciar_juego()  # Reiniciar el juego

    # Actualizar la pantalla
    pygame.display.flip()
    reloj.tick(30)

    # Verificar si se han agotado las vidas
    if vidas <= 0:
        ejecutando = False

# Salir de Pygame

pygame.quit()