import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# Definición de los parámetros del sistema (pendulo invertido)
M = 1.0  # masa del carro (kg)
m = 0.1  # masa del péndulo (kg)
l = 1.0  # longitud del péndulo (m)
g = 9.81  # aceleración de la gravedad (m/s^2)

# Función de transferencia sin controlador
num = [1]
den = [M*l, 0, -(M+m)*g]
sys_open = ctrl.TransferFunction(num, den)

# Ganancias de los controladores PID 
Kp = 50  # Ganancia proporcional
Ki = 1   # Ganancia integral
Kd = 10  # Ganancia derivativa

# Controlador P: solo un término proporcional
sys_p = Kp

# Controlador PI: Kp + Ki/s
sys_pi = Kp + Ki / ctrl.TransferFunction([1], [1, 0])

# Controlador PD: Kp + Kd*s
sys_pd = Kp + Kd * ctrl.TransferFunction([1, 0], [1])

# Controlador PID: Kp + Ki/s + Kd*s
sys_pid = Kp + Ki / ctrl.TransferFunction([1], [1, 0]) + Kd * ctrl.TransferFunction([1, 0], [1])

# Sistemas cerrados con controladores
sys_p_closed = ctrl.feedback(sys_p * sys_open)
sys_pi_closed = ctrl.feedback(sys_pi * sys_open)
sys_pd_closed = ctrl.feedback(sys_pd * sys_open)
sys_pid_closed = ctrl.feedback(sys_pid * sys_open)

# Tiempo de simulación
t = np.linspace(0, 10, 1000)

# Respuesta al escalón para cada controlador
t, y_p = ctrl.step_response(sys_p_closed, t)
t, y_pi = ctrl.step_response(sys_pi_closed, t)
t, y_pd = ctrl.step_response(sys_pd_closed, t)
t, y_pid = ctrl.step_response(sys_pid_closed, t)

# Graficar las respuestas
plt.figure(figsize=(10, 6))

plt.plot(t, y_p, label="Controlador P", linestyle='--')
plt.plot(t, y_pi, label="Controlador PI", linestyle='-.')
plt.plot(t, y_pd, label="Controlador PD", linestyle=':')
plt.plot(t, y_pid, label="Controlador PID", linewidth=2)

plt.title("Respuestas al escalón del sistema con diferentes controladores")
plt.xlabel("Tiempo [s]")
plt.ylabel("Ángulo del péndulo (θ)")
plt.legend(loc="best")
plt.grid(True)
plt.show()
