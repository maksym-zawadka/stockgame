# Tester umiejętności początkującego gracza giełdowego 

Jest to moja praca inżynierska, której celem było stworzenie aplikacji, która będzie wspierać osoby rozpoczynające swoją przygodę z inwestowaniem poprzez pomaganie im w zrozumieniu i rozwijaniu kluczowych umiejętności niezbędnych do skutecznego zarządzania portfelem inwestycyjnym.

## Koncepcja aplikacji
Aplikacja ma za zadanie umożliwić użytkownikowi wybór i analizowanie akcji 
z wykorzystaniem wskaźników analizy technicznej. Gracz może również dokonywać 
transakcji kupna oraz sprzedaży papierów wartościowych. W aplikacji znajduje się 
również panel edukacyjny, gdzie użytkownik może pogłębić swoją wiedzę na temat 
inwestowania i analizy technicznej.  Wobec tego, że aplikacja ma 
zapewnić użytkownikowi możliwość zastosowania analizy technicznej, konieczne 
będzie przedstawienie mu rezultatów swoich poczynań. Z tego powodu postanowiłem 
umieścić całą rozgrywkę w przeszłości, aby gracz mógł zweryfikować obrane przez 
siebie strategie inwestycyjne bez konieczności czekania tygodni czy też miesięcy. 

**Przyjęte założenia:**</br>
• Wartość początkowa portfela jest z góry ustalona i wynosi 5000 dolarów</br>
• Portfela nie można doładować, aby móc porównywać otrzymane na końcu rozgrywek wyniki</br>
• Rozgrywka dotyczy jednego użytkownika</br>
• Gra zaczyna się 02.01.2015</br>
• Gra kończy się ostatniego dnia, dla którego zgromadzone są dane, czyli 10.11.2017</br>
• Do dyspozycji gracza jest 458 wyselekcjonowanych spółek i indeksów o wysokiej płynności wybranych z amerykańskich giełd NYSE oraz NASDAQ

Diagram przypadków użycia</br>

![obraz](https://github.com/user-attachments/assets/3866d235-0725-4d6f-911b-4e9a17c2b073)</br>

## Architektura aplikacji</br>
Wybrany wzorzec architektoniczny to MVT(Model-View-Template)</br>
Model – reprezentacja danych oraz zarządzanie nimi.</br>
Widok – obsługa żądań, przetwarzanie danych</br>
Szablon – prezentacja danych użytkownikowi</br>

Schemat wzorca MVT</br>
![obraz](https://github.com/user-attachments/assets/600a228c-3a68-4a08-a0d8-d267f5cbd817)

## Pozyskanie i przygotowanie danych</br>
Zbiór danych ze strony kaggle.com</br>
https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs</br>
Wybrane zostały największe i najbardziej płynne spółki z amerykańskiego indeksu S&P 500</br>

Plik przechowujący dane poszczególnego papieru wartościowego składa się </br>
z rekordów zawierających informacje w następującej kolejności:</br>
– data rozpatrywanego dnia,</br>
– cena otwarcia,</br>
– najwyższa cena w ciągu dnia,</br>
– cena zamknięcia,</br>
– najniższa cena w ciągu dnia,</br>
– wolumen obrotów w danym dniu.</br>

Struktura pliku przechowującego dane na temat akcji na przykładzie akcji spółki Apple:</br>
![obraz](https://github.com/user-attachments/assets/cccab054-38d1-4f5a-b7b8-24531e127f24)

## Prezentacja aplikacji</br>

**Strona główna</br>**
![obraz](https://github.com/user-attachments/assets/a499a9fb-e1a9-4bf5-b819-699cd2480523)

**Ekran startowy panelu Analiza</br>**
![obraz](https://github.com/user-attachments/assets/0c94f62a-d8d0-44b7-a9ac-111f3078f4b6)

**Zaawansowana analiza akcji Apple</br>**
![obraz](https://github.com/user-attachments/assets/1121abc5-4200-40d3-9533-14b2234df6b4)

**Panel Portfela</br>**
![obraz](https://github.com/user-attachments/assets/a1bd088d-614b-4279-8751-d3ed30aff462)

**Panel Edukacja**</br>
![obraz](https://github.com/user-attachments/assets/78646cfb-eb2b-4d00-a48d-69316b9985f1)

**Podsumowanie rozgrywki**</br>
![obraz](https://github.com/user-attachments/assets/d02baa55-b900-4c75-993e-4d32e8c8f1d1)

