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

    def generar_respuestas(self, modo="manual", valores_optimos=None):
        """Genera las respuestas del sistema con diferentes controladores."""
        # Parámetros según el modo
        if modo == "manual":
            Kp, Ki, Kd = self.Kp, self.Ki, self.Kd
        elif modo == "genetico" and valores_optimos:
            Kp, Ki, Kd = valores_optimos
        else:
            raise ValueError("Modo no válido o valores óptimos no proporcionados para el modo genético.")

        # Definición del sistema abierto
        num = [1]
        den = [self.M * self.l, 0, -(self.M + self.m) * self.g]
        sys_open = ctrl.TransferFunction(num, den)

        # Controladores
        sys_p = Kp
        sys_pi = Kp + Ki / ctrl.TransferFunction([1], [1, 0])
        sys_pd = Kp + Kd * ctrl.TransferFunction([1, 0], [1])
        sys_pid = Kp + Ki / ctrl.TransferFunction([1], [1, 0]) + Kd * ctrl.TransferFunction([1, 0], [1])

        # Sistemas cerrados
        sys_p_closed = ctrl.feedback(sys_p * sys_open)
        sys_pi_closed = ctrl.feedback(sys_pi * sys_open)
        sys_pd_closed = ctrl.feedback(sys_pd * sys_open)
        sys_pid_closed = ctrl.feedback(sys_pid * sys_open)

        # Tiempo de simulación
        t = np.linspace(0, 10, 500)

        # Respuestas al escalón
        _, y_p = ctrl.step_response(sys_p_closed, t)
        _, y_pi = ctrl.step_response(sys_pi_closed, t)
        _, y_pd = ctrl.step_response(sys_pd_closed, t)
        _, y_pid = ctrl.step_response(sys_pid_closed, t)

        return t, [y_p, y_pi, y_pd, y_pid]

    def calcular_error(self, modo="manual", valores_optimos=None):
        """Calcula el error del sistema comparando referencia con la salida."""
        # Obtener la respuesta según el modo
        t, respuestas = self.generar_respuestas(modo, valores_optimos)
        y_pid = respuestas[3]  # Usar la respuesta del controlador PID

        # Referencia (suponiendo que es 0)
        referencia = np.zeros_like(t)

        # Calcular error
        error = referencia - y_pid
        return t, error

      
    def calcular_itae(self, Kp, Ki, Kd):
        """Calcula el criterio ITAE con penalización adicional para errores finales."""
        self.actualizar_parametros(self.M, self.m, self.l, self.g, Kp, Ki, Kd)
        t, respuestas = self.generar_respuestas()
        y_pid = respuestas[3]  # Obtener la respuesta PID (última de la lista)

        # Criterio ITAE
        itae = sum(t[i] * abs(y_pid[i]) for i in range(len(t)))

        # Penalización adicional para errores finales
        error_constante = abs(np.mean(y_pid[-100:]))  # Promedio de los últimos 100 valores
        penalizacion = 100 * error_constante
        return itae + penalizacion

    
