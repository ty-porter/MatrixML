from html.parser import HTMLParser
from MatrixML.elements import *
from MatrixML.errors import InvalidTagType, ParseError


class MatrixTemplateParser(HTMLParser):

    ELEMENT_TYPES = {
        'py': DynamicElement,
        'row': RowElement,
        'scroll': ScrollElement,
        'text': TextElement
    }

    def load_template(self, template_path):
        with open(template_path, 'r') as f:
            self.__html_raw = f.read()

    def register_screen(self, screen):
        self.screen = screen

    def parse(self):
        self.tokens = []
        self.feed(self.__html_raw)

        return self.parse_tokens(self.tokens)

    def handle_starttag(self, tag, attrs):
        self.validate_tag(tag)
        self.tokens.append({
            'tag': tag,
            'type': 'start',
            'attrs': attrs
        })

    def handle_endtag(self, tag):
        self.validate_tag(tag)
        self.tokens.append({
            'tag': tag, 
            'type': 'end', 
            'attrs': []
        })

    def handle_data(self, data):
        if data.strip() == '':
            return

        self.tokens.append({
            'data': data.strip()
        })

    def validate_tag(self, tag):
        if tag not in self.ELEMENT_TYPES:
            raise InvalidTagType(f'Tag "{tag}" is not a supported tag. Supported tags are: {", ".join(self.ELEMENT_TYPES)}.')

    def parse_tokens(self, tokens):
        stack = []
        output = []

        start = 0

        if len(tokens) == 1:
            return tokens[0].get('data')

        for i, token in enumerate(tokens):
            if token.get('type') == 'start':
                stack.append(token)

            if token.get('type') == 'end':
                prev_token = stack.pop()

                if prev_token.get('tag') != token.get('tag'):
                    raise ParseError(f'Mismatched tag {token.get("tag")}')

            if len(stack) == 0:
                subset = tokens[start + 1:i]
                element_type = self.fetch_element_type(token.get('tag'))
                element = element_type(self.screen, self.parse_tokens(subset), tokens[start].get("attrs"))
                element.hydrate()
                output.append(element)
                start = i + 1

        return output

    def fetch_element_type(self, token_type):
        element = self.ELEMENT_TYPES.get(token_type)

        if element is None:
            raise ParseError(f'Invalid element type for {token_type}')

        return element