import cv2
import time  
import datetime
import schedule
import psutil,os
cap=cv2.VideoCapture('rtmp://192.168.1.5/live/test')
fps = 30
size=(1280,720)
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

while 1:
    ret, frame = cap.read()
    frame=cv2.flip(frame,-1)
    if ret:
        #在左上角标注时间
        now_time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        cv2.putText(frame,
            now_time,
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            (255, 255, 255), 2)

        #展示Windows窗口
        cv2.namedWindow('frame',0)
        cv2.imshow("frame", frame)

        #计划每半小时分段录像
        schedule.run_pending()

        #压缩文件
        frame=cv2.resize(frame,(1280,720))

        #写入文件夹当中
        outVideo.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
outVideo.release()
cv2.destroyAllWindows()