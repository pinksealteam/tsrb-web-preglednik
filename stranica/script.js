function goBack() {
    alert("'Back' gumb navigira na prošlu stranicu u Vašoj povijesti pretraživanja. Dopušta Vam da ponovo posjetite stranicu koju ste posjetili prije trenutašnje.");
}

function goForward() {
    alert("'Forward' gumb navigira na sljedeću stranicu u Vašoj povijesti pretraživanja, ako je moguće. Koristite ovaj gumb da se pokrećete 'unaprijed' kroz stranice koje ste posjetili prije trenutašnje.");
}

function refreshPage() {
    alert("'Refresh' gumb ponovo učitava trenutačnu stranicu da pokaže nove promjene. Ovo je korisno za dobivanje najnovijeg sadržaja sa stranice.");
}

function showHistory() {
    alert("'History' gumb dopušta Vam da vidite i upravljati Vašom povijesti. Isto možete viditi popis stranica koje ste posjetili i izabrati jel ih želite ponovo posjetiti ili očisiti Vašu povijest.");
}

function manageBookmarks() {
    alert("'Bookmarks' gumb Vam daje mogućnost da spremite i organizirate Vaše najdraže web-stranice. Isto možete 'bookmark-at' bitne stranice za brzi pristup i upravljati Vašim bookmark-ovima za laganu upotrebu.");
}

// Slusaj za Ctrl + Shift + V 
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.shiftKey && event.key === 'V') {
        alert('Opening TSRB Browser');
        
    }
});
