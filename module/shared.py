# Paths
DB_PATH = "data/bookmarket.db"

YAML_PATH = "config/settings.yaml"


# Error messages
DB_ERROR = "Si è verificato un problema nella lettura del database."

PRICE_ERROR = "Prezzo non valido."

USERNAME_ERROR = "Per poter vendere libri devi avere un username pubblico, in modo tale che gli altri utenti possano contattarti. Puoi comunque acquistare libri con il comando /cerca."

ISBN_ERROR = "ISBN non valido. Deve essere un numero di 10 o di 13 cifre."


# Command usage
REQUEST_USAGE = "Utilizzo comando: /richiedi <ISBN>; <Prezzo>; <Titolo>; <Autori>\nNota bene: ogni campo deve essere separato dal carattere ';' seguito da uno spazio. \n\nEs: /richiedi 9788864201795; 4.08; One Piece 1; Eiichiro Oda"

DELETE_USAGE = "Utilizzo comando: /elimina"

MY_BOOKS_USAGE = "Utilizzo comando: /libri"

SEARCH_USAGE = "Utilizzo comando: /cerca <txt>"

SELL_USAGE = "Utilizzo comando: /vendi <ISBN> <Prezzo>"

START_MESSAGE = "Ciao! Con questo bot puoi mettere in vendita i tuoi libri usati e comprare libri che altri colleghi non utilizzano più. Per maggiori informazioni utilizza il comando /help"

HELP_MESSAGE = "Comandi disponibili:\n\n" \
    "/vendi <ISBN> <Prezzo>\nAggiungi un libro alla lista degli oggetti in vendita. Inserisci l'ISBN del tuo libro e il prezzo con il quale lo vorresti vendere.\nEs: /vendi 9788891296566 5.50\n\n" \
    "/cerca <txt>\nCerca un libro all'interno della lista degli oggetti in vendita. La ricerca si baserà su ciò che hai inserito successivamente al comando. All'interno dei risultati della ricerca sono presenti sia le informazioni sui libri sia il contatto della persona che l'ha messo in vendita.\nEs: /cerca modelli matematici\n\n" \
    "/elimina\nElimina un libro che avevi precedentemente inserito nella lista degli oggetti in vendita. Puoi utilizzare questo comando, ad esempio, quando avrai venduto il tuo libro o se non vorrai più venderlo.\nEs: /elimina\n\n" \
    "/libri\nElenca i tuoi libri in vendita.\nEs: /libri\n\n" \
    "/richiedi <ISBN>; <Prezzo>; <Titolo>; <Autori>\nRichiedi l'inserimento manuale di un libro non presente nei database locali e/o online. Un admin controllerà la tua richiesta e aggiungerà manualmente il libro agli altri oggetti in vendita.\nNota bene: ogni campo deve essere separato dal carattere ';' seguito da uno spazio.\nEs: /richiedi 9788864201795; 4.08; One Piece 1; Eiichiro Oda"

# Request
NEW_REQUEST = "new_request"

NEW_REQUEST_APPROVED = "new_request;Y;"

NEW_REQUEST_DECLINED = "new_request;N;"

REQUEST_SENT = "La richiesta è stata inoltrata agli admin. Grazie del supporto!"

REQUEST_ALREADY_SENT = "Hai già inviato una richiesta per questo libro. La tua richiesta è in elaborazione."

PENDING_REQUEST = "New Pending Request:\n"

ADMIN_REQUEST_ACCEPTED = "Richiesta accettata."

ADMIN_REQUEST_DECLINED = "Richiesta rifiutata."

USER_REQUEST_ACCEPTED = "La tua richiesta è stata accettata. Il libro è stato messo in vendita."

USER_REQUEST_DECLINED = "La tua richiesta è stata rifiutata. Controlla se i dati inseriti sono corretti e riprova."

CASCADE_REQUEST = "Richiesta accettata a cascata precedentemente."

BOOK_IS_PRESENT = "Il libro esiste già nel database locale. "


# Other constant
NO = "N"

YES = "Y"

ISBN_PREFIX_1 = "978"

ISBN_PREFIX_2 = "979"

INSERT = "insert"

SELECT = "select"

FIND = "find"

# Delete
DELETE = "delete"

DELETE_APPROVED = 'delete;'

DELETING = "Eliminazione del libro selezionato..."

DELETED = "Libro eliminato."

SELECT_BOOK_TO_DELETE = "Quale libro vuoi eliminare?"


# Books and Sales
ON_SALE_CONFIRM = "Il libro è stato messo in vendita."

LIST_BOOKS = "Hai i seguenti libri in vendita:\n"

NO_BOOKS = "Non hai libri in vendita."

BOOKS = "Books"

MARKET = "Market"

SEARCHING_ISBN = "Ricerca del libro associato all'ISBN inserito..."

SEARCH_RESULT = "La ricerca ha prodotto i seguenti risultati:\n"

NOTHING_FOUND = "Non ho trovato nulla."

BOOK_NOT_AVAILABLE = "Libro non trovato. Controlla di aver inserito correttamente l'ISBN. Se l'ISBN è corretto, utilizza il comando /richiedi per fare una richiesta di inserimento manuale."


#Scraping
URL_1 = "https://catalogo.unict.it/search/i?SEARCH="

URL_2 = "&sortdropdown=-&searchscope=9"

NO_MATCHES = "No matches found"
