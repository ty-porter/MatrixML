from MatrixML.display_adapter import MatrixDisplayAdapter
from MatrixML.parser import MatrixTemplateParser
from MatrixML.elements import ImageElement

import uuid


class MatrixScreenManager(MatrixDisplayAdapter):
    def __init__(self, *args, **kwargs):
        super(MatrixScreenManager, self).__init__(*args, **kwargs)

        self.screens = []
        self.current_screen = None

    def register_screen(self, screen):
        self.screens.append(screen)

        if self.current_screen is None:
            self.current_screen = 0

    def render(self):
        for row, element in enumerate(self.screens[self.current_screen].elements):
            if isinstance(element, ImageElement):
                element.render(self, 0, row * self.font.height)
            else:
                element.render(self, 0, row * self.font.height + self.font.height)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def run(self):
        self.canvas   = self.matrix.CreateFrameCanvas()
        self.font     = self.graphics.Font()
        self.font.LoadFont("./fonts/6x10.bdf")

        rotations = 0
        while True:
            if rotations > 2:
                rotations = 0
                self.current_screen += 1

                if self.current_screen == len(self.screens):
                    self.current_screen = 0

            i = 0
            
            self.screens[self.current_screen].refresh()

            while i < 500:
                self.canvas.Clear()
                self.render()
                i += 1

            rotations += 1


class MatrixScreen:
    def __init__(self, template_path):
        self.template_path = template_path
        self.image_cache = {}
        self.refresh()

    def refresh(self):
        self.before_refresh()
        value = self.__refresh_screen()
        self.after_refresh()

        return value

    def before_refresh(self):
        pass

    def after_refresh(self):
        pass

    def __refresh_screen(self):
        self.parser   = MatrixTemplateParser(self.template_path, self)
        self.elements = self.parser.parse()

    def cache_image(self, image, identifier=None):
        if identifier is None:
            identifier = str(uuid.uuid1())

        self.image_cache[identifier] = image

        return identifier