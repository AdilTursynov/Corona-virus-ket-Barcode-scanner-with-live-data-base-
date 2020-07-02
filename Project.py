import cv2
import pyzbar.pyzbar as pyzbar
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk
from PIL import Image,ImageTk
import matplotlib.pyplot as plt
import datetime
import numpy as np
import geocoder
def location():
    g = geocoder.ip('me')
    return (g.latlng)
window = tk.Tk()
window.geometry("305x310") #window's size
window.title(" Covid-19 KET KET  ") #title of win
name = tk.Label(text="Policemans No :") #text
name.grid(column=0, row=1) # place of text
temp = tk.Label(text="Temp :")
temp.grid(column=0, row=3)
nameEntry = tk.Entry()
nameEntry.grid(column=0, row=2)#input place
tempEntry = tk.Entry()
tempEntry.grid(column=0, row=4)
bos = tk.Label(text="")
bos.grid(column=0, row=5)
def sent(nameEntry,tempEntry):
    return  Codes().database().insert_row([tempEntry.get(), Codes().barscan(), str(location()), nameEntry.get(),str(datetime.datetime.now())]) #writer to google sheets
class Codes():
   def barscan(self):
        cap = cv2.VideoCapture(0) # online cam shower
        font = cv2.FONT_HERSHEY_PLAIN

        while True:
            c = 0
            _, frame = cap.read() # read  video

            decodedObjects = pyzbar.decode(frame) #find code in video
            for obj in decodedObjects: #show every found code
                cv2.putText(frame, str(obj.data), (50, 50), font, 2,
                            (255, 0, 0), 3)
                c += 1

            cv2.imshow("Frame", frame)

            key = cv2.waitKey(1) # wait time

            if c == 1:
                break
        a = str(obj.data).replace("b", " ") #code wich found function
        return (a)

   def database(self):
       scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"] #requests
       creds = ServiceAccountCredentials.from_json_keyfile_name("Data.json", scope) # keyfile for API
       client = gspread.authorize(creds) #read with API keys
       sheet = client.open("data").sheet1  # Open the spreadhseet
       return sheet
class Mine(Codes):
    def __init__(self, **kwargs):
        super(Mine, self).__init__(**kwargs)
        self.sheet=Codes().database()
        self.w=Codes()
    def p(self):
        col = self.sheet.col_values(4) #data from google sheets
        a = []
        for i in col:
            a.append(float(i))

        data = a

        # fixed bin size
        bins = np.arange(35, 40,0.21)  # fixed bin size

        plt.xlim([min(data) -1, max(data) + 1])

        plt.hist(data, bins=bins, alpha=0.5)
        plt.title('Analyze of data , which we save')
        plt.xlabel('Temperatura')
        plt.ylabel('count')

        plt.show()
    def wr(self):
        return sent(tempEntry,nameEntry) #write code which read barcode reader

    def pas(self,window):

        button = tk.Button(window, text="Barcode ", command=Mine().wr , bg="pink") #button for barcode reader
        button.grid(column=0, row=6)
        button2 = tk.Button(window, text="Statistics", command=Mine().p, bg="pink") #button for showing statistics
        button2.grid(column=0, row=7)
        image = Image.open('download.jpg') #shower image on window
        image.thumbnail((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label_image = tk.Label(image=photo)
        label_image.grid(column=0, row=0)
        window.mainloop() #player for window


if __name__ == "__main__":
    Mine().pas(window)