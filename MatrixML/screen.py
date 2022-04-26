from MatrixML.display_adapter import MatrixDisplayAdapter
from MatrixML.display_adapter import MatrixDisplayAdapter
from MatrixML.parser import MatrixTemplateParser


class MatrixScreenManager(MatrixDisplayAdapter):
    def __init__(self, *args, **kwargs):
        super(MatrixScreenManager, self).__init__(*args, **kwargs)

        self.screens = []

    def register_screen(self, screen):
        self.screens.append(screen)

    def render(self):
        for row, element in enumerate(self.screens[0].elements):
            element.render(self, 0, row * self.font.height + self.font.height)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def run(self):
        self.canvas   = self.matrix.CreateFrameCanvas()
        self.font     = self.graphics.Font()
        self.font.LoadFont("./fonts/6x10.bdf")

        while True:
            i = 0
            
            self.screens[0].refresh()

            while i < 150:
                self.canvas.Clear()
                self.render()
                i += 1


class MatrixScreen:
    def __init__(self, template_path):
        self.template_path = template_path
        self.parser        = MatrixTemplateParser()

        self.parser.load_template(template_path)
        self.parser.register_screen(self)

        self.elements = self.parser.parse()

    def resolve(self, binding):
        return getattr(self, binding)

    def refresh(self):
        raise NotImplementedError("Subclasses must implement screen refresh logic.")
