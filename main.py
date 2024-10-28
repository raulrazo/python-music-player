# Import dependencies

import pygame
from pygame import mixer
from tkinter import *
from tkinter import filedialog
from ttkbootstrap.constants import *
import ttkbootstrap as tb
import os

current_volume = 0.1
mixer.init()
current_song = None
timer_id = None
playlist = []
paused = False
remaining_duration = 0

def start_timer(callback):
    global timer_id, paused, remaining_duration
    if paused:
        return
    
    if remaining_duration > 0:
        remaining_duration -= 1
        song_duration_label.config(text=remaining_duration)
        timer_id = root.after(1000, start_timer, callback)
    else:
        callback()

def pause_timer():
    global paused, timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None
        paused = True

def unpaused_timer():
    global paused, timer_id, remaining_duration
    if paused:
        paused = False  
        start_timer(play_next_song)
        
def stop_timer():
    if timer_id is not None:
        root.after_cancel(timer_id)

def play_single():
    global paused, remaining_duration
    filename = filedialog.askopenfilename(initialdir="~/", title="Please select a field")
    song_title = filename.split("/")[-1]

    try:
        if current_song is not None:
            mixer.music.stop()
        mixer.music.load(filename)
        mixer.music.set_volume(current_volume)
        mixer.music.play()
        song_title_label.config(text="Now Playing : " + str(song_title), bootstyle="success") 
        remaining_duration = int(mixer.Sound(filename).get_length())
        start_timer(play_next_song)
    except pygame.error:
        song_title_label.config(bootstyle="warning", text="Error playing song")

def play_next_song():
    global paused, remaining_duration
    if not playlist:
        song_title_label.config(text="All Songs Have Been Played", bootstyle="success")
    song_path, song_title = playlist[0]
    try:
        if current_song is not None:
            mixer.music.stop()
        mixer.music.load(song_path)
        mixer.music.set_volume(current_volume)
        mixer.music.play()
        song_title_label.config(bootstyle="success", text="Now Playing : " + str(song_title))
        remaining_duration = int(mixer.Sound(song_path).get_length())
        if timer_id is not None:
            stop_timer()
        start_timer(play_next_song)
    except pygame.error:
        song_title_label.config(bootstyle="warning", text="Error playing song")
    playlist.pop(0)
    song_titles = [song[1] for song in playlist]
    song_list_string = "\n".join(song_titles)
    playlist_label.config(text=song_list_string)

def play_playlist():
    foldername = filedialog.askdirectory(initialdir="~/", title="Please Select a Folder")
    for root, _, files in os.walk(foldername): 
        for file in files:
            if file.lower().endswith((".mp3", ".wav", ".ogg", ".flac")):
                song_path = os.path.join(root, file)
                playlist.append([song_path, file])
    song_titles = [song[1] for song in playlist]
    song_list_string = "\n".join(song_titles)
    playlist_label.config(text=song_list_string)
    play_next_song()

def change_volume(volume):
    try:
        global current_volume
        current_volume = 1.0 - round(float(volume), 1)
        mixer.music.set_volume(current_volume)
    except Exception as e:
        print(e)
        song_title_label.config(bootstyle="warning", text="Track Hasn\'t Been Selected Yet")

def song_toggle():
    global paused
    if paused:
        try:
            mixer.music.unpause()
            unpaused_timer()
            paused = False
            toggle_button.config(text="Pause")
        except Exception as e:
            print(e)
            song_title_label.config(bootstyle="warning", text="Track Hasn\'t Been Selected Yet")
    else:
        try: 
            mixer.music.pause()
            pause_timer()
            paused = True
            toggle_button.config(text="Unpause")
        except Exception as e:
            print(e)
            song_title_label.config(bootstyle="warning", text="Track Hasn\'t Been Selected Yet")

def next_song():
    global playlist
    if not playlist:
        song_title_label.config(text="All Songs Have Been Played", bootstyle="success")
        return
    play_next_song()





        



# Instantiate Window
root = tb.Window(themename="journal")
root.title = ("Music Player")
root.geometry("900x500")

main_frame = tb.Frame(root)
main_frame.pack(side="top", fill="both", expand=True) # Sets position

title = tb.Label(main_frame, text="Python Custom Music Player", font=("Helvetica", 28), bootstyle="primary").pack(pady=5, padx=5)

# Song title
song_title_label = tb.Label(main_frame, text="Please Add Song", font=("Helvetica", 15))
song_title_label.pack(padx=10, pady=10)

song_duration_label = tb.Label(main_frame, text="0", font=("Helvetica", 10))
song_duration_label.pack(side="top", padx=5, pady=5)

# Grab song
select_button = tb.Button(main_frame, text="Select Song", bootstyle="secondary outline", command=play_single).pack(pady=5)

# Toggle button
toggle_button = tb.Button(main_frame, text="Pause", bootstyle="secondary outline", command=song_toggle)
toggle_button.pack(pady=5)

# Volume frame
volume_frame = tb.Frame(root)
volume_frame.pack(side="right", fill="both", expand=True)
volume = tb.Scale(volume_frame, orient="vertical", length=500, command=change_volume).pack(side="right", padx=15, pady=5)
volume_label = tb.Label(volume_frame, text="Volume Slider", bootstyle="primary", font=("Helvetica", 15)).pack(side="right", padx=5)

# Playlist frame
playlist_frame = tb.Frame(root)
playlist_frame.pack(side="left", fill="both", expand=True)

playlist_button = tb.Button(playlist_frame, text="Select Playlist", bootstyle="primary outline", command=play_playlist)
next_song_button = tb.Button(playlist_frame, text="Next Song", bootstyle="primary outline", command=next_song)
playlist_button.pack(side="top", padx=5, pady=5)
next_song_button.pack(side="top", padx=1, pady=5)

playlist_view = tb.LabelFrame(playlist_frame, text="Playlist", height=600, width=500, bootstyle="primary")
playlist_view.pack(side="top", padx=5, pady=5)

playlist_label = tb.Label(playlist_view, text="", bootstyle="primary", font=("Helvetica", 10))
playlist_label.pack(side="top", padx=5, pady=5)





root.mainloop()

