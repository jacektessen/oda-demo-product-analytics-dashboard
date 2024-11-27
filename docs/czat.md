Podsumowanie projektu demo dla ODA - Dashboard produktowy

**Cel projektu:** 
Stworzenie dashboardu wizualizującego dane produktowe z API ODA, pokazującego rozkład produktów według cen, marek i innych atrybutów.

**Stack technologiczny:**

Frontend:
- Next.js jako framework bazowy
- Tailwind CSS + DaisyUI dla stylowania
- Recharts do wykresów
- TanStack Table do tabel
- Zustand (opcjonalnie) do state management

Backend/Infrastruktura:
- Python script do agregacji danych z API ODA
- Redis jako storage dla zagregowanych danych
- Next.js API routes jako gateway
- Docker dla konteneryzacji
- GitHub Actions dla CI/CD

**Kluczowe funkcjonalności dashboardu:**
1. Analiza cenowa (wykresy rozkładu cen)
2. Analiza marek (udziały marek w asortymencie)
3. Statystyki dostępności produktów
4. Interaktywne filtry
5. Szczegółowe statystyki produktowe

**Testowanie:**
1. Playwright dla testów E2E 
2. Contract testy dla API
3. k6 dla performance testów
4. Abstrakcja dla logowania (bez pełnej implementacji Grafany/Prometheusa)

**API:**
- Endpoint ODA: `https://oda.com/api/v1/search/mixed/?q=`
- Iteracja przez strony dla pełnych danych
- Cache w Redis dla zoptymalizowanej wydajności

**Podejście do developmentu:**
1. Focus na wersji desktopowej (min. 1200-1400px szerokości)
2. Implementacja CI/CD przez GitHub Actions
3. Containerization przez Docker
4. Podstawowy monitoring i logi

**Uwagi dodatkowe:**
- Projekt ma charakter demo na rozmowę kwalifikacyjną
- Nacisk na jakość kodu i architekturę
- Możliwość łatwej prezentacji funkcjonalności
- Skalowalność rozwiązania

To podsumowanie zawiera wszystkie kluczowe elementy ustalone podczas naszej rozmowy i może służyć jako punkt startowy do implementacji projektu.


Na podstawie dostarczonego przykładu danych z API, oto kilka sugestii odnośnie wykresów i tabel, które mógłbyś zaprezentować użytkownikowi w dashboardzie produktowym:

1. Rozkład cenowy produktów:
   - Wykres słupkowy lub histogram pokazujący liczbę produktów w różnych przedziałach cenowych.
   - Oś X: Przedziały cenowe (np. 0-10 NOK, 10-20 NOK, 20-30 NOK itp.)
   - Oś Y: Liczba produktów w danym przedziale cenowym

2. Top marki według liczby produktów:
   - Wykres kołowy prezentujący udział najpopularniejszych marek w całym asortymencie.
   - Każdy wycinek koła reprezentuje markę i jej procentowy udział w całkowitej liczbie produktów.
   - Możesz ograniczyć się do top 10 marek, a pozostałe zgrupować jako "Inne".

3. Dostępność produktów:
   - Wykres słupkowy pokazujący liczbę produktów dostępnych i niedostępnych.
   - Kategorie: "Dostępne", "Niedostępne"
   - Wysokość słupków wskazuje liczbę produktów w każdej kategorii.

4. Tabela z filtrowaniem i sortowaniem:
   - Kolumny: Nazwa produktu, Marka, Cena, Dostępność
   - Możliwość filtrowania po marce, przedziale cenowym, dostępności
   - Sortowanie po nazwie, cenie rosnąco/malejąco
   - Paginacja wyników, jeśli liczba produktów jest duża

5. Statystyki dotyczące promocji i rabatów:
   - Wykres słupkowy pokazujący liczbę produktów objętych promocją lub rabatem vs produkty bez promocji.
   - Kategorie: "W promocji", "Bez promocji"
   - Wysokość słupków wskazuje liczbę produktów w każdej kategorii.

6. Rozkład produktów według specyfikacji (jeśli dostępne w API):
   - Wykresy kołowe lub słupkowe pokazujące liczbę/udział produktów w kategoriach takich jak "Bez glutenu", "Wegańskie", "Ekologiczne" itp.
   - Każda kategoria to osobny wykres.

7. Średnie ceny według marek:
   - Wykres słupkowy prezentujący średnią cenę produktu dla top marek.
   - Oś X: Marki
   - Oś Y: Średnia cena produktu danej marki

Pamiętaj, że to tylko sugestie na podstawie jednego przykładowego obiektu z API. W zależności od pełnej struktury danych i wymagań biznesowych, możesz dostosować wykresy i tabele do konkretnych potrzeb.

Kluczowe jest, aby wykresy i tabele były interaktywne, responsywne i łatwe w interpretacji dla użytkownika. Warto też zadbać o odpowiednie opisy osi, legendy i tytuły, aby użytkownik dokładnie wiedział, co przedstawiają dane.