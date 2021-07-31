import os
import random
import threading
import tkinter as tk
from tkinter import ttk

from PIL import Image


class Duplicator():

    def __init__(self):

        self.folder_originals = "originals"
        self.folder_duplicates = "duplicates"

        self.duplicating = False
        
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

        self.label_min_percent = ttk.Label(self.frame, text="min_percent:")
        self.label_min_percent.grid()

        self.stringvar_min_percent = tk.StringVar(value=90)
        self.entry_min_percent = tk.Entry(self.frame, textvariable=self.stringvar_min_percent)
        self.entry_min_percent.grid()

        self.label_max_percent = ttk.Label(self.frame, text="max_percent:")
        self.label_max_percent.grid()

        self.stringvar_max_percent = tk.StringVar(value=95)
        self.entry_max_percent = tk.Entry(self.frame, textvariable=self.stringvar_max_percent)
        self.entry_max_percent.grid()

        self.label_amount = ttk.Label(self.frame, text="amount:")
        self.label_amount.grid()

        self.stringvar_amount = tk.StringVar(value=2)
        self.entry_amount = tk.Entry(self.frame, textvariable=self.stringvar_amount)
        self.entry_amount.grid()

        self.button_duplicate = ttk.Button(self.frame, text="DUPLICATE", command=self.__start_duplicate)
        self.button_duplicate.grid()

        # Tkinter mainloop
        self.root.mainloop()
    
    def __start_duplicate(self):
        if self.duplicating:
            print("Already duplicating...")
        else:
            threading.Thread(target=self.__duplicate).start()
    
    def __duplicate(self):

        self.duplicating = True

        for file in os.listdir(self.folder_duplicates):
            os.remove(f"{self.folder_duplicates}/{file}")

        for file in os.listdir(self.folder_originals):

            try:
                image = Image.open(f"{self.folder_originals}/{file}")
            except:
                print(f"Skipping {file} due to error")
                continue
            
            image_name, image_extension = os.path.splitext(file)
            image_width, image_height = image.size
            
            used_size_multipliers = [] # to ensure unique multipliers for this image
            max_amount = int(self.stringvar_max_percent.get()) - int(self.stringvar_min_percent.get()) # to prevent an endless while loop below
            leading_chars = self.__get_random_string(2) # to name this image's duplicates

            for i in range(int(self.stringvar_amount.get())):

                size_multiplier = random.randint(int(self.stringvar_min_percent.get()), int(self.stringvar_max_percent.get())) / 100
                while size_multiplier in used_size_multipliers:
                    print(f"{size_multiplier} multiplier was already used, selecting different one...")
                    size_multiplier = random.randint(int(self.stringvar_min_percent.get()), int(self.stringvar_max_percent.get())) / 100
                
                new_image_name = f"{leading_chars}{i}{self.__get_random_string(5)}"
                new_image_width = int(image_width * size_multiplier)
                new_image_height = int(image_height * size_multiplier)

                new_image = image.resize((new_image_width, new_image_height))
                new_image.save(f"{self.folder_duplicates}/{new_image_name}{image_extension}")
                print(f"Duplicated {image_name}({image_width}x{image_height}) as {new_image_name}({new_image_width}x{new_image_height})")

                used_size_multipliers.append(size_multiplier)
                if len(used_size_multipliers) >= max_amount:
                    break

        print("Done")
        self.__update_treeview(self.treeview_duplicates, self.folder_duplicates)
        self.duplicating = False
    
    def __update_treeview(self, treeview, folder):
        # Empty treeview
        for child in treeview.get_children():
            treeview.delete(child)
        # Refill treeview
        for file in [file for file in os.listdir(folder) if not file.startswith(".")]:
            treeview.insert("", tk.END, text=file)
    
    def __get_random_string(self, length):
        chars = "abcdefghijklmnopqrstuvwxyz"
        string = ""
        for i in range(length):
            string += chars[random.randint(0, len(chars)-1)]
        return string


if __name__ == "__main__":
    Duplicator()