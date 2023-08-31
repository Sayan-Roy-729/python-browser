import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://google.com"))
        self.urlbar = QLineEdit()
        self.browser.urlChanged.connect(self.update_urlbar)
        self.browser.loadStarted.connect(self.page_load_started)
        self.browser.loadFinished.connect(self.page_load_finished)
        self.browser.loadProgress.connect(self.update_progress)
        self.status = QStatusBar()

        self.setCentralWidget(self.browser)

        self.setStatusBar(self.status)

        # increase the font size of the web page
        self.browser.page().profile().setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4240.193 Safari/537.36")

        # set the favicon for the application
        self.set_favicon()

        # Add Navigation bar
        navtb = QToolBar("Navigation")
        # add the back button to the toolbar
        self.addToolBar(navtb)
        back_btn = QAction("👈", self)
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # add the forward button to the toolbar
        next_btn = QAction("👉", self)
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # add the reload button to the toolbar
        reload_btn = QAction("👌", self)
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # add the home button to the toolbar
        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navtb.addWidget(self.urlbar)

        stop_btn = QAction("Stop", self)
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        self.progress_bar = QProgressBar()
        navtb.addWidget(self.progress_bar)

        # Connect the downloadRequested signal to the start_download method
        self.browser.page().profile().downloadRequested.connect(self.start_download)

        # Store the download item in a member variable to track the download progress
        self.current_download_item = None

        # show the window in full-screen mode
        self.showMaximized()

        self.show()

    def set_favicon(self):
        # load the favicon image file
        favicon_path = os.path.join(os.path.dirname(__file__), "assets/favicon.png")
        favicon = QIcon(favicon_path)

        # set the favicon for the application
        self.setWindowIcon(favicon)

        # set the favicon for the taskbar (Windows-specific)
        app = QApplication.instance()
        app.setWindowIcon(favicon)

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

    def page_load_started(self):
        self.progress_bar.setValue(0)
        self.status.showMessage("Page is loading...")

    def page_load_finished(self, ok):
        if ok:
            self.progress_bar.setValue(100)
        else:
            self.progress_bar.setValue(0)
        self.status.clearMessage()

    def update_progress(self, progress):
        self.progress_bar.setValue(progress)

    def start_download(self, download_item):
        # Get the suggested file name from the download item.
        suggested_file_name = download_item.suggestedFileName()

        # Prompt the user to select a download location and file name.
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", suggested_file_name, "All Files (*);;Text Files (*.txt)", options=options
        )

        if file_name:
            # Store the download item in a member variable to track the download progress
            self.current_download_item = download_item
            # Save the download to the specified file name and path.
            download_item.setPath(file_name)
            download_item.accept()
            # Connect the download progress signal to update the status
            self.current_download_item.downloadProgress.connect(self.update_download_progress)

    def update_download_progress(self, bytes_received, bytes_total):
        if bytes_total > 0:
            progress_percentage = int(bytes_received * 100 / bytes_total)
            self.progress_bar.setValue(progress_percentage)

        if bytes_received == bytes_total:
            self.status.showMessage("Download completed", 5000)
            self.current_download_item = None


app = QApplication(sys.argv)
app.setApplicationName("My Browser")
window = MainWindow()
app.exec_()
