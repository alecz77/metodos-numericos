import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import sympy as sp

def metodo_biseccion(f, a, b, max_iter, umbral):
    resultados = []
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        resultados.append((i, c, fc))
        if abs(fc) < umbral:
            break
        if f(a) * fc < 0:
            b = c
        else:
            a = c
    return resultados

def metodo_falsa_posicion(f, a, b, max_iter, umbral):
    resultados = []
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos")
    for i in range(max_iter):
        c = b - f(b)*(b - a)/(f(b) - f(a))
        fc = f(c)
        resultados.append((i, c, fc))
        if abs(fc) < umbral:
            break
        if f(a)*fc < 0:
            b = c
        else:
            a = c
    return resultados

def metodo_newton(f_str, x0, max_iter, umbral):
    x = sp.symbols('x')
    expr = sp.sympify(f_str)
    f = sp.lambdify(x, expr, 'numpy')
    df = sp.lambdify(x, sp.diff(expr, x), 'numpy')
    
    resultados = []
    for i in range(max_iter):
        fx = f(x0)
        dfx = df(x0)
        if dfx == 0:
            raise ValueError("La derivada no puede ser cero")
        x0 = x0 - fx/dfx
        resultados.append((i, x0, fx))
        if abs(fx) < umbral:
            break
    return resultados

def actualizar_campos(*args):
    metodo = combo_metodo.get()
    label_a.grid_remove()
    entry_a.grid_remove()
    label_b.grid_remove()
    entry_b.grid_remove()
    label_x0.grid_remove()
    entry_x0.grid_remove()
    
    if metodo in ["Bisección", "Falsa Posición"]:
        label_a.grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)
        entry_a.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=10)
        label_b.grid(row=2, column=0, sticky=tk.W, pady=5, padx=10)
        entry_b.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=10)
    elif metodo == "Newton-Raphson":
        label_x0.grid(row=1, column=0, sticky=tk.W, pady=5, padx=10)
        entry_x0.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=10)

def graficar():
    try:
        metodo = combo_metodo.get()
        f_str = entry_funcion.get()
        max_iter = int(entry_max_iter.get())
        umbral = float(entry_umbral.get())
        
        if metodo == "Bisección":
            a = float(entry_a.get())
            b = float(entry_b.get())
            f = lambda x: eval(f_str, {'x': x, 'math': sp, 'np': np})
            resultados = metodo_biseccion(f, a, b, max_iter, umbral)
            x_vals = np.linspace(a, b, 400)
            
        elif metodo == "Falsa Posición":
            a = float(entry_a.get())
            b = float(entry_b.get())
            f = lambda x: eval(f_str, {'x': x, 'math': sp, 'np': np})
            resultados = metodo_falsa_posicion(f, a, b, max_iter, umbral)
            x_vals = np.linspace(a, b, 400)
            
        elif metodo == "Newton-Raphson":
            x0 = float(entry_x0.get())
            resultados = metodo_newton(f_str, x0, max_iter, umbral)
            x_vals = np.linspace(resultados[-1][1]-3, resultados[-1][1]+3, 400)

        for row in tree.get_children():
            tree.delete(row)
        for i, c, fc in resultados:
            tree.insert("", "end", values=(i, f"{c:.8f}", f"{fc:.2e}"))

        fig.clear()
        ax = fig.add_subplot(111)
        ax.plot(x_vals, eval(f_str, {'x': x_vals, 'math': sp, 'np': np}))
        ax.axhline(0, color='black', linewidth=0.5)
        ax.plot(resultados[-1][1], 0, 'ro', markersize=8)
        ax.set_title(f"Método: {metodo}")
        canvas.draw()

    except Exception as e:
        print(f"Error: {e}")

# ========== INTERFAZ ORIGINAL (SIN MODIFICAR) ==========
root = tk.Tk()
root.title("Método de Bisección")
root.state('zoomed')
root.configure(bg="#E6F0FF")

frame_superior = ttk.Frame(root, padding="10")
frame_superior.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
frame_inferior = ttk.Frame(root, padding="10")
frame_inferior.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

style = ttk.Style()
style.configure("Blue.TFrame", background="#E6F0FF")

def crear_contorno_redondeado(parent, row, column, columnspan):
    canvas = tk.Canvas(parent, width=200, height=40, highlightthickness=0, bg="#E6F0FF")
    canvas.grid(row=row, column=column, columnspan=columnspan, pady=5, sticky=(tk.W, tk.E))
    canvas.create_rectangle(5, 5, 195, 35, fill="lightyellow", outline="gold", width=2)
    return canvas

crear_contorno_redondeado(frame_superior, 0, 0, 2)
crear_contorno_redondeado(frame_superior, 1, 0, 2)
crear_contorno_redondeado(frame_superior, 2, 0, 2)
crear_contorno_redondeado(frame_superior, 3, 0, 2)
crear_contorno_redondeado(frame_superior, 4, 0, 2)
crear_contorno_redondeado(frame_superior, 5, 0, 2)

ttk.Label(frame_superior, text="Function:", background="lightyellow").grid(row=0, column=0, sticky=tk.W, pady=5, padx=10)
entry_funcion = ttk.Entry(frame_superior)
entry_funcion.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=10)

label_a = ttk.Label(frame_superior, text="a:", background="lightyellow")
entry_a = ttk.Entry(frame_superior)
label_b = ttk.Label(frame_superior, text="b:", background="lightyellow")
entry_b = ttk.Entry(frame_superior)
label_x0 = ttk.Label(frame_superior, text="x0:", background="lightyellow")
entry_x0 = ttk.Entry(frame_superior)

ttk.Label(frame_superior, text="Método:", background="lightyellow").grid(row=3, column=0, sticky=tk.W, pady=5, padx=10)
combo_metodo = ttk.Combobox(frame_superior, values=["Bisección", "Falsa Posición", "Newton-Raphson"])
combo_metodo.current(0)
combo_metodo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=10)
combo_metodo.bind("<<ComboboxSelected>>", actualizar_campos)

ttk.Label(frame_superior, text="Max iter:", background="lightyellow").grid(row=4, column=0, sticky=tk.W, pady=5, padx=10)
entry_max_iter = ttk.Entry(frame_superior)
entry_max_iter.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=10)

ttk.Label(frame_superior, text="Umbral:", background="lightyellow").grid(row=5, column=0, sticky=tk.W, pady=5, padx=10)
entry_umbral = ttk.Entry(frame_superior)
entry_umbral.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=10)

ttk.Button(frame_superior, text="Graficar", command=graficar).grid(row=6, column=0, columnspan=2, pady=10)

columns = ("i", "c", "f(c)")
tree = ttk.Treeview(frame_inferior, columns=columns, show="headings")
tree.heading("i", text="i")
tree.heading("c", text="c")
tree.heading("f(c)", text="f(c)")
tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

fig = plt.Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=frame_inferior)
canvas.get_tk_widget().grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

frame_superior.grid_columnconfigure(1, weight=1)
frame_inferior.grid_columnconfigure(0, weight=1)
frame_inferior.grid_columnconfigure(1, weight=1)

actualizar_campos()
root.mainloop()