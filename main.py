import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *

class HistoryDialog(QDialog): #
    # Ova klasa ce nam sluziti za pozivanje Povijesti i dati korisniku mogucnost da upravlja s Povijesti.
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
        # Definiramo funkciju s kojom cemo cistiti listu Povijesti.
        self.list_widget.clear()


class BookmarkDialog(QDialog):
    # Ova klasa ce nam sluziti za pozivanje i upravljanje prozora "bookmark"
    bookmarkClicked = pyqtSignal(str)  # Signal koji ce nam trebati kada kliknemo na URL
    bookmarkRemoved = pyqtSignal(str)  # Signal koji ce nam trebati kada obrisemo URL iz bookmark prozorcica.

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

        self.list_widget.itemClicked.connect(self.on_item_clicked)  # Povezujemo funkciju kada pritisnemo na URL u prozoru.

        remove_button = QPushButton("Remove Bookmark")
        remove_button.clicked.connect(self.remove_bookmark)
        layout.addWidget(remove_button)

    def on_item_clicked(self, item):
        # Dojavljujemo signal koji smo gore nazvali da smo kliknuli na url
        url = item.text()
        self.bookmarkClicked.emit(url)

    def remove_bookmark(self):
        selected_item = self.list_widget.currentItem()
        if selected_item: # Provjerava upit da obrisemo URL iz nase liste.
            url = selected_item.text()
            self.bookmarkRemoved.emit(url)
            self.list_widget.takeItem(self.list_widget.row(selected_item))


