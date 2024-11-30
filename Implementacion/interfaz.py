import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk, Label, Scale, HORIZONTAL, Frame
from controlador import ControladorPID


class InterfazGrafica:
    """Clase que encapsula la interfaz gráfica para visualizar las respuestas del sistema."""
    
    def __init__(self, controlador):
        self.controlador = controlador  # Instancia del controlador PID
        
        # Crear la ventana principal
        self.ventana = Tk()
        self.ventana.title("Simulación de Controladores PID")
        
        # Crear el marco de controles
        self.frame_sliders = Frame(self.ventana)
        self.frame_sliders.pack(side="left", fill="y", padx=10, pady=10)
        
        # Crear el marco de gráficas
        self.frame_graficas = Frame(self.ventana)
        self.frame_graficas.pack(side="right", fill="both", expand=True)
        
        # Crear el área de gráficos
        self.fig, self.axes = plt.subplots(2, 2, figsize=(10, 8))
        self.axes = self.axes.flatten()  # Convertir en array para iterar
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_graficas)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Crear las barras deslizantes
        self.crear_sliders()
        
        # Inicializar las gráficas
        self.actualizar_graficas()

    def crear_sliders(self):
        """Crea las barras deslizantes para ajustar los parámetros."""
        sliders = [
            ("Masa del carro (M)", 0.5, 5, 0.1, self.controlador.M),
            ("Masa del péndulo (m)", 0.05, 1, 0.01, self.controlador.m),
            ("Longitud del péndulo (l)", 0.5, 5, 0.1, self.controlador.l),
            ("Gravedad (g)", 9.0, 10, 0.01, self.controlador.g),
            ("Ganancia proporcional (Kp)", 0, 100, 1, self.controlador.Kp),
            ("Ganancia integral (Ki)", 0, 10, 0.1, self.controlador.Ki),
            ("Ganancia derivativa (Kd)", 0, 50, 1, self.controlador.Kd),
        ]

        self.sliders = {}
        for text, from_, to, resolution, default in sliders:
            slider = Scale(
                self.frame_sliders, label=text, from_=from_, to=to,
                resolution=resolution, orient=HORIZONTAL, command=lambda _: self.actualizar_graficas()
            )
            slider.set(default)
            slider.pack(fill="x", pady=5)
            self.sliders[text] = slider

    def actualizar_graficas(self):
        """Actualiza las gráficas basadas en los valores actuales de los sliders."""
        # Obtener valores de los sliders
        M = self.sliders["Masa del carro (M)"].get()
        m = self.sliders["Masa del péndulo (m)"].get()
        l = self.sliders["Longitud del péndulo (l)"].get()
        g = self.sliders["Gravedad (g)"].get()
        Kp = self.sliders["Ganancia proporcional (Kp)"].get()
        Ki = self.sliders["Ganancia integral (Ki)"].get()
        Kd = self.sliders["Ganancia derivativa (Kd)"].get()
        
        # Actualizar los parámetros en el controlador
        self.controlador.actualizar_parametros(M, m, l, g, Kp, Ki, Kd)
        
        # Generar las respuestas del sistema
        t, respuestas = self.controlador.generar_respuestas()
        
        # Actualizar las gráficas
        titulos = ["P", "PI", "PD", "PID"]
        for ax, y, title in zip(self.axes, respuestas, titulos):
            ax.clear()
            ax.plot(t, y, linewidth=2)
            ax.set_title(f"Controlador {title}")
            ax.set_xlabel("Tiempo [s]")
            ax.set_ylabel("Ángulo del péndulo (θ)")
            ax.grid(True)
        
        self.canvas.draw()

    def ejecutar(self):
        """Ejecuta el bucle principal de la interfaz gráfica."""
        self.ventana.mainloop()


if __name__ == "__main__":
    # Crear la instancia del controlador PID
    controlador = ControladorPID()

    # Crear y ejecutar la interfaz gráfica
    interfaz = InterfazGrafica(controlador)
    interfaz.ejecutar()