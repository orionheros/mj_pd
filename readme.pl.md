# PD UI Manager
[![Licencja: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[🇵🇱 Polski] | [🇺🇸 English](readme.md)

Program komputerowy do obliczania średnich grubości podkładek regulacyjnych w pompowtryskiwaczach 1.9 i 2.0 TDI (Pumpe Düse). Zaprojektowane z myślą o mechanikach i pasjonatach silników diesla.

Szczegółowa instrukcja obsługi pojawi się wkrótce w programie.

## Funkcje
* **Precyzyjne obliczenia:** Dokładne wyliczanie grubości podkładek regulacyjnych dla zestawów wtryskiwaczy.
* **Nowoczesny interfejs:** Zbudowany w oparciu o PyQt6, zapewniający natywny wygląd i intuicyjną obsługę.
* **Wysoka wydajność:** Wizualizacja danych w czasie rzeczywistym przy użyciu biblioteki pyqtgraph.

## Instalacja

### WYMAGANIA:

- **Python 3.10+**

- **Git**

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/orionheros/mj_pd.git
   cd mj_pd
   ```
2. Przygotuj środowisko wirtualne .venv i zainstaluj wymagane biblioteki:

   Windows:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

   Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements_linux.txt
   ```

3. Uruchom program:

   ```bash
   python -m pd
   ```

## Geneza projektu

Pomysł na program zrodził się z potrzeby przyspieszenia i usprawnienia procesu ustawiania ciśnienia otwarcia w pompowtryskiwaczach (PD - Pumpe Duse). Celem narzędzia jest weryfikacja tezy o istnieniu uśrednionych, powtarzalnych grubości podkładek regulacyjnych (oraz ich sumy wraz ze sprężyną) wewnątrz wtryskiwacza. Program jest narzędziem analitycznym – jego sercem jest gromadzona baza danych, którą użytkownik buduje w folderze data.

Do bazy wprowadza się wyniki pomiarów otrzymane podczas regulacji ciśnienia. Na ich podstawie aplikacja wylicza wartości średnie oraz inne parametry (kolejne funkcjonalności pojawią się w przyszłych aktualizacjach).

## O autorze 

Moja przygoda z programowaniem rozpoczęła się latem 2025 roku. Mimo że naukę traktuję hobbystycznie i uczę się dla własnej satysfakcji, dążę do tworzenia darmowych narzędzi z otwartym kodem źródłowym, które mogą realnie pomóc innym w pracy.

Za każdą pomoc, uwagi, wsparcie lub słowa zachęty będę bardzo wdzięczny.