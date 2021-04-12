from tkinter import *
from PIL import ImageTk, Image #Tkinter's image management is outdated
import webbrowser

root = Tk()

class Application:

    def __init__(self, data):
        self.data = data
        icons, priceWidgets = self.create_widgets()

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

