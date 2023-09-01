from app import *
from tkinter.ttk import *
from ttkbootstrap import Style
from tkinter import filedialog, StringVar, Toplevel,Frame
from math import floor
from PIL import Image, ImageTk
from os import startfile
from os.path import exists
from json import dumps
from time import sleep
from platform import system as sys_platform
from subprocess import call
from requests import get
from random import shuffle
from round_corner import *
from get_color import *


style = Style()
window = style.master

window.title('Player')
window.iconbitmap(r'ico.ico')
window.state('zoomed')
window.geometry('1200x650')


length = 1
if_clicking = 0
if_volume_clicking = 0
is_end = 0
playing_num = 0
playlist = []
randomlist = []
temp_list = []
if_lyric = 0
lyric_num = 0
lyric_time = []
lyric_text = []
message_windows_num = 0


mixer.music.set_endevent()


class messagebox():
    global message_windows_num

    def show(self, mode, text, num):
        global message_windows_num
        message_windows_num += 1
        info = Toplevel()
        info.attributes('-alpha', 1)

        def set_position():
            info.geometry(
                f'+{self.winfo_x()+int(self.winfo_width()/2)}+{self.winfo_y()+num*20+30}')
            info.after(10, set_position)

        def destroy():
            global message_windows_num
            for i in range(10):
                info.attributes('-alpha', 1-(i+1)/10)
                sleep(0.01)
                info.update()
            info.destroy()
            message_windows_num -= 1
        info.overrideredirect(True)
        info.attributes('-topmost', 'true')
        Label(info, text=text, bootstyle=f"inverse-{mode}").pack()
        set_position()
        for i in range(10):
            info.attributes('-alpha', (i+1)/10)
            sleep(0.01)
            info.update()
        info.after(2000, destroy)


def window_update():
    global length, if_clicking, if_volume_clicking, time_str, chazhi,lyric_num

    def main():
        global length, chazhi,lyric_num
        if if_clicking:  # 检测是否按键按下
            pass  # 按下则停止更新进度条
        else:
            try:
                pos_Scale.set((get_pos()/(length*1000))*100)  # 更新进度条
                min = str(floor((get_pos()+1)/60000))
                second = str(round((get_pos()+1)/1000 -
                             floor((get_pos()+1)/60000)*60))
                if len(min) == 1:  # 不满两位转化为两位数，下同
                    min = f'0{min}'
                if len(second) == 1:
                    second = f'0{second}'
                time_str.set(f'{min}:{second}')  # 更新进度数字
            except:
                pass
        mixer.music.set_volume(volume_Scale.get()/100)
        window.update()
        window.after(10, main)
        if mixer.music.get_busy():
            if (length*1000-get_pos()) < 200:  # 播完了换下一首
                mixer.music.stop()
                pause_Button.configure(image=play_photo)
                play_end()
                playnext()
        if if_lyric:
            lyric_num = 0
            for i in lyric_time:
                if get_pos() > i*1000:
                    lyric_num = lyric_time.index(i)
                else:
                    lyric_Label.configure(text=lyric_text[lyric_num])

    main()


def playlist_manage():
    global playlist, playing_num, playing_num_Label
    playing_num = 0
    playing_num_Label.configure(text=f'{playing_num+1}/{len(playlist)}')
    print(playlist,randomlist)
    load_file(playlist[playing_num])


def playnext():
    global playing_num, playlist, playing_num_Label,randomlist
    if playing_num+1 > len(playlist)-1:
        messagebox.show(self=window, mode='success',
                        text='已播放至列表结尾', num=message_windows_num)
    else:
        playing_num += 1
        try:
            print(type(randomplay_str.get()))
            if randomplay_str.get() == 'True':
                print(randomplay_str.get())
                print(randomlist)
                load_file(randomlist[playing_num])
            else:
                load_file(playlist[playing_num])
                
        except:
            playing_num -= 1
        playing_num_Label.configure(text=f'{playing_num+1}/{len(playlist)}')


def playlast():
    global playing_num, playlist, playing_num_Label,randomlist
    if playing_num-1 < 0:
        messagebox.show(self=window, mode='success',
                        text='已是列表开头', num=message_windows_num)
    else:
        playing_num -= 1
        try:
            if randomplay_str.get() == 'True':
                load_file(randomlist[playing_num])
            else:
                load_file(playlist[playing_num])
        except:
            playing_num += 1
        playing_num_Label.configure(text=f'{playing_num+1}/{len(playlist)}')


