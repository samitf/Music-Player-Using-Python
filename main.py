import os
import webbrowser
from tkinter import *  # gui import
from tkinter import ttk, filedialog
from tkinter import messagebox
import time
from pygame import mixer  # loading and playing sound

from gif import GifLabel

#from musixmatch import Musixmatch

# spotify :
# client_id = '70d379b91b534068923f49d7131fb6a7'
# client_secret = '58bf9b42e6a14c258d0bfc74ff387cdc'

#with easter eggs! Xo'FTW, Good Luck ?!

root = Tk()
root.title("My Music Player") #title
root.geometry("920x720")#Window Size
#root.geometry("920x720")
root.configure(bg="#00ADB5") #Window bg
root.resizable(False,False) #window Resizable option set True to resize
#root.attributes("-fullscreen", True)

mixer.init() #function takes several optional arguments to control the playback rate and sample size.

#function to open folder
def open_folder():
    path= filedialog.askdirectory() #asks for the location from os
    if path:
        os.chdir(path)
        songs=os.listdir(path)
#        print(songs)
        for song in songs:
            if song.endswith(".mp3"):
                playlist.insert(END,song)

def play_song():
    global music_name, music_duration
    music_name = playlist.get(ACTIVE)
    mixer.music.load(music_name)
    mixer.music.play()
    sound = mixer.Sound(music_name)
    music_duration = int(sound.get_length())
    #music.config(text=music_name[0:-4] + ' - ' + str(music_duration) + ' sec')
    root.after(1000, update_music_duration)
    update_music_slider()


def update_music_duration():
    global music_duration
    if music_duration > 0:
        music_duration -= 1
        music.config(text=music_name[0:-4] )#+ ' - ' + str(music_duration) + ' sec')
        root.after(1000, update_music_duration)
    else:
        music.config(text='')

def update_music_slider():
    current_time = mixer.music.get_pos() / 1000 # in seconds
    song_length = music_duration
    if song_length:
        slider_position = (current_time / song_length) * 100 # scale from 0 to 100
        music_slider.set(slider_position)
    else:
        music_slider.set(0)
    music_slider.after(1000, update_music_slider) # update every second

def next_song():
    current_song_index = playlist.curselection()
    if current_song_index:
        next_song_index = current_song_index[0] + 1
        if next_song_index < playlist.size():
            playlist.selection_clear(0, END)
            playlist.activate(next_song_index)
            playlist.selection_set(next_song_index)
            play_song()

def previous_song():
    current_song_index = playlist.curselection()
    if current_song_index:
        previous_song_index = current_song_index[0] - 1
        if previous_song_index >= 0:
            playlist.selection_clear(0, END)
            playlist.activate(previous_song_index)
            playlist.selection_set(previous_song_index)
            play_song()

def open_new_window():
    new_window = Toplevel(root)
    new_window.title("About Me")
    new_window.geometry("1000x800")
    new_window.config(bg="#2C3333")

    # create a button widget and associate a function with its command parameter
    def update_label_text():
        label.config(text="Hi, This My Python Mini Project ,\nmade by samit & jaden.\nvisit greatness\nGOAT",cursor="hand2")
    button = Button(new_window, text="Click Me!", bg="#2C3333", fg="#FFDE59", command=update_label_text,cursor="hand2")
    button.pack()

    # create a label widget and add it to the new window
    label = Label(new_window, text="Hooray!,\nYou Made it this far...", fg="#FFDE59", bg="#2C3333")
    label.pack()
    label.bind("<Button-1>", lambda event: open_url("https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05PJ?si=gGnuwb3gRTObPzvVfjVPLg"))

def open_url(url):
    webbrowser.open_new(url)

def get_lyrics():
    global music_name
    music_name = playlist.get(ACTIVE)
    lrc_file = music_name[:-3] + 'lrc' # assuming the LRC file has the same name as the MP3 file
    if os.path.exists(lrc_file):
        with open(lrc_file, 'r') as f:
            lines = f.readlines()
            lyrics = []
            for line in lines:
                if line.startswith('['):
                    line = line.split(']')[1] # remove the time stamp from the line
                    lyrics.append(line.strip()) # remove leading and trailing white spaces
            if lyrics:
                lyrics_window = Toplevel(root)
                lyrics_window.title('Lyrics')
                lyrics_window.geometry('600x600')
                lyrics_window.config(bg='#2C3333')
                lyrics_window.resizable(False, False)

                scrollbar = Scrollbar(lyrics_window)
                scrollbar.pack(side=RIGHT, fill=Y)

                llabel = Text(lyrics_window, yscrollcommand=scrollbar.set, fg='#FFDE59', bg='#2C3333', font=('Helvetica', 14), wrap=WORD)
                llabel.insert(END, '\n'.join(lyrics))
                llabel.pack(padx=10, pady=10, fill=BOTH, expand=True)
                llabel.config(state='disabled')

                ltext = Label(lyrics_window, text="LYRICS", font=("arial",20), fg="#030920", bg="#FFDE59")
                ltext.pack(pady=10)

                scrollbar.config(command=llabel.yview)

                lyrics_window.mainloop()
            else:
                messagebox.showinfo('No lyrics found', 'Sorry, no lyrics found for this song.')
    else:
        messagebox.showinfo('No LRC file found', 'Sorry, no LRC file found for this song.')




