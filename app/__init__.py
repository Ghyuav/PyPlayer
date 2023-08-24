from pygame import mixer
from mutagen import File
from mutagen.flac import FLAC
from mutagen.wave import WAVE

mixer.init()


def player_load(filename):
    mixer.music.load(filename)
    if filename.split('.')[-1] == 'mp3' or filename.split('.')[-1] == 'MP3':
        print('*****mp3*****')
        audio = File(filename)
        try:
            title = audio['TIT2'].text[0]
        except:
            title = filename.split('/')[-1].split('.')[0]
        try:
            album = audio['TALB'].text[0]
        except:
            album = 'unknow'
        try:
            artist = audio['TPE1'].text[0]
        except:
            artist = 'unknow'
        try:
            img_data = audio['APIC:'].data
        except:
            img_data = ''
        length = audio.info.length
        return [title, artist, album, img_data,length]
    elif filename.split('.')[-1] == 'flac' or filename.split('.')[-1] == 'FLAC':
        
        print('*****flac*****')
        audio = FLAC(filename)
        try:
            title = audio['title'][0]
        except:
            title = filename.split('/')[-1].split('.')[0]
        try:
            album = audio['album'][0]
        except:
            album = 'unknow'
        try:
            artist = audio['artist'][0]
        except:
            artist = 'unknow'
        pics = audio.pictures
        for p in pics:
            if p.type == 3:  # front cover
                img_data = p.data
            else:
                img_data = ''
        length = audio.info.length 
        return [title, artist, album,img_data,length]
    elif filename.split('.')[-1] == 'wav' or filename.split('.')[-1] == 'WAV':
        
        print('*****wave*****')
        audio = WAVE(filename)

        title = filename.split('/')[-1].split('.')[0]
        try:
            album = audio['album'][0]
        except:
            album = 'unknow'
        try:
            artist = audio['artist'][0]
        except:
            artist = 'unknow'
        img_data = ''
        length = audio.info.length
        return [title, artist, album,img_data,length]
    else:
        print('*****unknow*****')
        title = filename.split('/')[-1].split('.')[0]
        album = 'unknow'
        artist = 'unknow'
        img_data = None
        length = None
        return [title, artist, album,img_data,length]


def player_play():
    mixer.music.play()



def get_pos():
    return mixer.music.get_pos()


def set_pos(arg):
    return mixer.music.set_pos(arg)
