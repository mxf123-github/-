import cv2
import time  
import datetime
import schedule
import psutil,os
import numpy as np
# cap1=cv2.VideoCapture('rtmp://192.168.1.5/live/test')
cap1=cv2.VideoCapture('rtsp://admin:@192.168.1.3/stream1')
cap2=cv2.VideoCapture('rtsp://admin:@192.168.0.105/stream1')

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

while 1:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    frame1 = cv2.resize(frame1, (960, 540))
    frame2 = cv2.resize(frame2, (960, 540))
    # frame=cv2.flip(frame,-1)
    if ret1&ret2:
        #在左上角标注时间
        frame3 = np.hstack((frame1, frame2))
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

        #压缩文件
        # frame=cv2.resize(frame,(1280,720))

        #写入文件夹当中
        outVideo3.write(frame3)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap1.release()
cap2.release()
outVideo3.release()
cv2.destroyAllWindows()