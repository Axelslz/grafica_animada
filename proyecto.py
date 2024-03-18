import numpy as np
import matplotlib.pyplot as plt
import os
from moviepy.editor import ImageSequenceClip, concatenate_videoclips, VideoFileClip
import tkinter as tk
from tkinter import ttk

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
    return np.log(x + phase)

# Actualización del diccionario de funciones
funciones = {
    "Sin": sin_function,
    "Cos": cos_function,
    "Tan": tan_function,
    "Exp": exp_function,
    "Log": log_function
}

# Función para guardar los frames de la animación
def guardar_frames(funcion, x_min, x_max, folder, texto):
    x = np.linspace(x_min, x_max, 400)
    num_frames = 60

    if not os.path.exists(folder):
        os.makedirs(folder)

    for i in range(num_frames):
        phase_shift = 2 * np.pi * i / num_frames
        y = funcion(x, phase_shift)
        plt.figure(figsize=(8, 6))
        plt.plot(x, y)
        plt.xlim([x_min, x_max])
        plt.ylim([-10, 10])
        plt.text(0.5, 0.9, texto, horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)
        plt.savefig(f"{folder}/{i}.png")
        plt.close()

# Función para combinar los videos
def combinar_videos():
    video_clips = []
    for funcion in funciones.keys():
        folder = f"{funcion}_frames"
        if os.path.exists(folder):
            frames = [f"{folder}/{i}.png" for i in range(60)]
            clip = ImageSequenceClip(frames, fps=10)
            clip.write_videofile(f"{funcion}.mp4")
            video_clips.append(f"{funcion}.mp4")

    if video_clips:
        final_clip = concatenate_videoclips([VideoFileClip(vc) for vc in video_clips])
        final_clip.write_videofile("video_combinado.mp4")

# Lógica principal para guardar los frames y combinar los videos
def on_submit():
    selected_function = function_listbox.get(function_listbox.curselection())
    lower_limit = float(lower_limit_entry.get())
    upper_limit = float(upper_limit_entry.get())

    funcion = funciones[selected_function]
    guardar_frames(funcion, lower_limit, upper_limit, f"{selected_function}_frames", selected_function)
    combinar_videos()

# Interfaz gráfica
root = tk.Tk()
root.title("Generador y Combinador de Videos")

main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10, fill='x', expand=True)

function_label = ttk.Label(main_frame, text="Seleccione una función:")
function_label.pack(fill='x', expand=True)
function_listbox = tk.Listbox(main_frame, selectmode='single', exportselection=0)
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

submit_button = ttk.Button(main_frame, text="Generar y combinar videos", command=on_submit)
submit_button.pack(fill='x', expand=True, pady=5)

root.mainloop()



