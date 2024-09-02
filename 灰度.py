import os
import cv2
import numpy as np

# 目标文件夹
input_folder = "0829/input_huidu1_cut2"
output_folder_intermediate = "0829/input_huidu1_cut2_huidu"
output_folder_final = "0829/input_huidu1_cut2_huiduEX"


def apply_gamma_correction(image, gamma=2.0):
    invGamma = 1.0 / gamma
    table = [((i / 255.0) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, dtype="uint8")
    return cv2.LUT(image, table)


def apply_clahe(image, clip_limit=1.0, tile_grid_size=(8, 8)):
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    return clahe.apply(image)


def unsharp_mask(image, sigma=1.0, strength=1.5):
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    sharpened = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
    return sharpened


def enhance_contrast(image, alpha=0.1):
    enhanced_image = cv2.equalizeHist(image)
    blended_image = cv2.addWeighted(image, alpha, enhanced_image, 1 - alpha, 0)
    return blended_image


def convert_to_grayscale(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image


def process_image_stage1(input_path, output_path):
    color_image = cv2.imread(input_path)
    grayscale_image = convert_to_grayscale(color_image)

    # 1. Gamma校正
    gamma_corrected = apply_gamma_correction(grayscale_image, gamma=0.5)

    # 2. CLAHE增强
    clahe_enhanced = apply_clahe(gamma_corrected, clip_limit=1.0)

    # 3. 非锐化掩蔽增强
    final_image = unsharp_mask(clahe_enhanced)

    cv2.imwrite(output_path, final_image)
    print("已处理 (第一阶段):", input_path, "并保存为:", output_path)


def process_image_stage2(input_path, output_path):
    color_image = cv2.imread(input_path)
    grayscale_image = convert_to_grayscale(color_image)

    # 增强灰度图像的对比度
    enhanced_image = enhance_contrast(grayscale_image)

    # 保存增强后的灰度图像
    cv2.imwrite(output_path, enhanced_image)
    print("已处理 (第二阶段):", input_path, "并保存为:", output_path)


def process_images_in_folder_stage1(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_image_path = os.path.join(input_folder, filename)
        output_image_path = os.path.join(output_folder, filename)

        if os.path.isfile(input_image_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            process_image_stage1(input_image_path, output_image_path)


def process_images_in_folder_stage2(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        input_image_path = os.path.join(input_folder, filename)
        output_image_path = os.path.join(output_folder, filename)

        if os.path.isfile(input_image_path) and filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            process_image_stage2(input_image_path, output_image_path)


def main(input_folder, output_folder_intermediate, output_folder_final):
    # 处理图像第一阶段
    process_images_in_folder_stage1(input_folder, output_folder_intermediate)

    # 处理图像第二阶段
    process_images_in_folder_stage2(output_folder_intermediate, output_folder_final)


if __name__ == "__main__":
    main(input_folder, output_folder_intermediate, output_folder_final)
