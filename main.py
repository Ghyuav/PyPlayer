from app import *
from tkinter.ttk import *
from ttkbootstrap import Style
from tkinter import filedialog, StringVar, messagebox,Toplevel
from math import floor
from PIL import Image, ImageTk
from os import startfile
style = Style()
window = style.master

window.title('Player')
# window.iconbitmap(r'profile\ico.ico')
# window.state('zoomed')
window.geometry('1200x650')


length = 1
if_clicking = 0
play_progress = 0
is_end = 0
playing_num = 0
playlist = []


mixer.music.set_endevent()


def window_update():
    global length, if_clicking, play_progress, time_str

    def w_update():
        global length
        global play_progress
        if if_clicking:  # 检测是否按键按下
            pass  # 按下则停止更新进度条
        else:
            try:
                pos_Scale.set((play_progress/(length*1000))*100)  # 更新进度条
                min = str(floor((play_progress/1000)/60))
                second = str(
                    round((play_progress/60000-floor(play_progress/60000))*60))
                if len(min) == 1:  # 不满两位转化为两位数，下同
                    min = f'0{min}'
                if len(second) == 1:
                    second = f'0{second}'
                time_str.set(f'{min}:{second}')  # 更新进度数字
            except:
                pass
        window.update()
        window.after(100, w_update)
        if mixer.music.get_busy():
            play_progress += 100  # 由于get_pos获取播放时长而不是播放进度，所以在此记录播放进度
            if (length*1000-play_progress) < 500:  # 播完了换下一首
                playnext()
    w_update()


def playlist_manage():
    global playlist, playing_num
    load_file(playlist[0])
    playing_num = 0


def playnext():
    global playing_num, playlist, play_progress
    play_progress = 0
    playing_num += 1
    try:
        load_file(playlist[playing_num])
    except IndexError as e:
        if str(e) == 'list index out of range':
            pass  # 列表播放完了


def playlast():
    global playing_num, playlist, play_progress
    play_progress = 0
    playing_num -= 1
    try:
        load_file(playlist[playing_num])
    except IndexError as e:
        if str(e) == 'list index out of range':
            pass  # 列表播放完了


def open_file():
    global length, play_progress, playlist
    playlist = list(filedialog.askopenfilenames())
    playlist_manage()


def load_file(path=''):
    global length, play_progress, photo, pos_Scale, time_Label

    try:
        data = player_load(path)
    except:
        messagebox.showerror('标题', '不支持的类型:'+path.split('.')[-1]+',切换到下一首')
    try:  # 若播放不了则不支持播放，直接跳过（有点草率，之后再来优化）
        if data[0]:
            title_str.set(data[0])
            window.title(f'{data[0]} - PyPlayer')
        else:
            title_str.set(path.split('/')[-1].split('.')[0])  # 没有返回值则设为文件名
            window.title(f'{path.split("/")[-1].split(".")[0]} - PyPlayer')
        artist_str.set(data[1])
        album_str.set(data[2])
        try:
            with open('song.png', 'wb') as f:
                f.write(data[3])

            img = Image.open('song.png').resize((512, 512))
        except:
            img = Image.open('none.png').resize((512, 512))
        photo = ImageTk.PhotoImage(img)
        img_Label.configure(image=photo)
        if data[4]:  # 获取不了时长就禁用控件
            length = data[4]  # 歌曲总长度
            pos_Scale['state'] = 'normal'
            time_Label['state'] = 'normal'
        else:
            pos_Scale.set(0)
            time_str.set('∞')
            pos_Scale['state'] = 'disable'
            time_Label['state'] = 'disable'
            length = 0
        play_progress = 0  # 播放进度归零
        play()

    except:
        playnext()


def play():
    global play_progress
    play_progress = 0  # 播放进度归零
    player_play()


def click():
    global if_clicking
    if_clicking = 1


