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

FILENAME = 'apple.jpg'
DEFAULT_ALPHA = 1.5
DEFAULT_BETA = 10


def get_image():
    """Get image"""
    # read the input image
    image = cv2.imread(FILENAME)
    return image


class GraphingApp(App):
    """Image Editor App"""
    average_label = StringProperty()
    status_label = StringProperty()

    def __init__(self, **kwargs):
        """Construct main app."""
        super().__init__(**kwargs)
        self.image = get_image()

    def build(self):
        """Build the Kivy app from the kv file."""
        self.title = "Image Editor App"
        self.root = Builder.load_file('app.kv')
        self.display_img()
        return self.root

    def display_img(self):
        """Display image"""
        # define the alpha and beta
        alpha = DEFAULT_ALPHA  # Contrast control
        beta = DEFAULT_BETA  # Brightness control

        # call convertScaleAbs function
        adjusted = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
        cv2.imwrite(FILENAME, adjusted)
        self.root.ids.img.source = FILENAME

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
    GraphingApp().run()
