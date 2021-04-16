"""
This is the module containing the graphical user interface for
my Newegg tracker application
"""

from tkinter import *
from tkinter import ttk
import webbrowser
from PIL import ImageTk, Image #Tkinter's image management is outdated



root = Tk()
root.config(bg="#2D2D2D")
root.title("Newegg tracker by Joey-Boivin on GitHub")
root.geometry("1050x900")

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(bg='#2D2D2D', yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox('all')))

second_frame = Frame(my_canvas)
second_frame.config(bg='#2D2D2D')

my_canvas.create_window((0,0), window=second_frame, anchor='nw')


class Application:
    """
    This is the class containing the graphical user interface.
    """

    def __init__(self, data:dict):
        self.data = data
        icons, price_widgets, name_widgets, meta_widgets, button_widgets = self.create_widgets()
        self.show_widgets(icons, price_widgets, name_widgets, meta_widgets, button_widgets)


    def create_widgets(self):
        """
        Creates all the widgets for the gui, including icons, name labels,
        metadata about the items, and a "show on Newegg" button.
        """

        icons = []
        price_widgets = []
        name_widgets = []
        meta_widgets = []
        newegg_button_widgets = []

        for tag, _data in self.data['items'].items():
            path = f'./Graphic/Images/{_data["img-token"]}.png'
            img = ImageTk.PhotoImage(Image.open(path).resize((100,100)))
            icons.append(img)

            price = list(_data['history'].values())[-1] #last value
            price_widget = Label(second_frame, text=price, bg='#2D2D2D', fg='white')
            price_widgets.append(price_widget)

            metadata = _data['metadata']
            display = ""
            if metadata:
                for key, value in metadata.items():
                    display +=  str(key) + ': ' + str(value)
                    if len(metadata.items()) > 1:
                        display += '\n'
            display = Label(second_frame, text=display, bg='#2D2D2D', fg='white')
            meta_widgets.append(display)

            name = _data['product-name']
            name_widget = Label(second_frame, text=name, bg='#2D2D2D', fg='white')
            name_widgets.append(name_widget)

            newegg_button = Button(second_frame, text='See on Newegg.ca', bg='Black', fg='white', command=lambda tag=tag: self.show_on_newegg(tag))
            newegg_button_widgets.append(newegg_button)

        return icons, price_widgets, name_widgets, meta_widgets, newegg_button_widgets


    def show_widgets(
                    self, icons:list, price_widgets:list,
                    name_widgets:list, meta_widgets:list, button_widgets:list
                    ):
        """
        Shows the widgets for the gui
        """

        for i in range(int(self.data['number-of-items'])):
            panel = Label(second_frame, image=icons[i])
            panel.grid(row=i, column=0, padx = '50', pady='10')
            name_widgets[i].grid(row=i, column=1, padx = '50', pady='10')
            price_widgets[i].grid(row=i,column=2, padx = '50', pady='10')
            meta_widgets[i].grid(row=i,column=3, padx = '50', pady='10')
            button_widgets[i].grid(row=i, column=4, padx = '40', pady='10')

        root.mainloop()


    @staticmethod
    def show_on_newegg(tag:str):
        """
        Opens a new tab on Newegg.ca the tracked item.
        """

        webbrowser.open_new(f'www.newegg.ca/{tag}')
