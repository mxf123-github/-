import win32con
import win32gui
import os
import time
import threading
hwnd = win32gui.FindWindow(None,"《串口键盘软件V1.0》                      ")
close_count = 0
isopen=False
def __init__():
    # 查找窗口句柄
    # print('串口软件句柄',hwnd)
    if hwnd==0:
        os.startfile('C:/Users/96437/Desktop/串口键盘软件')
        time.sleep(8)   #目测等8秒开软件
        hwnd = win32gui.FindWindow(None,"《串口键盘软件V1.0》                      ")
    # print('串口软件句柄',hwnd)
    if hwnd != 0:
        # win32gui.SetForegroundWindow(hwnd)  # 设置前置窗口
        combobox_hwnd = win32gui.FindWindowEx(hwnd, None, "ThunderRT6ComboBox", None)
        for i in range(4):
            combobox_hwnd = win32gui.FindWindowEx(hwnd, combobox_hwnd, "ThunderRT6ComboBox", None)
            #这里我并不知道为什么循环4次刚好能选中正确串口
        # print('下拉框句柄',combobox_hwnd)
        edit_hwnd=win32gui.FindWindowEx(combobox_hwnd,0,"Edit",None)
        # print('下拉框编辑句柄',edit_hwnd)
        win32gui.SendMessage(edit_hwnd, win32con.WM_SETTEXT, None, "COM5")  
        # 这里选择需要使用的端口

def button(order):
    if hwnd != 0:
        button_hwnd=win32gui.FindWindowEx(hwnd,None,"ThunderRT6CommandButton",None)
        for i in range(30):
            if win32gui.GetWindowText(button_hwnd)==order:
                break
            button_hwnd=win32gui.FindWindowEx(hwnd,button_hwnd,"ThunderRT6CommandButton",None)
        # print('此句柄',button_hwnd,'的按钮行为',win32gui.GetWindowText(button_hwnd))
        win32gui.SendMessage(hwnd, win32con.WM_COMMAND, 1,button_hwnd)
        # print('已运行此句柄按钮',order)

def get_son_windows(parent):
    if hwnd != 0:
        hWnd_child_list = []
        win32gui.EnumChildWindows(parent, lambda hWnd, param: param.append(hWnd), hWnd_child_list)
        for i in hWnd_child_list:
            title = win32gui.GetWindowText(i)
            print('句柄',i,'的窗口标题:%s' % (title))
        return hWnd_child_list

def control_cheku_action(action):
    global isopen,close_count
    print('action:',action)
    if(action=='open'):
        # 开栏杆10s，并且在扫描到此车牌号后，保持在10s开门时间，
        # 10s内没有车牌才关门
        # 关门的过程中有车经过时，立即开门10s
        print('已经开启栏杆，10秒后关闭')
        if(isopen==False):
            button('停栏杆')
            time.sleep(0.5)
            button('开栏杆')
            isopen=True
            start_thread()
        else:
            close_count=0
        
    if(action=='close'):
        button('停栏杆')
        time.sleep(0.5)
        button('关栏杆')
        print('已经关闭栏杆')
        isopen=False
        close_count=0
    if(action=='about'):
        time.sleep(0.5)
        button('about')

def wait_close():
    global close_count,isopen
    print(close_count)
    while close_count<10 and isopen==True:
        close_count+=1
        time.sleep(1)
        print(close_count)
    control_cheku_action('close')

def start_thread():
    thread = threading.Thread(target=wait_close)
    thread.start()
    return thread

if __name__ == '__main__':
    # c.get_son_windows(c.hwnd)     #获取全部子窗口
    control_cheku_action('open')   #在此设置你想要执行的命令
    time.sleep(1)
    control_cheku_action('open')   #在此设置你想要执行的命令
    time.sleep(2)
    control_cheku_action('open')   #在此设置你想要执行的命令
    time.sleep(1)
    control_cheku_action('open')   #在此设置你想要执行的命令
    time.sleep(12)
    control_cheku_action('open')   #在此设置你想要执行的命令