from MatrixML.screen import MatrixScreen, MatrixScreenManager


# Main function
if __name__ == "__main__":
    template = "samples/test.matrix.html"
    screen   = MatrixScreen(template)
    manager  = MatrixScreenManager()
    manager.register_screen(screen)

    def print_elements(elements, level=0):
        for element in elements:
            if isinstance(element.data, list):
                print_elements(element.data, level + 1)
            else:
                print("  " * level + element.data)

    print_elements(screen.elements)

    if (not manager.process()):
        manager.print_help()