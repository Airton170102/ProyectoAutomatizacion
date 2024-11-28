import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import control as ctrl
from tkinter import Tk, Label, Scale, HORIZONTAL, Frame, Button


class ControladorPID:
    """Clase que encapsula la lógica de simulación del sistema con diferentes controladores."""
    
    def __init__(self):
        # Valores por defecto
        self.M = 1.0  # Masa del carro
        self.m = 0.1  # Masa del péndulo
        self.l = 1.0  # Longitud del péndulo
        self.g = 9.81  # Gravedad
        self.Kp = 50  # Ganancia proporcional
        self.Ki = 1   # Ganancia integral
        self.Kd = 10  # Ganancia derivativa

    def actualizar_parametros(self, M, m, l, g, Kp, Ki, Kd):
        """Actualiza los parámetros del sistema y las ganancias del controlador."""
        self.M = M
        self.m = m
        self.l = l
        self.g = g
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

    def generar_respuestas(self):
        pass


class InterfazGrafica:
    pass

# Crear la instancia del controlador PID
controlador = ControladorPID()

# Crear y ejecutar la interfaz gráfica
interfaz = InterfazGrafica(controlador)
interfaz.ejecutar()
