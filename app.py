import tkinter as tkr #used to develop GUI
from tkinter.simpledialog import askstring
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random
import time

option = Options()
option.add_argument("--headless")

music_player = tkr.Tk()
music_player.title('Shuffle')
music_player.geometry('450x350')

def exit():
    driver.stop_client()
    driver.quit()
    music_player.destroy()

album = askstring('Album link', 'Insert bandcamp album link')
driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),
options=option)
driver.get(album)
list = driver.find_elements_by_class_name('track-title')
playlist = {}
song_list = {}
link_list = []
for element in list:
    song_list[element.get_attribute('innerHTML')] = element.find_element_by_xpath('..').get_attribute('href')
song_names = []
for i in song_list.keys():
    song_names.append(i)
random.shuffle(song_names)

play_list = tkr.Listbox(music_player, font='Helvetica 12 bold', bg='yellow',
selectmode=tkr.SINGLE)
for item in song_names:
    pos = 0
    play_list.insert(pos, item)
    pos += 1

def play():
    if str(driver.current_url) != str(song_list[play_list.get(tkr.ACTIVE)]):
        link = song_list[play_list.get(tkr.ACTIVE)]
        driver.get(link)
        time.sleep(1)
    driver.find_element_by_class_name('playbutton').click()
    Button1.configure(state='disabled')
    Button2.configure(state='normal')
def pause():
    driver.find_element_by_class_name('playbutton').click()
    Button1.configure(state='normal')
    Button2.configure(state='disabled')
def next():
    if Button2['state'] == tkr.NORMAL:
        pause()
    selected_song = play_list.curselection()
    next_song = 0
    if len(selected_song) > 0:
        last_song = int(selected_song[-1])
        play_list.selection_clear(selected_song)
        if last_song < play_list.size() - 1:
            next_song = last_song + 1
    play_list.activate(next_song)
    play_list.selection_set(next_song)
    play()
# def progress():
     # TODO

Button1 = tkr.Button(music_player, width=5, height=3, font='Helvetica 12 bold',
text='PLAY', command=play, bg='blue', fg='white')
Button2 = tkr.Button(music_player, width=5, height=3, font='Helvetica 12 bold',
text='PAUSE', command=pause, state='disabled', bg='purple', fg='white')
Button3 = tkr.Button(music_player, width=5, height=3, font='Helvetica 12 bold',
text='NEXT', command=next, bg='orange', fg='white')

var = tkr.StringVar()
song_title = tkr.Label(music_player, font='Helvetica 12 bold',
textvariable=var)

song_title.pack()
Button1.pack(fill='x')
Button2.pack(fill='x')
Button3.pack(fill='x')
play_list.pack(fill='both', expand='yes')
music_player.protocol('WM_DELETE_WINDOW', exit)
music_player.mainloop()
