from MatrixML.screen import MatrixScreenManager
from samples.crypto_ticker.screen import CryptoTickerScreen
from samples.picture_frame.screen import PictureFrameScreen

SCREENS = [
    PictureFrameScreen("samples/picture_frame/picture_frame.matrix.html"),
    CryptoTickerScreen("samples/crypto_ticker/crypto_ticker.matrix.html")
]

manager  = MatrixScreenManager()

for screen in SCREENS:
    manager.register_screen(screen)

def print_elements(elements, level=0):
    for element in elements:
        if isinstance(element.data, list):
            print_elements(element.data, level + 1)
        else:
            print("  " * level + element.data)

# Main function
if __name__ == "__main__":
    if (not manager.process()):
        manager.print_help()