def open_file(mode=''):
    global length, playlist,randomlist,temp_list

    def set():
        global playlist, open_list,randomlist,temp_list
        if len(open_list):  # 防止文件打开失败却更新了播放列表
            playlist = open_list
            randomlist = []
            temp_list = []
            for i in open_list:
                randomlist.append(i)
                temp_list.append(i)
            shuffle(randomlist)
            playlist_manage()
            if settings['autoplay'] == "False":  # 如果没启用自动播放，那就在播放后立即暂停
                mixer.music.pause()
        else:
            messagebox.show(window, mode='danger',
                            text='没有打开任何文件', num=message_windows_num)
    if mode:
        def close():
            global open_list
            open_list = ask_Entry.get().split(';')
            set()

        ask_win = Toplevel()
        ask_win.iconbitmap('ico.ico')
        ask_Entry = Entry(ask_win)
        Label(ask_win, text='输入歌曲url, 用;隔开').pack(side='left')
        ask_Entry.pack(side='left')
        close_Button = Button(ask_win, text='提交', command=close)
        close_Button.pack()
    else:
        global open_list
        open_list = list(filedialog.askopenfilenames())
        set()


def load_file(path='', if_last=''):
    global length, photo, pos_Scale, time_Label, total_time_Label, playing_num,if_lyric,lyric_time,lyric_text
    name = ''
    lyric_path = path[0:len(path)-len(path.split('.')[-1])]+'lrc'
    if exists(lyric_path):
        if_lyric = 1
        lyric_time = []
        lyric_text = []
        with open(lyric_path,'r',encoding='utf-8') as f:
            lyric_data = f.read().split('\n')
        for i in lyric_data:
            if i:
                if i.split(']')[-1]:
                    lyric_text.append(i.split(']')[-1])
                    try:
                        lyric_time.append(int(i.split(']')[0].split('[')[-1].split(':')[0])*60+float(i.split(']')[0].split('[')[-1].split(':')[-1]))
                    except:
                        pass
    else:
        if_lyric = 0
        lyric_Label.configure(text='')


    if path[0:4] == 'http':
        mixer.music.unload()
        f = open('temp', 'wb')
        f.write(get(path).content)
        f.close()
        name = path.split("/")[-1].split(".")[0]
        path = 'temp'
    try:
        data = player_load(path)
        if name:
            data[0] = name
        if data[0]:
            title_str.set(data[0])
            window.title(f'{data[0]} - PyPlayer')
        else:
            title_str.set(path.split('/')[-1].split('.')[0])  # 没有返回值则设为文件名
            window.title(f'{path.split("/")[-1].split(".")[0]} - PyPlayer')
        artist_str.set(data[1])
        album_str.set(data[2])
        try:
            with open('song.jpg', 'wb') as f:
                f.write(data[3])

            img = Image.open('song.jpg').resize((400, 400))
            if autocolor_str.get() == 'True':
                color = get_dominant_colors(img)
                for i in [window,title_Label,artist_Label,album_Label,img_Label,time_Label,total_time_Label,playing_num_Label,info_Frame,time_Frame,buttons_Frame,volume_up_Lable,volume_down_Lable,divide_point]:
                    i.configure(background=color)
            img = circle_corner(img, 20)
        except Exception as e:
            print(e)
            img = Image.open('none.png').resize((400, 400))
            img = circle_corner(img, 20)
        photo = ImageTk.PhotoImage(img)
        img_Label.configure(image=photo)
        if data[4]:  # 获取不了时长就禁用控件
            length = data[4]  # 歌曲总长度
            pos_Scale['state'] = 'normal'
            time_Label['state'] = 'normal'
            min = str(floor(length/60))
            second = str(
                round((length/60-floor(length/60))*60))
            if len(min) == 1:  # 不满两位转化为两位数，下同
                min = f'0{min}'
            if len(second) == 1:
                second = f'0{second}'
            total_time_Label.configure(text=f'{min}:{second}')
        else:
            pos_Scale.set(0)
            time_str.set('∞')
            pos_Scale['state'] = 'disable'
            time_Label['state'] = 'disable'
            length = 0
            total_time_Label.configure(text='00:00')

        pause_Button['state'] = 'normal'
        next_Button['state'] = 'normal'
        last_Button['state'] = 'normal'

        play()

    except Exception as e:

        if if_last:
            messagebox.show(self=window, mode='danger',
                            text=f'播放出错: {str(e)},播放上一首', num=message_windows_num)
            playlast()
        else:
            messagebox.show(self=window, mode='danger',
                            text=f'播放出错: {str(e)},播放下一首', num=message_windows_num)
            playnext()


