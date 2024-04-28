import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *

class HistoryDialog(QDialog):
    def __init__(self, history_list):
        super().__init__()
        self.setWindowTitle("History")
        self.setMinimumWidth(400)
        self.setWindowIcon(QIcon('tsrb_logo.png'))

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.list_widget = QListWidget()
        for item in history_list:
            self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)

        clear_button = QPushButton("Ocisti Povijest")
        clear_button.clicked.connect(self.clear_history)
        layout.addWidget(clear_button)

    def clear_history(self):
        self.list_widget.clear()


class BookmarkDialog(QDialog):
    bookmarkClicked = pyqtSignal(str)  # Custom signal to emit URL when bookmark is clicked
    bookmarkRemoved = pyqtSignal(str)  # Custom signal to emit URL when bookmark is removed

    def __init__(self, bookmarks):
        super().__init__()
        self.setWindowTitle("Bookmarks")
        self.setMinimumWidth(400)
        self.setWindowIcon(QIcon('tsrb_logo.png'))

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.list_widget = QListWidget()
        for item in bookmarks:
            self.list_widget.addItem(item)

        layout.addWidget(self.list_widget)

        self.list_widget.itemClicked.connect(self.on_item_clicked)  # Connect itemClicked signal

        remove_button = QPushButton("Remove Bookmark")
        remove_button.clicked.connect(self.remove_bookmark)
        layout.addWidget(remove_button)

    def on_item_clicked(self, item):
        # Emit custom signal with URL of clicked bookmark
        url = item.text()
        self.bookmarkClicked.emit(url)

    def remove_bookmark(self):
        selected_item = self.list_widget.currentItem()
        if selected_item:
            url = selected_item.text()
            self.bookmarkRemoved.emit(url)
            self.list_widget.takeItem(self.list_widget.row(selected_item))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        self.setWindowIcon(QIcon('tsrb_logo.png'))

        # navigacijska traka
        navbar = QToolBar()
        self.addToolBar(navbar)

        back_button = QAction(QIcon('icons/back.png'), 'Back', self)
        back_button.triggered.connect(self.browser.back)
        navbar.addAction(back_button)

        forward_button = QAction(QIcon('icons/forward.png'), 'Forward', self)
        forward_button.triggered.connect(self.browser.forward)
        navbar.addAction(forward_button)

        refresh_btn = QAction(QIcon('icons/refresh.png'), 'Refresh', self)
        refresh_btn.triggered.connect(self.browser.reload)
        navbar.addAction(refresh_btn)

        home_btn = QAction(QIcon('icons/home.png'), 'Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        history_btn = QAction(QIcon('icons/history.png'), 'History', self)
        history_btn.triggered.connect(self.show_history)
        navbar.addAction(history_btn)

        tsrb_btn = QAction('TSRB', self)
        tsrb_btn.triggered.connect(self.navigate_tsrb)
        navbar.addAction(tsrb_btn)
        
        self.history_list = [] # sa ovime postavljamo i kreiramo listu za prikaz "Povijesti"

        self.bookmarks = [] # sa ovime postavljamo i kreiramo listu za prikaz "Bookmarks"

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)
        
        open_index_file = QAction('Open Index File', self)
        open_index_file.setShortcut(QKeySequence('Ctrl+Shift+V'))
        open_index_file.triggered.connect(self.open_index_html)
        self.addAction(open_index_file)

        bookmark_btn = QAction(QIcon('icons/bookmark.png'), 'Bookmark', self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        bookmark_btn.triggered.connect(self.show_bookmarks)
        navbar.addAction(bookmark_btn)

        self.browser.urlChanged.connect(self.update_history) # Provjerava URL Adresnu traku za nove linkove koji su drugaciji da ih moze dodati u listu "Povijest"
        self.browser.urlChanged.connect(self.update_url) # Provjerava URL Adresnu traku za najnovije linkove tako da ih moze postaviti u url traku
    
    

    def add_bookmark(self):
        current_url = self.browser.url().toString()
        if current_url not in self.bookmarks:
            self.bookmarks.append(current_url)
            QMessageBox.information(self, "Bookmark Added", "Bookmark has been added successfully.")

    def open_index_html(self):
        # Definiramo adresu i put do nase stranice
        index_html_path = '/stranica/index.html'

        # Ucitava nasu stranicu
        self.browser.setUrl(QUrl.fromLocalFile(index_html_path))

    def show_bookmarks(self):
        bookmark_dialog = BookmarkDialog(self.bookmarks)
        bookmark_dialog.bookmarkClicked.connect(self.navigate_to_bookmark)  # Connect custom signal
        bookmark_dialog.bookmarkRemoved.connect(self.remove_bookmark)  # Connect custom signal
        bookmark_dialog.exec_()

    def navigate_to_bookmark(self, url):
        self.browser.setUrl(QUrl(url))

    def remove_bookmark(self, url):
        if url in self.bookmarks:
            self.bookmarks.remove(url)


    def navigate_home(self):
        self.browser.setUrl(QUrl('http://google.com'))
    
    def navigate_to_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl('http://' + url))
        # Add the URL to history list
        self.history_list.append('http://' + url)

    def update_url(self, new_url):
        url = new_url.toString()
        self.url_bar.setText(new_url.toString())    

    def update_history(self, new_url):
        # Nadodaje URL u listu "Povijest" ako vec nije dodan.
        url = new_url.toString()
        if url not in self.history_list:
            self.history_list.append(url) # append funkcija je koristena za nadodavanje stvari u listu, a nasa "Povijest" je napravljena i tretirana kao lista


    def navigate_tsrb(self):
        self.browser.setUrl(QUrl('http://tsrb.hr'))
        
    def show_history(self):
        history_dialog = HistoryDialog(self.history_list)
        history_dialog.exec_()

    def keyPressEvent(self, event):
        # Ova funkcija ce nam dopustiti da kada kliknemo CTRL+H izade history tab
        if event.key() == Qt.Key_H and event.modifiers() == Qt.ControlModifier:
            self.show_history()
        else:
            super(MainWindow, self).keyPressEvent(event)    

app = QApplication(sys.argv)
QApplication.setApplicationName('TSRB Browser')
window = MainWindow()
app.exec_()