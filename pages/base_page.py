class BasePage:

    def __init__(self, browser, base_url):
        self.browser = browser
        self.url = base_url

    def go(self, url):
        self.url = url

    def open(self):
        self.browser.get(self.url)
