import cv2
import os
import shutil

# 设置输入文件夹和输出文件夹路径
input_folder = "2024-8-2/input"
output_folder = "2024-8-2/input-5"
# 设置每隔几张处理一次
Interval = 5

def extract_images(input_folder, output_folder, interval=5):
    """
    从文件夹中每隔指定间隔提取一张图片到输出文件夹
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 获取输入文件夹中的所有图片文件
    image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]

    # 遍历图片文件，每隔指定间隔提取一张图片到输出文件夹
    for i in range(0, len(image_files), interval):
        image_file = image_files[i]
        input_image_path = os.path.join(input_folder, image_file)
        output_image_path = os.path.join(output_folder, image_file)
        shutil.copyfile(input_image_path, output_image_path)
        print(f"Extracted: {image_file}")




# 每隔10张提取一张图片
extract_images(input_folder, output_folder, interval=Interval)
