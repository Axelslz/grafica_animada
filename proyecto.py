import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import ttk
from moviepy.editor import ImageSequenceClip, VideoFileClip, concatenate_videoclips

# Definición de las funciones trigonométricas
def sin_function(x, phase=0):
    return np.sin(x + phase)

def cos_function(x, phase=0):
    return np.cos(x + phase)

def tan_function(x, phase=0):
    return np.tan(x + phase)

def exp_function(x, phase=0):
    return np.exp(x + phase)

def log_function(x, phase=0):
    return np.log(x + phase + 1e-3) # Agregamos un pequeño número para evitar el logaritmo de cero

# Añade aquí más funciones si lo deseas
funciones = {
    "Sin": sin_function,
    "Cos": cos_function,
    "Tan": tan_function,
    "Exp": exp_function,
    "Log": log_function
}

# Función para guardar los frames de la animación
def guardar_frames(funcion, x_min, x_max, folder, texto, duration=5, fps=60):
    x = np.linspace(x_min, x_max, 400)
    num_frames = fps * duration

    if not os.path.exists(folder):
        os.makedirs(folder)

    fig, ax = plt.subplots(figsize=(8, 6))
    for i in range(num_frames):
        phase_shift = 2 * np.pi * i / num_frames
        y = funcion(x, phase_shift)
        ax.clear()
        ax.plot(x, y)
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([-2, 2])  # Ajusta el rango de Y si es necesario
        ax.text(0.05, 0.95, texto, transform=ax.transAxes, fontsize=8, color='red')
        plt.savefig(f"{folder}/{i:04d}.png")
    plt.close(fig)

# Función para generar la animación en vídeo
def generar_animacion(funcion_name, folder, output_filename, fps=60):
    frames = [f"{folder}/{i:04d}.png" for i in range(fps * 5)]
    clip = ImageSequenceClip(frames, fps=fps)
    clip.write_videofile(output_filename)

# Función que se llama cuando el usuario presiona el botón de enviar
def on_submit():
    selected_indices = function_listbox.curselection()
    if not selected_indices:
        print("Por favor, seleccione al menos una función.")
        return

    selected_functions = [function_listbox.get(i) for i in selected_indices]
    lower_limit = float(lower_limit_entry.get())
    upper_limit = float(upper_limit_entry.get())
    texto = "Axel Ricardo Salazar Ramos - 211103"

    for funcion_name in selected_functions:
        funcion = funciones[funcion_name]
        folder = f"{funcion_name}_frames"
        output_filename = f"{funcion_name}_animacion.mp4"
        guardar_frames(funcion, lower_limit, upper_limit, folder, texto)
        # Asegúrate de que generar_animacion esté creando el archivo correctamente
        generar_animacion(funcion_name, folder, output_filename)

    # Si solo hay una función, renombrar directamente
    if len(selected_functions) == 1:
        source_file = f"{selected_functions[0]}_animacion.mp4"
        os.rename(source_file, "video_final.mp4")
    else:
        # Si hay dos funciones, combinar los vídeos
        video_files = [f"{funcion}_animacion.mp4" for funcion in selected_functions]
        final_clip = concatenate_videoclips([VideoFileClip(vc) for vc in video_files], method="compose")
        final_clip.write_videofile("video_combinado.mp4")

# Interfaz gráfica
root = tk.Tk()
root.title("Generador de Animaciones de Funciones Trigonométricas y Matemáticas")

main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10, fill='x', expand=True)

function_label = ttk.Label(main_frame, text="Seleccione dos funciones:")
function_label.pack(fill='x', expand=True)
function_listbox = tk.Listbox(main_frame, selectmode='multiple', exportselection=0)
for function in funciones:
    function_listbox.insert(tk.END, function)
function_listbox.pack(fill='x', expand=True)

limites_frame = ttk.Frame(main_frame)
limites_frame.pack(fill='x', expand=True)

limite_inferior_label = ttk.Label(limites_frame, text="Límite inferior de x:")
limite_inferior_label.pack(side='left')
lower_limit_entry = ttk.Entry(limites_frame)
lower_limit_entry.pack(side='left', padx=(0, 10))

limite_superior_label = ttk.Label(limites_frame, text="Límite superior de x:")
limite_superior_label.pack(side='left')
upper_limit_entry = ttk.Entry(limites_frame)
upper_limit_entry.pack(side='left')

submit_button = ttk.Button(main_frame, text="Generar y combinar animaciones", command=on_submit)
submit_button.pack(fill='x', expand=True, pady=5)

root.mainloop()



