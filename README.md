如何选中需要处理的图片所在的路径

文件的目录：最好是文件和代码在同一个目录下 同时只允许用英文或者数字的命名格式
![image](https://github.com/user-attachments/assets/ec6c201c-fe4d-4ceb-bdc6-16f8915685ef)

假设图片文件以日期命名 最好在日期文件夹中创建一个 input 文件夹 将图片放到 input 文件夹中
![image](https://github.com/user-attachments/assets/dc805fa1-1d5f-4d82-b52b-53967c481485)

将目标的input文件夹按照下面这个方式修改 修改为相对路径
![image](https://github.com/user-attachments/assets/bca455c7-e96a-4c91-9d0a-f19d53195d91)
![image](https://github.com/user-attachments/assets/a92d30cb-350f-4bf3-9524-5550b7e037ee)
如果使用pycharm 就可以按照下面这个步骤 获得文件的相对路径
![image](https://github.com/user-attachments/assets/446998ca-a98f-4a0f-ab3e-70b1e2a45742)
![image](https://github.com/user-attachments/assets/4d4a616a-19db-4afd-b00f-d81dc4ff1c9b)

在图片选中里有两个python文件
![image](https://github.com/user-attachments/assets/c5962ae9-f967-4ad9-a5e4-c504eca6d551)

如果需要使用这两个代码 请注意 前面的 ../  不能删去
 ![image](https://github.com/user-attachments/assets/ceff16a2-2107-44dd-ae43-f76626a4155e)

 一般处理步骤
 1 -- 先使用灰度增强.py
 2 -- 运行text2.py

 5张处理.py  -- 可以将图片每隔55张取一张
 input_video.py -- 将图片转换为视频
 图片框选.py -- 从图片中框选出目标区域 获得坐标 然后将坐标复制下来 然后将坐标给 图片截取.py 批量截取
 ![image](https://github.com/user-attachments/assets/fa22184b-d977-423e-b38b-e467110e9b1a)
![image](https://github.com/user-attachments/assets/f7607005-7a39-4170-93a5-edb1088f860c)

 

