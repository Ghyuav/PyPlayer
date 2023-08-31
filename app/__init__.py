from pygame import mixer
from tinytag import TinyTag

mixer.init()
chazhi = 0

def player_load(filename):
    global chazhi
    mixer.music.load(filename)
    chazhi = 0

    audio = TinyTag.get(filename,image=1)

    title = filename.split('/')[-1].split('.')[0]
    album = 'unknow'
    artist = 'unknow'

    if audio.title:
        title = audio.title
    if audio.album:
        album = audio.album
    if audio.artist:
        artist = audio.artist

    img_data = audio.get_image()

    length = audio.duration
    return [title, artist, album, img_data,length]


def player_play():
    mixer.music.play()



def get_pos():
    return mixer.music.get_pos()+chazhi*1000


def set_pos(arg):
    global old_v,chazhi
    old_v = get_pos()/1000
    chazhi += arg-old_v
    return mixer.music.set_pos(arg)

def play_end():
    global chazhi
    chazhi =  0