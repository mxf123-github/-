import cv2
import detect_with_API
from PIL import Image
from paddleocr import PaddleOCR
import control_cheku
import db
import torch
import os
import sys
import psutil
import schedule
import time
import datetime
import threading
import numpy as np
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


# 捕获视频播放
a = detect_with_API.detectapi()
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
cap1=cv2.VideoCapture('rtsp://admin:@192.168.1.3/stream1')
cap2=cv2.VideoCapture('rtsp://admin:@192.168.0.105/stream1')
# cap=cv2.VideoCapture('video.mp4')
# cap=cv2.VideoCapture('D:\DevFiles\pr\车牌测试.mp4')
ret1, frame1 = cap1.read()
ret2, frame2 = cap2.read()
rectangle_count = 10

fps = 30
# size=(1280,720)
size=(1920,540)
print("fps:",fps,"size:",size)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
# location1='D:\\车库入口录像\\'
# location2='D:\\车库出口录像\\'
location3='D:\\车库入口和出口录像\\'
def change_outVideo():
    global outVideo3,fourcc,fps,size,location3
    d = psutil.disk_partitions()
    p = psutil.disk_usage(d[1][0]) #D盘
    print('D盘使用百分比:',p[-1])
    while(p[-1]>=80):
        last_file3=os.listdir(location3)
        print(last_file3[0])
        print('由于硬盘满载，删除文件：',last_file3[0])
        os.remove(location3+""+last_file3[0])
        d = psutil.disk_partitions()
        p = psutil.disk_usage(d[1][0]) #D盘
        print('D盘使用百分比:',p[-1])

    str3=location3+now_time+".mp4"
    outVideo3 = cv2.VideoWriter(str3, fourcc, 15, size)
    print(str3)

schedule.every(30).minutes.do(change_outVideo)
now_time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
change_outVideo()

def cap_read():
    global detect_img
    while 1:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        frame1 = cv2.resize(frame1, (960, 540))
        frame2 = cv2.resize(frame2, (960, 540))
        # frame=cv2.flip(frame,-1)
        if ret1&ret2:
                # 在左上角标注时间
            frame3 = np.hstack((frame1, frame2))
            detect_img=frame3
            now_time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            cv2.putText(frame3,now_time,
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 255, 255), 2)

            #展示Windows窗口，入口
            cv2.namedWindow('frame3',0)
            cv2.resizeWindow("frame3", 1920, 540)
            cv2.imshow("frame3", frame3)

            #计划每半小时分段录像
            schedule.run_pending()
            # 压缩文件
            # frame=cv2.resize(frame,(1280,720))

            # 计划每半小时分段录像
            schedule.run_pending()
            #写入文件夹当中
            outVideo3.write(frame3)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break


thread1 = threading.Thread(target=cap_read, daemon=True)
thread1.start()

# 识别
with torch.no_grad():
    # print(ret)
    time.sleep(1)
    while ret1&ret2:
        result, names = a.detect([detect_img])
        detect_img = result[0][0]  # 每一帧图片的处理结果图片
        # img=cv2.imread('test.jpg')
        # 每一帧图像的识别结果（可包含多个物体）
        for cls, (x1, y1, x2, y2), conf in result[0][1]:
            # 识别物体种类、左上角x坐标、左上角y轴坐标、右下角x轴坐标、右下角y轴坐标，置信度
            print(names[cls], x1, y1, x2, y2, conf)
            # print()#将每一帧的结果输出分开
            target_img = detect_img[y1:y2, x1:x2]
            rectangle_count = 0
            # cv2.namedWindow('license',0) 
            # cv2.resizeWindow("license",int((x2-x1)/2),int((y2-y1)/2))
            # cv2.imshow('license',target_img)
            # cv2.waitKey(1)
            result = ocr.ocr(target_img)
            print(result)
            if(result != [[]]):
                for detected_char in result[-1]:
                    license = detected_char[-1][0]
                    print(license)
                    if(len(license) == 5):
                        db_result=db.select(license)
                        if(db_result=='ok'):
                            control_cheku.control_cheku_action('open')
                        elif(db_result=='expired'):
                            print('expired')
                        else:
                            print('not sign')

