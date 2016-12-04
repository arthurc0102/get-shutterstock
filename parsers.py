from html.parser import HTMLParser


class GetPostDataParser(HTMLParser):
    def __init__(self):
        super(GetPostDataParser, self).__init__()
        self.post_data = {}

    def error(self, message):
        print(message)

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

    def error(self, message):
        print(message)

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for name, value in attrs:
                if name == 'class' and value == 'total-pages':
                    self.in_total_page = True
                    break

    def handle_data(self, data):
        if self.in_total_page:
            total_page = data.rstrip().lstrip().split(' ')
            self.total_page = total_page[-1]
            self.in_total_page = False


class GetImageDownloadUrlParser(HTMLParser):
    def __init__(self):
        super(GetImageDownloadUrlParser, self).__init__()
        self.images_download_url = []

    def error(self, message):
        print(message)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            is_image_tag_a = False
            url = None
            for name, value in attrs:
                if name == 'class' and value == 'btn btn-small btn-primary':
                    is_image_tag_a = True
                elif name == 'href':
                    url = value
            if is_image_tag_a and url is not None:
                self.images_download_url.append(url)


class GetImageUrlParser(HTMLParser):
    def __init__(self):
        super(GetImageUrlParser, self).__init__()
        self.in_image = False
        self.image_url = ''
        self.image_url_unsure = ''

    def error(self, message):
        print(message)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    self.image_url_unsure = value
                    self.in_image = True

    def handle_data(self, data):
        if self.in_image and self.image_url_unsure != '' \
           and data == 'manually':
            self.image_url = self.image_url_unsure
            self.image_url_unsure = ''
            self.in_image = False
