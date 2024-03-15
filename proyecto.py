import tkinter as tk
from tkinter import ttk, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from matplotlib.animation import FuncAnimation
from moviepy.editor import concatenate_videoclips, VideoFileClip

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

# Función para animar una función matemática
def animar_funcion(func, lower_limit, upper_limit, filename):
    fig, ax = plt.subplots()
    x = np.linspace(lower_limit, upper_limit, 300)
    y = func(x)
    line, = ax.plot(x, y, 'b-')

    duration = upper_limit - lower_limit
    frames = int(60 * duration)

    def update(frame):
        line.set_ydata(func(x + frame / 10.0))
        return line,

    ani = FuncAnimation(fig, update, frames=frames, interval=50, blit=True)
    ani.save(filename, writer='ffmpeg', fps=60, codec='libx264')
    plt.close(fig)

# Función para combinar videos
def combine_videos(video_filenames, output_filename):
    clips = [VideoFileClip(filename) for filename in video_filenames]
    combined_clip = concatenate_videoclips(clips, method="compose")
    combined_clip.write_videofile(output_filename)

# Función ejecutada al presionar el botón de submit
def on_submit():
    selected_indexes = list(map(int, function_listbox.curselection()))
    selected_functions = [function_listbox.get(idx) for idx in selected_indexes]
    ordered_functions = [(functions_dict[func_name], func_name) for _, func_name in sorted(zip(selected_indexes, selected_functions))]
    
    lower_limit = float(lower_limit_entry.get())
    upper_limit = float(upper_limit_entry.get())

    video_filenames = []

    for _, func_name in ordered_functions:
        video_filename = f"{func_name}_animation.mp4"
        func = functions_dict[func_name]
        animar_funcion(func, lower_limit, upper_limit, video_filename)
        video_filenames.append(video_filename)

    if len(video_filenames) > 1:
        combined_filename = "combined_video.mp4"
        combine_videos(video_filenames, combined_filename)
        print(f"Video combinado creado: {combined_filename}")
    else:
        print("Videos individuales creados.")

# Interfaz gráfica
root = tk.Tk()
root.title("Graficador de Funciones y Generador de Videos")

main_frame = ttk.Frame(root)
main_frame.pack(padx=10, pady=10, fill='x', expand=True)

# Selector de funciones con orden
function_label = ttk.Label(main_frame, text="Seleccione una función y defina un orden:")
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

# Botón para generar los videos
submit_button = ttk.Button(main_frame, text="Generar y combinar videos", command=on_submit)
submit_button.pack(fill='x', expand=True, pady=5)

root.mainloop()

