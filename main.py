import tkinter as tk



COLOR_FONDO = "#0B1720"
COLOR_PANEL = "#142630"
COLOR_BORDE = "#263B45"
COLOR_VERDE = "#65E6B1"
COLOR_TEXTO = "#F3F7F8"
COLOR_TEXTO_SUAVE = "#9FB2BB"

ventana = tk.Tk()
ventana.title("Temporizador de estudio")
ventana.geometry("460x670")
ventana.resizable(False, False)
ventana.configure(bg=COLOR_FONDO)

panel = tk.Frame(
    ventana, 
    bg=COLOR_PANEL, 
    padx=28, 
    pady=25
)

panel.pack(
    expand=True, 
    padx=20, 
    pady=20, 
    fill="both"
)

encabezado = tk.Frame(
    panel, 
    bg=COLOR_PANEL
)

encabezado.pack(
    fill="x"
)

tk.Label(
    encabezado,
    text="TEMPORIZADOR DE ESTUDIO",
    font=("Arial", 19, "bold"),
    fg=COLOR_TEXTO,
    bg=COLOR_PANEL,
).pack()

tk.Frame(
    panel, 
    bg=COLOR_BORDE, 
    height=1).pack(fill="x", pady=18)

estadoTemporizador = tk.Label(
    panel,
    text="LISTO PARA EMPEZAR",
    font=("Arial", 10, "bold"),
    fg=COLOR_VERDE,
    bg=COLOR_PANEL,
)

estadoTemporizador.pack(pady=(0, 8))

circulo = tk.Canvas(
    panel,
    width=320,
    height=320,
    bg=COLOR_PANEL,
    highlightthickness=0,
)
circulo.pack()

circulo.create_oval(
    24, 24, 296, 296,
    outline=COLOR_BORDE,
    width=14,
)

arcoProgreso = circulo.create_arc(
    24, 24, 296, 296,
    start=90,
    extent=360,
    style="arc",
    outline=COLOR_VERDE,
    width=14,
)

horas = 0
minutos = 25
segundos = 0
duracionTotal = 25 * 60
temporizadorId = None

textoTemporizador = circulo.create_text(
    160, 160,
    text=f"{horas:02d}:{minutos:02d}:{segundos:02d}",
    fill=COLOR_TEXTO,
    font=("Arial", 31, "bold"),
)

entradasTiempo = tk.Frame(panel, bg=COLOR_PANEL)
entradasTiempo.pack(pady=(0, 22))


def crearSelectorTiempo(etiqueta, valores, valorInicial):
    tarjeta = tk.Frame(
        entradasTiempo,
        bg="#1C323D",
        padx=11,
        pady=9,
    )

    tk.Label(
        tarjeta,
        text=etiqueta,
        font=("Arial", 9, "bold"),
        fg=COLOR_TEXTO_SUAVE,
        bg="#1C323D",
    ).pack(pady=(0, 5))

    selector = tk.Spinbox(
        tarjeta,
        values=valores,
        font=("Arial", 19, "bold"),
        width=3,
        justify="center",
        bg="#1C323D",
        fg=COLOR_TEXTO,
        buttonbackground="#31505A",
        readonlybackground="#1C323D",
        relief="flat",
        bd=0,
        highlightthickness=0,
        wrap=True,
    )
    selector.delete(0, tk.END)
    selector.insert(0, str(valorInicial))
    selector.configure(state="readonly")
    selector.pack()
    tarjeta.pack(side="left", padx=5)

    return selector


entradaHoras = crearSelectorTiempo("HORAS", tuple(range(100)), 0)
entradaMinutos = crearSelectorTiempo("MINUTOS", tuple(range(60)), 25)
entradaSegundos = crearSelectorTiempo("SEGUNDOS", tuple(range(60)), 0)

botones = tk.Frame(panel, bg=COLOR_PANEL)
botones.pack()


def mostrarTiempo():
    circulo.itemconfigure(
        textoTemporizador,
        text=f"{horas:02d}:{minutos:02d}:{segundos:02d}",
    )


def comenzarTemporizador():
    global horas, minutos, segundos, duracionTotal, temporizadorId

    horas = int(entradaHoras.get())
    minutos = int(entradaMinutos.get())
    segundos = int(entradaSegundos.get())
    duracionTotal = horas * 3600 + minutos * 60 + segundos

    if duracionTotal == 0:
        estadoTemporizador.configure(text="ELIGE UNA DURACIÓN")
        return

    mostrarTiempo()
    circulo.itemconfigure(arcoProgreso, extent=360)
    estadoTemporizador.configure(text="TEMPORIZADOR EN MARCHA")
    botonComenzar.configure(state="disabled")
    botonResetear.configure(state="normal")

    def actualizarTemporizador():
        global horas, minutos, segundos, temporizadorId

        if horas == 0 and minutos == 0 and segundos == 0:
            temporizadorId = None
            estadoTemporizador.configure(text="SESIÓN COMPLETADA")
            botonComenzar.configure(state="normal")
            return

        if segundos > 0:
            segundos -= 1
        elif minutos > 0:
            minutos -= 1
            segundos = 59
        else:
            horas -= 1
            minutos = 59
            segundos = 59

        tiempoRestante = horas * 3600 + minutos * 60 + segundos
        avance = tiempoRestante / duracionTotal
        circulo.itemconfigure(arcoProgreso, extent=360 * avance)
        mostrarTiempo()

        if tiempoRestante == 0:
            temporizadorId = None
            estadoTemporizador.configure(text="SESIÓN COMPLETADA")
            botonComenzar.configure(state="normal")
            return

        temporizadorId = ventana.after(1000, actualizarTemporizador)

    temporizadorId = ventana.after(1000, actualizarTemporizador)


def resetearTemporizador():
    global horas, minutos, segundos, temporizadorId

    if temporizadorId is not None:
        ventana.after_cancel(temporizadorId)
        temporizadorId = None

    horas = int(entradaHoras.get())
    minutos = int(entradaMinutos.get())
    segundos = int(entradaSegundos.get())

    mostrarTiempo()
    circulo.itemconfigure(arcoProgreso, extent=360)
    estadoTemporizador.configure(text="LISTO PARA EMPEZAR")
    botonComenzar.configure(state="normal")


botonComenzar = tk.Button(
    botones,
    text="Comenzar",
    font=("Arial", 11, "bold"),
    bg=COLOR_VERDE,
    fg="#10231F",
    activebackground="#52D39F",
    activeforeground="#10231F",
    disabledforeground="#71847E",
    width=14,
    pady=10,
    relief="flat",
    borderwidth=0,
    cursor="hand2",
    command=comenzarTemporizador,
)
botonComenzar.pack(side="left", padx=6)

botonResetear = tk.Button(
    botones,
    text="Reiniciar",
    font=("Arial", 11, "bold"),
    bg="#2B414C",
    fg=COLOR_TEXTO,
    activebackground="#385460",
    activeforeground=COLOR_TEXTO,
    width=14,
    pady=10,
    relief="flat",
    borderwidth=0,
    cursor="hand2",
    command=resetearTemporizador,
)
botonResetear.pack(side="left", padx=6)

ventana.mainloop()
