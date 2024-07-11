import numpy as np
import heapq

# Paso 1 Creamos las clases principales Mapa, BuscarCamino, InterfazUsuario
class Mapa:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.mapa = np.zeros((filas, columnas), dtype=int)

    def agregar_obstaculo(self, x, y):
        self.mapa[x, y] = 1

    def eliminar_obstaculo(self, x, y):
        self.mapa[x, y] = 0

    def agregar_punto_partida(self, x, y):
        self.mapa[x, y] = 2

    def agregar_destino(self, x, y):
        self.mapa[x, y] = 3

    def obtener_vecinos(self, pos_actual):
        vecinos = []
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            x, y = pos_actual[0] + dx, pos_actual[1] + dy
            if 0 <= x < self.filas and 0 <= y < self.columnas and self.mapa[x,y] != 1:
                vecinos.append((x,y))
        return vecinos

    def agregar_simbolos(self):
        simbolos = {
            0: '\u25A1', 1: '\u25A0', 2: 'p', 3: 'D', 4: '\u25CF'
        }
        return np.array([[simbolos.get(celda, str(celda)) for celda in fila] for fila in self.mapa])

    def imprimir(self):
        mapa_convertido = self.agregar_simbolos()
        for fila in mapa_convertido:
            print(' '.join(fila))

class BuscadorCamino:

    # Paso 3 decoramos los métodos de forma estática (@staticmethod) porque no necesitan acceder a ningún estado de instancia.
    @staticmethod
    def obtener_distancia(pos_a, pos_b):
        return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])

    @staticmethod
    def encontrar_camino(mapa, punt_partida, destino):
        puntaje_g = {punt_partida: 0}
        puntaje_f = {punt_partida: BuscadorCamino.obtener_distancia(punt_partida, destino)}
        list_abierta = [(0, punt_partida)]
        vino_desde = {}

        while list_abierta:
            punt_actual_f, pos_actual = heapq.heappop(list_abierta)

            if pos_actual == destino:
                camino = []
                while pos_actual in vino_desde:
                    camino.append(pos_actual)
                    pos_actual = vino_desde[pos_actual]
                camino.append(punt_partida)
                return camino[::-1]

            for vecino in mapa.obtener_vecinos(pos_actual):
                punt_tentativo_g = puntaje_g[pos_actual] + 1

                if vecino not in puntaje_g or punt_tentativo_g < puntaje_g[vecino]:
                    vino_desde[vecino] = pos_actual
                    puntaje_g[vecino] = punt_tentativo_g
                    puntaje_f[vecino] = puntaje_g[vecino] + BuscadorCamino.obtener_distancia(vecino, destino)
                    heapq.heappush(list_abierta, (puntaje_f[vecino], vecino))

        return None

class InterfazUsuario:
    @staticmethod
    def obtener_dimensiones():
        while True:
            try:
                print("Ingrese las dimensiones del mapa: MINIMO 5X5 | MAXIMO 30X30")
                filas = int(input("Numero de Filas: "))
                columnas = int(input("Numero de Columnas: "))
                if 5 <= filas <= 30 and 5 <= columnas <= 30:
                    return filas, columnas
                print("\nError: supera el MINIMO o MAXIMO establecido. Inténtelo nuevamente.")
            except ValueError:
                print("\nError: Ambos valores deben ser números enteros. Inténtelo nuevamente.")

    @staticmethod
    def obtener_obstaculos(mapa):
        while True:
            respuesta = input("¿Desea agregar un obstáculo? (s = si / n = no): ").lower()
            if respuesta != 's':
                break
            try:
                x = int(input(f"Ingrese la coordenada x (de 0 a {mapa.filas-1}): "))
                y = int(input(f"Ingrese la coordenada y (de 0 a {mapa.columnas-1}): "))
                if 0 <= x < mapa.filas and 0 <= y < mapa.columnas and mapa.mapa[x,y] != 1:
                    mapa.agregar_obstaculo(x, y)
                else:
                    print("\nCoordenadas fuera de rango o ya fue elegido como obstáculo.")
            except ValueError:
                print("\nError: Ambos valores deben ser números enteros. Inténtelo nuevamente.")

    # Paso 4 Mejoramos el código con la opción de eliminar obstáculos
    @staticmethod
    def eliminar_obstaculos(mapa):
        while True:
            respuesta = input("¿Desea eliminar un obstáculo? (s = si / n = no): ").lower()
            if respuesta != 's':
                break
            try:
                x = int(input(f"Ingrese la coordenada x (de 0 a {mapa.filas-1}): "))
                y = int(input(f"Ingrese la coordenada y (de 0 a {mapa.columnas-1}): "))
                if 0 <= x < mapa.filas and 0 <= y < mapa.columnas and mapa.mapa[x,y] != 0:
                    mapa.eliminar_obstaculo(x, y)
                else:
                    print("\nCoordenadas fuera de rango o ya fue eliminado.")
            except ValueError:
                    print("\nError: Ambos valores deben ser números enteros. Inténtelo nuevamente.")

    @staticmethod
    def obtener_punto(mapa, mensaje, valor, coordenada_actual = None):
        while True:
            try:
                print(mensaje)
                x = int(input(f"Ingrese la coordenada x (de 0 a {mapa.filas-1}): "))
                y = int(input(f"Ingrese la coordenada y (de 0 a {mapa.columnas-1}): "))
                if 0 <= x < mapa.filas and 0 <= y < mapa.columnas and mapa.mapa[x, y] != 1:
                    # Verificar que la segunda coordenada no coincida con la primera ingresada
                    if coordenada_actual and (x,y) == coordenada_actual:
                        print("\nError: El punto de partida no puede ser igual al destino.")
                        continue
                    
                    if valor == 2:
                        mapa.agregar_punto_partida(x, y)
                    else:
                        mapa.agregar_destino(x, y)
                    return x, y
                print("\nCoordenadas fuera de rango o ya fue seleccionado.")
            except ValueError:
                print("\nError: Ambos valores deben ser números enteros. Inténtelo nuevamente.")

# Paso 2 Creamos la funcion main() donde creamos nuestro objeto y llamamos a todas las clases
def main():
    filas, columnas = InterfazUsuario.obtener_dimensiones()
    mapa = Mapa(filas, columnas)
    
    print("\nMapa Creado:")
    mapa.imprimir()
    
    InterfazUsuario.obtener_obstaculos(mapa)
    
    print("\nMapa con obstáculos:")
    mapa.imprimir()
    
    InterfazUsuario.eliminar_obstaculos(mapa)
    
    print("\nMapa con obstáculos actualizado:")
    mapa.imprimir()

    x_inicio, y_inicio = InterfazUsuario.obtener_punto(mapa, "\nIngrese el punto de partida", 2)
    x_fin, y_fin = InterfazUsuario.obtener_punto(mapa, "\nIngrese el destino", 3, coordenada_actual=(x_inicio, y_inicio))
    
    print("\nMapa final:")
    mapa.imprimir()
    
    punt_partida = (x_inicio, y_inicio)
    destino = (x_fin, y_fin)
    
    camino = BuscadorCamino.encontrar_camino(mapa, punt_partida, destino)
    
    if camino:
        print(f"\nPuedes ir de {punt_partida} a {destino} tomando este camino:")
        for x, y in camino:
            if (x,y) != punt_partida and (x, y) != destino:
                mapa.mapa[x,y] = 4
        mapa.imprimir()
    else:
        print("No se encontró un camino.")

if __name__ == "__main__":
    main()