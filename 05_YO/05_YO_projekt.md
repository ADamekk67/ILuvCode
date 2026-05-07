# Dailyo

## Popis a cíl projektu
Dailyo je jednoduchá desktopová aplikace vytvořená pomocí `customtkinter`. Cílem projektu je mít startovací okno s názvem a vlastní ikonou, které může být později rozšířeno o funkce pro správu denních úkolů nebo připomínek.

## Funkcionalita programu
- Aplikace spouští hlavní `CTk` okno s titulem `Dailyo v0.1.0`.
- Nastavuje pevnou velikost okna `400x300`.
- Načítá ikonu z `assets/icon.png` a používá ji pro okno, pokud soubor existuje.
- Pokud ikona chybí, zobrazí se varování v konzoli.

## Technická část
- Použité knihovny:
  - `customtkinter` pro moderní Tkinter GUI.
  - `Pillow` (`PIL`) pro načítání obrázku, pokud je ikona ve formátu `.png`.
  - `pathlib` pro práci s cestami k souborům relativně ke skriptu.
- Struktura programu:
  - `app.py` obsahuje třídu `App(ctk.CTk)`.
  - V konstruktoru se inicializuje okno, nastaví se titulek a rozměry.
  - Ikona se načítá z místní složky `05_DailYO/assets`.
  - Nejprve se hledá `icon.ico`; pokud není dostupný, použije se `icon.png`.
  - Pro `.ico` se volá `self.iconbitmap(...)`, pro `.png` se ikona převede přes `ImageTk.PhotoImage`.
  - V aktuálním stavu aplikace není žádné další GUI ovládání kromě základního okna.
