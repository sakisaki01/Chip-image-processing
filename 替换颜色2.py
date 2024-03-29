import os
import cv2
import numpy as np
from opening import opening_operation


def replace_color_by_rgb(image, background_color, *args):
    """
    根据 RGB 颜色范围将图像中多个范围内的颜色替换为相应的目标颜色
    """

    # 确保参数数量正确
    if len(args) % 3 != 0:
        raise ValueError("每个颜色范围应由下色、上色和目标颜色组成")

    # 初始化结果图像
    result = np.copy(image)

    # 遍历每个颜色范围和目标颜色
    for i in range(0, len(args), 3):
        lower_color = args[i]
        upper_color = args[i + 1]
        target_color = args[i + 2]

        # 创建颜色范围的掩码
        mask = cv2.inRange(image, lower_color, upper_color)

        # 使用掩码将范围内的像素替换为目标颜色
        target_image = np.zeros_like(image)
        target_image[:, :] = target_color
        result = np.where(mask[:, :, np.newaxis] == 255, target_image, result)

        erosion_iterations = 1
        # 执行腐蚀操作，排除不需要的颜色范围
        kernel = np.ones((1, 1), np.uint8)
        result = cv2.erode(result, kernel, iterations=erosion_iterations)

    return result


def main():
    # 读取图像
    image = cv2.imread("S2_2_enhanced_contrast/photo_20240308_144157.jpg")

    # 找到图像中最深的像素的索引
    max_pixel_index = np.argmax(image)

    # 根据索引获取最深像素的RGB颜色值
    max_pixel_color = image.flatten()[max_pixel_index]

    # 定义背景颜色（在 RGB 中）
    background_color = np.array([0, 0, 0])  # 背景颜色值（黑色）

    # 定义不同范围内的颜色和目标颜色
    lower_color1 = np.array([0, 0, 0])  # 第一个范围的低颜色值
    upper_color1 = np.array([50, 50, 50])  # 第一个范围的高颜色值
    target_color1 = np.array([0, 0, 255])  # 第一个范围的目标颜色（红色）

    lower_color2 = np.array([51, 51, 51])  # 第二个范围的低颜色值
    upper_color2 = np.array([55, 55, 55])  # 第二个范围的高颜色值
    target_color2 = np.array([0, 255, 0])  # 第二个范围的目标颜色（绿色）

    lower_color3 = np.array([56, 56, 56])  # 第二个范围的低颜色值
    upper_color3 = np.array([60, 60, 60])  # 第二个范围的高颜色值
    target_color3 = np.array([255, 0, 0])  # 第二个范围的目标颜色（蓝色）

    lower_color4 = np.array([61, 61, 61])  # 第二个范围的低颜色值
    upper_color4 = np.array([73, 73, 73])  # 第二个范围的高颜色值
    target_color4 = np.array([255, 55, 0])  # 第二个范围的目标颜色（蓝色）

    lower_color5 = np.array([74, 74, 74])  # 第二个范围的低颜色值
    upper_color5 = np.array([78, 78, 78])  # 第二个范围的高颜色值
    target_color5 = np.array([255, 155, 0])  # 第二个范围的目标颜色（蓝色）



    '''
    ## 定义源颜色范围（在 RGB 中）
    lower_color = np.array([0,0,0])  # 低范围颜色值（色）
    upper_color = np.array([85, 85, 85])  # 高范围颜色值（较亮的颜色）

    # 定义目标颜色（在 RGB 中）
    target_color = np.array([136, 39, 10])  # 目标颜色值（某种蓝色）
    
    # 替换图像中指定范围内的颜色
    result = replace_color_by_rgb(image, lower_color, upper_color, target_color)
    '''

    result = replace_color_by_rgb(image, background_color,
                                  lower_color1, upper_color1, target_color1,
                                  lower_color2, upper_color2, target_color2,
                                  lower_color3, upper_color3, target_color3,
                                  lower_color4, upper_color4, target_color4,
                                  lower_color5, upper_color5, target_color5)

    result_uint8 = np.uint8(result)

    # 显示结果
    cv2.imshow("Original Image", image)
    cv2.imshow("Result Image", result_uint8)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    output_folder = "output_folder"
    output_path = os.path.join(output_folder, "output_image2.jpg")
    cv2.imwrite(output_path, result_uint8)


if __name__ == "__main__":
    main()
