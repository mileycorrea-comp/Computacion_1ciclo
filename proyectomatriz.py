import random
import os

# Habilita los colores ANSI en la consola de Windows
os.system("")

# --- CÓDIGOS ANSI PARA COLORES ---
AZUL = '\033[34m'
ROJO = '\033[31m'
BLANCO = '\033[37m'
RESET = '\033[0m'

# --- FUNCIONES DE COLOCACIÓN DE BARCOS ---
def colocar_barco_cuadrado(tablero, tamaño):
    colocado = False
    while not colocado:
        f = random.randint(0, tamaño - 2)
        c = random.randint(0, tamaño - 2)
        
        # Validar que el espacio 2x2 esté libre
        if (tablero[f][c] == "~" and tablero[f+1][c] == "~" and 
            tablero[f][c+1] == "~" and tablero[f+1][c+1] == "~"):
            
            tablero[f][c] = "B"
            tablero[f+1][c] = "B"
            tablero[f][c+1] = "B"
            tablero[f+1][c+1] = "B"
            colocado = True
 
def colocar_barco_lineal(tablero, tamaño, longitud):
    colocado = False
    while not colocado:
        f = random.randint(0, tamaño - 1)
        c = random.randint(0, tamaño - 1)
        orientacion = random.choice(["Horizontal", "Vertical"])
        puede_colocarse = True
        
        if orientacion == "Horizontal":
            if c + longitud > tamaño:
                puede_colocarse = False
            else:
                for i in range(longitud):
                    if tablero[f][c + i] != "~":
                        puede_colocarse = False
            
            if puede_colocarse:
                for i in range(longitud):
                    tablero[f][c + i] = "B"
                colocado = True
                
        elif orientacion == "Vertical":
            if f + longitud > tamaño:
                puede_colocarse = False
            else:
                for i in range(longitud):
                    if tablero[f + i][c] != "~":
                        puede_colocarse = False
            
            if puede_colocarse:
                for i in range(longitud):
                    tablero[f + i][c] = "B"
                colocado = True

# --- FUNCIÓN DE VALIDACIÓN DE ENTRADA ---
def pedir_coordenada(texto_input, tamaño_tablero):
    while True:
        entrada = input(texto_input)
        try:
            numero = int(entrada)
            if 1 <= numero <= tamaño_tablero:
                return numero - 1
            else:
                print(f"⚠ Error: Fuera de rango. Ingresa un número entre 1 y {tamaño_tablero}.")
        except ValueError:
            print("⚠ Error: Carácter inválido. Por favor, ingresa solo números.")

# --- CONFIGURACIÓN INICIAL DEL JUEGO ---
tamaño = 7 # Modificado a 7x7
impactos_necesarios = 10  # 4 (cuadrado) + 3 + 2 + 1
impactos_logrados = 0
turnos = 0

tablero_visible = [["~" for _ in range(tamaño)] for _ in range(tamaño)]
tablero_oculto  = [["~" for _ in range(tamaño)] for _ in range(tamaño)]

# Colocamos la flota (de mayor a menor para que no se tranque)
colocar_barco_cuadrado(tablero_oculto, tamaño)
colocar_barco_lineal(tablero_oculto, tamaño, 3)
colocar_barco_lineal(tablero_oculto, tamaño, 2)
colocar_barco_lineal(tablero_oculto, tamaño, 1)

# --- BUCLE PRINCIPAL ---
print("\n¡BIENVENIDO A BATALLA NAVAL!")
print("La misión es hundir 4 barcos enemigos:")
print("1 Portaaviones (cuadrado 2x2), 1 Submarino (3), 1 Destructor (2) y 1 Bote (1).")

while impactos_logrados < impactos_necesarios:
    turnos += 1
    print("\n" + "="*30)
    print("--- RADAR COMANDANTE ---")
    print("   1 2 3 4 5 6 7") # Modificado para llegar hasta 7
    
    for i in range(tamaño):
        fila_coloreada = ""
        for celda in tablero_visible[i]:
            if celda == "~":
                fila_coloreada += AZUL + "~ " + RESET
            elif celda == "X":
                fila_coloreada += ROJO + "X " + RESET
            elif celda == "O":
                fila_coloreada += BLANCO + "O " + RESET
            else:
                fila_coloreada += celda + " "
                
        numero_fila = str(i + 1).rjust(2)
        print(f"{numero_fila} {fila_coloreada}")
    
    print(f"\nImpactos confirmados: {impactos_logrados}/{impactos_necesarios}")
    fila_disparo = pedir_coordenada("Ingresa la FILA (1-7): ", tamaño) # Texto modificado
    columna_disparo = pedir_coordenada("Ingresa la COLUMNA (1-7): ", tamaño) # Texto modificado
    
    # Procesar el disparo
    if tablero_oculto[fila_disparo][columna_disparo] == "B":
        print("\nImpacto directo.")
        tablero_visible[fila_disparo][columna_disparo] = "X"
        tablero_oculto[fila_disparo][columna_disparo] = "X"
        impactos_logrados += 1
        
    elif tablero_oculto[fila_disparo][columna_disparo] == "~":
        print("\n¡Fallo! Misil al agua.")
        tablero_visible[fila_disparo][columna_disparo] = "O"
        tablero_oculto[fila_disparo][columna_disparo] = "O"
        
    else:
        print("\nComandante, ya disparamos ahí.")

# --- FIN DEL JUEGO ---
print("\n" + "="*30)
print(f"¡VICTORIA! Hundiste toda la flota enemiga en {turnos} turnos.")