from datetime import datetime, timedelta
#cerinta 1, instaleaza modului pygal si apoi importeaza; pip install pygal
import pygal
from pygal.style import NeonStyle
#cerinta 3, trimite mail cu fisa produsului
import smtplib
from email.message import EmailMessage
#cerinta 4, regex
import re
#cerinta 5, creaza baza de date
import csv, sqlite3
from sqlite3 import Error

#metoda aprovizionare produs if sold < o anumita valoare; face verificare sold (in metoda iesiri?)

class Stoc:
    produse=list()                      # initializare lista cu produsele
    tprod = 0                           # variabila cu numar de produse create
    categorii =list()                   # initializare lista cu categorii
    tcateg = 0                          # variabila cu numar de categorii create
    categ_produse = {}                  # initializare dictionar cu categorii si produse
    totalcasa = 0                       # initializare total bani in casa
    def __init__(self, prod, categ, limita, um='Buc', sold=0, pret=0, plata=0, tplata=0, incasat=0, tincasat=0, casa=0):
        self.prod = prod			            # parametri cu valori default ii lasam la sfarsitul listei
        self.categ = categ
        if self.prod in Stoc.produse:
            print (f"{self.prod} exista deja in Stoc")
        Stoc.produse.append(prod)               # adaugare nume produs in lista
        Stoc.tprod += 1                         # se numara un produs nou
        if categ not in Stoc.categorii:
            Stoc.categorii.append(categ)        # adaugare nume categorie in lista (daca nu exista deja)
            Stoc.tcateg += 1                    # se numara o categorie noua
            Stoc.categ_produse[categ] = {prod}  # se completeaza in dict produsul aferent categoriei
        else:
            Stoc.categ_produse[categ].add(prod) # se adauga in dict categoria si produsul
        self.sold = sold			    # soldul va fi zero
        self.um = um
        self.i = {}					    # fiecare instanta va avea trei dictionare intrari, iesiri, data
        self.e = {}					    # pentru mentinerea corelatiilor cheia operatiunii va fi unica
        self.d = {}
        self.dstoc = {}                 # dictionarul stocului (contine data, intrari, iesiri din stoc)
        self.limita = limita            # cantitatea limita in stoc, per produs
        self.pret = pret
        self.plata = plata              # bani cheltuiti la aprovizionare (intr)
        self.tplata = tplata            # total bani cheltuiti pe aprovizionari (intrari in stoc)
        self.incasat = incasat          # bani incasati la vanzare (iesi)
        self.tincasat = tincasat        # total bani incasati pe vanzari (iesiri din stoc)
        self.casa = casa                # total bani in casa
        self.pi = {}                    # dict cu pretul produsului la intrare in stoc
        self.pe = {}                    # dict cu pretul produsului la iesire din stoc (pretn)

    def intr(self, cant, pret, data=str(datetime.now().strftime('%d-%m-%Y'))):
        self.data = data
        self.cant = cant
        self.pret = pret
        self.sold += cant                           # recalculam soldul dupa fiecare tranzactie
        plata = float(cant * pret)                  # valoare cheltuita la fiecare intrare
        self.plata = plata
        self.tplata += plata                        # valoare totala cheltuita
        self.casa -= plata                          # valoare totala in casa per produs
        Stoc.totalcasa -= self.plata                # fiecare plata e scazuta din total bani in casa
        if self.sold !=0:
            pretm = round(self.tplata / self.sold, 2)  # pretul mediu ponderat (de iesire)
        else:
            pretm = self.pret
        self.pretm = pretm
        if self.dstoc.keys():               # dictionarul data are toate cheile (fiecare tranzactie are data)
            nrtrz = max(self.dstoc.keys()) + 1 #numerotarea tranzactiilor in dictionar
        else:
            nrtrz = 1
        self.i[nrtrz] = cant       # introducem data si cant. produsului intrat in stoc in dict. stocului
        self.d[nrtrz] = data
        self.pi[nrtrz] = pret                  #introducem pretul initial in dictionar
        self.pe[nrtrz] = pretm                 #introducem pretul de iesire (nou) in dictionar
        self.dstoc[nrtrz] = (self.data, self.cant, 0, self.pret)

    def iesi(self, cant, data=str(datetime.now().strftime('%d-%m-%Y'))):
        self.data = data
        self.cant = cant
        self.pret = self.pretm
        incasat = cant * self.pret
        self.incasat = incasat                      # valoare incasata la fiecare iesire
        self.tincasat += incasat                    # valoare totala incasata
        self.casa += incasat                        # valoare totala in casa
        Stoc.totalcasa += self.incasat              # fiecare incasare este adaugata la totalul de bani in casa
        self.sold -= self.cant
        if self.dstoc.keys():
            nrtrz = max(self.dstoc.keys()) + 1
        else:
            nrtrz = 1
        self.e[nrtrz] = cant       # similar, introducem data si cant. produsul iesit din stoc in dict.
        self.d[nrtrz] = data
        self.dstoc[nrtrz] = (self.data, 0, self.cant, self.pret)
        if self.sold <= self.limita:          # verificarea stocului pentru a nu atinge limita, la fiecare iesire
            print(f'Atentie, cantitatea de {self.prod} din stoc este egala sau mai mica decat limita stabilita de {self.limita} {self.um}. Aprovizionati stocul cu {self.prod}')
        else:
            print(f'Cantitatea de {self.prod} este suficienta momentan, soldul fiind de {self.sold} {self.um}')

    def fisap(self):       # Printeaza fisa produsului in consola si o salveaza intr-un fisier (pt cerinta 3)
            f = open('fisa.txt', 'w')
            print('*-* ' * 13, file = f)
            print('Fisa produsului ' + self.prod + ', um = ' + self.um, file = f)
            print(52 * '_', file = f)
            print(' Nrc ', '  Data  ', '     Intrari', '    Iesiri', '    Pret / um', file = f)
            print(52 * '_', file = f)
            for tranzactie in self.dstoc:
                print(str(tranzactie).rjust(3),
                            str(self.dstoc[tranzactie][0]).rjust(14),
                            str(self.dstoc[tranzactie][1]).rjust(8),
                            str(self.dstoc[tranzactie][2]).rjust(8),
                            str(self.dstoc[tranzactie][3]).rjust(8), file = f)
            print(52 * '_', file = f)
            print('Stoc actual:      ' + str(self.sold).rjust(10), file = f)
            print('Total incasari:   ' + str(self.tincasat).rjust(10), file = f)
            print('Total plati:      ' + str(self.tplata).rjust(10), file = f)
            print('Total in casa     ' + str(self.casa).rjust(10), file = f)
            print('*-* ' * 13, file = f)
            f.close()
            f = open('fisa.txt')
            for line in f:
                print(line)
            f.close()

    def mailfisap(self, destinatar):    #cerinta 3: trimite e-mail cu fisa produsului
        self.destinatar = destinatar
        msg = EmailMessage()
        msg['Subject'] = f'Fisa produsului {self.prod}'
        msg['From'] = 'chelarutest@gmail.com'
        msg['To'] = destinatar
        #Adauga atasament
        with open('fisa.txt', 'rb') as content_file:
            content = content_file.read()
            msg.add_attachment(content, maintype='application', subtype='svg', filename='fisa.txt')
        #Trimite e-mail via serverul SMTP .
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login("chelarutest@gmail.com", "ChelaruTest23")
            server.send_message(msg)
            print('Mesaj expediat cu succes!')
            server.quit()
        except:
            print('Mesajul nu a putut fi expediat!')

    def cauta_prod(self):               #cerinta 4: cauta produs folosind regex
        pattern = str(input("Introduceti produsul pe care il cautati: "))
        r = re.compile(pattern)
        produs = list(filter(r.match, Stoc.produse))
        if not produs:
            print("Produsul nu a fost gasit")
        else:
            print("Produsul a fost gasit: ", produs)

    def cauta_trz(self):  # cerinta 4: cauta tranzactie folosind regex
        pattern = str(input("Introduceti valoarea tranzactiei pe care o cautati: "))
        r = re.compile(pattern)
        lista = [(v) for v in self.dstoc.values()]  # extragerea tranzactiilor din dstoc
        listastr = [[str(x) for x in tup] for tup in lista]  # conv in strings
        for a in listastr:
            gasit = list(filter(r.match, a))
            for cantitate in gasit:
                if cantitate not in a[1] and cantitate not in a[2]:
                    print("Valoarea nu a fost gasita in tranzactiile de pe stoc")
                elif cantitate in a[2]:
                    print(f"Gasit {cantitate} in tranzactia de iesire {a}")
                elif cantitate in a[1]:
                    print(f"Gasit {cantitate} in tranzactia de intrare {a}")

    def crearebd(self): #cerinta 5: crearea unei baze de date cu tabelele cerute
        try:
            conn = sqlite3.connect('stoc.db')
            print('Conectat cu succes la baza de date')
            c = conn.cursor()
            c.execute('PRAGMA foreign_keys=ON')  # activare foreign key
            # crearea bazei de date
            c.executescript('''CREATE TABLE Categoria(
                                idc INTEGER NOT NULL    PRIMARY KEY,
                                denc    TEXT    NOT NULL);
                            CREATE TABLE Produs(
                                idp INTEGER NOT NULL    PRIMARY KEY,
                                idc INTEGER NOT NULL, denp    TEXT, pret    REAL    DEFAULT O,
                                FOREIGN KEY (idc)    REFERENCES Categoria (idc)  ON UPDATE   CASCADE ON DELETE   RESTRICT);
                            CREATE TABLE Operatiuni(
                                ido INTEGER     NOT NULL    PRIMARY KEY,
                                idp INTEGER NOT NULL, cant    REAL    DEFAULT 0, date    DATE);
                            ''')
            conn.commit()
            print("Tabel creat cu succes")
            conn.close()
        except sqlite3.Error as error:
            print('Eroare la crearea tabelului', error)
        finally:
            if (conn):
                conn.close()
                print('Baza de date a fost inchisa')

    def proiectie(self):        #proiect cerinta 1
        chart = pygal.StackedBar(fill=True, interpolate='cubic', style=NeonStyle, value_font_size=6)
        chart.human_readablle = True
        chart.title = f'Tranzactii {self.prod}'
        chart.x_labels = self.d.values()
        chart.y_title = self.um
        chart.add('In', self.i.values())
        chart.add('Out', self.e.values())
        chart.render_to_file('proiectie.svg')

    def __str__(self):
        return f'Produs = {self.prod}, Categoria = {self.categ}'

