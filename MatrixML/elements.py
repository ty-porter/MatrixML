from math import floor


class MatrixElement:
    def __init__(self, data):
        self.data = data

    def render(self, *_args):
        raise NotImplementedError

    def raw(self):
        output = ""

        for element in self.data:
            output += element.raw()

        return output


class RowElement(MatrixElement):
    def render(self, adapter, x_position, y_position):
        for element in self.data:
            x_position += element.render(adapter, x_position, y_position)


class ScrollElement(MatrixElement):
    def __init__(self, data):
        super(ScrollElement, self).__init__(data)

        # Helpers to delay start/stop of scrolling
        self.previous_tick  = 0
        self.current_tick   = 0
        self.delay_position = 0
        self.delay_length   = 120
        self.delay_until    = self.delay_length

    def render(self, adapter, x_position, y_position):
        self.tick()

        # Past the delay point, so the delay and tick count needs to be reset
        if self.current_tick > self.delay_until and self.has_set_delay():
            # If the scrolling has ended, also delay at the start of the next scroll for easier reading of first word
            if self.has_ended_scroll(adapter, x_position):
                self.delay(self.delay_length)
                self.delay_position = 0
            # Otherwise, just stop delaying
            else:
                self.delay(-1)

            self.reset_ticks()

        # The end of the text is visible on the matrix and no other delay is present, so create a delay position and delay
        if self.has_ended_scroll(adapter, x_position) and not self.has_set_delay():
            self.delay_position = x_position - floor(self.current_tick / 20)
            self.delay(self.current_tick + self.delay_length)

        # Handle the rendering, and return the total pixel width of the text
        total_width = 0
        for element in self.data:
            # The text overflows the matrix and should be scrolled
            if self.has_overflow(adapter):
                # Handle the delay position if not done delaying
                if self.delay_until >= self.current_tick:
                    total_width += element.render(adapter, self.delay_position, y_position)
                # Otherwise resolve the position based on tick count
                else:
                    total_width += element.render(adapter, x_position - floor(self.current_tick / 20), y_position)
            else:
                total_width += element.render(adapter, x_position, y_position)

            x_position += total_width

        return total_width

    def tick(self):
        self.previous_tick = self.current_tick
        self.current_tick += 1

    def reset_ticks(self):
        self.previous_tick = 0
        self.current_tick  = 0

    def delay(self, amt):
        self.delay_until = amt

    def pixel_size(self, adapter):
        return sum(adapter.font.CharacterWidth(ord(char)) for char in self.raw())

    def has_set_delay(self):
        return self.delay_until >= 0

    def has_overflow(self, adapter):
        return self.pixel_size(adapter) > adapter.matrix.width

    def has_ended_scroll(self, adapter, x_position):
        return (self.pixel_size(adapter) + x_position - floor(self.current_tick / 20)) < adapter.matrix.width


class TextElement(MatrixElement):
    def render(self, adapter, x_position, y_position):
        return adapter.graphics.DrawText(adapter.canvas, 
                                         adapter.font, 
                                         x_position,
                                         y_position, 
                                         adapter.graphics.Color(255, 255, 0), 
                                         self.data)

    def raw(self):
        return self.data