#icon
image_icon = PhotoImage(file="icons/logo.png") #Fetch titleLogo png
root.iconphoto(True, image_icon) #display titlelogo

Top = PhotoImage(file="icons/top.png") #top window png
Label(root, image=Top, bg="#222831").pack() #bg of top window


#gif
gif_label = GifLabel(root, gif_path='icons/gif.gif', width=500, height=500, bg="#00ADB5",cursor="hand2")
gif_label.place(x=450, y=600)
gif_label.bind("<Button-1>", lambda event: get_lyrics ())


#play button
play_button = PhotoImage(file="icons/play.png") #extract play logo
Button(root,image=play_button,bg="#00ADB5",bd=0,command=play_song,cursor="hand2").place(x=450, y=470) #bg and place play logo

#pause button
pause_button = PhotoImage(file="icons/pause.png") #extract play logo
Button(root,image=pause_button,bg="#00ADB5",bd=0,command=mixer.music.pause,cursor="hand2").place(x=570, y=670) #bg and place play logo

#resume button
resume_button = PhotoImage(file="icons/resume.png") #extract play logo
Button(root,image=resume_button,bg="#00ADB5",bd=0,command=mixer.music.unpause,cursor="hand2").place(x=450, y=740) #bg and place play logo

#stop button
stop_button = PhotoImage(file="icons/stop.png") #extract play logo
Button(root,image=stop_button,bg="#00ADB5",bd=0,command=mixer.music.stop,cursor="hand2").place(x=320, y=670) #bg and place play logo

#next button
next_button = PhotoImage(file="icons/next.png") #extract next logo
Button(root,image=next_button,bg="#00ADB5",bd=0,command=next_song,cursor="hand2").place(x=570, y=550) #bg and place next logo

#previous button
previous_button = PhotoImage(file="icons/previous.png") #extract previous logo
Button(root,image=previous_button,bg="#00ADB5",bd=0,command=previous_song,cursor="hand2").place(x=320, y=550) #bg and place previous logo


#music label

# create a new frame for the label
label_frame = Frame(root, bg='#030920')
label_frame.pack(fill=X, padx=20, pady=10)


# create the label inside the new frame
music = Label(label_frame, text="", font=("arial", 15), fg="#030920", bg="#FFDE59")
music.pack(padx=10, pady=5, side=LEFT)

#music menu
Menu=PhotoImage(file="icons/menu.png") #locate menu png
menu_label = Label(root,image=Menu,bg="#00ADB5")#.pack(padx=11,pady=48,side=RIGHT) #label,bg,placing
menu_label.place(x=1000, y=350) # set x and y coordinates as desired

music_frame = Frame(root,bg="#393E46",bd=2,relief=RIDGE) #frame inside menu label,bg,border,3d border
music_frame.place(x=1020,y=370,width=560,height=250) #size of frame


#open folder button
Button(root,text="Open Folder",width=15,height=2,font=("arial",10,"bold"),fg="#FFDE59",bg="#393E46",command=open_folder,cursor="hand2").place(x=1225,y=300) #folder button inside menu label,dimensions and font

scroll = Scrollbar(music_frame) #scroll bar for menu
playlist = Listbox(music_frame,width=100,font=("arial",10),bg="#333333",fg="#FFDE59",selectbackground="#00ADB5",cursor="hand2",bd=0,yscrollcommand=scroll.set) #define scrollbar attributes
scroll.config(command=playlist.yview)#command when scroll will be touched

scroll.pack(side=RIGHT, fill=Y) #positioning of scroll i.e x axis or y axis
playlist.pack(side=LEFT,fill=BOTH)  #




#music slider style
style = ttk.Style()
style.theme_use('default')
style.configure('My.Horizontal.TScale',
                sliderlength=10,
                sliderthickness=8,
                slidercolor='#FFFFFF',
                troughcolor='#FFDE59',
                bordercolor='#FFDE59',
                lightcolor='#FFDE59',
                darkcolor='#FFDE59',
                gripcount=0,
                gripmargin=0,
                background='#030920',
                foreground='#030920',
                troughrelief='flat',
                sliderrelief='flat')


#music slider



music_slider = ttk.Scale(root, from_=0, to=200, orient=HORIZONTAL, value=0, length=500,style='My.Horizontal.TScale',cursor="hand2")
music_slider.place(x=1050, y=630)
#music_slider.pack(pady=10)  # add padding to the bottom

#volume slider style
style = ttk.Style()
style.configure('My.Vertical.TScale',
                sliderlength=10,
                sliderthickness=8,
                slidercolor='#FFFFFF',
                troughcolor='#030920',
                bordercolor='#030920',
                lightcolor='#030920',
                darkcolor='#030920',
                gripcount=0,
                gripmargin=0,
                background='#FFDE59',
                foreground='#FFDE59',
                troughrelief='flat',
                sliderrelief='flat')

#volume control
# volume control
volume_slider = ttk.Scale(root, from_=1, to=0, orient=VERTICAL, value=0.5, length=200,style='My.Vertical.TScale',cursor="hand2", command=lambda x: mixer.music.set_volume(volume_slider.get()))
volume_slider.place(x=950, y=520)

#about button
about_button = PhotoImage(file="icons/about.png") #extract play logo
Button(root,image=about_button,bg="#00ADB5",bd=0,command=open_new_window,cursor="hand2").place(x=10, y=900) #bg and place play logo



root.mainloop()








