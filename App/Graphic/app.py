from tkinter import *
from PIL import ImageTk, Image #Tkinter's image management is outdated
import webbrowser

root = Tk()

class Application:

    def __init__(self, data):
        self.data = data
        icons, priceWidgets = self.create_widgets()
        self.show_widgets(icons, priceWidgets)

    def create_widgets(self):
        icons = []
        priceWidgets = []
        nameWidgets = []
        for tag, _data in self.data['items'].items():
            path = f'./Images/{_data["img-token"]}.png'
            img = ImageTk.PhotoImage(Image.open(path).resize((100,100)))
            icons.append(img)

            price = list(_data['history'].values())[-1] #last value
            priceWidget = Label(root, text=price)
            priceWidgets.append(priceWidget)

        return icons, priceWidgets

    def show_widgets(self, icons, priceWidgets):

        count = 0
        for icon in icons:
            panel = Label(root, image=icon)
            panel.grid(row=count, column=0)
            count+=1
        count = 0
        for price in priceWidgets:
            price.grid(row=count,column=1)
            count +=1
        root.mainloop()


