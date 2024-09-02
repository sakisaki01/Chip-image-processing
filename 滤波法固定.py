import numpy as np
import cv2
import os

# 定义平滑半径
'''如果图像帧抖动较大，可以增加这个值以获得更平滑的结果；如果图像帧抖动较小，则可以减小这个值以保持更自然的运动 
   设置过高可能会导致图像模糊'''
SMOOTHING_RADIUS = 300

# 获取图像帧路径列表
image_folder = '0828/IL6+IL6R 2/input_huidu1'
# 创建输出目录
output_folder = '0828/IL6+IL6R 2/input_huidu1-lubo'


# 移动平均滤波函数
def moving_average(curve, radius):
    window_size = 2 * radius + 1
    f = np.ones(window_size) / window_size
    curve_pad = np.lib.pad(curve, (radius, radius), 'edge')
    curve_smoothed = np.convolve(curve_pad, f, mode='same')
    return curve_smoothed[radius:-radius]


# 平滑轨迹函数
def smooth_trajectory(trajectory):
    smoothed_trajectory = np.copy(trajectory)
    for i in range(3):
        smoothed_trajectory[:, i] = moving_average(trajectory[:, i], radius=SMOOTHING_RADIUS)
    return smoothed_trajectory


# 修复边界函数
def fix_border(frame):
    s = frame.shape
    T = cv2.getRotationMatrix2D((s[1] / 2, s[0] / 2), 0, 1.04)
    return cv2.warpAffine(frame, T, (s[1], s[0]))


# 计算帧之间的变换矩阵的平均值
def average_transforms(transforms):
    avg_transforms = np.copy(transforms)
    for i in range(1, len(transforms)):
        avg_transforms[i] = (transforms[i] + transforms[i - 1]) / 2
    return avg_transforms


image_paths = sorted([os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith((".jpg", ".png"))])

# 检查是否有图像帧
if not image_paths:
    print("Error: No image frames found in the specified directory.")
    exit()

# 初始化
n_frames = len(image_paths)
first_frame = cv2.imread(image_paths[0])
h, w = first_frame.shape[:2]
transforms = np.zeros((n_frames - 1, 3), np.float32)

# 处理每个图像帧
prev_gray = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
for i in range(1, n_frames):
    """
    maxCorners : 如果处理后的图像抖动仍然较大，可以尝试增加这个值；如果处理速度较慢，可以尝试减小这个值。
    qualityLevel : 如果图像中特征点较少，可以尝试降低这个值，以检测更多的特征点；如果特征点过多且不稳定，可以提高这个值。
    minDistance : 如果特征点密集分布且导致计算不稳定，可以尝试增加这个值；如果特征点较少，可以减小这个值。
    blockSize : 可以根据图像的分辨率和细节调整此参数，尝试不同的值来获取更好的特征点
    """
    prev_pts = cv2.goodFeaturesToTrack(prev_gray, maxCorners=500, qualityLevel=0.05, minDistance=30, blockSize=3)
    curr_frame = cv2.imread(image_paths[i])
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    curr_pts, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None)
    idx = np.where(status == 1)[0]
    prev_pts = prev_pts[idx]
    curr_pts = curr_pts[idx]

    if prev_pts.shape[0] < 4:
        m = np.eye(2, 3, dtype=np.float32)
    else:
        m, _ = cv2.estimateAffinePartial2D(prev_pts, curr_pts)

    if m is None:
        m = np.eye(2, 3, dtype=np.float32)

    dx, dy, da = m[0, 2], m[1, 2], np.arctan2(m[1, 0], m[0, 0])
    transforms[i - 1] = [dx, dy, da]
    prev_gray = curr_gray

    print(f"Frame: {i}/{n_frames - 1} - Tracked points: {len(prev_pts)}")

# 计算并平滑轨迹
trajectory = np.cumsum(transforms, axis=0)
smoothed_trajectory = smooth_trajectory(trajectory)
difference = smoothed_trajectory - trajectory
transforms_smooth = transforms + difference

# 创建输出目录
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 应用平滑变换并保存稳定后的帧
for i in range(n_frames):
    curr_frame = cv2.imread(image_paths[i])
    if i < n_frames - 1:
        dx, dy, da = transforms_smooth[i]
    else:
        dx, dy, da = 0, 0, 0

    m = np.zeros((2, 3), np.float32)
    m[0, 0], m[0, 1], m[1, 0], m[1, 1] = np.cos(da), -np.sin(da), np.sin(da), np.cos(da)
    m[0, 2], m[1, 2] = dx, dy

    frame_stabilized = cv2.warpAffine(curr_frame, m, (w, h))
    frame_stabilized = fix_border(frame_stabilized)

    output_filename = os.path.join(output_folder, f"output_frame_{i:04d}.png")
    cv2.imwrite(output_filename, frame_stabilized)
    print(f"Saved stabilized frame {i + 1}/{n_frames}")

print(f"Image sequence stabilization completed. add：{output_folder}")
