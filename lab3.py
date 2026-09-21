import math
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def cda(pixels, w, h, x1, y1, x2, y2, color):
    if round(x1) == round(x2) and round(y1) == round(y2):
        ix, iy = int(math.floor(x1)), int(math.floor(y1))
        if 0 <= ix < w and 0 <= iy < h:
            pixels[ix, iy] = color
        return

    if abs(x2 - x1) >= abs(y2 - y1):
        l = abs(x2 - x1)
    else:
        l = abs(y2 - y1)

    dx = (x2 - x1) / l
    dy = (y2 - y1) / l

    x = x1 + 0.5 * sign(dx)
    y = y1 + 0.5 * sign(dy)

    for _ in range(int(round(l)) + 1):
        ix, iy = int(math.floor(x)), int(math.floor(y))
        if 0 <= ix < w and 0 <= iy < h:
            pixels[ix, iy] = color
        x += dx
        y += dy


def brezf(pixels, w, h, x1, y1, x2, y2, color):
    if round(x1) == round(x2) and round(y1) == round(y2):
        ix, iy = int(math.floor(x1)), int(math.floor(y1))
        if 0 <= ix < w and 0 <= iy < h:
            pixels[ix, iy] = color
        return

    sx = sign(x2 - x1)
    sy = sign(y2 - y1)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x = x1
    y = y1
    f = 0

    if dy > dx:
        t = dx
        dx = dy
        dy = t
        f = 1

    e = dy / dx - 0.5

    for _ in range(int(round(dx)) + 1):
        ix, iy = int(math.floor(x)), int(math.floor(y))
        if 0 <= ix < w and 0 <= iy < h:
            pixels[ix, iy] = color
        if e >= 0:
            if f == 1:
                x += sx
            else:
                y += sy
            e -= 1.0
        if f == 1:
            y += sy
        else:
            x += sx
        e += dy / dx


def brezi(pixels, w, h, x1, y1, x2, y2, color):
    x1, y1 = int(round(x1)), int(round(y1))
    x2, y2 = int(round(x2)), int(round(y2))

    if x1 == x2 and y1 == y2:
        if 0 <= x1 < w and 0 <= y1 < h:
            pixels[x1, y1] = color
        return

    sx = sign(x2 - x1)
    sy = sign(y2 - y1)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x = x1
    y = y1
    f = 0

    if dy > dx:
        t = dx
        dx = dy
        dy = t
        f = 1

    e = 2 * dy - dx

    for _ in range(dx + 1):
        if 0 <= x < w and 0 <= y < h:
            pixels[x, y] = color
        if e >= 0:
            if f == 1:
                x += sx
            else:
                y += sy
            e -= 2 * dx
        if f == 1:
            y += sy
        else:
            x += sx
        e += 2 * dy