# creare instante
banane = Stoc('banane', 'fructe', 20, 'kg')
nuci = Stoc('nuci', 'fructe', 20, 'kg')
magneziu = Stoc('magneziu', 'suplimente', 50)
calciu = Stoc('calciu', 'suplimente', 50)
nurofen = Stoc('nurofen', 'medicamente', 100)
claritine = Stoc('claritine', 'medicamente', 100)

#verificare liste produse, liste categorii si dictionar categorii-produse
Stoc.produse
Stoc.categorii
Stoc.categ_produse

#introduceri si iesiri din stoc pentru instante diferite, cu cantitati, preturi si date diferite
#pretul la iesiri este calculat automat, nu se mentioneaza
#verificare si CERINTA 2
banane.intr(100, 5, '10-01-2021')
banane.iesi(10, '10-01-2021')
banane.iesi(20, '11-01-2021')
banane.iesi(30, '12-01-2021')
banane.iesi(20, '13-01-2021')
banane.iesi(20, '14-01-2021')

banane.intr(300, 4, '15-01-2021')
banane.iesi(100, '16-01-2021')
banane.iesi(200, '17-01-2021')

magneziu.intr(200, 10, '10-01-2021')
magneziu.iesi(10, '10-01-2021')
magneziu.iesi(60, '12-01-2021')
magneziu.iesi(130, '13-01-2021')

