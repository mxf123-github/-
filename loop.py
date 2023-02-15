from os import system
import time
while 1:
    # 在system里放入需要执行的命令即可
    # 执行的程序会不停止运行，占用此线程，停止释放线程并再次启动程序
    print('重新执行程序')
    system("call activate base")
    system("python C:\\Users\\123\\Desktop\\python\\License_yolov7_paddleocr\\run.py")