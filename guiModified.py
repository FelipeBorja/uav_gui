# Shivam Chourey
# A user interface that allows user to view the map, update the map, draw rectangle
# using mouse, and also allows user to input text. It also has window to display text.

import PIL.Image
import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import *

# Following class has the implementation for the User-interface
class UserInterfaceHIL(Frame):
    def __init__(self,master):

        Frame.__init__(self,master=None)
        # Frame.geometry("1080x960")
        global clickedChoose
        clickedChoose = 0
        self.x = self.y = 0
        self.canvas = Canvas(self, cursor="cross")
        self.canvas.config(width=1000, height=750)

        self.pointList = []

        # Scroll bars
        self.sbarv=Scrollbar(self,orient=VERTICAL)
        self.sbarh=Scrollbar(self,orient=HORIZONTAL)
        self.sbarv.config(command=self.canvas.yview)
        self.sbarh.config(command=self.canvas.xview)

        self.canvas.config(yscrollcommand=self.sbarv.set)
        self.canvas.config(xscrollcommand=self.sbarh.set)

        self.canvas.grid(row=0,column=0,sticky=N+S+E+W)
        self.sbarv.grid(row=0,column=1,stick=N+S)
        self.sbarh.grid(row=1,column=0,sticky=E+W)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        # Rectangle drawing related code
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None

        self.im = PIL.Image.open("mosaic.jpg")
        self.wazil,self.lard=self.im.size
        self.canvas.config(scrollregion=(0,0,self.wazil,self.lard))
        self.tk_im = ImageTk.PhotoImage(self.im)
        self.imgArea = self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

        # button to finish and plan the path
        self.button = Button(master, text="Save visitation goals", command=self.on_update_button, width=70, height=4)
        # self.button.configure(width = 20, activebackground = "#33B5E5",relief = FLAT)
        self.button.place(x=495, y=675)
        
        # button to choose whether or not to set points
        self.choosePtsButton = Button(master, text="Choose visitation goals", command=self.on_update_choosePtsButton, width=70, height=4)
        # move button to top right
        # IMPORTANT: CHANGE THIS AND THE OTHER BUTTON TO NOT GET PLACED OVER IMAGE, DOING THIS BY UPDATING X AND 
        # Y VALUES AS IMAGE DIMENSIONS CHANGE
        self.choosePtsButton.place(x=0, y=675)
        
        # # Text input Box and button
        # self.entry = Entry(root, width=100)
        # self.entertextbutton = Button(text='Enter text', command=self.on_enter_text_button)
        # self.entertextbutton.pack(side = BOTTOM)
        # self.entry.pack(side = BOTTOM)
        # self.inputtext = ""

        # # Text ouptut displayed on screen
        # self.displaytext = Label(root, text="Some dummy text to be displayed.")
        # self.displaytext.pack(side = BOTTOM)


########### FOLLOWING FUNCTIONS TAKE INPUT FROM MOUSE TO DRAW A RECTANGLE #################################
    def on_button_press(self, event):
        global clickedChoose

        if clickedChoose == 1:
            #this records where the the mouse was clicked
            self.start_x = self.canvas.canvasx(event.x)
            self.start_y = self.canvas.canvasy(event.y)
            #creates a red dot where the mouse was clicked
            self.canvas.create_oval(self.start_x-5, self.start_y-5, self.start_x+5, self.start_y+5, fill='red')
            #adds it to list
            point = [ int(self.start_x),  int(self.start_y)]
            #adds it to point list 
            #might be redundant might not be i dont want to fuck with it for the time being
            self.pointList.append(point)
            
            a = len(self.pointList)
            
            print(a)
            if (a > 1):
                temp=self.pointList[(a-2)]
                self.canvas.create_line(int(self.start_x), int(self.start_y), temp[0], temp[1])
                print(int(self.start_x))
                print(temp[0])
                print(int(self.start_y))
                print(temp[1])
            #prints info
            print("[INFO] Point drawn on following image coordinates ")
            print("", self.start_x, " ",self.start_y)
            #sets click state to 0
            clickedChoose=0


        # save mouse drag start position
    

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        if event.x > 0.9*w:
            self.canvas.xview_scroll(1, 'units')
        elif event.x < 0.1*w:
            self.canvas.xview_scroll(-1, 'units')
        if event.y > 0.9*h:
            self.canvas.yview_scroll(1, 'units')
        elif event.y < 0.1*h:
            self.canvas.yview_scroll(-1, 'units')

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)


############  FUNCTION TO UPDATE THE IMAGE IN THE CANVAS  ##################################################################

    def on_update_button(self):
        # print("[INFO] Update button pressed")
        # self.im = PIL.Image.open("mosaic.jpg")
        # self.img = ImageTk.PhotoImage(self.im)
        # self.canvas.itemconfig(self.imgArea, image = self.img)
        # print("[INFO] Map updated")

        print("[INFO] Writing the coordinates to text file")
        print("[INFO] Point List \n", self.pointList)

        textFile = open("test.txt","w")

        for points in self.pointList:
            for coord in points:
                textFile.write(str(coord))
                textFile.write(" ")
            textFile.write("\n")

        textFile.close()

        print("[INFO] Exiting the program")
        #exit()
        
############  FUNCTION TO USE THE ADD POINTS BUTTON  ##################################################################
    def on_update_choosePtsButton(self):
        global clickedChoose
        #if the button has already been clicked once and the state goes to one then if clicked again it will reset to unclicked
        #which means clickedChoose would be set to zero
        if clickedChoose == 1:
            clickedChoose = 0
        else:
            clickedChoose=1

        
        


######   M A I N    F U N C T I O N   ########################################################################################

if __name__ == "__main__":

    root=Tk()
    root.title('Overhead Mosaic Image')
    #root.geometry("1920x1080")

    app = UserInterfaceHIL(root)
    app.pack()
    root.mainloop()
