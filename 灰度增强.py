import os
import cv2


# 目标文件夹
input_folder = "2024-8-2/input"
# 输出文件夹 如果没有将自动创建
output_folder = "2024-8-2/input_huidu3"


def enhance_contrast(image, alpha=0.3):  # 通常alpha=0.1 可以通过修改alpha的值来改变图像对比度 越小对比越明显
    """
    增强图像对比度
    """

    # 将灰度图像应用直方图均衡化
    enhanced_image = cv2.equalizeHist(image)
    # 将原始图像和均衡化后的图像进行加权混合
    blended_image = cv2.addWeighted(image, alpha, enhanced_image, 1 - alpha, 0)
    return blended_image


def convert_to_grayscale(image):
    """
    将图像转换为灰度图像
    """
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


def process_images_path(input_path, output_path):
    color_image = cv2.imread(input_path)
    # 将彩色图像转换为灰度图像
    grayscale_image = convert_to_grayscale(color_image)

    # 增强灰度图像的对比度
    enhanced_image = enhance_contrast(grayscale_image)

    # 保存增强后的灰度图像
    cv2.imwrite(output_path, enhanced_image)

    print("已处理:", input_path, "并保存为:", output_path)


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
            # 读取彩色图像
            color_image = cv2.imread(input_image_path)

            # 将彩色图像转换为灰度图像
            grayscale_image = convert_to_grayscale(color_image)

            # 增强灰度图像的对比度
            enhanced_image = enhance_contrast(grayscale_image)

            # 保存增强后的灰度图像
            cv2.imwrite(output_image_path, enhanced_image)

            print("已处理:", input_image_path, "并保存为:", output_image_path)


def main(input_folder, output_folder):
    # 输入文件夹路径（相对路径下的 "dataset" 文件夹）
    Input_folder = input_folder

    # 输出文件夹路径（如果不存在，则创建）
    Output_folder = output_folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # # 处理图像文件夹中的所有图像
    process_images_in_folder(Input_folder, Output_folder)


if __name__ == "__main__":
    main(input_folder, output_folder)
