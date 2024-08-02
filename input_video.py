import cv2
import os

input_folder = '2024-8-2/input_huidu3'
output_video_path = '2024-8-2/input_huidu3.mp4'   #后面的 .mp4 不能删去
fps = 30  # 视频帧率


def images_to_video(input_folder, output_video_path, fps):
    # 获取输入文件夹中所有图片的文件名，并按照文件名排序
    image_files = sorted([os.path.join(input_folder, file) for file in os.listdir(input_folder) if
                          file.endswith(('.jpg', '.png', '.jpeg'))])

    # 读取第一张图片，获取图片尺寸
    first_image = cv2.imread(image_files[0])
    height, width, _ = first_image.shape

    # 创建视频编写器
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 可以根据需要更改编码器
    video_writer = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    # 逐帧写入视频
    for image_file in image_files:
        image = cv2.imread(image_file)
        video_writer.write(image)

    # 释放资源
    video_writer.release()
    print("将文件夹：" + input_folder + "导出为MP4格式，地址为：" + output_video_path)


# 调用函数将图片合成为视频
images_to_video(input_folder, output_video_path, fps)
