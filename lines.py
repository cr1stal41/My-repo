import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
from matplotlib.patches import FancyArrow

# Алгоритм Брезенхема для окружности
def bresenham_circle(xc, yc, r, num_points=100, compression_x=1, compression_y=1):
    points = []
    for i in range(num_points):
        theta = 2 * math.pi * i / num_points
        x = xc + r * math.cos(theta)
        y = yc + r * math.sin(theta)
        points.append((x * compression_x, y * compression_y))  # Применение коэффициента сжатия
    return points

# Алгоритм Брезенхема для эллипса
def bresenham_ellipse(xc, yc, a, b, num_points=100, compression_x=1, compression_y=1):
    points = []
    for i in range(num_points):
        theta = 2 * math.pi * i / num_points
        x = xc + a * math.cos(theta)
        y = yc + b * math.sin(theta)
        points.append((x * compression_x, y * compression_y))  # Применение коэффициента сжатия
    return points

# Алгоритм параметрического уравнения эллипса
def parametric_ellipse(xc, yc, a, b, num_points=100):
    points = []
    for i in range(num_points):
        theta = 2 * math.pi * i / num_points
        x = xc + a * math.cos(theta)
        y = yc + b * math.sin(theta)
        points.append((x, y))
    return points

# Функция для сортировки точек по углу
def sort_points_by_angle(points, xc, yc):
    return sorted(points, key=lambda p: math.atan2(p[1] - yc, p[0] - xc))

# Отрисовка
def draw_segment():
    try:
        ax.clear()

        # Получаем коэффициенты сжатия
        compression_x = float(entry_compression_x.get())
        compression_y = float(entry_compression_y.get())

        # Синий отрезок
        x1, y1 = map(float, entry_start.get().split(','))
        x2, y2 = map(float, entry_end.get().split(','))
        ax.plot([x1 * compression_x, x2 * compression_x], [y1 * compression_y, y2 * compression_y], marker='o', color='blue')
        ax.text(x1 * compression_x, y1 * compression_y, f'({x1}, {y1})', fontsize=10, ha='right')
        ax.text(x2 * compression_x, y2 * compression_y, f'({x2}, {y2})', fontsize=10, ha='left')

        # Красный ориентированный отрезок
        ox1, oy1 = map(float, entry_oriented_start.get().split(','))
        ox2, oy2 = map(float, entry_oriented_end.get().split(','))
        direction = direction_var.get()
        if direction == "A→B":
            arrow_start = (ox1 * compression_x, oy1 * compression_y)
            arrow_end = (ox2 * compression_x, oy2 * compression_y)
        else:
            arrow_start = (ox2 * compression_x, oy2 * compression_y)
            arrow_end = (ox1 * compression_x, oy1 * compression_y)

        dx = arrow_end[0] - arrow_start[0]
        dy = arrow_end[1] - arrow_start[1]
        ax.add_patch(FancyArrow(arrow_start[0], arrow_start[1], dx, dy,
                                width=0.05, head_width=0.2, head_length=0.3, color='red'))
        ax.text(arrow_start[0], arrow_start[1], 'A', color='red', fontsize=10, ha='right')
        ax.text(arrow_end[0], arrow_end[1], 'B', color='red', fontsize=10, ha='left')

        # Зелёные окружности — рисуем линией
        for (xc, yc, r) in circles:
            points = bresenham_circle(xc, yc, r, num_points=200, compression_x=compression_x, compression_y=compression_y)
            points = sort_points_by_angle(points, xc, yc)
            xs, ys = zip(*points)
            ax.plot(xs, ys, color='green')

        # Зелёные эллипсы — рисуем линией
        for (xc, yc, a, b) in ellipses:
            points = bresenham_ellipse(xc, yc, a, b, num_points=200, compression_x=compression_x, compression_y=compression_y)
            points = sort_points_by_angle(points, xc, yc)
            xs, ys = zip(*points)
            ax.plot(xs, ys, color='green')

        # Жёлтые эллипсы по параметрическому уравнению
        for (xc, yc, a, b) in parametric_ellipses:
            points = parametric_ellipse(xc, yc, a, b, num_points=200)
            xs, ys = zip(*points)
            ax.plot(xs, ys, color='yellow')

        # Масштаб
        all_x = [x1, x2, ox1, ox2] + [c[0] for c in circles] + [e[0] for e in ellipses] + [p[0] for p in parametric_ellipses]
        all_y = [y1, y2, oy1, oy2] + [c[1] for c in circles] + [e[1] for e in ellipses] + [p[1] for p in parametric_ellipses]
        margin = max([c[2] for c in circles] + [max(e[2], e[3]) for e in ellipses], default=1) + 1
        if all_x and all_y:
            ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
            ax.set_ylim(min(all_y) - margin, max(all_y) + margin)
        else:
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)

        ax.set_aspect('equal', adjustable='box')
        ax.grid(True)
        ax.set_title("Отрезки, окружности, эллипсы")

        canvas.draw()

    except Exception as e:
        messagebox.showerror("Ошибка ввода", "Проверьте правильность всех координат.")

def add_circle():
    try:
        xc = float(entry_circle_center.get().split(',')[0])
        yc = float(entry_circle_center.get().split(',')[1])
        r = int(entry_circle_radius.get())
        if r <= 0:
            raise ValueError("Радиус должен быть положительным.")
        circles.append((xc, yc, r))
        draw_segment()
    except:
        messagebox.showerror("Ошибка ввода", "Введите центр как x,y и положительный радиус.")

