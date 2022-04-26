from MatrixML.screen import MatrixScreen
import random


class SampleScreen(MatrixScreen):
    def __init__(self, template_path):
        self.randint = str(random.randint(1, 10))

        super(SampleScreen, self).__init__(template_path)

    def refresh(self):
        self.randint = str(random.randint(1, 10))

        for element in self.elements:
            element.hydrate()