from tkinter import *
import pandas as pd
import cv2
import os
import json
from pytube import YouTube 
import ssl
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import numpy as np
import PIL.Image, PIL.ImageTk
import threading
import time
from tkinter.font import Font
#Autocomplete
from ttkwidgets.autocomplete import AutocompleteEntry
from placeDict import placeDict

download_pause = False
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
object_string = "plane window sky airport"
location_value = ""
search_response = ""
next_page_token = ""


def auth():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client

    youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey="insert-developer-key-here")
    return youtube

def search():
    youtube = auth()
    
    filename = f'{object_string}{location_value}/JSON/youtubeSearch{object_string}.json'

    request = youtube.search().list(
        part="snippet",
        location=location_value,
        locationRadius="50km",
        maxResults=50,
        pageToken=next_page_token,
        q= object_string,
        videoDimension='2d',
        type="video",
        videoDuration="short",
        access_token="oauth2-token",

    )
    response = request.execute()

    global search_response 
    search_response = response

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(response, f)



def parse():
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 5000)
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    filename = f'{object_string}{location_value}/JSON/youtubeSearch{object_string}.json'

    with open(f'{filename}') as data_file:    
        data = json.load(data_file)  

    next_page_check = "nextPageToken" in data
    print(next_page_check)
    if next_page_check == True: 
        global next_page_token
        next_page_token = data['nextPageToken']
    else:
        next_page_token = ""
    
    print(next_page_token)
    print(data['pageInfo'])

    norm = pd.json_normalize(data, record_path=['items']) 
    df = pd.DataFrame(norm)
    newDf= df[['snippet.title']].copy()
    youtubeLink = 'https://www.youtube.com/watch?v='
    newDf['videoLink'] = youtubeLink + df[['id.videoId']]
    newDf['snippet.publishTime'] = df[['snippet.publishTime']]
    newDf['id.videoId'] = df[['id.videoId']]
    newDf['snippet.liveBroadcastContent'] = df[['snippet.liveBroadcastContent']]
    newDf = newDf[newDf['snippet.liveBroadcastContent'] == 'none']
    return newDf

def download():
    ssl._create_default_https_context = ssl._create_unverified_context

    video_output = f'{object_string}{location_value}/Video/'
    newDf = parse()

    links = newDf['videoLink'].values.tolist()
    global download_pause
    while not(download_pause):
        for count, x in enumerate(links):
            print(count)
            vids = YouTube(x) 

            global vid_views
            vid_views = vids.views

            global vid_title
            vid_title = vids.title
            
            print(f"title: {vid_title}")
            print(f"views: {vid_views}")

            filtered = vids.streams.filter(file_extension='mp4', type='video')

            downloadable = filtered.get_lowest_resolution()

            print(f"Filesize: {downloadable._filesize/(1024*1024)}")
            if downloadable._filesize/(1024*1024) > 15:
                continue 

            os.makedirs(os.path.dirname(video_output), exist_ok=True)

            if download_pause == True:
                print("download stopped")
                break
            
            if os.path.isfile(f"{video_output}{downloadable.default_filename}") == True:
                print('file already exists')
                file_path = f"{video_output}{downloadable.default_filename}"
                vid = cv2.VideoCapture(file_path)
                height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
                width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)   
                aspect_ratio = width/height
                print(f"aspect ratio: {aspect_ratio}")
                if aspect_ratio < 2:
                    get_video(f"{video_output}{downloadable.default_filename}")
                    time.sleep(20)
                continue
            else:
                print('file does not exist')

            if downloadable._filesize == 0:
                pass
            else:
                downloadable.download(output_path=video_output)
                print(f"{video_output}{downloadable.default_filename}")

                file_path = f"{video_output}{downloadable.default_filename}"
                vid = cv2.VideoCapture(file_path)
                height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
                width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)   
                aspect_ratio = width/height
                print(f"aspect ratio: {aspect_ratio}")
                if aspect_ratio < 2:
                    get_video(f"{video_output}{downloadable.default_filename}")
                    time.sleep(20)
                else:
                    print("video is landscape")
        print('done with json, restarting')

            

        

main_window = Tk()

#Frame styling 

main_window.geometry("605x1080+0+0")
main_window.configure(background= 'blue')

#General Styling
myFont = Font(family="IBM Plex Sans Light", weight="normal", size=24)
subFont = Font(family="IBM Plex Sans", weight="normal", size=12)

mainFont = Font(family="IBM Plex Sans", size=24)


# Frame update, can go soon
count = 0
count_str = StringVar()
count_str.set('hey')

screen_width = 1600
screen_height = 900

video_x_values = 0
video_y_values = 22

newWindow = Toplevel(main_window)
newWindow.geometry("605x1080+605+0")
newWindow.configure(bg="black")

