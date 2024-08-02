from PIL import Image
import os


# 原始图片文件夹路径
input_folder = '../2024-8-2/input-5'
# 裁剪后图片保存文件夹路径
output_folder = '../2024-8-2/input-5_cut'

 # 816.0, 344.0, 1028.0, 814.0
def crop_images(input_folder, output_folder, left, top, right, bottom):
    # 确保输出文件夹存在，如果不存在则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    crop_box = (left, top, right, bottom)

    # 遍历输入文件夹中的所有图片文件
    for filename in os.listdir(input_folder):
        if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                # 裁剪图片
                cropped_img = img.crop(crop_box)
                # 构建输出文件路径
                output_path = os.path.join(output_folder, filename)
                # 保存裁剪后的图片
                cropped_img.save(output_path)
                print(f"已将文件：{img_path}处理为{output_path}")

    print("所有图片已成功裁剪并保存到新的文件夹中！")


# 获取用户输入的矩形坐标范围
print("请输入矩形的坐标范围，格式为 left, top, right, bottom（例如：292.0, 185.0, 363.0, 260.0）：")
input_coords = input().strip()  # 获取用户输入并去除首尾空格1070.0, 456.0, 1689.0, 776.0
left, top, right, bottom = map(float, input_coords.split(','))  # 解析输入的坐标

crop_images(input_folder, output_folder, left, top, right, bottom)
