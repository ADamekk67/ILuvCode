# Automatizace Cookie Clicker

## Popis a cíl projektu
Tento projekt je Python skript pro automatizaci klikání ve hře Cookie Clicker pomocí knihovny `pyautogui`. Cílem je automatizovat generování cookies pro zábavu a testování automatizace.

## Funkcionalita programu
Program obsahuje dva současné smyčky: jednu pro automatické klikání myší a druhou pro sledování klávesnice. Používá threading pro současný běh.

**Klávesové zkratky:**
- `k` - přepnutí automatického klikání (on/off)
- `0` - otevření nabídky možností
- `e` - ukončení programu (v nabídce možností)
- `1` - nastavení času mezi kliky
- `2` - nastavení souřadnic upgradu
- `3` - nastavení souřadnic celkového počtu cookies
- `x`, `y` - nastavení souřadnic pro počet cookies

### Technická část
- **Použité knihovny:** 
  - `pyautogui` - ovládání myši a pozice kurzoru
  - `keyboard` - detekce stisků kláves
  - `threading` - souběžný běh klikacích a klávesových smyček

- **Architektura:**
  - `click_loop()` - daemon thread pro automatické klikání na Cookie
  - `keyboard_loop()` - hlavní thread pro zpracování vstupů z klávesnice
  - Globální flagi: `AutoClicker` (stav klikání), `RunMain` (běh programu)

- **Parametry:**
  - `ClickTime` - prodleva mezi kliky (výchozí 0.05s)
  - `BigCookieCoords` - souřadnice velké cookies pro klikání
  - `TotalCookiesCoords` - souřadnice pro zobrazení počtu cookies

## Podmínky projektu
1. Průběžná práce na GitHubu  
   Práce bude průběžně ukládána do veřejného repozitáře na GitHubu.  
   Během týdne musí proběhnout vaše aktivita. Aktuální týden se počítá vždy od pondělí do neděle (23:59).  
   Alespoň 3 commity týdně: Během tohoto období musíte provést minimálně tři smysluplné commity.  
   Pravidlo 12 hodin: Mezi každým ze tří povinných commitů musí uběhnout časový rozestup alespoň 12 hodin.  

2. Kvalita commitů  
   Commit musí být smysluplně popsán.  

3. Komentování kódu  
   Kód musí být smysluplně okomentován.  

4. Technická dokumentace  
   Souběžně s programováním budete tvořit technickou dokumentaci.  

### Postup práce  
Výběr názvu projektu a organizace souborů podle pravidel. Dokumentace v souboru končícím _projekt.md.
