import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *


class BrowserTab(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.browser = QWebEngineView()
        self.browser.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.browser)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        self.add_tab()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        self.new_tab_button = QPushButton("+", self)
        self.new_tab_button.clicked.connect(self.add_new_tab)
        self.new_tab_button.setMaximumWidth(30)
        self.tabs.setCornerWidget(self.new_tab_button)

        self.showMaximized()

    def add_tab(self, qurl=None):
        if qurl is None:
            qurl = QUrl("https://google.com")

        browser = BrowserTab()
        i = self.tabs.addTab(browser, "Loading...")  # Set a temporary label

        self.tabs.setCurrentIndex(i)
        browser.browser.setUrl(qurl)
        browser.browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.browser.titleChanged.connect(lambda title, i=i: self.update_tab_label(i, title))
        browser.browser.loadStarted.connect(lambda: self.page_load_started(browser))
        browser.browser.loadFinished.connect(lambda ok: self.page_load_finished(browser, ok))

    def update_tab_label(self, index, title):
        self.tabs.setTabText(index, title)


    def close_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def update_title(self, browser):
        title = browser.browser.page().title()
        self.setWindowTitle("%s - Browser" % title)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().browser.setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)
        self.update_title(browser)

    def page_load_started(self, browser):
        if browser != self.tabs.currentWidget():
            return

        self.status.showMessage("Page is loading...")

    def page_load_finished(self, browser, ok):
        if browser != self.tabs.currentWidget():
            return

        if ok:
            self.status.clearMessage()
        else:
            self.status.showMessage("Page load failed", 5000)

    def add_new_tab(self):
        self.add_tab()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("My Browser")
    window = MainWindow()
    app.exec_()
