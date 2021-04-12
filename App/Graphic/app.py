from tkinter import *
from PIL import ImageTk, Image #Tkinter's image management is outdated

root = Tk()
root.config(bg='#2D2D2D')
class Application:

    def __init__(self, data):
        self.data = data
        icons, priceWidgets, nameWidgets, metaWidgets = self.create_widgets()
        self.show_widgets(icons, priceWidgets, nameWidgets, metaWidgets)

    def create_widgets(self):
        icons = []
        priceWidgets = []
        nameWidgets = []
        metaWidget = []
        for tag, _data in self.data['items'].items():
            path = f'./Graphic/Images/{_data["img-token"]}.png'
            img = ImageTk.PhotoImage(Image.open(path).resize((100,100)))
            icons.append(img)

            price = list(_data['history'].values())[-1] #last value
            priceWidget = Label(root, text=price, bg='#2D2D2D', fg='white')
            priceWidgets.append(priceWidget)

            metadata = _data['metadata']
            display = ""
            if metadata:
                for key, value in metadata.items():
                    display +=  str(key) + ': ' + str(value) + ' \n'

            display = Label(root, text=display, bg='#2D2D2D', fg='white')
            metaWidget.append(display)

            name = _data['product-name']
            nameWidget = Label(root, text=name, bg='#2D2D2D', fg='white')
            nameWidgets.append(nameWidget)


        return icons, priceWidgets, nameWidgets, metaWidget

    def show_widgets(self, icons, priceWidgets, nameWidgets, metaWidgets):

        count = 0
        for icon in icons:
            panel = Label(root, image=icon)
            panel.grid(row=count, column=0, padx = '50', pady='10')
            count+=1
        count = 0
        for name in nameWidgets:
            name.grid(row=count, column=1, padx = '50', pady='10')
            count+=1
        count = 0
        for price in priceWidgets:
            price.grid(row=count,column=2, padx = '50', pady='10')
            count +=1
        count = 0
        for metadata in metaWidgets:
            metadata.grid(row=count,column=3, padx = '50', pady='10')
            count +=1
        
        root.mainloop()

