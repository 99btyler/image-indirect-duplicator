import os
import random
import tkinter as tk
from tkinter import ttk

from PIL import Image


class Duplicator():

    def __init__(self):

        self.folder_images = "images"
        self.folder_duplicates = "images/duplicates"

        self.chars = "abcdefghijklmnopqrstuvwxyz"
        
        # Tkinter root
        self.root = tk.Tk()
        self.root.title("image-indirect-duplicator")
        self.root.resizable(False, False)

        # Tkinter frame
        self.frame = ttk.Frame(self.root)
        self.frame.grid()

        # Tkinter widgets
        self.treeview_duplicates = ttk.Treeview(self.frame)
        self.treeview_duplicates.grid()

        self.label_minpercent = ttk.Label(self.frame, text="minpercent:")
        self.label_minpercent.grid()

        self.stringvar_minpercent = tk.StringVar(value=70)
        self.entry_minpercent = tk.Entry(self.frame, textvariable=self.stringvar_minpercent)
        self.entry_minpercent.grid()

        self.label_maxpercent = ttk.Label(self.frame, text="maxpercent:")
        self.label_maxpercent.grid()

        self.stringvar_maxpercent = tk.StringVar(value=99)
        self.entry_maxpecent = tk.Entry(self.frame, textvariable=self.stringvar_maxpercent)
        self.entry_maxpecent.grid()

        self.label_amount = ttk.Label(self.frame, text="amount:")
        self.label_amount.grid()

        self.stringvar_amount = tk.StringVar(value=2)
        self.entry_amount = tk.Entry(self.frame, textvariable=self.stringvar_amount)
        self.entry_amount.grid()

        self.button_duplicate = ttk.Button(self.frame, text="DUPLICATE", command=self.__duplicate)
        self.button_duplicate.grid()

        # Tkinter mainloop
        self.root.mainloop()
    
    def __duplicate(self):
        for file in os.listdir(self.folder_images):
            try:

                # Get info from the image
                image = Image.open(f"{self.folder_images}/{file}")
                image_name, image_extension = os.path.splitext(file)
                image_width, image_height = image.size
                
                # Create info for the image's duplicate
                leading_chars = self.__get_random_string(2)

                treeviewdata = []

                for i in range(int(self.stringvar_amount.get())):

                    new_image_name = f"{leading_chars}{i}{self.__get_random_string(5)}"

                    multiplier = random.randint(int(self.stringvar_minpercent.get()), int(self.stringvar_maxpercent.get())) / 100
                    new_image_width = int(image_width * multiplier)
                    new_image_height = int(image_height * multiplier)
                    
                    # Save the duplicate
                    new_image = image.resize((new_image_width, new_image_height))
                    new_image.save(f"{self.folder_duplicates}/{new_image_name}{image_extension}")
                    treeviewdata.append(f"{new_image_name}({new_image_width}x{new_image_height})")
                    print(f"Duplicated {image_name}({image_width}x{image_height}) as {new_image_name}({new_image_width}x{new_image_height})")
                
                self.__update_treeview_duplicates(treeviewdata)

            except:
                pass
    
    def __update_treeview_duplicates(self, treeviewdata):
        self.treeview_duplicates.delete(*self.treeview_duplicates.get_children())
        for data in treeviewdata:
            self.treeview_duplicates.insert("", tk.END, text=data)
    
    def __get_random_string(self, length):
        string = ""
        for i in range(length):
            string += self.chars[random.randint(0, len(self.chars)-1)]
        return string


if __name__ == "__main__":
    Duplicator()