def play():
    player_play()
    pause_Button.configure(image=pause_photo)
    set_pos(0)


def click():
    global if_clicking
    if_clicking = 1


def release():
    global if_clicking
    try:
        try:
            set_pos((pos_Scale.get()/100)*length)
        except:
            player_play()
            set_pos((pos_Scale.get()/100)*length)
    except:
        pass
    if_clicking = 0


def pause():
    if mixer.music.get_busy():
        mixer.music.pause()
        pause_Button.configure(image=play_photo)
    else:
        mixer.music.unpause()
        pause_Button.configure(image=pause_photo)
        if mixer.music.get_busy():
            pass
        else:
            play()


def save_settings():
    global settings
    style.theme_use(theme_name.get())
    settings['theme'] = theme_name.get()
    settings['autoplay'] = autoplay_str.get()
    settings['autocolor'] = autocolor_str.get()
    with open('settings.json', 'w') as f:
        f.write(str(dumps(settings)))
    setting_window.withdraw()
    messagebox.show(window, mode='success', text='设置已保存',
                    num=message_windows_num)


def volume_release():
    settings['volume'] = volume_Scale.get()
    with open('settings.json', 'w') as f:
        f.write(str(dumps(settings)))


def show_setting_window():
    setting_window.deiconify()  # 显示设置窗口


def start_img(fileDir):
    platform = sys_platform()
    if platform == 'Linux':
        call(['xdg-open', fileDir])
    else:
        startfile(fileDir)

def random_play():
    global randomlist,playlist,temp_list,playing_num
    if randomplay_str.get() == 'True':
        playlist = randomlist
        playing_num = randomlist.index(temp_list[playing_num])
    else:
        playlist = temp_list
        playing_num = playlist.index(randomlist[playing_num])


title_str = StringVar()
artist_str = StringVar()
album_str = StringVar()
theme_name = StringVar()
time_str = StringVar()
autoplay_str = StringVar()
autocolor_str = StringVar()
randomplay_str = StringVar()

with open('settings.json', 'r') as f:
    settings = eval(f.read())

f = open('song.jpg', 'w')
f.close()

previous_img = Image.open(r'icon/previous.png').resize((20,20))
previous_photo = ImageTk.PhotoImage(previous_img)
pause_img = Image.open(r'icon/pause.png').resize((25,25))
pause_photo = ImageTk.PhotoImage(pause_img)
play_img = Image.open(r'icon/play.png').resize((25,25))
play_photo = ImageTk.PhotoImage(play_img)
next_img = Image.open(r'icon/next.png').resize((20,20))
next_photo = ImageTk.PhotoImage(next_img)
random_img = Image.open(r'icon/random.png').resize((20,20))
random_photo = ImageTk.PhotoImage(random_img)


info_Frame = Frame(window)
time_Frame = Frame(window)
buttons_Frame = Frame(window)

img = Image.open('none.png')
photo = ImageTk.PhotoImage(img)
img_Label = Label(window, image=photo)
title_Label = Label(window, textvariable=title_str, font=('微软雅黑', 25))
artist_Label = Label(info_Frame, textvariable=artist_str, font=('微软雅黑', 15))
divide_point = Label(info_Frame, text='•', font=('微软雅黑', 25))
album_Label = Label(info_Frame, textvariable=album_str, font=('微软雅黑', 15))
lyric_Label = Label(window,text='',font=('微软雅黑', 20))
time_Label = Label(time_Frame, textvariable=time_str, font=('微软雅黑', 10))
playing_num_Label = Label(time_Frame, text='/', font=('微软雅黑', 10))
total_time_Label = Label(time_Frame, text='00:00', font=('微软雅黑', 10))
pos_Scale = Scale(from_=0, to=100, bootstyle="primary")
last_Button = Button(buttons_Frame, image=previous_photo,
                     bootstyle=('primary'), command=playlast)
pause_Button = Button(buttons_Frame, image=play_photo,
                      bootstyle=('primary'), command=pause)
next_Button = Button(buttons_Frame, image=next_photo,
                     bootstyle=('primary'), command=playnext)
