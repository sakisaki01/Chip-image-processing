import cv2
import time
import numpy as np
import os


class Stable:
    # 处理视频文件路径
    __video_path = None

    # surf 特征提取
    __surf = {
        # surf算法
        'surf': None,
        # 提取的特征点
        'kp': None,
        # 描述符
        'des': None,
        # 过滤后的特征模板
        'template_kp': None
    }

    # capture
    __capture = {
        # 捕捉器
        'cap': None,
        # 视频大小
        'size': None,
        # 视频总帧
        'frame_count': None,
        # 视频帧率
        'fps': None,
        'video': None
    }

    # 配置
    __config = {
        # 要保留的最佳特征的数量
        'key_point_count': 5000,
        # Flann特征匹配
        'index_params': dict(algorithm=0, trees=5),
        'search_params': dict(checks=50),
        'ratio': 0.5,
        'frame_count': 9999
    }

    # 当前处理帧数
    __current_frame = 0

    # 需要处理帧数
    __handle_count = 0

    # 处理时间
    __handle_timer = {
        'init': 0,
        'handle': 0,
        'read': 0,
        'key': 0,
        'matrix': 0,
        'flann': 0,
        'perspective': 0,
        'write': 0,
        'other': 0,
    }

    # 帧队列
    __frame_queue = None

    # 需要写入的帧队列
    __write_frame_queue = None

    # 特征提取列表
    __surf_list = []

    def __init__(self):
        pass

    # 初始化capture
    def __init_capture(self):
        self.__capture['cap'] = cv2.VideoCapture(self.__video_path)
        self.__capture['size'] = (int(self.__capture['cap'].get(cv2.CAP_PROP_FRAME_WIDTH)),
                                  int(self.__capture['cap'].get(cv2.CAP_PROP_FRAME_HEIGHT)))

        self.__capture['fps'] = self.__capture['cap'].get(cv2.CAP_PROP_FPS)

        self.__capture['video'] = cv2.VideoWriter(self.__video_path.replace('.', '_stable.'),
                                                  cv2.VideoWriter_fourcc(*"mp4v"),
                                                  self.__capture['fps'],
                                                  self.__capture['size'])

        self.__capture['frame_count'] = int(self.__capture['cap'].get(cv2.CAP_PROP_FRAME_COUNT))

        self.__handle_count = min(self.__config['frame_count'], self.__capture['frame_count'])

    # 初始化surf
    def __init_surf(self):
        st = time.time()
        self.__capture['cap'].set(cv2.CAP_PROP_POS_FRAMES, 0)
        state, first_frame = self.__capture['cap'].read()

        self.__capture['cap'].set(cv2.CAP_PROP_POS_FRAMES, self.__capture['frame_count'] - 20)
        state, last_frame = self.__capture['cap'].read()

        # 使用 ORB 替代 SURF
        self.__surf['surf'] = cv2.ORB_create(self.__config['key_point_count'])

        # ORB 特征提取
        self.__surf['kp'], self.__surf['des'] = self.__surf['surf'].detectAndCompute(first_frame, None)
        kp, des = self.__surf['surf'].detectAndCompute(last_frame, None)

        # 使用 BFMatcher 替代 FLANN
        self.bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = self.bf.match(self.__surf['des'], des)
        matches = sorted(matches, key=lambda x: x.distance)

        # 选择良好的匹配
        self.__surf['template_kp'] = []
        for f in matches[:50]:  # 你可以调整这里的数量来选取最佳匹配
            self.__surf['template_kp'].append(self.__surf['kp'][f.queryIdx])

        self.__capture['cap'].set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.__handle_timer['init'] = int((time.time() - st) * 1000)
        print("[INFO] init time:{}ms".format(self.__handle_timer['init']))

    # 初始化 队列
    def __init_data(self):
        pass

    # 初始化
    def __init(self):
        self.__init_capture()
        self.__init_surf()
        self.__init_data()

    # 处理
    def __process(self):

        self.__current_frame = 1

        while True:

            if self.__current_frame > self.__handle_count:
                break

            start_time = time.time()

            # 抽帧
            success, frame = self.__capture['cap'].read()
            self.__handle_timer['read'] = int((time.time() - start_time) * 1000)

            if not success: return

            # 计算
            frame = self.detect_compute(frame)

            # 写帧
            st = time.time()
            self.__capture['video'].write(frame)
            self.__handle_timer['write'] = int((time.time() - st) * 1000)

            self.__handle_timer['handle'] = int((time.time() - start_time) * 1000)

            self.__current_frame += 1

            self.print_handle_time()

    # 视频稳像
    def stable(self, path):
        self.__video_path = path
        self.__init()
        self.__process()

    # 打印耗时
    def print_handle_time(self):
        print(
            "[INFO] handle frame:{}/{} time:{}ms(read:{}ms key:{}ms flann:{}ms matrix:{}ms perspective:{}ms write:{}ms)".
            format(self.__current_frame,
                   self.__handle_count,
                   self.__handle_timer['handle'],
                   self.__handle_timer['read'],
                   self.__handle_timer['key'],
                   self.__handle_timer['flann'],
                   self.__handle_timer['matrix'],
                   self.__handle_timer['perspective'],
                   self.__handle_timer['write']))

    # 特征点提取
    def detect_compute(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 计算特征点
        st = time.time()
        kp, des = self.__surf['surf'].detectAndCompute(frame_gray, None)
        self.__handle_timer['key'] = int((time.time() - st) * 1000)

        # 特征点匹配
        st = time.time()
        matches = self.bf.match(self.__surf['des'], des)
        matches = sorted(matches, key=lambda x: x.distance)
        self.__handle_timer['flann'] = int((time.time() - st) * 1000)

        # 计算单应性矩阵
        st = time.time()
        p1, p2 = [], []
        for f in matches[:50]:  # 选择前50个匹配点
            p1.append(self.__surf['kp'][f.queryIdx].pt)
            p2.append(kp[f.trainIdx].pt)

        H, _ = cv2.findHomography(np.float32(p2), np.float32(p1), cv2.RHO)
        self.__handle_timer['matrix'] = int((time.time() - st) * 1000)

        # 透视变换
        st = time.time()
        output_frame = cv2.warpPerspective(frame, H, self.__capture['size'], borderMode=cv2.BORDER_REPLICATE)
        self.__handle_timer['perspective'] = int((time.time() - st) * 1000)

        return output_frame


s = Stable()

s.stable('20240812/0808_huidu3.mp4')