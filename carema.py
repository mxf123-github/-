import cv2
import threading

def show_video():
    cap = cv2.VideoCapture('rtmp://169.254.50.100/live/test')
    while True:
        ret, frame = cap.read()
        if ret:
            cv2.namedWindow('frame',0)
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
    thread = threading.Thread(target=show_video)
    thread.start()
