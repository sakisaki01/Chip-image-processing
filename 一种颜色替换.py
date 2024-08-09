import os
import cv2
import numpy as np

# 定义颜色范围
blu_lower_color = 121
blu_upper_color = 150
blu_gap = 10
blu_range = 5

input_folder = "2024.0809/input_cut"  # 输入文件夹路径
output_folder = "2024.0809/input_cut+color22"  # 输出文件夹路径

# 去除噪点的像素大小（3x3）
kernel_size = 3


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


def remove_flickering_noise(image, kernel_size=3):
    """
    使用中值滤波去除局部大小为3x3的噪点
    """
    clean_image = cv2.medianBlur(image, kernel_size)
    return clean_image


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

    # 只处理红色
    for i in range(blu_range):  # 红色
        lower_color = np.array(
            [blu_lower_color + i * blu_gap, blu_lower_color + i * blu_gap, blu_lower_color + i * blu_gap])
        upper_color = np.array(
            [blu_upper_color + i * blu_gap, blu_upper_color + i * blu_gap, blu_upper_color + i * blu_gap])
        target_color = np.array([255, 255 - 50 * i, 0])
        color_ranges.append((lower_color, upper_color))
        target_colors.append(target_color)

    result = replace_color_by_rgb(image, background_color, list(zip(color_ranges, target_colors)))
    result_uint8 = np.uint8(result)
    # 去除噪点
    result_uint8 = remove_flickering_noise(result_uint8, kernel_size=kernel_size)

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
process_images_in_folder(input_folder, output_folder)