magneziu.intr(200, 16, '14-01-2021')
magneziu.iesi(180, '17-01-2021')

#verificare pret produs la intrare (pret) si la iesire (pretm) (identic doar dupa o singura aprovizionare/intrare)
#verificare CERINTA 8
banane.pret
banane.pretm
magneziu.pret
magneziu.pretm

#verificare bani - tranzactii
banane.incasat  # incasat la ultima tranzactie de iesire
banane.tincasat # incasat in total (toate iesirile)
banane.plata    # platit la ultima tranzactie de intrare
banane.tplata   # platit in total (toate intrarile)
banane.casa     # total banuti ramasi dupa aprovizionari (intrari) si vanzari (iesiri), per produs

magneziu.tincasat
magneziu.tplata
magneziu.casa

Stoc.totalcasa  # total banuti in casa (toate produsele)

#verificare dictionare per produs
banane.dstoc    # dict cu toate iesirile si intrarile (miscarile) din stoc, numerotate
banane.i        # dict cu intrarile si numarul miscarii in stoc
banane.e        # dict cu iesirile si numarul miscarii in stoc
banane.d        # dict cu datele miscarilor din stoc
banane.pi       # dict cu preturile de intrare ale produsului (si nr. aferent miscarii)
banane.pe       # dict cu preturile de iesire ale produsului (si nr. aferent miscarii)

#verificare metoda fisap
banane.fisap()
magneziu.fisap()

#verificare metoda mailfisap (CERINTA 3)
banane.mailfisap('ramonachelaru@ymail.com')
#magneziu.mailfisap('paul@infoacademy.net')

#verificare metoda cauta_prod (CERINTA 4)
banane.cauta_prod()
#verificare metoda cauta_trz  (CERINTA 4)
banane.cauta_trz()

#verificare metoda crearedb   (CERINTA 5)
banane.crearebd()

#verificare CERINTA 1
banane.proiectie()
