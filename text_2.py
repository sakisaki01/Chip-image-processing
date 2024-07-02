import os
import cv2
import numpy as np


def replace_color_by_rgb(image, background_color, color_ranges_with_targets):
    """
    根据 RGB 颜色范围将图像中指定范围内的颜色替换为目标颜色

    Parameters:
        image (numpy.ndarray): 输入图像.
        background_color (numpy.ndarray): 背景颜色.
        color_ranges_with_targets (list): 包含颜色范围和目标颜色的列表.

    Returns:
        numpy.ndarray: 替换颜色后的图像.
    """
    image = np.uint8(image)
    image = image.astype(np.float32)

    result = np.copy(image)

    non_selected_mask = np.ones(image.shape[:2], dtype=np.uint8)

    for color_range, target_color in color_ranges_with_targets:
        lower_color, upper_color = color_range

        mask = cv2.inRange(image, lower_color, upper_color)

        result = np.where(mask[:, :, np.newaxis] == 255, target_color, result)

        non_selected_mask = cv2.bitwise_and(non_selected_mask, cv2.bitwise_not(mask))

    background_image = np.zeros_like(image)
    background_image[:, :] = background_color
    result = np.where(non_selected_mask[:, :, np.newaxis] == 1, background_image, result)

    # 腐蚀效果
    erosion_iterations = 1
    kernel = np.ones((2, 2), np.uint8)
    result = cv2.erode(result, kernel, iterations=erosion_iterations)

    return result


def replace_color(input_path, output_folder, output_name=None):
    """
    读取图像，根据预定义的颜色范围进行颜色替换，保存处理后的图像.

    Parameters:
        input_path (str): 输入图像的文件路径.
        output_folder (str): 输出图像的文件夹路径.
        output_name (str, optional): 输出图像的文件名. 默认为 None.
    """
    image = cv2.imread(input_path)

    color_ranges = []
    target_colors = []

    background_color = np.array([0, 0, 0])

    for i in range(3):  # 红色
        lower_color = np.array([8 + i * 1, 8 + i * 1, 8 + i * 1])
        upper_color = np.array([9 + i * 1, 9 + i * 1, 9 + i * 1])
        target_color = np.array([0, 200 - i * 50, 255])
        color_ranges.append((lower_color, upper_color))
        target_colors.append(target_color)

    for i in range(3):  # 绿色
        lower_color = np.array([12 + i * 1, 12 + i * 1, 12 + i * 1])
        upper_color = np.array([13 + i * 1, 13 + i * 1, 13 + i * 1])
        target_color = np.array([0, 255, i * 50])
        color_ranges.append((lower_color, upper_color))
        target_colors.append(target_color)

    for i in range(5):  # 蓝色
        lower_color = np.array([16 + i * 2, 16 + i * 2, 16 + i * 2])
        upper_color = np.array([30 + i * 2, 30 + i * 2, 30 + i * 2])
        target_color = np.array([255, 255-50*i, 0])
        color_ranges.append((lower_color, upper_color))
        target_colors.append(target_color)

    result = replace_color_by_rgb(image, background_color, list(zip(color_ranges, target_colors)))
    result_uint8 = np.uint8(result)

    if output_name is None:
        output_name = os.path.basename(input_path)

    output_path = os.path.join(output_folder, output_name)
    cv2.imwrite(output_path, result_uint8)


def process_images_in_folder(input_folder, output_folder):
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 遍历输入文件夹中的所有图片文件
    for filename in os.listdir(input_folder):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(input_folder, filename)
            output_name = filename  # 使用原始文件名作为输出文件名
            replace_color(input_path, output_folder, output_name)

            print("已处理:", input_path, "并保存为:", output_name)


# 调用函数处理文件夹中的所有图片
input_folder = "2024-07-02/output"  # 输入文件夹路径
output_folder = "2024-07-02/output1"  # 输出文件夹路径
process_images_in_folder(input_folder, output_folder)
