System można uruchomić na dwa sposoby. Pierwszy i najłatwiejszym jest wejście na https://future-farm.herokuapp.com i uwierzytelnienie się za pomocą konta demo.

Login: demo
Hasło: KontoDemo123

Drugi podejście wymaga zainstalowania:
-Python https://www.python.org/downloads/
-Virtualenv https://virtualenv.pypa.io/en/latest/installation.html

Po zainstalowaniu ww należy otworzyć wiersz poleceń w folderze projektu i wpisać komendę:

virtualenv <nazwa> 

Następnie stworzone wirtualne środowisko należy aktywować wpisując komendę:

source <nazwa>/bin/activate

W aktywowanym środowisku instalujemy wszystkie niezbędne biblioteki i narzędzia wpisując komendę:

pip install -r requirements.txt

Po pomyślnym zainstalowaniu należy przeprowadzić stworzyć bazę danych poprzez przeprowadzenie migracji:

python manage.py migrate

Ostatnim krokiem jest uruchomienie serwera developerskiego:

python manage.py runserver

System jest gotowy do użycia pod wskazanym w wierszu poleceń adresem

Wyłączanie serwera:

ctrl+c

Deaktywacja wirtualnego środowiska:

deactivate

PROSZE MIEĆ NA UWADZE ŻE KOMENDY python I pip KORZYSTAJĄC Z PYTHONA 3 MAJĄ POSTAĆ python3 I pip3