def add_ellipse():
    try:
        xc, yc = map(float, entry_ellipse_center.get().split(','))
        a, b = map(int, entry_ellipse_axes.get().split(','))
        if a <= 0 or b <= 0:
            raise ValueError("Полуоси должны быть положительными.")
        ellipses.append((xc, yc, a, b))
        draw_segment()
    except:
        messagebox.showerror("Ошибка ввода", "Введите центр как x,y и полуоси как a,b (целые > 0).")

def add_parametric_ellipse():
    try:
        xc, yc = map(float, entry_parametric_ellipse_center.get().split(','))
        a, b = map(int, entry_parametric_ellipse_axes.get().split(','))
        if a <= 0 or b <= 0:
            raise ValueError("Полуоси должны быть положительными.")
        parametric_ellipses.append((xc, yc, a, b))
        draw_segment()
    except:
        messagebox.showerror("Ошибка ввода", "Введите центр как x,y и полуоси как a,b (целые > 0).")

# Интерфейс
root = tk.Tk()
root.title("Отрезки, окружности, эллипсы")

# Синий отрезок
tk.Label(root, text="Синий отрезок: начальная точка (x,y):").grid(row=0, column=0, sticky="e")
entry_start = tk.Entry(root)
entry_start.grid(row=0, column=1)
entry_start.insert(0, "0,0")

tk.Label(root, text="Синий отрезок: конечная точка (x,y):").grid(row=1, column=0, sticky="e")
entry_end = tk.Entry(root)
entry_end.grid(row=1, column=1)
entry_end.insert(0, "4,2")

# Красный ориентированный отрезок
tk.Label(root, text="Ориент. отрезок: точка A (x,y):").grid(row=2, column=0, sticky="e")
entry_oriented_start = tk.Entry(root)
entry_oriented_start.grid(row=2, column=1)
entry_oriented_start.insert(0, "1,1")

tk.Label(root, text="Ориент. отрезок: точка B (x,y):").grid(row=3, column=0, sticky="e")
entry_oriented_end = tk.Entry(root)
entry_oriented_end.grid(row=3, column=1)
entry_oriented_end.insert(0, "3,3")

tk.Label(root, text="Направление:").grid(row=4, column=0, sticky="e")
direction_var = tk.StringVar(value="A→B")
tk.OptionMenu(root, direction_var, "A→B", "B→A").grid(row=4, column=1)

# Окружности
tk.Label(root, text="Центр окружности (x,y):").grid(row=5, column=0, sticky="e")
entry_circle_center = tk.Entry(root)
entry_circle_center.grid(row=5, column=1)
entry_circle_center.insert(0, "2,2")

tk.Label(root, text="Радиус окружности:").grid(row=6, column=0, sticky="e")
entry_circle_radius = tk.Entry(root)
entry_circle_radius.grid(row=6, column=1)
entry_circle_radius.insert(0, "3")

tk.Button(root, text="Добавить окружность", command=add_circle).grid(row=7, column=0, columnspan=2, pady=5)

# Эллипсы
tk.Label(root, text="Центр эллипса (x,y):").grid(row=8, column=0, sticky="e")
entry_ellipse_center = tk.Entry(root)
entry_ellipse_center.grid(row=8, column=1)
entry_ellipse_center.insert(0, "5,5")

tk.Label(root, text="Полуоси эллипса a,b:").grid(row=9, column=0, sticky="e")
entry_ellipse_axes = tk.Entry(root)
entry_ellipse_axes.grid(row=9, column=1)
entry_ellipse_axes.insert(0, "4,2")

tk.Button(root, text="Добавить эллипс (Брезенхем)", command=add_ellipse).grid(row=10, column=0, columnspan=2, pady=5)

# Параметрический эллипс (жёлтый)
tk.Label(root, text="Центр параметр. эллипса (x,y):").grid(row=11, column=0, sticky="e")
entry_parametric_ellipse_center = tk.Entry(root)
entry_parametric_ellipse_center.grid(row=11, column=1)
entry_parametric_ellipse_center.insert(0, "6,6")

tk.Label(root, text="Полуоси параметр. эллипса a,b:").grid(row=12, column=0, sticky="e")
entry_parametric_ellipse_axes = tk.Entry(root)
entry_parametric_ellipse_axes.grid(row=12, column=1)
entry_parametric_ellipse_axes.insert(0, "5,3")

tk.Button(root, text="Добавить параметр. эллипс (жёлтый)", command=add_parametric_ellipse).grid(row=13, column=0, columnspan=2, pady=5)

# Коэффициенты сжатия
tk.Label(root, text="Коэффициент сжатия по оси X:").grid(row=14, column=0, sticky="e")
entry_compression_x = tk.Entry(root)
entry_compression_x.grid(row=14, column=1)
entry_compression_x.insert(0, "1")

tk.Label(root, text="Коэффициент сжатия по оси Y:").grid(row=15, column=0, sticky="e")
entry_compression_y = tk.Entry(root)
entry_compression_y.grid(row=15, column=1)
entry_compression_y.insert(0, "1")

# Полотно
fig, ax = plt.subplots(figsize=(6, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=16, column=0, columnspan=2)

# Хранилище
circles = []
ellipses = []
parametric_ellipses = []

# Первый запуск
draw_segment()

root.mainloop()
