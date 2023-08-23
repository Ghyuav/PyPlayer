from app import *
from tkinter.ttk import *
from ttkbootstrap import Style
from tkinter import filedialog,StringVar,messagebox
from math import floor
from PIL import Image,ImageTk
from windnd import hook_dropfiles
from os import startfile
style = Style()
window = style.master

style.theme_use('darkly')
window.title('Player')
# window.iconbitmap(r'profile\ico.ico')
window.state('zoomed')
length = 1
if_clicking = 0
play_progress = 0
mixer.music.set_endevent()
def window_update():
    global length,if_clicking,play_progress,time_str
    def w_update():
        global length
        global play_progress
        if if_clicking:
            pass
        else:
            try:
                pos_Scale.set((play_progress/(length*1000))*100)
                min = str(floor((play_progress/1000)/60))
                second = str(round((play_progress/60000-floor(play_progress/60000))*60))
                if len(min) == 1:
                    min = f'0{min}'
                if len(second) == 1:
                    second = f'0{second}'
                time_str.set(f'{min}:{second}')
            except:
                pass
        window.update()
        window.after(100,w_update)
        if mixer.music.get_busy():
            play_progress += 100
    w_update()
def open_file(path='',mode=''):
    global length,play_progress,photo
    if path:
        if mode:
            dir = path
        else:
            try:
                dir = b'\n'.join(path).decode(encoding='gbk').replace('\\','/')
            except:
                dir = b'\n'.join(path).decode(encoding='utf-8').replace('\\','/')
    else:
        dir = filedialog.askopenfilename()
    try:
        data = player_load(dir)
    except :
        messagebox.showerror('标题','不支持的类型:'+dir.split('.')[-1])
    if data:
        pass
    else:
        data = ['','','','','']
    if data[0]:
        title_str.set(data[0])
        window.title(f'{data[0]} - PyPlayer')
    else:
        title_str.set(dir.split('/')[-1].split('.')[0])
        window.title(f'{dir.split("/")[-1].split(".")[0]} - PyPlayer')
    artist_str.set(data[1])
    album_str.set(data[2])
    try:
        with open('song.png','wb') as f:
            f.write(data[3])
        
        img = Image.open('song.png').resize((512,512))
    except:
        img = Image.open('none.png').resize((512,512))
    photo = ImageTk.PhotoImage(img)
    img_Label.configure(image=photo)
    length = data[4]
    play_progress = 0 
    play()
def play():
    global play_progress
    play_progress = 0
    player_play()

def click():
    global if_clicking
    if_clicking = 1
def release():
    global if_clicking,play_progress
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

title_str = StringVar()
artist_str = StringVar()
album_str = StringVar()
time_str = StringVar()

info_Frame = Frame(window)
buttons_Frame = Frame(window)

img = Image.open('none.png')
photo = ImageTk.PhotoImage(img)
img_Label = Label(window,image=photo)
pos_Scale = Scale(from_=0,to=100,bootstyle="info")
title_Label = Label(window,textvariable=title_str,font=('微软雅黑',25))
artist_Label = Label(info_Frame,textvariable=artist_str,font=('微软雅黑',15))
album_Label = Label(info_Frame,textvariable=album_str,font=('微软雅黑',15))
ask_file_Button = Button(buttons_Frame,text="打开文件",bootstyle=('info', 'outline'),command=open_file)
pause_Button = Button(buttons_Frame,text='⏯️',bootstyle=('info', 'outline'),command=pause)
time_Label = Label(buttons_Frame,textvariable=time_str,font=('微软雅黑',10))
Scale(bootstyle="info")

img_Label.pack(pady=10,padx=20)
artist_Label.pack(side='left',fill='x',padx=5,pady=5)
Label(info_Frame,text='•',font=('微软雅黑',25)).pack(side='left')
album_Label.pack(side='left',fill='x',padx=5,pady=5)
pause_Button.pack(side='left',fill='x',padx=5,pady=5)
ask_file_Button.pack(side='left',fill='x',padx=5,pady=5)
time_Label.pack(side='left',anchor='e',expand='yes',padx=5)

buttons_Frame.pack(side='bottom',fill='both')
pos_Scale.pack(side='bottom',fill='x')
info_Frame.pack(side='bottom')
title_Label.pack(side='bottom',pady=5)

pos_Scale.bind("<Button-1>",lambda a: click())
pos_Scale.bind("<ButtonRelease-1>",lambda a:release())
img_Label.bind("<Double-Button-1>",lambda a:startfile('song.png'))
img_Label.bind("<Button-3>",lambda a:startfile('song.png'))
window_update()
hook_dropfiles(window, func=open_file)

window.mainloop()
