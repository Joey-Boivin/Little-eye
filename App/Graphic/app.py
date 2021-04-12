from tkinter import *
from PIL import ImageTk, Image #Tkinter's image management is outdated

root = Tk()
class Application:

    def __init__(self, data):
        self.data = data
        icons, priceWidgets, nameWidgets = self.create_widgets()
        self.show_widgets(icons, priceWidgets, nameWidgets)

    def create_widgets(self):
        icons = []
        priceWidgets = []
        nameWidgets = []
        for tag, _data in self.data['items'].items():
            path = f'./Graphic/Images/{_data["img-token"]}.png'
            img = ImageTk.PhotoImage(Image.open(path).resize((100,100)))
            icons.append(img)

            price = list(_data['history'].values())[-1] #last value
            priceWidget = Label(root, text=price)
            priceWidgets.append(priceWidget)

            name = _data['product-name']
            nameWidget = Label(root, text=name)
            nameWidgets.append(nameWidget)
        return icons, priceWidgets, nameWidgets

    def show_widgets(self, icons, priceWidgets, nameWidgets):

        count = 0
        for icon in icons:
            panel = Label(root, image=icon)
            panel.grid(row=count, column=0, padx = '50')
            count+=1
        count = 0
        for name in nameWidgets:
            name.grid(row=count, column=1, padx = '50')
            count+=1
        count = 0
        for price in priceWidgets:
            price.grid(row=count,column=2, padx = '50')
            count +=1
        
        root.mainloop()

