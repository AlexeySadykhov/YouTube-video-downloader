import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from PIL import ImageTk
from urllib.request import urlopen
import pytube


def download():
    try:
        status_bar['text'] = 'Downloading...'
        status_bar['foreground'] = 'red'
        window.update()
        yt = pytube.YouTube(url_entry.get())
        mode = mode_box.get()
        resolution = quality_box.get()
        if mode == 'Download video':
            stream = yt.streams.get_by_resolution(resolution)
        else:
            stream = yt.streams.get_audio_only()
        stream.download()
        status_bar['text'] = 'Downloaded'
        status_bar['foreground'] = 'green'
        mb.showinfo('Ready', 'Video has been downloaded')
        download_btn['state'] = 'disabled'
    except Exception:
        status_bar['text'] = 'Error'
        status_bar['foreground'] = 'red'
        mb.showerror("Error", "Undefined error occurred. Try to use another resolution.")


def parse():
    if not url_entry.get():
        mb.showerror('Error', 'There is no link.')
    else:
        try:
            status_bar.pack(side='bottom', fill='x')
            window.update()
            yt = pytube.YouTube(url_entry.get())
            window.geometry('500x500')
            download_btn.pack(side='bottom', fill='x')
            mode_box.pack(side='bottom', fill='x')
            mode_label.pack(side='bottom', fill='x')
            quality_box['values'] = [stream.resolution for stream in yt.streams.filter(progressive=True)]
            quality_box.current(0)
            quality_box.pack(side='bottom', fill='x')
            quality_label.pack(side='bottom', fill='x')
            video_title = tk.Label(master=window, text=yt.title)
            video_title.pack(side='bottom', fill='x')
            img_data = urlopen(yt.thumbnail_url).read()
            img = ImageTk.PhotoImage(data=img_data)
            canvas = tk.Canvas(master=window, width=640, height=480)
            canvas.pack(side='bottom', fill='both')
            canvas.create_image(0, 0, image=img, anchor='nw')
            status_bar['text'] = 'Parsed'
            status_bar['foreground'] = 'green'
            parse_btn['state'] = 'disabled'
            window.mainloop()
        except Exception:
            status_bar.pack_forget()
            mb.showerror("Error", "Can't find this link.")


window = tk.Tk()
window.title('YouTube video downloader')
window.geometry('500x150')
window.resizable(width=False, height=False)

url_label = tk.Label(master=window, text='Enter YouTube video URL:')
url_entry = tk.Entry(master=window)
parse_btn = tk.Button(master=window, text='Parse', command=parse)
download_btn = tk.Button(master=window, text='Download', command=download)
mode_box = ttk.Combobox(master=window, state='readonly', values=['Download video', 'Download only audio'])
mode_box.current(0)
mode_label = tk.Label(master=window, text='Mode:')
quality_box = ttk.Combobox(master=window, state='readonly')
quality_label = tk.Label(master=window, text='Quality:')
status_bar = tk.Label(master=window, text='Parsing...', foreground='red')

url_label.pack(side='top', fill='x')
url_entry.pack(side='top', fill='x')
parse_btn.pack(side='top', fill='x')

window.mainloop()
