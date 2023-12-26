"""
Image Editor App
Date Started:24/12/2023
by Quentin Bouet
"""

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import StringProperty
import tkinter.filedialog
import cv2
import os
import shutil

DEFAULT_ALPHA = 1.5
DEFAULT_BETA = 10
APP_PATH = "C:/Users/cheva/OneDrive/Desktop/Image Editor App/"
DEFAULT_IMAGE_NAME = "default_image.JPG"


class ImageEditorApp(App):
    """Image Editor App"""
    status_label = StringProperty()

    def __init__(self, **kwargs):
        """Construct main app."""
        super().__init__(**kwargs)
        self.image = cv2.imread(DEFAULT_IMAGE_NAME)
        self.images = self.select_directory()
        self.images_index = 0
        self.last_images_index = 0

    def build(self):
        """Build the Kivy app from the kv file."""
        self.title = "Image Editor App"
        self.root = Builder.load_file('app.kv')
        self.display_image(False, False)
        return self.root

    def display_image(self, back, next):
        """Display image"""
        # define the alpha and beta
        alpha = DEFAULT_ALPHA  # Contrast control
        beta = DEFAULT_BETA  # Brightness control

        try:
            if back:
                self.images_index += -1
            elif next:
                self.images_index += 1
            image_name = self.images[self.images_index]
            self.last_images_index = self.images_index
        except IndexError:
            # remain on same image by reusing the last index
            image_name = self.images[self.last_images_index]
            self.images_index = self.last_images_index
            # image_name = DEFAULT_IMAGE_NAME

        print(f"Image name: {image_name}")
        self.image = cv2.imread(image_name)

        # call convertScaleAbs function
        adjusted = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
        cv2.imwrite(image_name, adjusted)
        self.root.ids.img.source = image_name

    def select_directory(self):
        """Select directory with chosen images"""
        # select directory
        selected_path = tkinter.filedialog.askdirectory()
        print(selected_path)

        self.images = [f for f in os.listdir(selected_path) if '.jpg' in f.lower()]

        for image in self.images:
            new_path = APP_PATH + image
            old_path = selected_path + "/" + image
            shutil.copy(old_path, new_path)
        print(self.images)
        return self.images

    def clear_inputs(self):
        """Clear inputs"""
        pass

    def save_image(self):
        """Save image as jpeg or png image"""
        image = tkinter.filedialog.asksaveasfilename(filetypes=[("jpeg image", ".jpeg"), ("png image", ".png")],
                                                     defaultextension=".jpeg")
        if image:  # user selected image
            graph = self.image.convert('RGB')
            graph.save(image)
        else:  # user cancel the file browser window
            print("No file chosen")


if __name__ == '__main__':
    ImageEditorApp().run()