random_Button = Checkbutton(buttons_Frame,bootstyle="toolbutton", image=random_photo,onvalue="True", offvalue="False", variable=randomplay_str,command=random_play)
setting_Button = Button(buttons_Frame, text="选项",
                        bootstyle=('primary'), command=show_setting_window)
ask_file_Button = Button(buttons_Frame, text="打开文件",
                         bootstyle=('primary'), command=open_file)
volume_up_Lable = Label(buttons_Frame, text='🔊', font=('微软雅黑', 15))
volume_Scale = Scale(buttons_Frame, from_=0, to=100, bootstyle="primary")
volume_down_Lable = Label(buttons_Frame, text='🔉', font=('微软雅黑', 15))


last_Button.pack(side='left', fill='x', padx=20, pady=5)
pause_Button.pack(side='left', fill='x', padx=5, pady=5)
next_Button.pack(side='left', fill='x', padx=20, pady=5)
random_Button.pack(side='left', fill='x', padx=20, pady=5)
setting_Button.pack(side='right', fill='x', padx=5, pady=5)
ask_file_Button.pack(side='right', fill='x', padx=5, pady=5)
volume_up_Lable.pack(side='right')
volume_Scale.pack(side='right', padx=5, pady=5)
volume_down_Lable.pack(side='right')
buttons_Frame.pack(side='bottom', fill='both', pady=5)
pos_Scale.pack(side='bottom', fill='x')
time_Label.pack(side='left', anchor='w', expand='yes', padx=5)
playing_num_Label.pack(side='left', anchor='center', expand='yes', padx=5)
total_time_Label.pack(side='left', anchor='e', expand='yes', padx=5)
time_Frame.pack(side='bottom', fill='x', pady=5)
img_Label.pack(side='left', pady=10, padx=20)
title_Label.pack(pady=5)
artist_Label.pack(side='left', fill='x', padx=5, pady=5)
divide_point.pack(side='left')
album_Label.pack(side='left', fill='x', padx=5, pady=5)
info_Frame.pack(pady=5)
lyric_Label.pack(anchor='center',expand=True)

# 设置窗口
setting_window = Toplevel()
setting_window.geometry('400x200')
setting_window.title('选项')
setting_window.iconbitmap(r'ico.ico')
theme_Frame = Frame(setting_window)
theme_Frame.pack(fill='x')
Label(theme_Frame, text='选择一个主题: ').pack(side='left')
theme_Combobox = Combobox(theme_Frame, state="readonly",
                          textvariable=theme_name, values=style.theme_names())
theme_name.set(settings["theme"])
theme_Combobox.pack(side='left', fill='x')
autoplay_Button = Checkbutton(setting_window,text='打开文件后自动播放', bootstyle="round-toggle",
                              onvalue="True", offvalue="False", variable=autoplay_str)
autocolor_Button = Checkbutton(setting_window,text='打开文件后自动根据封面更改背景颜色', bootstyle="round-toggle",
                              onvalue="True", offvalue="False", variable=autocolor_str)
autoplay_Button.pack(fill='x')
autocolor_Button.pack(fill='x')
Button(setting_window, text="保存并关闭", command=save_settings).pack(side='bottom')
Label(setting_window, text='Made by Haoyu').pack(side='bottom')
setting_window.protocol('WM_DELETE_WINDOW', setting_window.withdraw)
setting_window.withdraw()


pos_Scale.bind("<Button-1>", lambda a: click())
pos_Scale.bind("<ButtonRelease-1>", lambda a: release())
volume_Scale.bind("<ButtonRelease-1>", lambda a: volume_release())
volume_down_Lable.bind("<Button-1>", lambda a: volume_Scale.set(volume_Scale.get()-10))
volume_up_Lable.bind("<Button-1>", lambda a: volume_Scale.set(volume_Scale.get()+10))
img_Label.bind("<Double-Button-1>", lambda a: start_img('song.jpg'))
img_Label.bind("<Button-3>", lambda a: start_img('song.jpg'))
ask_file_Button.bind("<Button-3>", lambda a: open_file(mode=1))


style.theme_use(settings["theme"])
volume_Scale.set(settings["volume"])
autoplay_str.set(settings["autoplay"])
autocolor_str.set(settings["autocolor"])
randomplay_str.set('False')
pause_Button['state'] = 'disable'
next_Button['state'] = 'disable'
last_Button['state'] = 'disable'

window_update()


window.mainloop()
