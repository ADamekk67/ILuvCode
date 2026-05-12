# YO

## Popis a cíl projektu
YO je jednoduchá desktopová aplikace vytvořená pomocí `customtkinter`. Cílem projektu je vytvořit moderní okno s kontextovým menu, které může být dále rozšířeno o správu uzlů („nodes“) a další interaktivní funkce.

## Funkcionalita programu
- Aplikace spouští hlavní `CTk` okno s titulkem `YO v0.1.7`.
- Nastavuje pevnou velikost okna `1200x600`.
- Načítá ikonu z `assets/icon.ico`, pokud soubor existuje.
- Obsahuje pravé tlačítko myši pro zobrazení rychlého kontextového menu.
- Kontextové menu má položky `New Node`, `Nodes List`, `Remove Node` a `Settings`.
- `New Node` otevře vstupní dialog pro zadání názvu uzlu a uloží ho do seznamu `nodes`.
- `Nodes List` zobrazí aktuální seznam uzlů v konzoli (placeholder).
- `Remove Node` odstraní poslední uzel ze seznamu.
- `Settings` otevře nastavení (placeholder).

## Technická část
- Použité knihovny:
  - `customtkinter` pro moderní GUI komponenty.
  - `tkinter` pro nativní menu a dialogy.
  - `pathlib` pro práci s cestami k souborům.
  - `json` je importován pro budoucí ukládání nastavení.
- Struktura programu:
  - `app.py` obsahuje třídu `App(ctk.CTk)` s inicializací hlavního okna.
  - V konstruktoru se nastavuje titulek, velikost, ikona a zpracování události zavírání okna.
  - Vytváří se rámec `CTkFrame`, na který je navázána pravým tlačítkem metoda `on_right_click`.
  - Kontekstové menu se vytváří pomocí `tk.Menu` s vlastním stylováním (font, barvy) a zobrazuje při pravém kliknutí.
  - Funkce `qm_new_node` zobrazí vstupní dialog pro vytvoření nového uzlu a uloží ho do seznamu `nodes`.
  - Funkce `qm_remove_node` odstraní poslední uzel ze seznamu.
  - Položky menu `Nodes List` a `Settings` jsou momentálně placeholdery, které vypisují informace do konzole.

## Stav projektu
- Aplikace je v prototypové fázi.
- Základní GUI a kontextové menu fungují.
- Chybí vizualizace uzlů a trvalé uložení dat.
- Následující rozšíření může zahrnovat grafické zobrazení uzlů, práci se souborem `settings.json`, a více funkcí v kontextovém menu.