class MainWindow(QMainWindow):
    def __init__(self):
        # Glavni Prozor aplikacije, a ispod su njegove postavke.
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView() 
        self.browser.setUrl(QUrl('http://google.com')) # Postavljamo Google kao normalni search-engine, odnosno web trazilicu
        self.setCentralWidget(self.browser)
        self.showMaximized() # Prozor se prikazuje u cijelom-ekranu 

        self.setWindowIcon(QIcon('tsrb_logo.png')) # Postavljamo logo aplikacije

        # navigacijska traka
        navbar = QToolBar()
        self.addToolBar(navbar)

        # Gumb za povratak prethodne stranice
        back_button = QAction(QIcon('icons/back.png'), 'Back', self) # Postavljamo ikonu i ime gumba, te ga definiramo.
        back_button.triggered.connect(self.browser.back) # Dodajemo funkcionalnost gumba
        navbar.addAction(back_button) # Dodajemo gumb na navigacijsku traku

        # Gumb za ici na sljedecu stranicu
        forward_button = QAction(QIcon('icons/forward.png'), 'Forward', self) # Postavljamo ikonu i ime gumba, te ga definiramo
        forward_button.triggered.connect(self.browser.forward) # Dodajemo funkcionalnost gumba
        navbar.addAction(forward_button) # Dodajemo gumb na navigacijsku traku

        # Gumb za osvjezenje stranice
        refresh_btn = QAction(QIcon('icons/refresh.png'), 'Refresh', self) # Postavljamo ikonu i ime gumba, te ga definiramo
        refresh_btn.triggered.connect(self.browser.reload) # Dodajemo funkcionalnost gumba
        navbar.addAction(refresh_btn) # Dodajemo gumb na navigacijsku traku

        # Gumb za povratak na pocetnu stranicu
        home_btn = QAction(QIcon('icons/home.png'), 'Home', self) # Postavljamo ikonu i ime gumba, te ga definiramo
        home_btn.triggered.connect(self.navigate_home) # Dodajemo funkcionalnost gumba sa funkcijom navigate_home
        navbar.addAction(home_btn) # Dodajemo gumb na navigacijsku traku

        # Gumb za Povijest
        history_btn = QAction(QIcon('icons/history.png'), 'History', self) # Postavljamo ikonu i ime gumba, te ga definiramo
        history_btn.triggered.connect(self.show_history) # Dodajemo funkcionalnost gumba
        navbar.addAction(history_btn) # Dodajemo gumb na navigacijsku traku

        # Gumb za tsrb.hr
        tsrb_btn = QAction('TSRB', self) # Postavljamo samo ime gumba
        tsrb_btn.triggered.connect(self.navigate_tsrb) # Dodajemo funkcionalnost gumba
        navbar.addAction(tsrb_btn) # Dodajemo gumb na navigacijsku traku
        
        self.history_list = [] # sa ovime postavljamo i kreiramo listu za prikaz "Povijesti"

        self.bookmarks = [] # sa ovime postavljamo i kreiramo listu za prikaz "Bookmarks"

        # Stvaramo Adresnu Traku pomocu elementa QLineEdit
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url) # Dodajemo funkcionalnost trake, odnosno kada se unese text on se pretvori u url i navigira korisnika na tu adresu/stranicu
        navbar.addWidget(self.url_bar) # Dodajemo Adresnu Traku na Navigacijsku Traku
        
        # Varijabla pod elementom QAction, s kojom se moze otvoriti nasa stranica pomocu koristenja precice Ctrl+Shift+V
        open_index_file = QAction('Open Index File', self)
        open_index_file.setShortcut(QKeySequence('Ctrl+Shift+V'))
        open_index_file.triggered.connect(self.open_index_html) # Koristi funkciju da otvori stranicu
        self.addAction(open_index_file)

        # Gumb za bookmark klasu
        bookmark_btn = QAction(QIcon('icons/bookmark.png'), 'Bookmark', self) # Postavljamo ikonu i ime gumba, te ga definiramo
        bookmark_btn.triggered.connect(self.add_bookmark) # Dodajemo funkciju add_bookmark koja nadodaje url pod favorite
        bookmark_btn.triggered.connect(self.show_bookmarks) # Pozivamo funkciju da pozove Bookmark Klasu da otvorimo prozor gdje mozemo upravljati nasim bookmark-s
        navbar.addAction(bookmark_btn) # Dodajemo na navigacijsku traku

        self.browser.urlChanged.connect(self.update_history) # Provjerava URL Adresnu traku za nove linkove koji su drugaciji da ih moze dodati u listu "Povijest"
        self.browser.urlChanged.connect(self.update_url) # Provjerava URL Adresnu traku za najnovije linkove tako da ih moze postaviti u url traku
    
    

    def add_bookmark(self): # Definiramo funkciju koja dodaje URL-ove pod favorite u Bookmark klasu
        current_url = self.browser.url().toString() # Ucitava trenutacni url kao string da ga dodaje na listu
        if current_url not in self.bookmarks: # Provjerava jel trenutacni URL vec pod favoritima
            self.bookmarks.append(current_url) # Ako nije, onda ga dodaje
            QMessageBox.information(self, "Bookmark Added", "Bookmark has been added successfully.") #Izbacuje potvrdu da smo nadodali URL pod favorite

    def open_index_html(self): # Funkcija da otvori nasu stranicu
        # Definiramo adresu i put do nase stranice
        index_html_path = '/stranica/index.html'

        # Ucitava nasu stranicu
        self.browser.setUrl(QUrl.fromLocalFile(index_html_path))

    def show_bookmarks(self): # Funkcija za izbacivanje prozora za upravljanje s Bookmark-ovima
        bookmark_dialog = BookmarkDialog(self.bookmarks) # Definiramo taj prozor
        bookmark_dialog.bookmarkClicked.connect(self.navigate_to_bookmark)  # Povezujemo signal od prije, kada se pritisne link otvori se u web pregledniku
        bookmark_dialog.bookmarkRemoved.connect(self.remove_bookmark)  # Povezujemo drugi singal od prije, da maknemo taj bookmark od favorita
        bookmark_dialog.exec_() # Pozivamo taj prozor

    def navigate_to_bookmark(self, url): # Funkcija kojom kad se klikne na url u prozoru za Bookmark, 
        self.browser.setUrl(QUrl(url)) # Navigiramo na taj URL nakon klika

    def remove_bookmark(self, url): # Funkcija kojom micemo URL iz favorita
        if url in self.bookmarks: # Provjeravamo jel taj URL uopce pod favoritima
            self.bookmarks.remove(url) # Ako je, maknemo ga.


    def navigate_home(self): # Funkcija kojom navigiramo na pocetnu stranicu
        self.browser.setUrl(QUrl('http://google.com')) 
    
    def navigate_to_url(self): # Funkcija kojom navigiramo stranice preko adresne trake
        url = self.url_bar.text()
        self.browser.setUrl(QUrl('http://' + url))
        # Dodajemo taj URL u listu Povijesti
        self.history_list.append('http://' + url)

    def update_url(self, new_url): # Funkcija koja azurira adresnu traku s obzirom na kojom smo stranici
        url = new_url.toString()
        self.url_bar.setText(new_url.toString())    

    def update_history(self, new_url): # Funkcija koja azurira povijest s obzirom na novih linkova
        # Nadodaje URL u listu "Povijest" ako vec nije dodan.
        url = new_url.toString()
        if url not in self.history_list:
            self.history_list.append(url) # append funkcija je koristena za nadodavanje stvari u listu, a nasa "Povijest" je napravljena i tretirana kao lista


    def navigate_tsrb(self): # Navigira na tsrb.hr
        self.browser.setUrl(QUrl('http://tsrb.hr'))
        
    def show_history(self): # Funkcija kojom pozivamo da otvorimo prozor Povijest
        history_dialog = HistoryDialog(self.history_list)
        history_dialog.exec_()

    def keyPressEvent(self, event): 
        # Ova funkcija ce nam dopustiti da kada kliknemo CTRL+H izade history tab
        if event.key() == Qt.Key_H and event.modifiers() == Qt.ControlModifier:
            self.show_history()
        else:
            super(MainWindow, self).keyPressEvent(event)    

app = QApplication(sys.argv) 
QApplication.setApplicationName('TSRB Browser') # Postavljamo ime aplikacije
window = MainWindow()
app.exec_() # Pokrecemo aplikaciju