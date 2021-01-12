from datetime import datetime
#cerinta 1, instaleaza modului pygal si apoi importeaza; pip install pygal
import pygal

class Stoc:
    """Tine stocul unui depozit"""

    def __init__(self, prod, categ, um='Buc', sold=0):
        self.prod = prod			# parametri cu valori default ii lasam la sfarsitul listei
        self.categ = categ  		# fiecare instanta va fi creata obligatoriu cu primii trei param.
        self.sold = sold			# al patrulea e optional, soldul va fi zero
        self.um = um
        self.i = {}					# fiecare instanta va avea trei dictionare intrari, iesiri, data
        self.e = {}					# pentru mentinerea corelatiilor cheia operatiunii va fi unica
        self.d = {}

    def intr(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        self.data = data
        self.cant = cant
        self.sold += cant          # recalculam soldul dupa fiecare tranzactie
        if self.d.keys():               # dictionarul data are toate cheile (fiecare tranzactie are data)
            cheie = max(self.d.keys()) + 1
        else:
            cheie = 1
        self.i[cheie] = cant       # introducem valorile in dictionarele de intrari si data
        self.d[cheie] = self.data

    def iesi(self, cant, data=str(datetime.now().strftime('%Y%m%d'))):
        #   datetime.strftime(datetime.now(), '%Y%m%d') in Python 3.5
        self.data = data
        self.cant = cant
        self.sold -= self.cant
        if self.d.keys():
            cheie = max(self.d.keys()) + 1
        else:
            cheie = 1
        self.e[cheie] = self.cant       # similar, introducem datele in dictionarele iesiri si data
        self.d[cheie] = self.data

    def fisap(self):

        print('Fisa produsului ' + self.prod + ': ' + self.um)
        print(40 * '-')
        print(' Nrc ', '  Data ', 'Intrari', 'Iesiri')
        print(40 * '-')
        for v in self.d.keys():
            if v in self.i.keys():
                print(str(v).rjust(5), self.d[v], str(self.i[v]).rjust(6), str(0).rjust(6))
            else:
                print(str(v).rjust(5), self.d[v], str(0).rjust(6), str(self.e[v]).rjust(6))
        print(40 * '-')
        print('Stoc actual:      ' + str(self.sold).rjust(10))
        print(40 * '-' + '\n')

    def proiectie(self, perioada, prod):        #proiect cerinta 1  Implementati o solutie care sa returneze o proiectie grafica a intrarilor si iesirilor intr-o
anumita perioada, pentru un anumit produs;
        self.perioada = perioada

        stoc_chart = pygal.Bar()
        stoc_chart.add( 'Proiectie grafica Stoc',

banane = Stoc('banane', 'fructe', 'kg')     # creare instante pentru categoria "fructe" din clasa Stoc
struguri = Stoc('struguri', 'fructe', 'kg')

bere = Stoc('bere', 'alcool', 'litru')      # creare instante pentru categoria "alcool" din clasa Stoc
vodka = Stoc('vodka', 'alcool', 'litru')

magneziu = Stoc('magneziu', 'suplimente')       # creare instante pentru categoria "suplimente" din clasa Stoc
calciu = Stoc('calciu', 'suplimente')

nurofen = Stoc('nurofen', 'medicamente')        # creare instante pentru categoria "medicamente" din clasa Stoc
claritine = Stoc('claritine', 'medicamente')

"""
fragute.sold                    # ATRIBUTE
fragute.prod
fragute.intr(100)
fragute.iesi(73)
fragute.intr(100)
fragute.iesi(85)
fragute.intr(100)
fragute.iesi(101)

fragute.d                       # dictionarele produsului cu informatii specializate
fragute.i
fragute.e

fragute.sold
fragute.categ
fragute.prod
fragute.um

fragute.fisap()

lapte.intr(1500)
lapte.iesi(975)
lapte.intr(1200)
lapte.iesi(1490)
lapte.intr(1000)
lapte.iesi(1200)

lapte.fisap()

l = [fragute, lapte, ceasuri]

for i in l:
    i.fisap()
"""