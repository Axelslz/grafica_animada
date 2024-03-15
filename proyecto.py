import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from moviepy.editor import concatenate_videoclips, VideoFileClip
import os

video_filenames = []  # Declara video_filenames como variable global

# Funciones matemáticas
def sin_function(x):
    return np.sin(x)

def cos_function(x):
    return np.cos(x)

def exp_function(x):
    return np.exp(x)

def log_function(x):
    return np.log(x)

def tan_function(x):
    return np.tan(x)

# Diccionario de funciones
functions_dict = {
    "Sin": sin_function,
    "Cos": cos_function,
    "Exp": exp_function,
    "Log": log_function,
    "Tan": tan_function
}

def animar_funcion(func, lower_limit, upper_limit, filename):
    fig, ax = plt.subplots()
    x = np.linspace(lower_limit, upper_limit, 300)
    y = func(x)
    line, = ax.plot(x, y, 'b-')

    def update(frame):
        line.set_ydata(func(x + frame / 10.0))  # Actualiza los datos de la función
        return line,

    ani = FuncAnimation(fig, update, frames=100, interval=50, blit=True)

    # Guardar la animación como video
    ani.save(filename, writer='ffmpeg', fps=60, codec='libx264')
    plt.close(fig)

def combine_videos(video_filenames, output_filename):
    clips = [VideoFileClip(filename) for filename in video_filenames]
    combined_clip = concatenate_videoclips(clips, method="compose")
    combined_clip.write_videofile(output_filename)

def on_submit():
    global video_filenames  # Declara video_filenames como global

    selected_functions = [function_listbox.get(idx) for idx in function_listbox.curselection()]
    lower_limit = float(lower_limit_entry.get())
    upper_limit = float(upper_limit_entry.get())

    video_filenames = []  # Vacía video_filenames antes de volver a llenarlo
    for func_name in selected_functions:
        video_filename = f"{func_name}_animation.mp4"
        func = functions_dict[func_name]
        animar_funcion(func, lower_limit, upper_limit, video_filename)
        video_filenames.append(video_filename)

    if len(video_filenames) > 1:
        combine_videos(video_filenames, "combined_video.mp4")
        print("Video combinado creado.")
    else:
        print("Videos individuales creados.")

# Interfaz gráfica
root = tk.Tk()
root.title("Graficador de Funciones")

# Contenedor principal
main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10, fill='x', expand=True)

# Selector de funciones
function_label = ttk.Label(main_frame, text="Seleccione una función:")
function_label.pack(fill='x', expand=True)
function_listbox = tk.Listbox(main_frame, selectmode='multiple', exportselection=0)
for function in functions_dict:
    function_listbox.insert(tk.END, function)
function_listbox.pack(fill='x', expand=True)

# Entradas para los límites de x
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

# Botones
buttons_frame = ttk.Frame(main_frame)
buttons_frame.pack(fill='x', expand=True)

submit_button = ttk.Button(buttons_frame, text="Graficar y guardar frames", command=on_submit)
submit_button.pack(side='left', fill='x', expand=True, padx=(0, 10))

combine_button = ttk.Button(buttons_frame, text="Combinar videos", command=lambda: combine_videos(video_filenames, "combined_video.mp4"))
combine_button.pack(side='left', fill='x', expand=True)

root.mainloop()
