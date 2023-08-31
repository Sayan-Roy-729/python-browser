import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://google.com"))
        self.urlbar = QLineEdit()
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadFinished.connect(self.update_title)
        self.status = QStatusBar()

        self.setCentralWidget(self.browser)

        self.setStatusBar(self.status)

        # Add Navigation bar
        navtb = QToolBar("Navigation")

        # add the back button to the toolbar
        self.addToolBar(navtb)
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # add the forward button to the toolbar
        next_btn = QAction("Forward", self)
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # add the reload button to the toolbar
        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # add the home button to the toolbar
        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navtb.addWidget(self.urlbar)

        stop_btn = QAction("Stop", self)
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        # Connect the downloadRequested signal to the start_download method
        self.browser.page().profile().downloadRequested.connect(self.start_download)

        self.show()

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.browser.setUrl(q)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://google.com"))

    def update_urlbar(self, q):
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def update_title(self):
        title = self.browser.page().title()
        self.setWindowTitle("%s - Browser" % title)

    def start_download(self, download_item):
        # Get the suggested file name from the download item.
        suggested_file_name = download_item.suggestedFileName()

        # Prompt the user to select a download location and file name.
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", suggested_file_name, "All Files (*);;Text Files (*.txt)", options=options)

        if file_name:
            # Start the download with the specified file name and and path.
            download_item.setPath(file_name)
            download_item.accept()


app = QApplication(sys.argv)
app.setApplicationName("My Browser")
window = MainWindow()
app.exec_()
