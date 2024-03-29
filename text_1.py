import os
import cv2
import numpy as np


def replace_color_by_rgb(image, background_color, color_ranges_with_targets):
    """
    根据 RGB 颜色范围将图像中指定范围内的颜色替换为目标颜色
    """
    # 将图像转换为 8 位无符号整数类型
    image = np.uint8(image)
    image = image.astype(np.float32)

    result = np.copy(image)  # 复制原图像，避免修改原图像

    # 创建与输入图像相同尺寸的全白掩码
    non_selected_mask = np.ones(image.shape[:2], dtype=np.uint8)

    for color_range, target_color in color_ranges_with_targets:
        lower_color, upper_color = color_range

        # 创建颜色范围的掩码
        mask = cv2.inRange(image, lower_color, upper_color)

        # 将目标颜色应用于指定范围内的像素
        result = np.where(mask[:, :, np.newaxis] == 255, target_color, result)

       # 更新非选定区域的掩码
        non_selected_mask = cv2.bitwise_and(non_selected_mask, cv2.bitwise_not(mask))

    # 将非选定区域替换为背景颜色
    background_image = np.zeros_like(image)
    background_image[:, :] = background_color
    result = np.where(non_selected_mask[:, :, np.newaxis] == 1, background_image, result)

    erosion_iterations = 1
    # 执行腐蚀操作，排除不需要的颜色范围
    kernel = np.ones((2, 1), np.uint8)
    result = cv2.erode(result, kernel, iterations=erosion_iterations)

    return result


def main():
    # 读取图像
    image = cv2.imread("S2_3_enhanced_contrast/photo_20240308_144157.jpg")

    # 定义初始颜色范围和目标颜色
    color_ranges = []
    target_colors = []

    # 定义背景颜色（在 RGB 中）
    background_color = np.array([0, 0, 0])  # 背景颜色值（黑色）

    # 红色范围和目标颜色
    for i in range(4):
        lower_color = np.array([10 + i * 2, 10 + i * 2, 10 + i * 2])
        upper_color = np.array([19 + i * 2, 19 + i * 2, 19 + i * 2])
        target_color = np.array([0, 200 - i * 50, 255])
        color_ranges.append((lower_color, upper_color))
        target_colors.append(target_color)

    # 绿色范围和目标颜色
    for i in range(4):
        lower_color = np.array([20 + i * 1, 20 + i * 1, 20 + i * 1])
        upper_color = np.array([25 + i * 1, 25 + i * 1, 259 + i * 1])
        target_color = np.array([0, 255, i * 50])
        color_ranges.append((lower_color, upper_color))
        target_colors.append(target_color)

    # 蓝色范围和目标颜色
    for i in range(5):
        lower_color = np.array([26 + i * 1, 26 + i * 1, 26 + i * 1])
        upper_color = np.array([30 + i * 2, 30 + i * 2, 30 + i * 2])
        target_color = np.array([255-i * 20, 0, 0])
        color_ranges.append((lower_color, upper_color))
        target_colors.append(target_color)

    # 替换图像中指定范围内的颜色
    result = replace_color_by_rgb(image,background_color, list(zip(color_ranges, target_colors)))
    result_uint8 = np.uint8(result)

    # 显示结果
    cv2.imshow("input image", image)
    cv2.imshow("Result Image", result_uint8)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    output_folder = "output_folder"
    output_path = os.path.join(output_folder, "output_image13.jpg")
    cv2.imwrite(output_path, result_uint8)


if __name__ == "__main__":
    main()
