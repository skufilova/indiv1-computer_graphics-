
import tkinter as tk
import math


class Graham:
    def __init__(self, root):
        self.root = root
        self.root.title("Построение выпуклой оболочки методом Грэхема")

        self.points = []

        self.canvas = tk.Canvas(root, width=800, height=550, bg="white")
        self.canvas.pack(padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.add_point)

        frame = tk.Frame(root)
        frame.pack(pady=5)

        tk.Button(frame, text="Построить оболочку", command=self.build_hull).pack(side=tk.LEFT, padx=5)
        tk.Button(frame, text="Очистить", command=self.clear).pack(side=tk.LEFT, padx=5)

        self.info = tk.Label(root, text="Добавьте точки нажатием мыши")
        self.info.pack(pady=5)

    def add_point(self, event):
        point = (event.x, event.y)

        if point in self.points:
            return

        self.points.append(point)
        self.draw_points()
        self.info.config(text=f"Количество точек: {len(self.points)}")

    def draw_points(self):
        self.canvas.delete("all")

        for x, y in self.points:
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="blue", outline="blue")

    def cross(self, a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    def graham_scan(self, points):
        points = list(set(points))

        if len(points) < 3:
            return points

        start = min(points, key=lambda p: (p[1], p[0]))
        points.remove(start)

        def polar_key(p):
            dx = p[0] - start[0]
            dy = p[1] - start[1]
            angle = math.atan2(dy, dx)
            distance = dx * dx + dy * dy
            return angle, distance

        points.sort(key=polar_key)

        hull = [start]

        for point in points:
            while len(hull) >= 2 and self.cross(hull[-2], hull[-1], point) <= 0:
                hull.pop()

            hull.append(point)

        return hull

    def build_hull(self):
        self.draw_points()

        if len(self.points) < 3:
            self.info.config(text="Для построения нужно минимум 3 точки")
            return

        hull = self.graham_scan(self.points)

        if len(hull) < 3:
            self.info.config(text="Все точки лежат на одной прямой")
            if len(hull) == 2:
                self.canvas.create_line(*hull[0], *hull[1], fill="red", width=2)
            return

        for i in range(len(hull)):
            p1 = hull[i]
            p2 = hull[(i + 1) % len(hull)]

            self.canvas.create_line(*p1, *p2, fill="red", width=2)

        for x, y in hull:
            self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", outline="red")

        self.info.config(text=f"Точек: {len(self.points)} | Вершин оболочки: {len(hull)}")

    def clear(self):
        self.points.clear()
        self.canvas.delete("all")
        self.info.config(text="Добавьте точки нажатием мыши")


if __name__ == "__main__":
    root = tk.Tk()
    app = Graham(root)
    root.mainloop()
