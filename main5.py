import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTabWidget, QWidget


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
        backward_icon_path = os.path.join(os.path.dirname(__file__), "assets", "left-arrow.png")
        backward_icon_size = QSize(20, 20)
        backward_pixmap = QPixmap(backward_icon_path)
        backward_pixmap = backward_pixmap.scaled(backward_icon_size)
        backward_icon = QIcon(backward_pixmap)
        navtb = QToolBar("Navigation")
        # add the back button to the toolbar
        self.addToolBar(navtb)
        back_btn = QAction(backward_icon, "Back", self)
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        # add the forward button to the toolbar
        forward_icon_path = os.path.join(os.path.dirname(__file__), "assets", "right-arrow.png")
        forward_icon_size = QSize(20, 20)
        forward_pixmap = QPixmap(forward_icon_path)
        forward_pixmap = forward_pixmap.scaled(forward_icon_size)
        forward_icon = QIcon(forward_pixmap)
        next_btn = QAction(forward_icon, "Next", self)
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        # add the reload button to the toolbar
        reload_icon_path = os.path.join(os.path.dirname(__file__), "assets", "refresh.png")
        reload_icon_size = QSize(20, 20)
        reload_pixmap = QPixmap(reload_icon_path)
        reload_pixmap = reload_pixmap.scaled(reload_icon_size)
        reload_icon = QIcon(reload_pixmap)
        reload_btn = QAction(reload_icon, "Reload", self)
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        # add the home button to the toolbar
        home_icon_path = os.path.join(os.path.dirname(__file__), "assets", "home.png")
        home_icon_size = QSize(20, 20)
        home_pixmap = QPixmap(home_icon_path)
        home_pixmap = home_pixmap.scaled(home_icon_size)
        home_icon = QIcon(home_pixmap)
        home_btn = QAction(home_icon, "Home", self)
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

class TabbedBrowser(QTabWidget):
    def __init__(self):
        super(TabbedBrowser, self).__init__()

        self.addTab(MainWindow(), "Tab 1")

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        new_tab_button = QPushButton("+")
        new_tab_button.clicked.connect(self.add_new_tab)
        self.setCornerWidget(new_tab_button)

    def add_new_tab(self):
        self.add_new_tab_with_url("https://google.com")

    def add_new_tab_with_url(self, url):
        browser = MainWindow()
        browser.browser.setUrl(QUrl(url))
        self.addTab(browser, "New Tab")
        self.setCurrentWidget(browser)

    def close_tab(self, index):
        if self.count() > 1:
            widget = self.widget(index)
            widget.deleteLater()
            self.removeTab(index)



app = QApplication(sys.argv)
app.setApplicationName("Magenta Cake")
window = TabbedBrowser()
window.add_new_tab()
window.showMaximized()
app.exec_()
