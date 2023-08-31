import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *


class BrowserTab(QWebEngineView):

    def __init__(self):
        super().__init__()

        self.urlChanged.connect(self.update_urlbar)
        self.titleChanged.connect(self.update_title)
        self.loadStarted.connect(self.page_load_started)
        self.loadFinished.connect(self.page_load_finished)
        self.loadProgress.connect(self.update_progress)
        self.page().profile().downloadRequested.connect(self.start_download)

    def update_urlbar(self, q):
        self.parent().urlbar.setText(q.toString())
        self.parent().urlbar.setCursorPosition(0)

    def update_title(self, title):
        self.setWindowTitle("%s - Browser" % title)

    def page_load_started(self):
        self.parent().progress_bar.setValue(0)
        self.parent().status.showMessage("Page is loading...")

    def page_load_finished(self, ok):
        if ok:
            self.parent().progress_bar.setValue(100)
        else:
            self.parent().progress_bar.setValue(0)
        self.parent().status.clearMessage()

    def update_progress(self, progress):
        self.parent().progress_bar.setValue(progress)

    def start_download(self, download_item):
        suggested_file_name = download_item.suggestedFileName()

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", suggested_file_name, "All Files (*);;Text Files (*.txt)", options=options)

        if file_name:
            download_item.download(file_name)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction("Back", self)
        back_btn.triggered.connect(self.navigate_back)
        navtb.addAction(back_btn)

        next_btn = QAction("Forward", self)
        next_btn.triggered.connect(self.navigate_forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(self.reload_page)
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction("Stop", self)
        stop_btn.triggered.connect(self.stop_loading)
        navtb.addAction(stop_btn)

        self.progress_bar = QProgressBar()
        navtb.addWidget(self.progress_bar)

        self.show()

    def add_new_tab(self, qurl=QUrl('https://google.com'), label='Blank'):
        browser = BrowserTab()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def current_tab_changed(self, i):
        if i == -1:
            return

        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl)
        self.update_title()

    def navigate_back(self):
        self.tabs.currentWidget().back()

    def navigate_forward(self):
        self.tabs.currentWidget().forward()

    def reload_page(self):
        self.tabs.currentWidget().reload()

    def stop_loading(self):
        self.tabs.currentWidget().stop()

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)


app = QApplication(sys.argv)
app.setApplicationName("My Browser")
window = MainWindow()
window.add_new_tab()
app.exec_()
