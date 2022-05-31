#MELİKE BUĞA
#Python 3.8.2 ile Tkinter, Pygame, Mutagen kütüphaneleri kullanarak mp3 oynatıcısı yapılmıştır.


#Gerekli kütüphanelerin yüklenmesi
from tkinter import *
import pygame
from tkinter import filedialog
import os
from pygame.mixer import pause
from mutagen.mp3 import MP3
import time
import tkinter.ttk as ttk

#Tkinter'ı t olarak kullanacağız ve pencerenin yapısını belirliyoruz
t = Tk()
t.title("Python ile Müzik Oynatıcısı")
t.geometry("500x400")

#Pygame mixer'inin başlatma durumunu kontrol eder
pygame.mixer.init()

#Şarkı uzunluğunu gösterir
def play_time():
    #if döngüsü ile çift zamanlamayı kontrol et
    if stopped:
        return
    #Geçerli Şarkının Geçen Süresini Yakala
    current_time = pygame.mixer.music.get_pos() /1000
    #Zaman biçimine dönüştür 
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    #Çalma listesinden Şarkı başlığını al
    song = song_box.get(ACTIVE)
    #dizin yapısı ekle
    song = f"D:/python example/musicplayerpython/audio/{song}.mp3"
    #Mutagen ile Şarkıyı Yükle
    song_mut = MP3(song)
    #Şarkı Uzunluğunu Al
    global song_length
    song_length = song_mut.info.length
    #Zaman biçimine dönüştür
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    #Geçerli zamanı 1 saniye artır, burda status bar'ın yazdığı zamanın 1 saniye artırılmasının sebebi ise şarkının geçmesini sağlamaktır.
    current_time +=1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')
    elif paused:    
        pass
    elif int(my_slider.get()) == int(current_time):
        #Slider konumlandırmak için güncellenir
        slider_position = int(song_length)    
        my_slider.config(to=slider_position, value=current_time)
    else:
        #Slider konumunu güncelle
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        #zaman formatına dönüştürülmüş
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        #status bar çıkış zamanı güncellenir
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length} ')
        #bunu bir saniye ilerletir
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    
    #zamanı güncelle
    status_bar.after(1000, play_time)

#şarkı ekleme fonksiyonu
def add_song():
    song = filedialog.askopenfilename(initialdir='audio/', title="Select a song",filetypes=(("mp3 files", "*.mp3"),))
    
    #dizin bilgisini ve .mp3 uzantısını çıkarıyoruz
    song = song.replace("D:/python example/musicplayerpython/audio", "")
    song = song.replace(".mp3", "")

    #playliste şarkıyı ekle
    song_box.insert(END, song)

#playliste birden çok şarkı ekleyebilmek için fonksiyon
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Select a song",filetypes=(("mp3 files", "*.mp3"),))
    
    #Şarkı listesinde dolaşın ve dizin bilgisini ve .mp3 uzantısını değiştirin
    for song in songs:
        song = song.replace("D:/python example/musicplayerpython/audio", "")
        song = song.replace(".mp3", "")
        #Şarkıyı çalma listesine ekle
        song_box.insert(END, song)

#Seçilen şarkıyı oynatma fonksiyonu
def play():
    #Şarkının çalınabilmesi için durdurulan değişkeni false olarak ayarlayın
    global stopped
    stopped=False
    song= song_box.get(ACTIVE)
    song = f"D:/python example/musicplayerpython/audio/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #Şarkı uzunluğunu almak için play_time işlevini çağırın
    play_time()

#Mevcut şarkıyı çalmayı durdur
global stopped
stopped = False

#Şarkıyı durdurma fonksiyonu
def stop():
    #Slider ve status bar kısımları sıfırlıyoruz
    status_bar.config(text="")
    my_slider.config(value=0)
    #çalma listesinden şarkıyı durdur
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    #status bar temizlenir
    status_bar.config(text="")

    #stop değişkenini true olarak ayarla
    global stopped
    stopped = True

#çalma listesindeki bir sonraki şarkıyı çal
def next_song(): 
    #Slider ve status bar kısımları sıfırlıyoruz
    status_bar.config(text="")
    my_slider.config(value=0)

    #geçerli şarkı numarasını alın.
    next_one = song_box.curselection()
    #geçerli şarkı numarasına bir tane ekleyin.
    next_one = next_one[0] + 1
    #çalma listesinden şarkı başlığını alın
    song = song_box.get(next_one)
    #şarkı başlığına dizin yapısı ve .mp3 ekleyin.
    song = f"D:/python example/musicplayerpython/audio/{song}.mp3"
    #şarkıyı yükle ve çal.
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #listedeki şarkının aktif çubuğu temizle.
    song_box.selection_clear(0, END)

    #yeni şarkı çubuğunu etkinleştir.
    song_box.activate(next_one)

    #aktif çubuğu sonraki şarkıya ayarla.
    song_box.selection_set(next_one, last=None)

