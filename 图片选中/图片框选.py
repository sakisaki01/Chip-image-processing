import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

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
        self.scale = 1.0  # 初始化缩放比例为1
        self.max_scale = 1.0  # 初始化最大缩放比例

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        self.load_image()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        self.image = Image.open(file_path)

        # 计算缩放比例使图片完整显示在画布上
        self.max_scale = min(self.root.winfo_screenwidth() / self.image.width,
                             self.root.winfo_screenheight() / self.image.height)
        self.scale = self.max_scale

        self.imagetk = ImageTk.PhotoImage(self.image.resize((int(self.image.width * self.scale),
                                                            int(self.image.height * self.scale))))

        self.root.geometry(f"{self.imagetk.width()}x{self.imagetk.height()}")
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imagetk)

        self.canvas.config(scrollregion=(0, 0, self.imagetk.width(), self.imagetk.height()))

    def zoom_in(self):
        # 限制最大缩放比例为1.5倍的max_scale
        if self.scale < self.max_scale * 1.5:
            self.scale *= 1.1
            self.update_image()

    def zoom_out(self):
        # 限制最小缩放比例为1
        if self.scale > 1:
            self.scale /= 1.1
            self.update_image()

    def update_image(self):
        new_width = int(self.image.width * self.scale)
        new_height = int(self.image.height * self.scale)
        self.resized_image = self.image.resize((new_width, new_height), Image.LANCZOS)
        self.imagetk = ImageTk.PhotoImage(self.resized_image)
        self.canvas.itemconfig(self.image_on_canvas, image=self.imagetk)

        # 更新画布的scrollregion
        self.canvas.config(scrollregion=(0, 0, new_width, new_height))

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

        # 将缩小后的坐标转换回原始图片的坐标
        crop_box = (min(self.start_x, self.end_x) / self.scale,
                    min(self.start_y, self.end_y) / self.scale,
                    max(self.start_x, self.end_x) / self.scale,
                    max(self.start_y, self.end_y) / self.scale)

        coordinate = (crop_box[0], crop_box[1], crop_box[2], crop_box[3])
        print(f"矩形坐标（原始图片）：({crop_box[0]}, {crop_box[1]}, {crop_box[2]}, {crop_box[3]})")
        return coordinate

        # 可以将crop_box用于进一步处理，比如保存到文件或者传递给其他函数使用


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()




