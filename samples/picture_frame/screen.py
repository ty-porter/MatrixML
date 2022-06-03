from MatrixML.screen import MatrixScreen

from PIL import Image
import os

class PictureFrameScreen(MatrixScreen):

    IMAGE_PATH = os.path.join(os.path.dirname(__file__), "./assets/mm.png")
    REMOTE_IMAGE_URL = "https://imgur.com/EuS0MsS.png"

    def __init__(self, template_path):
        self.current_image = -1

        super(PictureFrameScreen, self).__init__(template_path)

        self.__preload_image()
    
    def __preload_image(self):
        image = Image.open(PictureFrameScreen.IMAGE_PATH).convert("RGB")

        self.image_identifier = self.cache_image(image)

    def after_refresh(self):
        self.current_image += 1
        
        if self.current_image > 1:
            self.current_image = 0
