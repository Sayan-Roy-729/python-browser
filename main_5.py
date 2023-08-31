from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

class MyBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.webview = QWebEngineView()
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.webview, "New Tab")
        self.setCentralWidget(self.tab_widget)

        # Create the context menu with the "Open link in a new tab" option
        self.webview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.webview.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        menu = QMenu(self)
        link_action = QAction("Open link in a new tab", self)
        link_action.triggered.connect(self.open_link_in_new_tab)
        menu.addAction(link_action)
        menu.exec_(self.mapToGlobal(pos))

    def open_link_in_new_tab(self):
        link_action = self.sender()  # Get the triggered QAction
        link_url = link_action.url()
        self.add_new_tab(link_url)

    def add_new_tab(self, url):
        webview = QWebEngineView()
        webview.load(url)
        self.tab_widget.addTab(webview, "New Tab")


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    browser = MyBrowser()
    browser.show()
    sys.exit(app.exec_())
