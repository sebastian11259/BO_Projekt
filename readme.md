classes.xlsx - plik zaweirający liste sal (numery sal)\
teacheers.xlsx - plik zawierający listę nauczycieli (imiona i nazwiska)

# structures.py
## opis 
plik zawiera klasy na których odbywa się optymalizacja

## klasy, metody oraz atrybuty

* Teachers:
  * ```__init__``` - tworzy pustą listę: "list" oraz słownik: "dict"
  * ```add_teacher``` - dodaje nauczyciela przyjmuję jedne argument "name" typu string który dodawnay jest do list a w słowniku tworzony jest do niego zkrelwoany index
  * ```get_id``` - zwraca index nauczciela, przyjmuje jeden argument "name" i zwraca zkorelowany index ze słownika

* Classes:
  * ```__init__``` - tworzy pustą listę: "list" oraz słownik: "dict"
  * ```add_calss``` - dodaje nauczyciela przyjmuję jedne argument "nr" typu int który dodawnay jest do list a w słowniku tworzony jest do niego zkrelwoany index
  * ```get_id``` - zwraca index nauczciela, przyjmuje jeden argument "nr" i zwraca zkorelowany index ze słownika

* Subject:
  * ```__init__```:
    * argumenty:
      * name - nazwa przedmiotu
      * hours - liczba godzin w tygodniu
      * teachers - lista nauczycieli mogących prowadzić dany przedmiot
      * classes - lista sal w których może odbuywać się przedmiot
    * działanie:
      ```python
        self.name = name
        self.hours = hours
        self.hours_left = hours#zmienna pomocnicza
        #opisująca ile pozostało godzin do rozłozenia
        self.teachers = teachers
        self.classes = classes
      ```
  * ```get_t``` - zwraca listenauczycieli
  * ```get_c``` - zwraca liste klas
* Year:
  * ```__init__```
    * args: name: str
      * fun:
      ```python
        self.name = name
        self.subjects: List[Subject] = []
        self.hours_left = 0 
        #liczba godzi ncałego roku
      ```


* TimeTable:
  * ```__init__``` - 
    * args: None
    * fun:
      * ładuje klasy z xlsx do zmiennej calsses
      * ładuje nauczycieli z xlsx do zmiennej teachers
      * tworzy liste roczników "years"
      * tworzy słownik roczników "d_years"
      * tworzy tablice 4 wymairową gdzie: pierwszy wymiar to przejście między kalendarzami(index 0 = klasy, 1 = nauczycielowie, 2 = sale), 2gi wymiar to index poszczególnych klsa, nauczycieli oraz klas, 3ci wymiar to dni tygodnia, a 6 to bloki godzinowe
  * ```update_size``` - ustawia rozmiar klas w atrybucie tables na liczbe roczników, nie przyjmuje argumentów
  * ```add_year``` - pobiera zmienną typu "Year" i dodaje ją do klasy
  * ```choose_teacher``` - pobiera przedmiot, dzień, oraz okno czasowe i zwraca pierwszego wolnego nauczyciela 
  * ```choose_class``` - to samo co wyżej
  * ```put_sub``` - ustawia przedmiot w kalendarzu klas oraz w miare możliwości w kalendarzach nauczycieli oraz sal
  * ```get_year_id``` - przyjmuje rok typu "Year" zwraca jego index
  * ```all_years``` - zwraca liste roczników
  * ```all_teachers```  -||-
  * ```all_classes```  -||-
  * ```load_year``` - dodaje roczniki z folderu 'Klasy'
  * ```get_tables``` - zwraca liste planów dla roczników
  * ```initial_1``` - rozkłada zajęcia po kolei w wolnych terminach
  * ```initial_2``` - rozkłada zajęcia po kolei w wolnych terminach tylko gdy jest wolny nauczyciel i sala, dopiero potem jak sie nie udało rozdzielić wszystkich to reszte rozklada w pierwszysch wolnych terminach
  * ```beggining_time``` - zwraca liste dla każdego rocznika, kar za opóźnienie w rozpoczęciu zajęć 
  * ```finishing_time``` - zwraca liste dla każdego rocznika, kar za opóźnienie w zakonczeniu zajęć (wagi są ujemne ponieważ liczy jako im wcześniej tym lepiej)
  * ```windows``` - zwraca liste dla każdego rocznika, kar za okienka w  zajęciach
  * ```lack_of_teacher``` - zwraca liste dla każdego rocznika, kar za brak nauczyciela
  * ```lack_of_rooms``` - zwraca liste dla każdego rocznika, kar za brak sali