#play previous song in playlist
def previous_song():
    #Slider ve status bar kısımları sıfırlıyoruz
    status_bar.config(text="")
    my_slider.config(value=0)
    #geçerli şarkı numarasını alın.
    previous_one = song_box.curselection()
    #geçerli şarkı numarasına bir tane ekleyin.
    previous_one = previous_one[0] - 1
    #çalma listesinden şarkı başlığını alın.
    song = song_box.get(previous_one)
    #şarkı başlığına dizin yapısı ve .mp3 ekleyin.
    song = f"D:/python example/musicplayerpython/audio/{song}.mp3"
    #şarkıyı yükle ve çal.
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    #listedeki şarkının aktif çubuğu temizle.
    song_box.selection_clear(0, END)
    #yeni şarkı çubuğunu etkinleştir.
    song_box.activate(previous_one)
    #aktif çubuğu önceki şarkıya ayarla
    song_box.selection_set(previous_one, last=None)

#listeden bir şarkı sil
def delete_song():
    stop() 
    #şu anda seçili şarkıyı sil
    song_box.delete(ANCHOR)
    #müzik çalıyorsa durdur
    pygame.mixer.music.stop()

#listede tüm şarkıları sil
def delete_all_songs():
    stop()
    #tüm şarkıları sil
    song_box.delete(0, END)
    #müzik çalıyorsa durdur
    pygame.mixer.music.stop()

#global duraklama değişkeni oluştur
global paused
paused = False

#mevcut şarkıyı duraklatın ve başlatın
def pause(is_paused):
    global paused
    paused=is_paused
    if paused:
        #unpause
        pygame.mixer.music.unpause()
        paused=False
    else:
        #pause
        pygame.mixer.music.pause()
        paused = True

#Slider fonksiyonu
def slide(x):
    song= song_box.get(ACTIVE)
    song = f"D:/python example/musicplayerpython/audio/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))

#Ses ayarlama fonksiyonu
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()

#ana çerçeve oluşturma
master_frame = Frame(t)
master_frame.pack(pady=20)

#şarkı çalma listesi kutusu oluştur
song_box = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground="gray", selectforeground="black")
song_box.grid(row=0, column=0)

#kullanıcı kontrol butonlarının resimlerini tanımla
pause_img = PhotoImage(file="D:/python example/musicplayerpython/img/pauseio.png")
play_img = PhotoImage(file="D:/python example/musicplayerpython/img/playio.png")
stop_img = PhotoImage(file="D:/python example/musicplayerpython/img/stopio.png")
back_img = PhotoImage(file="D:/python example/musicplayerpython/img/backio.png")
forward_img = PhotoImage(file="D:/python example/musicplayerpython/img/forwardio.png")

#kullanıcı kontrol çerçevesi oluştur
controls = Frame(master_frame)
controls.grid(row=1, column=0, pady=20)

#Ses çerçevesini oluşturma
volume_frame = LabelFrame(master_frame, text="Ses")
volume_frame.grid(row=0, column=1, padx=20)

#kullanıcı kontrol butonlarını tanımlama
pause_button= Button(controls, image=pause_img, borderwidth=0, command=lambda: pause(paused))
play_button= Button(controls, image=play_img, borderwidth=0, command=play)
stop_button= Button(controls, image=stop_img, borderwidth=0, command=stop)
back_button = Button(controls, image=back_img, borderwidth=0, command=previous_song)
forward_button = Button(controls, image=forward_img, borderwidth=0, command=next_song)

#kullanıcı kontrol butonlarını konumlandır
pause_button.grid(row=0, column=3, padx=10)
play_button.grid(row=0, column=2, padx=10)
stop_button.grid(row=0, column=4, padx=10)  
back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)

#Playliste yeni şarkı ekleme menüsünü oluşturma
menu = Menu(t)
t.config(menu=menu)
add_songs_menu =Menu(menu)
menu.add_cascade(label="Şarkı Ekle", menu=add_songs_menu)
add_songs_menu.add_command(label="Listeye Şarkı Ekle", command=add_many_songs)

#Playlistten şarkı silme menüsünü oluşturma
remove_song_menu =Menu(menu)
menu.add_cascade(label="Şarkı Sil", menu=remove_song_menu)
remove_song_menu.add_command(label="Şarkıyı Sil", command=delete_song)
remove_song_menu.add_command(label="Bütün Şarkıları Sil", command=delete_all_songs)

#status bar oluşturma
status_bar= Label(t, text="", bd=1, relief=GROOVE, anchor=E )
status_bar.pack( fill=X, side=BOTTOM, ipady=2)

#müzik konumu slider ını oluşturma
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)

#ses için slider oluşturma
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.grid(pady=10)

t.mainloop()