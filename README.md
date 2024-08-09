下载代码解压后 在当前文件夹中右键打开终端
首先在终端输入代码
pip install -r requirements.txt


如何选中需要处理的图片所在的路径

文件的目录：最好是文件和代码在同一个目录下 同时只允许用英文或者数字的命名格式

![image](https://github.com/user-attachments/assets/ec6c201c-fe4d-4ceb-bdc6-16f8915685ef)

假设图片文件以日期命名 最好在日期文件夹中创建一个 input 文件夹 将图片放到 input 文件夹中

![image](https://github.com/user-attachments/assets/dc805fa1-1d5f-4d82-b52b-53967c481485)

将目标的input文件夹按照下面这个方式修改 修改为相对路径

![image](https://github.com/user-attachments/assets/bca455c7-e96a-4c91-9d0a-f19d53195d91)
![image](https://github.com/user-attachments/assets/a92d30cb-350f-4bf3-9524-5550b7e037ee)

如果使用pycharm 就可以按照下面这个步骤 获得文件的 相对路径

![image](https://github.com/user-attachments/assets/446998ca-a98f-4a0f-ab3e-70b1e2a45742)
![image](https://github.com/user-attachments/assets/4d4a616a-19db-4afd-b00f-d81dc4ff1c9b)

在图片选中里有两个python文件
![image](https://github.com/user-attachments/assets/c5962ae9-f967-4ad9-a5e4-c504eca6d551)

如果需要使用这两个代码 请注意 前面的 ../  不能删去
![image](https://github.com/user-attachments/assets/ceff16a2-2107-44dd-ae43-f76626a4155e)



其他代码的说明
 5张处理.py  -- 可以将图片每隔5张取一张 可以自己修改参数

 ![image](https://github.com/user-attachments/assets/4a418987-5049-4c42-a02f-fb286643556e)

 input_video.py -- 将图片转换为视频
 
 ![image](https://github.com/user-attachments/assets/38b3f2a0-5ed9-4a8c-bee6-862e55b71572)

 
 图片框选.py -- 从图片中框选出目标区域 获得坐标 然后将坐标复制下来 然后将坐标给 图片截取.py 批量截取
![image](https://github.com/user-attachments/assets/fa22184b-d977-423e-b38b-e467110e9b1a)
![image](https://github.com/user-attachments/assets/f7607005-7a39-4170-93a5-edb1088f860c)

灰度增强.py -- 可以通过调节alpha来调整图片的明暗度 alpha越接近0 明暗对比越大 建议每次加减0.1

![image](https://github.com/user-attachments/assets/290736ce-836c-412d-8f04-de006f90af16)

text2.py -- 给特征上色 去除噪点

![image](https://github.com/user-attachments/assets/b21f115c-8df3-4e8b-8c60-66db8044392a)

这三个范围优先修改蓝色 主要根据灰度处理图片的rgb的值的范围去确定
假定最低值在15
![image](https://github.com/user-attachments/assets/982ddbdf-3906-458e-b892-38372d594c11)

最高值在66
![image](https://github.com/user-attachments/assets/4dcc587d-ec6e-4a8f-b840-8181c8723a2c)

那么蓝色范围可以修改为（range不做修改）
![image](https://github.com/user-attachments/assets/e7f0bac1-d9c7-4ef6-bac6-ff9da5e0bd58)

去除噪点 一般芯片会产生噪点 可以通过修改kernel_size 的大小来去除 建议不超过3

![image](https://github.com/user-attachments/assets/51b7aef5-1ec0-4406-b2c5-2c9b644f46a1)



 一般处理步骤
 如果每隔5张取一张 就先运行5张处理.py
 
 1 -- 框选目标区域
 
 ![image](https://github.com/user-attachments/assets/fa22184b-d977-423e-b38b-e467110e9b1a)

 2 -- 截取目标区域

 ![image](https://github.com/user-attachments/assets/f7607005-7a39-4170-93a5-edb1088f860c)
 
 3 -- 先使用灰度增强.py
 4 -- 运行text2.py
 5 -- 运行input_video.py 将图片转为视频
 

 




 