class Form1:
    def __init__(self, root):
        self.root = root
        self.root.title("Form1")
        self.root.geometry("490x560")
        self.root.resizable(False, False)

        self.w = 450
        self.h = 400

        self.bitmap = Image.new("RGB", (self.w, self.h), (255, 255, 255))
        self.pixels = self.bitmap.load()
        self.tk_bitmap = None

        top_frame = tk.Frame(root)
        top_frame.place(x=20, y=10, width=450, height=60)

        tk.Label(top_frame, text="A", font=("Tahoma", 10)).grid(
            row=0, column=0, padx=3, pady=2, sticky="e"
        )
        self.edit_a = tk.Entry(top_frame, width=7, font=("Tahoma", 10))
        self.edit_a.insert(0, "160")
        self.edit_a.grid(row=0, column=1, padx=4, pady=2)

        tk.Label(top_frame, text="B", font=("Tahoma", 10)).grid(
            row=1, column=0, padx=3, pady=2, sticky="e"
        )
        self.edit_b = tk.Entry(top_frame, width=7, font=("Tahoma", 10))
        self.edit_b.insert(0, "160")
        self.edit_b.grid(row=1, column=1, padx=4, pady=2)

        self.btn_all = tk.Button(
            top_frame,
            text="Все сразу",
            width=9,
            font=("Tahoma", 9),
            command=self.draw_all,
        )
        self.btn_all.grid(row=0, column=2, padx=8, pady=2)

        self.btn_clear = tk.Button(
            top_frame,
            text="Очистить",
            width=9,
            font=("Tahoma", 9),
            command=self.clear_canvas,
        )
        self.btn_clear.grid(row=1, column=2, padx=8, pady=2)

        self.btn_save = tk.Button(
            top_frame,
            text="Сохранить",
            width=9,
            font=("Tahoma", 9),
            command=self.button_save_click,
        )
        self.btn_save.grid(row=0, column=3, padx=4, pady=2)

        algo_frame = tk.Frame(root)
        algo_frame.place(x=20, y=75, width=450, height=35)

        tk.Button(
            algo_frame,
            text="ЦДА (синий)",
            width=12,
            font=("Tahoma", 8),
            command=lambda: self.draw_single("cda"),
        ).grid(row=0, column=0, padx=2)
        tk.Button(
            algo_frame,
            text="Брезенхем (кр)",
            width=13,
            font=("Tahoma", 8),
            command=lambda: self.draw_single("brezf"),
        ).grid(row=0, column=1, padx=2)
        tk.Button(
            algo_frame,
            text="Целочисл. (зел)",
            width=13,
            font=("Tahoma", 8),
            command=lambda: self.draw_single("brezi"),
        ).grid(row=0, column=2, padx=2)
        tk.Button(
            algo_frame,
            text="Встроенные (сер)",
            width=13,
            font=("Tahoma", 8),
            command=lambda: self.draw_single("builtin"),
        ).grid(row=0, column=3, padx=2)

        self.image_area = tk.Canvas(
            root,
            bg="white",
            highlightthickness=1,
            highlightbackground="gray70",
        )
        self.image_area.place(x=20, y=115, width=self.w, height=self.h)

        self.refresh_display()

    def refresh_display(self):
        self.tk_bitmap = ImageTk.PhotoImage(self.bitmap)
        self.image_area.create_image(0, 0, anchor="nw", image=self.tk_bitmap)

    def clear_canvas(self):
        self.bitmap = Image.new("RGB", (self.w, self.h), (255, 255, 255))
        self.pixels = self.bitmap.load()
        self.image_area.delete("all")
        self.refresh_display()

    def get_spidron_segments(self):
        try:
            a = float(self.edit_a.get())
            b = float(self.edit_b.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите числовые значения!")
            return []

        base_size = min(self.w, self.h) * 0.42
        scale = base_size / max(a, 1.0)
        curr_a = a * scale

        cx = self.w // 2 - 20
        cy = self.h // 2 + 50

        p0 = (cx - curr_a / 2, cy)
        p1 = (cx + curr_a / 2, cy)
        segments = []

        for _ in range(8):
            dx = p1[0] - p0[0]
            dy = p1[1] - p0[1]
            cos60 = 0.5
            sin60 = -math.sqrt(3) / 2
            p2 = (
                p0[0] + dx * cos60 - dy * sin60,
                p0[1] + dx * sin60 + dy * cos60,
            )

            segments.append((p0[0], p0[0 + 1], p1[0], p1[1]))
            segments.append((p1[0], p1[1], p2[0], p2[1]))
            segments.append((p2[0], p2[1], p0[0], p0[1]))

            dx2 = p2[0] - p1[0]
            dy2 = p2[1] - p1[1]
            k = 1.0 / math.sqrt(3)
            ang = -math.pi / 6
            p3 = (
                p1[0] + k * (dx2 * math.cos(ang) - dy2 * math.sin(ang)),
                p1[1] + k * (dx2 * math.sin(ang) + dy2 * math.cos(ang)),
            )

            segments.append((p1[0], p1[1], p3[0], p3[1]))
            segments.append((p2[0], p2[1], p3[0], p3[1]))

            p0 = p3
            p1 = p2

        return segments

    def draw_single(self, method):
        segments = self.get_spidron_segments()
        if not segments:
            return

        if method == "builtin":
            for x1, y1, x2, y2 in segments:
                self.image_area.create_line(
                    round(x1),
                    round(y1),
                    round(x2),
                    round(y2),
                    fill="#7F7F7F",
                    width=1,
                )
                brezi(
                    self.pixels,
                    self.w,
                    self.h,
                    round(x1),
                    round(y1),
                    round(x2),
                    round(y2),
                    (127, 127, 127),
                )
            return

        color_map = {
            "cda": (127, 127, 255),
            "brezf": (255, 127, 127),
            "brezi": (127, 255, 127),
        }
        color = color_map[method]

        for x1, y1, x2, y2 in segments:
            if method == "cda":
                cda(self.pixels, self.w, self.h, x1, y1, x2, y2, color)
            elif method == "brezf":
                brezf(self.pixels, self.w, self.h, x1, y1, x2, y2, color)
            elif method == "brezi":
                brezi(
                    self.pixels,
                    self.w,
                    self.h,
                    round(x1),
                    round(y1),
                    round(x2),
                    round(y2),
                    color,
                )

        self.refresh_display()

    def draw_all(self):
        self.draw_single("cda")
        self.draw_single("brezf")
        self.draw_single("brezi")
        self.draw_single("builtin")

    def button_save_click(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".bmp",
            filetypes=[
                ("Bitmap (*.bmp)", "*.bmp"),
                ("Portable Bitmap (*.pbm)", "*.pbm"),
                ("PNG (*.png)", "*.png"),
            ],
        )
        if file_path:
            self.bitmap.save(file_path)
            messagebox.showinfo("Сохранение", f"Файл сохранен:\n{file_path}")


if __name__ == "__main__":
    app_root = tk.Tk()
    Form1(app_root)
    app_root.mainloop()