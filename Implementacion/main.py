from controlador import ControladorPID
from algoritmo_genetico import AlgoritmoGenetico

if __name__ == "__main__":
    controlador = ControladorPID()

    rangos = [(0, 100), (0, 10), (0, 50)]
    algoritmo = AlgoritmoGenetico(controlador, n_individuos=20, generaciones=50, rangos=rangos)

    print("Iniciando optimización PID con Algoritmos Genéticos...")
    mejor_individuo = algoritmo.optimizar()

    print("\nOptimización completada.")
    print(f"Mejores parámetros encontrados: Kp = {mejor_individuo[0]:.2f}, Ki = {mejor_individuo[1]:.2f}, Kd = {mejor_individuo[2]:.2f}")