def get_video(filename):
    class App:
        def __init__(self, window, window_title, video_source):
            self.window = window
            self.window.title(window_title)
            self.video_source = video_source
            self.window.overrideredirect(1)
            window.overrideredirect(1)

            # open video source
            self.vid = MyVideoCapture(video_source)

            # Create a canvas that can fit the above video source size
            self.canvas = Canvas(window, width = self.vid.width, height = self.vid.height, borderwidth = 0, highlightthickness = 0)
            self.canvas.pack()

            global video_x_values
            global video_y_values

            print(video_x_values)
            print(video_y_values)

            # Frame Updates in ms
            self.delay = 150
            self.update()


            #self.window.mainloop()
        def update(self):
            ret, frame = self.vid.get_frame()
            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
            
            self.window.after(self.delay, self.update)

        

        

    class MyVideoCapture:
        def __init__(self, video_source):
            # Open the video source
            self.vid = cv2.VideoCapture(video_source)
            if not self.vid.isOpened():
                raise ValueError("Unable to open video source", video_source)
    
            # Get video source width and height
            self.original_width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.original_height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.aspect_ratio = self.original_width / self.original_height
            
            # Desired Height of Video
            self.height = 800
            self.width = self.height * self.aspect_ratio

        def get_frame(self):
            if self.vid.isOpened():
                ret, frame = self.vid.read()
                if ret:
                    frame = cv2.resize(frame,(int(self.width), self.height))
                    # Return a boolean success flag and the current frame converted to BGR
                    return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                else:
                    return (ret, None)
            else:
                return (ret, None)

        # Release the video source when the object is destroyed
        def __del__(self):
            if self.vid.isOpened():
                self.vid.release()

    # Destroy previous videos
    for widget in newWindow.winfo_children():
        widget.destroy()

    # Title above video
    global vid_title
    title_var = StringVar()
    title_var.set(vid_title)
    title_label = Label(newWindow, textvariable=title_var, anchor='w', fg='white', bg='black', wraplength=2160, justify=LEFT, font= mainFont)

    # Views above video
    global vid_views
    views_var = StringVar()
    views_var.set(f"views: {vid_views}")
    view_label = Label(newWindow, textvariable=views_var, anchor='w', fg='white', bg='black', wraplength=2160, justify=LEFT, font= mainFont)

    title_label.pack(fill='both')
    view_label.pack(fill='both')

    # Remove Toplevel if want to show in main_window
    App(newWindow, f"Video {filename}", filename)
    
def destroy_all():
    global download_pause
    download_pause = True
    for widget in newWindow.winfo_children():
        widget.destroy()
    global video_x_values
    global video_y_values
    video_x_values = 0
    video_y_values = 0


def begin_threading():
    
    global download_pause
    download_pause = False

    threading.Thread(target=final).start()


coord_dict = placeDict

def gui():

    def retrieve_location():
        global location_value
        place = user_input.get("1.0","end-1c")
        location_value = coord_dict[place]
        print(location_value)
        object_var.set(f"Travelling to {place} {location_value}")

    object_var = StringVar()

    main_question = Label(main_window, text="Where would you like to go?", anchor='center', fg='white', bg='blue', font= myFont)
    input_label = Label(main_window, textvariable=object_var, anchor='w', fg='white', bg='blue', font= myFont)
    press_enter = Label(main_window, text="then pick a city and press 'enter' to go", anchor='center', fg='white', bg='blue', font= subFont)

    press_escape = Label(main_window, text="first press 'esc' to leave", anchor='center', fg='white', bg='blue', font= subFont)

    def retrieve_input_autocomplete():
        global location_value
        place = auto_complete.get()
        location_value = coord_dict[place]
        print(location_value)
        object_var.set(f"Travelling to {place}")

    auto_complete = AutocompleteEntry(
    main_window, 
    width=30, 
    font=('', 18),
    completevalues=coord_dict
    )
    auto_complete.focus_force()

    def Return(e):
        destroy_all()
        time.sleep(5)
        retrieve_input_autocomplete()
        begin_threading()
        
    def Escape(e):
        destroy_all()
        global location_value
        object_var.set("")
        
    from threading import Timer, Thread


    main_window.bind('<Return>', Return)
    main_window.bind('<Escape>', Escape)


    main_question.place(x=300, y=400, anchor='center')
    auto_complete.place(x=300, y=450, anchor='center')
    press_escape.place(x=300, y=500, anchor='center')
    press_enter.place(x=300, y=550, anchor='center')
    input_label.place(x=300, y=600, anchor='center')
    
    main_window.mainloop()

def final():
    for x in range(1):
        if download_pause == True:
            print("for loop stopped")
            break
        print(f"Loop Number : {x}")
        search()
        parse()
        download()

auth()
gui()
