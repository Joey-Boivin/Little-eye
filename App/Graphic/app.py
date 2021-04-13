from tkinter import *
from PIL import ImageTk, Image #Tkinter's image management is outdated
import webbrowser
root = Tk()
root.config(bg='#2D2D2D')
root.title("Newegg tracker")
class Application:

    def __init__(self, data):
        self.data = data
        icons, priceWidgets, nameWidgets, metaWidgets, buttonWidgets = self.create_widgets()
        self.show_widgets(icons, priceWidgets, nameWidgets, metaWidgets, buttonWidgets)

    def create_widgets(self):
        icons = []
        priceWidgets = []
        nameWidgets = []
        metaWidgets = []
        neweggButtonWidgets = []
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
            metaWidgets.append(display)

            name = _data['product-name']
            nameWidget = Label(root, text=name, bg='#2D2D2D', fg='white')
            nameWidgets.append(nameWidget)

            #https://stackoverflow.com/questions/10865116/tkinter-creating-buttons-in-for-loop-passing-command-arguments
            newegg_button = Button(root, text='See on Newegg.ca', bg='Black', fg='white', command=lambda tag=tag: self.show_on_newegg(tag))
            neweggButtonWidgets.append(newegg_button)

            
        return icons, priceWidgets, nameWidgets, metaWidgets, neweggButtonWidgets

    def show_widgets(self, icons, priceWidgets, nameWidgets, metaWidgets, buttonWidgets):

        for i in range(int(self.data['number-of-items'])):
            panel = Label(root, image=icons[i])
            panel.grid(row=i, column=0, padx = '50', pady='10')
            nameWidgets[i].grid(row=i, column=1, padx = '50', pady='10')
            priceWidgets[i].grid(row=i,column=2, padx = '50', pady='10')
            metaWidgets[i].grid(row=i,column=3, padx = '50', pady='10')
            remove_button = Button(
                root, text='Remove', padx=40, pady=0,
                command=None, fg="white", bg = "Black"
                )
            remove_button.grid(row=i, column=4)
            buttonWidgets[i].grid(row=i, column=5, padx = '40', pady='10')

        root.mainloop()
    
    @staticmethod
    def show_on_newegg(tag):
        webbrowser.open_new(f'www.newegg.ca/{tag}')
    