import numpy as np
import matplotlib.pyplot as plt
from control import tf, step_response, feedback

# Parámetros del sistema 
M = 0.5  # Masa del carro (kg)
m = 0.2  # Masa del péndulo (kg)
l = 1.0  # Longitud de la varilla (m)
g = 9.81  # Gravedad (m/s^2)

# Función de transferencia 

numerator = [m * l]
denominator = [M + m, 0, -m * g * l]

# Sistema sin control
pendulum = tf(numerator, denominator)


Kp = 10  # Ganancia proporcional
P_controller = Kp
controlled_p = feedback(P_controller * pendulum, 1)  # Realimentación unitaria

time = np.linspace(0, 5, 500)  # Tiempo de simulación
response_p, time_p = step_response(controlled_p, time)

# Controlador PI
Ki = 1
PI_controller = Kp + Ki / tf([1, 0], [1])  # Controlador PI
controlled_pi = feedback(PI_controller * pendulum, 1)
response_pi, time_pi = step_response(controlled_pi, time)

# Controlador PD
Kd = 1
PD_controller = Kp + Kd * tf([1, 0], [1])  # Controlador PD
controlled_pd = feedback(PD_controller * pendulum, 1)
response_pd, time_pd = step_response(controlled_pd, time)

# Controlador PID
PID_controller = Kp + Ki / tf([1, 0], [1]) + Kd * tf([1, 0], [1])  # Controlador PID
controlled_pid = feedback(PID_controller * pendulum, 1)
response_pid, time_pid = step_response(controlled_pid, time)

# Gráficos de respuesta
plt.figure(figsize=(12, 8))
plt.plot(time_p, response_p, label="Controlador P")
plt.plot(time_pi, response_pi, label="Controlador PI")
plt.plot(time_pd, response_pd, label="Controlador PD")
plt.plot(time_pid, response_pid, label="Controlador PID")
plt.title("Respuesta del sistema con diferentes controladores")
plt.xlabel("Tiempo (s)")
plt.ylabel("Salida (posición del carro o ángulo)")
plt.legend()
plt.grid()
plt.show()
