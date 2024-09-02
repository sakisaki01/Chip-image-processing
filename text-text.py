import os
import cv2
import numpy as np

# 目标文件夹
input_folder = "0829/input"
# 输出文件夹 如果没有将自动创建
output_folder = "0829/input_huidu2"


def enhance_contrast(image, alpha=1.5, beta=-130, clip_limit=2.0, tile_grid_size=(8, 8), blend_alpha=0.5):
    """
    通过调整亮度和对比度并结合CLAHE来增强图像，同时平衡亮度

    Parameters:
        image (numpy.ndarray): 输入的灰度图像.
        alpha (float): 对比度增强因子，值越大对比度越高.
        beta (int): 亮度调节因子，正值增加亮度，负值降低亮度.
        clip_limit (float): CLAHE的剪辑限制，用于控制对比度限制.
        tile_grid_size (tuple): CLAHE的网格大小，用于控制局部对比度增强.
        blend_alpha (float): 原图与CLAHE处理图像的混合权重，值越大保留原图细节越多.

    Returns:
        numpy.ndarray: 处理后的增强图像.
    """
    # Step 1: 调整对比度和亮度
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Step 2: 使用CLAHE增强局部对比度
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    clahe_image = clahe.apply(adjusted_image)

    # Step 3: 混合原图和CLAHE处理后的图像
    enhanced_image = cv2.addWeighted(adjusted_image, blend_alpha, clahe_image, 1 - blend_alpha, 0)

    return enhanced_image


def convert_to_grayscale(image):
    """
    将图像转换为灰度图像
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


def gamma_correction(image, gamma=1.0):
    """
    通过伽马矫正增强对比度，使暗色部分更暗，亮色部分更亮
    """
    inv_gamma = 1.0 / gamma
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in range(256)], dtype="uint8")
    adjusted_image = cv2.LUT(image, table)
    return adjusted_image


def process_images_in_folder(input_folder, output_folder):
    """
    处理指定文件夹中的所有图像文件，将其转换为灰度图像、增强对比度并保存到输出文件夹
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_image_path = os.path.join(input_folder, filename)
        output_image_path = os.path.join(output_folder, filename)

        # 如果是图像文件
        if os.path.isfile(input_image_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            color_image = cv2.imread(input_image_path)

            # 将彩色图像转换为灰度图像
            grayscale_image = convert_to_grayscale(color_image)

            # 增强灰度图像的对比度和亮度，同时结合CLAHE
            enhanced_image = enhance_contrast(grayscale_image)

            enhanced_image = gamma_correction(enhanced_image)

            # 保存增强后的灰度图像
            cv2.imwrite(output_image_path, enhanced_image)

            print("已处理:", input_image_path, "并保存为:", output_image_path)


if __name__ == "__main__":
    process_images_in_folder(input_folder, output_folder)
