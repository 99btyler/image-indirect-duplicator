import os
import random

from PIL import Image


class Duplicator():

    def __init__(self):

        self.folder_images = "images"
        self.folder_duplicates = "images/duplicates"

        self.chars = "abcdefghijklmnopqrstuvwxyz"
        self.duplicates_per_image = 3

        self.__duplicate()
    
    def __duplicate(self):
        for file in os.listdir(self.folder_images):
            try:

                # Get info from the image
                image = Image.open(f"{self.folder_images}/{file}")
                image_name, image_extension = os.path.splitext(file)
                image_width, image_height = image.size
                
                # Create info for the image's duplicate
                leading_chars = self.__get_random_string(2)

                for i in range(self.duplicates_per_image):

                    new_image_name = f"{leading_chars}{i}{self.__get_random_string(5)}"

                    multiplier = random.randint(70, 99) / 100
                    new_image_width = int(image_width * multiplier)
                    new_image_height = int(image_height * multiplier)
                    
                    # Save the duplicate
                    new_image = image.resize((new_image_width, new_image_height))
                    new_image.save(f"{self.folder_duplicates}/{new_image_name}{image_extension}")
                    print(f"Duplicated {image_name}({image_width}x{image_height}) as {new_image_name}({new_image_width}x{new_image_height})")

            except:
                pass
    
    def __get_random_string(self, length):
        string = ""
        for i in range(length):
            string += self.chars[random.randint(0, len(self.chars)-1)]
        return string


if __name__ == "__main__":
    Duplicator()