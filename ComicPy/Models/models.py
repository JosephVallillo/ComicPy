class Series:
    def __init__(self, root, name, issues=None):
        self.root = root
        self.name = name
        self.issues = issues if issues is not None else []

    def add_issue(self, issue):
        self.issues.append(issue)


class Issue:
    def __init__(self, name, url, author=None, event=None, pages=None):
        self.name = name
        self.url = url
        self.author = author
        self.event = event
        self.pages = pages if pages is not None else []

    def add_page(self, page):
        self.pages.append(page)


class Page:
    def __init__(self, page_num, url, image):
        self.page_num = page_num
        self.url = url
        self.image = image
