# MinMax Algorithm - Lines and Boxes (Timbiriche)

## Descripción del Problema

**Dot and Boxes** es un juego de mesa en el que dos jugadores se turnan para dibujar líneas entre puntos adyacentes en una cuadrícula. El objetivo es completar más cuadros que el oponente. Cuando un jugador completa un cuadro, recibe un punto y toma otro turno.

## Tablero Inicial

El tablero inicial de Dot and Boxes es una cuadrícula de puntos. Aquí se muestra un ejemplo de una cuadrícula de 2x2:

```
•---•---•
|       |
|       |
•---•---•
|       |
|       |
•---•---•
```

## Requisitos del Proyecto

### 1. Implementación del Algoritmo Minimax
- Implementar el algoritmo Minimax
- Diseñar una función de evaluación heurística que estime la ventaja de un jugador en cualquier estado del juego

### 2. Representación del Tablero y Movimientos
- Diseñar una estructura para representar el estado del tablero, incluyendo líneas dibujadas y cuadros completados
- Implementar una función que genere los posibles movimientos legales desde un estado dado
- Implementar una función que aplique un movimiento y genere un nuevo estado del tablero

### 3. Función Objetivo
- Definir claramente el estado objetivo (fin del juego con todos los cuadros completados)
- Implementar una función que verifique si se ha alcanzado el estado objetivo

### 4. Salida y Resultados
- Mostrar el camino desde el estado inicial hasta el estado objetivo, incluyendo los movimientos realizados
- Mostrar el número de movimientos realizados y el tiempo de ejecución del algoritmo

---