def release():
    global if_clicking, play_progress
    try:
        try:
            set_pos((pos_Scale.get()/100)*length)
        except:
            player_play()
            set_pos((pos_Scale.get()/100)*length)
        play_progress = (pos_Scale.get()/100)*length*1000
    except:
        pass
    if_clicking = 0


def pause():
    global play_progress
    if mixer.music.get_busy():
        mixer.music.pause()
    else:
        mixer.music.unpause()
        if mixer.music.get_busy():
            pass
        else:
            play()

def change_theme():
    global settings
    style.theme_use(theme_name.get())
    settings['theme'] = theme_name.get()
    with open('settings.json','w') as f:
        f.write(str(settings))
def setting():
    global theme_Combobox,theme_name
    setting_window = Toplevel()
    setting_window.geometry('400x200')
    theme_name = StringVar()
    Label(setting_window,text='选择一个主题: ').pack(side='left')
    theme_Combobox = Combobox(setting_window,state="readonly",textvariable=theme_name,values=style.theme_names())
    theme_name.set(settings["theme"])
    theme_Combobox.pack(side='left',fill='x')
    theme_Combobox.bind('<<ComboboxSelected>>',lambda a:change_theme())

title_str = StringVar()
artist_str = StringVar()
album_str = StringVar()
time_str = StringVar()

info_Frame = Frame(window)
buttons_Frame = Frame(window)

img = Image.open('none.png')
photo = ImageTk.PhotoImage(img)
img_Label = Label(window, image=photo)
pos_Scale = Scale(from_=0, to=100, bootstyle="primary")
title_Label = Label(window, textvariable=title_str, font=('微软雅黑', 25))
artist_Label = Label(info_Frame, textvariable=artist_str, font=('微软雅黑', 15))
album_Label = Label(info_Frame, textvariable=album_str, font=('微软雅黑', 15))
ask_file_Button = Button(buttons_Frame, text="打开文件",
                         bootstyle=('primary', 'outline'), command=open_file)
setting_Button = Button(buttons_Frame, text="选项",
                         bootstyle=('primary', 'outline'), command=setting)
pause_Button = Button(buttons_Frame, text='⏯️',
                      bootstyle=('primary', 'outline'), command=pause)
next_Button = Button(buttons_Frame, text='⏭️',
                     bootstyle=('primary', 'outline'), command=playnext)
last_Button = Button(buttons_Frame, text='⏮️',
                     bootstyle=('primary', 'outline'), command=playlast)
time_Label = Label(buttons_Frame, textvariable=time_str, font=('微软雅黑', 10))
Scale(bootstyle="primary")

artist_Label.pack(side='left', fill='x', padx=5, pady=5)
Label(info_Frame, text='•', font=('微软雅黑', 25)).pack(side='left')
album_Label.pack(side='left', fill='x', padx=5, pady=5)
last_Button.pack(side='left', fill='x', padx=20, pady=5)
pause_Button.pack(side='left', fill='x', padx=5, pady=5)
next_Button.pack(side='left', fill='x', padx=20, pady=5)
ask_file_Button.pack(side='left', fill='x', padx=5, pady=5)
setting_Button.pack(side='left', fill='x', padx=5, pady=5)
time_Label.pack(side='left', anchor='e', expand='yes', padx=5)
buttons_Frame.pack(side='bottom', fill='both')
pos_Scale.pack(side='bottom', fill='x')
img_Label.pack(side='left', pady=10, padx=20)
title_Label.pack(pady=5)
info_Frame.pack()



pos_Scale.bind("<Button-1>", lambda a: click())
pos_Scale.bind("<ButtonRelease-1>", lambda a: release())
img_Label.bind("<Double-Button-1>", lambda a: startfile('song.png'))
img_Label.bind("<Button-3>", lambda a: startfile('song.png'))
window_update()

f = open('song.png','w')
f.close()
with open('settings.json','r') as f:
    settings = eval(f.read())

style.theme_use(settings["theme"])
window.mainloop()
