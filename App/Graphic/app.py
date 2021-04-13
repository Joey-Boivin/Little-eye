from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image #Tkinter's image management is outdated
import webbrowser
import Tracker

root = Tk()
root.config(bg='#2D2D2D')
root.title("Newegg tracker by Joey-Boivin on GitHub")
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2 - 500)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2 - 200)
root.geometry(f'1000x500+{positionRight}+{positionDown}')

#Create a Main Frame
main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

#Create a canvas
my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

#Add a scrollbar

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

#Config the canvas

my_canvas.configure(bg='#2D2D2D', yscrollcommand=my_scrollbar.set)

my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

#create another frame inside canvas

second_frame = Frame(my_canvas)

#add that new window to the canvas

my_canvas.create_window((0,0), window=second_frame, anchor='nw')
second_frame.config(bg='#2D2D2D')
class Application:

    def __init__(self, data):
        self.data = data
        icons, priceWidgets, nameWidgets, metaWidgets, buttonWidgets, deleteButtonWidgets = self.create_widgets()
        self.show_widgets(icons, priceWidgets, nameWidgets, metaWidgets, buttonWidgets, deleteButtonWidgets)

    def create_widgets(self):
        icons = []
        priceWidgets = []
        nameWidgets = []
        metaWidgets = []
        neweggButtonWidgets = []
        deleteButtonWidgets = []
        for tag, _data in self.data['items'].items():
            path = f'./Graphic/Images/{_data["img-token"]}.png'
            img = ImageTk.PhotoImage(Image.open(path).resize((100,100)))
            icons.append(img)

            price = list(_data['history'].values())[-1] #last value
            priceWidget = Label(second_frame, text=price, bg='#2D2D2D', fg='white')
            priceWidgets.append(priceWidget)

            metadata = _data['metadata']
            display = ""
            if metadata:
                for key, value in metadata.items():
                    display +=  str(key) + ': ' + str(value)
                    if len(metadata.items()) > 1:
                        display += '\n' 
            display = Label(second_frame, text=display, bg='#2D2D2D', fg='white')
            metaWidgets.append(display)

            name = _data['product-name']
            nameWidget = Label(second_frame, text=name, bg='#2D2D2D', fg='white')
            nameWidgets.append(nameWidget)

            #https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
            newegg_button = Button(second_frame, text='See on Newegg.ca', bg='Black', fg='white', command=lambda tag=tag: self.show_on_newegg(tag))
            neweggButtonWidgets.append(newegg_button)

            delete_button = Button(second_frame, text='Remove', bg='Black', fg='white', command=lambda tag=tag: self.remove(tag))
            deleteButtonWidgets.append(delete_button)

            
        return icons, priceWidgets, nameWidgets, metaWidgets, neweggButtonWidgets, deleteButtonWidgets

    def show_widgets(self, icons, priceWidgets, nameWidgets, metaWidgets, buttonWidgets, deleteButtonWidgets):

        for i in range(int(self.data['number-of-items'])):
            panel = Label(second_frame, image=icons[i])
            panel.grid(row=i, column=0, padx = '50', pady='10')
            nameWidgets[i].grid(row=i, column=1, padx = '50', pady='10')
            priceWidgets[i].grid(row=i,column=2, padx = '50', pady='10')
            metaWidgets[i].grid(row=i,column=3, padx = '50', pady='10')
            buttonWidgets[i].grid(row=i, column=4, padx = '40', pady='10')
            deleteButtonWidgets[i].grid(row=i, column=5, padx = '40', pady='10')

        root.mainloop()
    
    @staticmethod
    def show_on_newegg(tag):
        webbrowser.open_new(f'www.newegg.ca/{tag}')
    
    @staticmethod
    def remove(tag):
        print(tag)

        #Tracker.remove_an_existing_item(tag) at the end