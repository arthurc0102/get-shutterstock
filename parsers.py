from html.parser import HTMLParser


class GetPostDataParser(HTMLParser):
    def __init__(self):
        super(GetPostDataParser, self).__init__()

        self.post_data = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            tag_name = None
            tag_value = None

            for name, value in attrs:
                if name == 'name':
                    tag_name = value
                elif name == 'value':
                    tag_value = value

            if tag_name is not None:
                self.post_data[tag_name] = tag_value


class GetTotalPageParser(HTMLParser):
    def __init__(self):
        super(GetTotalPageParser, self).__init__()

        self.total_page = None
        self.in_total_page = False

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for name, value in attrs:
                if name == 'class' and value == 'total-pages':
                    self.in_total_page = True
                    break

    def handle_data(self, data):
        if self.in_total_page:
            total_page = data.rstrip().lstrip().split(' ')
            self.total_page = total_page[len(total_page) - 1]
            self.in_total_page = False
