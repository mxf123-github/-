import cv2
import time  
import datetime
import schedule

cap=cv2.VideoCapture('rtmp://192.168.1.5/live/test')
fps = cap.get(cv2.CAP_PROP_FPS) 
fps = 30
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print("fps:",fps,"size:",size)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
def change_outVideo():
    global outVideo,fourcc,fps,size
    outVideo=''
    if(outVideo!=''):
        outVideo.release()
    str="D:\\车库入口录像\\"+now_time+".mp4"
    outVideo = cv2.VideoWriter(str, fourcc, fps, size)
    print(str)
schedule.every(30).minutes.do(change_outVideo)
now_time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
change_outVideo()

while 1:
    ret, frame = cap.read()
    frame=cv2.flip(frame,-1)
    if ret:
        now_time=datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        cv2.putText(frame,
            now_time,
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
            (255, 255, 255), 2)
        cv2.namedWindow('frame',0)
        cv2.imshow("frame", frame)

        schedule.run_pending()
        outVideo.write(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()
outVideo.release()
cv2.destroyAllWindows()