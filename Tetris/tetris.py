import pygame
import random

# Inicialización de Pygame
pygame.init()

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
CYAN = (0, 255, 255)
AMARILLO = (255, 255, 0)
MAGENTA = (255, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
NARANJA = (255, 165, 0)

# Configuración de la pantalla
ANCHO_CELDA = 30
ANCHO_TABLERO = 10
ALTO_TABLERO = 20
ANCHO_PANTALLA = ANCHO_CELDA * (ANCHO_TABLERO + 6)
ALTO_PANTALLA = ANCHO_CELDA * ALTO_TABLERO

# Configuración del juego
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Tetris AI')
reloj = pygame.time.Clock()

# Definición de las piezas
PIEZAS = [
    [[1, 1, 1, 1]], # I
    [[1, 1], [1, 1]], # O
    [[1, 1, 1], [0, 1, 0]], # T
    [[1, 1, 1], [1, 0, 0]], # L
    [[1, 1, 1], [0, 0, 1]], # J
    [[1, 1, 0], [0, 1, 1]], # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

COLORES = [CYAN, AMARILLO, MAGENTA, NARANJA, AZUL, VERDE, ROJO]

class Pieza:
    def __init__(self):
        self.forma = random.choice(PIEZAS)
        self.color = COLORES[PIEZAS.index(self.forma)]
        self.x = ANCHO_TABLERO // 2 - len(self.forma[0]) // 2
        self.y = 0

    def rotar(self):
        self.forma = list(zip(*self.forma[::-1]))
        
    def get_forma(self):
        return [list(fila) for fila in self.forma]

class IA:
    def __init__(self, tablero):
        self.tablero = tablero
        self.mejor_movimiento = None
        self.mejor_rotacion = 0
        self.siguiente_pieza = None
        self.acumulador_caida = 0.0
        
    def evaluar_posicion(self, grid, pieza, x, y):
        # Copia del grid para simulación
        temp_grid = [fila[:] for fila in grid]
        
        # Simular colocación de la pieza
        for py, fila in enumerate(pieza):
            for px, celda in enumerate(fila):
                if celda and 0 <= y + py < ALTO_TABLERO and 0 <= x + px < ANCHO_TABLERO:
                    temp_grid[y + py][x + px] = 1

        # Criterios de evaluación
        altura_total = 0
        huecos = 0
        lineas_completas = 0
        huecos_adyacentes = 0
        bumpiness = 0
        rectangularidad = 0
        contactos = 0
        alturas_columnas = []
        
        # Calcular altura total y huecos
        for x in range(ANCHO_TABLERO):
            columna = [temp_grid[y][x] for y in range(ALTO_TABLERO)]
            if 1 in columna:
                altura = ALTO_TABLERO - columna.index(1)
                altura_total += altura
                alturas_columnas.append(altura)
                
                # Contar huecos y huecos adyacentes
                hueco_anterior = False
                for y in range(columna.index(1), ALTO_TABLERO):
                    if columna[y] == 0:
                        huecos += 1
                        if hueco_anterior:
                            huecos_adyacentes += 2  # Penalizar más los huecos adyacentes
                        hueco_anterior = True
                    else:
                        hueco_anterior = False
                        
                        # Evaluar contactos con más peso en la base
                        if y < ALTO_TABLERO - 1 and columna[y + 1] == 1:
                            contactos += 2  # Más peso a contactos verticales
                        if x > 0 and temp_grid[y][x-1] == 1:
                            contactos += 1
                        if x < ANCHO_TABLERO - 1 and temp_grid[y][x+1] == 1:
                            contactos += 1
            else:
                alturas_columnas.append(0)

        # Evaluar rectangularidad y líneas
        for y in range(ALTO_TABLERO):
            fila_actual = temp_grid[y]
            bloques_en_fila = sum(1 for celda in fila_actual if celda == 1)
            
            # Premiar líneas completas y casi completas
            if bloques_en_fila == ANCHO_TABLERO:
                lineas_completas += 1
                rectangularidad += 200  # Bonus extra por línea completa
            elif bloques_en_fila >= ANCHO_TABLERO - 1:
                rectangularidad += 100  # Bonus por línea casi completa
            elif bloques_en_fila >= ANCHO_TABLERO - 2:
                rectangularidad += 50
            
            # Evaluar grupos de bloques contiguos
            bloques_contiguos = 0
            for x in range(ANCHO_TABLERO):
                if fila_actual[x] == 1:
                    bloques_contiguos += 1
                else:
                    if bloques_contiguos >= 3:
                        rectangularidad += bloques_contiguos * 20
                    bloques_contiguos = 0
            if bloques_contiguos >= 3:
                rectangularidad += bloques_contiguos * 20

        # Calcular bumpiness (diferencia de alturas)
        for i in range(len(alturas_columnas) - 1):
            diff = abs(alturas_columnas[i] - alturas_columnas[i + 1])
            bumpiness += diff * diff  # Penalización cuadrática para diferencias grandes
        
        # Penalización por altura excesiva
        altura_maxima = max(alturas_columnas) if alturas_columnas else 0
        penalizacion_altura = max(0, altura_maxima - ALTO_TABLERO/2) * 3
        
        # Bonificación por líneas completas (cuadrática para premiar múltiples líneas)
        bonus_lineas = lineas_completas * lineas_completas * 200
        
        # Pesos ajustados para mejor estrategia
        return (
            -altura_total * 0.510
            -huecos * 0.850        # Aumentado para evitar huecos
            -huecos_adyacentes * 0.500
            -bumpiness * 0.320     # Aumentado para mantener superficie más plana
            -penalizacion_altura * 0.400
            +bonus_lineas * 0.950  # Aumentado para priorizar líneas
            +rectangularidad * 0.600
            +contactos * 0.450
        )

    def encontrar_mejor_movimiento(self):
        pieza_actual = self.tablero.pieza_actual
        mejor_puntuacion = float('-inf')
        self.mejor_movimiento = None
        self.mejor_rotacion = 0
        
        # Probar todas las rotaciones posibles
        for rotacion in range(4):
            pieza_forma = pieza_actual.get_forma()
            
            # Probar todas las posiciones posibles
            for x in range(-2, ANCHO_TABLERO + 2):
                # Probar diferentes alturas
                for y_offset in range(4):
                    y = 0
                    while y < ALTO_TABLERO and not self.tablero.colision(x - pieza_actual.x, y - pieza_actual.y, pieza_forma):
                        y += 1
                    y -= 1 + y_offset
                    
                    if y >= 0:
                        puntuacion = self.evaluar_posicion(self.tablero.grid, pieza_forma, x, y)
                        
                        if puntuacion > mejor_puntuacion:
                            mejor_puntuacion = puntuacion
                            self.mejor_movimiento = x
                            self.mejor_rotacion = rotacion
            
            # Rotar para la siguiente iteración
            pieza_forma = list(zip(*pieza_forma[::-1]))
    
    def ejecutar_movimiento(self):
        if self.mejor_movimiento is None:
            self.encontrar_mejor_movimiento()
        
        # Realizar rotaciones
        for _ in range(self.mejor_rotacion):
            self.tablero.pieza_actual.rotar()
        
        # Mover horizontalmente
        dx = self.mejor_movimiento - self.tablero.pieza_actual.x
        if dx < 0:
            for _ in range(-dx):
                if not self.tablero.colision(-1):
                    self.tablero.pieza_actual.x -= 1
        else:
            for _ in range(dx):
                if not self.tablero.colision(1):
                    self.tablero.pieza_actual.x += 1
        
        # Caída más lenta y controlada
        if not self.tablero.colision(0, 1):
            # Determinar la velocidad de caída
            if self.tablero.colision(0, 2):
                velocidad = 0.2  # Muy lento cerca del fondo
            elif self.tablero.colision(0, 4):
                velocidad = 0.5  # Medio lento cuando se acerca
            else:
                velocidad = 1.0  # Velocidad normal
            
            # Acumular la caída
            self.acumulador_caida += velocidad
            
            # Si el acumulador supera 1, mover la pieza
            if self.acumulador_caida >= 1.0:
                movimientos = int(self.acumulador_caida)
                self.tablero.pieza_actual.y += movimientos
                self.acumulador_caida -= movimientos
                
                # Verificar si después del movimiento hay colisión
                if self.tablero.colision():
                    self.tablero.pieza_actual.y -= 1
                    self.tablero.fijar_pieza()
                    self.mejor_movimiento = None
                    self.acumulador_caida = 0.0
        else:
            self.tablero.fijar_pieza()
            self.mejor_movimiento = None
            self.acumulador_caida = 0.0

class Tablero:
    def __init__(self):
        self.grid = [[NEGRO for x in range(ANCHO_TABLERO)] for y in range(ALTO_TABLERO)]
        self.pieza_actual = Pieza()
        self.siguiente_pieza = Pieza()
        self.game_over = False
        self.puntuacion = 0

    def dibujar(self):
        # Dibujar el tablero
        for y in range(ALTO_TABLERO):
            for x in range(ANCHO_TABLERO):
                pygame.draw.rect(pantalla, self.grid[y][x],
                               (x * ANCHO_CELDA, y * ANCHO_CELDA, ANCHO_CELDA - 1, ANCHO_CELDA - 1))

        # Dibujar la pieza actual
        if self.pieza_actual:
            for y, fila in enumerate(self.pieza_actual.forma):
                for x, celda in enumerate(fila):
                    if celda:
                        pygame.draw.rect(pantalla, self.pieza_actual.color,
                                       ((self.pieza_actual.x + x) * ANCHO_CELDA,
                                        (self.pieza_actual.y + y) * ANCHO_CELDA,
                                        ANCHO_CELDA - 1, ANCHO_CELDA - 1))
        
        # Dibujar la siguiente pieza
        self.dibujar_siguiente_pieza()

    def dibujar_siguiente_pieza(self):
        # Posición de la siguiente pieza en la pantalla
        siguiente_x = ANCHO_TABLERO * ANCHO_CELDA + 50
        siguiente_y = 100
        
        # Dibujar marco
        pygame.draw.rect(pantalla, BLANCO, 
                        (siguiente_x - 10, siguiente_y - 10, 
                         5 * ANCHO_CELDA, 5 * ANCHO_CELDA), 1)
        
        # Dibujar texto
        fuente = pygame.font.Font(None, 36)
        texto = fuente.render("Siguiente:", True, BLANCO)
        pantalla.blit(texto, (siguiente_x, siguiente_y - 40))
        
        # Dibujar la pieza
        for y, fila in enumerate(self.siguiente_pieza.forma):
            for x, celda in enumerate(fila):
                if celda:
                    pygame.draw.rect(pantalla, self.siguiente_pieza.color,
                                   (siguiente_x + x * ANCHO_CELDA,
                                    siguiente_y + y * ANCHO_CELDA,
                                    ANCHO_CELDA - 1, ANCHO_CELDA - 1))

    def colision(self, dx=0, dy=0, forma=None):
        if forma is None:
            forma = self.pieza_actual.forma
            
        for y, fila in enumerate(forma):
            for x, celda in enumerate(fila):
                if celda:
                    nuevo_x = self.pieza_actual.x + x + dx
                    nuevo_y = self.pieza_actual.y + y + dy

                    if nuevo_x < 0 or nuevo_x >= ANCHO_TABLERO or nuevo_y >= ALTO_TABLERO:
                        return True
                    if nuevo_y >= 0 and self.grid[nuevo_y][nuevo_x] != NEGRO:
                        return True
        return False

    def fijar_pieza(self):
        for y, fila in enumerate(self.pieza_actual.forma):
            for x, celda in enumerate(fila):
                if celda:
                    self.grid[self.pieza_actual.y + y][self.pieza_actual.x + x] = self.pieza_actual.color
        
        self.eliminar_lineas()
        self.pieza_actual = self.siguiente_pieza
        self.siguiente_pieza = Pieza()
        if self.colision():
            self.game_over = True

    def eliminar_lineas(self):
        lineas = 0
        for y in range(ALTO_TABLERO - 1, -1, -1):
            if NEGRO not in self.grid[y]:
                del self.grid[y]
                self.grid.insert(0, [NEGRO for _ in range(ANCHO_TABLERO)])
                lineas += 1
        
        if lineas > 0:
            self.puntuacion += lineas * 100

def main():
    tablero = Tablero()
    ia = IA(tablero)
    tiempo_caida = 0
    velocidad_base = 400  # Velocidad base más lenta para mejor toma de decisiones
    nivel = 1
    piezas_para_nivel = 0
    
    # Función para calcular la velocidad según el nivel
    def calcular_velocidad(nivel):
        # Reducción más gradual de la velocidad
        return max(100, velocidad_base - (nivel - 1) * 25)  # Mínimo 100ms, reducción de 25ms por nivel

    velocidad_caida = calcular_velocidad(nivel)

    while not tablero.game_over:
        tiempo_actual = pygame.time.get_ticks()
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and velocidad_base < 1000:
                    velocidad_base += 100
                    velocidad_caida = calcular_velocidad(nivel)
                if evento.key == pygame.K_DOWN and velocidad_base > 200:  # Mínimo 200ms
                    velocidad_base -= 100
                    velocidad_caida = calcular_velocidad(nivel)

        if tiempo_actual - tiempo_caida > velocidad_caida:
            ia.ejecutar_movimiento()
            tiempo_caida = tiempo_actual
            piezas_para_nivel += 1
            
            # Aumentar nivel cada 25 piezas (antes era 20)
            if piezas_para_nivel >= 25:
                nivel += 1
                piezas_para_nivel = 0
                velocidad_caida = calcular_velocidad(nivel)

        pantalla.fill(NEGRO)
        tablero.dibujar()
        
        # Mostrar información
        fuente = pygame.font.Font(None, 36)
        texto_puntuacion = fuente.render(f'Puntuación: {tablero.puntuacion}', True, BLANCO)
        pantalla.blit(texto_puntuacion, (ANCHO_CELDA * (ANCHO_TABLERO + 1), 30))
        
        texto_nivel = fuente.render(f'Nivel: {nivel}', True, BLANCO)
        pantalla.blit(texto_nivel, (ANCHO_CELDA * (ANCHO_TABLERO + 1), 60))
        
        texto_velocidad = fuente.render(f'Delay: {velocidad_caida}ms', True, BLANCO)
        pantalla.blit(texto_velocidad, (ANCHO_CELDA * (ANCHO_TABLERO + 1), 90))
        
        # Mostrar piezas/nivel
        texto_piezas = fuente.render(f'Piezas: {piezas_para_nivel}/25', True, BLANCO)
        pantalla.blit(texto_piezas, (ANCHO_CELDA * (ANCHO_TABLERO + 1), 120))
        
        fuente_pequeña = pygame.font.Font(None, 24)
        texto_controles = fuente_pequeña.render('↑/↓: Ajustar velocidad', True, BLANCO)
        pantalla.blit(texto_controles, (ANCHO_CELDA * (ANCHO_TABLERO + 1), ALTO_PANTALLA - 30))
        
        pygame.display.flip()
        reloj.tick(60)

    # Game Over
    pantalla.fill(NEGRO)
    fuente = pygame.font.Font(None, 48)
    texto = fuente.render('¡GAME OVER!', True, BLANCO)
    texto_rect = texto.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2))
    pantalla.blit(texto, texto_rect)
    
    fuente_puntuacion = pygame.font.Font(None, 36)
    texto_puntuacion = fuente_puntuacion.render(f'Puntuación Final: {tablero.puntuacion}', True, BLANCO)
    texto_puntuacion_rect = texto_puntuacion.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 + 50))
    pantalla.blit(texto_puntuacion, texto_puntuacion_rect)
    
    texto_nivel_final = fuente_puntuacion.render(f'Nivel Alcanzado: {nivel}', True, BLANCO)
    texto_nivel_rect = texto_nivel_final.get_rect(center=(ANCHO_PANTALLA//2, ALTO_PANTALLA//2 + 90))
    pantalla.blit(texto_nivel_final, texto_nivel_rect)
    
    pygame.display.flip()
    pygame.time.wait(3000)

if __name__ == '__main__':
    main()
    pygame.quit() 