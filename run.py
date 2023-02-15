import cv2
import detect_with_API
from PIL import Image
from paddleocr import PaddleOCR
import control_cheku
import db
import torch
import os,sys,psutil
import schedule
import time,datetime
import threading
os.environ['KMP_DUPLICATE_LIB_OK']='True'
a = detect_with_API.detectapi()
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
# cap=cv2.VideoCapture('rtmp://192.168.1.5/live/test')
# cap=cv2.VideoCapture('video.mp4')
cap=cv2.VideoCapture('D:\DevFiles\pr\车牌测试3.mp4')
ret, img = cap.read()
def cap_read():
    global ret,img,cap
    while 1:
        ret, img = cap.read()
        # img=cv2.flip(img,-1)
        if ret:
            now_time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            cv2.putText(img,
            now_time,
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 255, 255), 2)
            cv2.namedWindow('frame',0)
            cv2.resizeWindow("frame", 1280, 720)
            cv2.imshow("frame", img)

            #计划每半小时分段录像
            schedule.run_pending()

            #压缩文件
            # frame=cv2.resize(frame,(1280,720))

            #写入文件夹当中
            outVideo.write(img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                ret=0
                break
        else:
            break
            
thread1 = threading.Thread(target=cap_read,daemon=True)
thread1.start()

fps = 60
# size=(1280,720)
size=(1920,1080)
print("fps:",fps,"size:",size)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
location='D:\\车库入口录像\\'
def change_outVideo():
    global outVideo,fourcc,fps,size,d,p,location
    d = psutil.disk_partitions()
    p = psutil.disk_usage(d[1][0]) #D盘
    print('D盘使用百分比:',p[-1])
    if(p[-1]>=80):
        last_file=os.listdir(location)
        print(last_file[0])
        print('由于硬盘满载，删除文件：',last_file[0])
        os.remove(location+""+last_file[0])
    str=location+now_time+".mp4"
    outVideo = cv2.VideoWriter(str, fourcc, fps, size)
    print(str)
schedule.every(30).minutes.do(change_outVideo)
now_time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
change_outVideo()

with torch.no_grad():
    while ret:
        time.sleep(1)
        result,names = a.detect([img])
        img=result[0][0] #每一帧图片的处理结果图片
        # img=cv2.imread('test.jpg')
        # 每一帧图像的识别结果（可包含多个物体）
        for cls,(x1,y1,x2,y2),conf in result[0][1]:
            print(names[cls],x1,y1,x2,y2,conf)#识别物体种类、左上角x坐标、左上角y轴坐标、右下角x轴坐标、右下角y轴坐标，置信度
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0))
            cv2.putText(img,names[cls],(x1,y1-20),cv2.FONT_HERSHEY_DUPLEX,1.5,(255,0,0))
            # print()#将每一帧的结果输出分开
            target_img =img[y1:y2, x1:x2]
            cv2.namedWindow('license',0)
            cv2.resizeWindow("license",int((x2-x1)/2),int((y2-y1)/2))
            cv2.imshow('license',target_img)
            cv2.waitKey(1)
            result = ocr.ocr(target_img)
            print(result)
            if(result!=[[]]):
                for detected_char in result[-1]:
                    license=detected_char[-1][0]
                    print(license)
                    if(len(license)==5):
                        if(db.select(license)):
                            control_cheku.control_cheku_action('open')
                        else:
                            print('not license or expired')
            
    