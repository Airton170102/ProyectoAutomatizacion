import numpy as np
import control as ctrl


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
        """Genera las respuestas del sistema con diferentes controladores."""
        # Definición del sistema abierto
        num = [1]
        den = [self.M * self.l, 0, -(self.M + self.m) * self.g]
        sys_open = ctrl.TransferFunction(num, den)

        # Controladores
        sys_p = self.Kp
        sys_pi = self.Kp + self.Ki / ctrl.TransferFunction([1], [1, 0])
        sys_pd = self.Kp + self.Kd * ctrl.TransferFunction([1, 0], [1])
        sys_pid = self.Kp + self.Ki / ctrl.TransferFunction([1], [1, 0]) + self.Kd * ctrl.TransferFunction([1, 0], [1])

        # Sistemas cerrados
        sys_p_closed = ctrl.feedback(sys_p * sys_open)
        sys_pi_closed = ctrl.feedback(sys_pi * sys_open)
        sys_pd_closed = ctrl.feedback(sys_pd * sys_open)
        sys_pid_closed = ctrl.feedback(sys_pid * sys_open)

        # Tiempo de simulación
        t = np.linspace(0, 10, 1000)

        # Respuestas al escalón
        _, y_p = ctrl.step_response(sys_p_closed, t)
        _, y_pi = ctrl.step_response(sys_pi_closed, t)
        _, y_pd = ctrl.step_response(sys_pd_closed, t)
        _, y_pid = ctrl.step_response(sys_pid_closed, t)

        return t, [y_p, y_pi, y_pd, y_pid]
