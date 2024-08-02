import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import 图片截取

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片选择器")

        self.canvas = tk.Canvas(root, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.imagetk = None

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.load_image()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.image = Image.open(file_path)
        self.imagetk = ImageTk.PhotoImage(self.image)

        # 调整窗口大小以匹配图片尺寸
        self.root.geometry(f"{self.image.width}x{self.image.height}")

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imagetk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_button_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def on_mouse_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)

        self.canvas.coords(self.rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)

        crop_box = (min(self.start_x, self.end_x), min(self.start_y, self.end_y),
                    max(self.start_x, self.end_x), max(self.start_y, self.end_y))

        coordinate = (crop_box[0],crop_box[1],crop_box[2],crop_box[3])
        print(f"矩形坐标：({crop_box[0]}, {crop_box[1]}, {crop_box[2]}, {crop_box[3]})")
        return coordinate

        # 可以将crop_box用于进一步处理，比如保存到文件或者传递给其他函数使用


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()




