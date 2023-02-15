import cv2
import detect_with_API
from PIL import Image
from paddleocr import PaddleOCR
import control_cheku
import db
import torch
import os,sys
import time
import threading
os.environ['KMP_DUPLICATE_LIB_OK']='True'
a = detect_with_API.detectapi()
ocr = PaddleOCR(use_angle_cls=True, lang="ch")
cap=cv2.VideoCapture('rtmp://192.168.1.5/live/test')
# cap=cv2.VideoCapture('video.mp4')
ret, img = cap.read()
def cap_read():
    global ret,img,cap
    while 1:
        ret, img = cap.read()
        # img=cv2.flip(img,-1)
        if ret:
            cv2.namedWindow('frame',0)
            cv2.imshow("frame", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                ret=0
                break
        else:
            break
            

if __name__ == '__main__':
    thread1 = threading.Thread(target=cap_read,daemon=True)
    thread1.start()
    
    with torch.no_grad():
        while ret:
            time.sleep(0.5)
            result,names = a.detect([img])
            img=result[0][0] #每一帧图片的处理结果图片
            # img=cv2.imread('test.jpg')
            # 每一帧图像的识别结果（可包含多个物体）
            for cls,(x1,y1,x2,y2),conf in result[0][1]:
                print(names[cls],x1,y1,x2,y2,conf)#识别物体种类、左上角x坐标、左上角y轴坐标、右下角x轴坐标、右下角y轴坐标，置信度
                # '''
                # cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0))
                # cv2.putText(img,names[cls],(x1,y1-20),cv2.FONT_HERSHEY_DUPLEX,1.5,(255,0,0))'''
                # print()#将每一帧的结果输出分开
                target_img =img[y1:y2, x1:x2]
                # cv2.imshow('license',target_img)
                # cv2.waitKey(1)
                result = ocr.ocr(target_img)
                print(result)
                if(result!=[[]]):
                    license=result[-1][-1][-1][0]
                    print(license)
                    if(len(license)==5):
                        if(db.select(license)):
                            control_cheku.control_cheku_action('open')
                        else:
                            print('not license or expired')

    