import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import control as ctrl
from tkinter import Tk, Label, Scale, HORIZONTAL, Frame, Button


# Función para actualizar las gráficas
def actualizar_graficas():
    # Leer valores de las barras deslizantes
    M = slider_M.get()
    m = slider_m.get()
    l = slider_l.get()
    g = slider_g.get()
    Kp = slider_Kp.get()
    Ki = slider_Ki.get()
    Kd = slider_Kd.get()

    # Definición del sistema
    num = [1]
    den = [M * l, 0, -(M + m) * g]
    sys_open = ctrl.TransferFunction(num, den)

    # Controladores
    sys_p = Kp
    sys_pi = Kp + Ki / ctrl.TransferFunction([1], [1, 0])
    sys_pd = Kp + Kd * ctrl.TransferFunction([1, 0], [1])
    sys_pid = Kp + Ki / ctrl.TransferFunction([1], [1, 0]) + Kd * ctrl.TransferFunction([1, 0], [1])

    # Sistemas cerrados con retroalimentación
    sys_p_closed = ctrl.feedback(sys_p * sys_open)
    sys_pi_closed = ctrl.feedback(sys_pi * sys_open)
    sys_pd_closed = ctrl.feedback(sys_pd * sys_open)
    sys_pid_closed = ctrl.feedback(sys_pid * sys_open)

    # Tiempo de simulación
    t = np.linspace(0, 10, 1000)

    # Respuestas al escalón para cada controlador
    _, y_p = ctrl.step_response(sys_p_closed, t)
    _, y_pi = ctrl.step_response(sys_pi_closed, t)
    _, y_pd = ctrl.step_response(sys_pd_closed, t)
    _, y_pid = ctrl.step_response(sys_pid_closed, t)

    # Actualizar cada gráfica
    for ax, y, title in zip(axes, [y_p, y_pi, y_pd, y_pid], ["P", "PI", "PD", "PID"]):
        ax.clear()
        ax.plot(t, y, linewidth=2)
        ax.set_title(f"Controlador {title}")
        ax.set_xlabel("Tiempo [s]")
        ax.set_ylabel("Ángulo del péndulo (θ)")
        ax.grid(True)
    canvas.draw()


# Crear la ventana principal
ventana = Tk()
ventana.title("Simulación de Controladores PID")

# Crear un marco para las barras deslizantes
frame_sliders = Frame(ventana)
frame_sliders.pack(side="left", fill="y", padx=10, pady=10)

# Crear un marco para las gráficas
frame_graficas = Frame(ventana)
frame_graficas.pack(side="right", fill="both", expand=True)

# Crear el área de gráficos
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.flatten()  # Convertir las gráficas en un array para iterar más fácilmente
canvas = FigureCanvasTkAgg(fig, master=frame_graficas)
canvas.get_tk_widget().pack(fill="both", expand=True)

# Crear las barras deslizantes
slider_M = Scale(frame_sliders, from_=0.5, to=5, resolution=0.1, label="Masa del carro (M)", orient=HORIZONTAL, command=lambda _: actualizar_graficas())
slider_M.set(1.0)
slider_M.pack(fill="x", pady=5)

slider_m = Scale(frame_sliders, from_=0.05, to=1, resolution=0.01, label="Masa del péndulo (m)", orient=HORIZONTAL, command=lambda _: actualizar_graficas())
slider_m.set(0.1)
slider_m.pack(fill="x", pady=5)

slider_l = Scale(frame_sliders, from_=0.5, to=5, resolution=0.1, label="Longitud del péndulo (l)", orient=HORIZONTAL, command=lambda _: actualizar_graficas())
slider_l.set(1.0)
slider_l.pack(fill="x", pady=5)

slider_g = Scale(frame_sliders, from_=9.0, to=10, resolution=0.01, label="Gravedad (g)", orient=HORIZONTAL, command=lambda _: actualizar_graficas())
slider_g.set(9.81)
slider_g.pack(fill="x", pady=5)

slider_Kp = Scale(frame_sliders, from_=0, to=100, resolution=1, label="Ganancia proporcional (Kp)", orient=HORIZONTAL, command=lambda _: actualizar_graficas())
slider_Kp.set(50)
slider_Kp.pack(fill="x", pady=5)

slider_Ki = Scale(frame_sliders, from_=0, to=10, resolution=0.1, label="Ganancia integral (Ki)", orient=HORIZONTAL, command=lambda _: actualizar_graficas())
slider_Ki.set(1)
slider_Ki.pack(fill="x", pady=5)

slider_Kd = Scale(frame_sliders, from_=0, to=50, resolution=1, label="Ganancia derivativa (Kd)", orient=HORIZONTAL, command=lambda _: actualizar_graficas())
slider_Kd.set(10)
slider_Kd.pack(fill="x", pady=5)

# Botón para inicializar las gráficas
Button(frame_sliders, text="Actualizar Gráficas", command=actualizar_graficas).pack(pady=10)

# Inicializar las gráficas
actualizar_graficas()

# Ejecutar la ventana
ventana.mainloop()