# <ins>_ ESTIMAREA DIMENSIUNII/FORMEI MELANOMULUI</ins>_


## SCURTĂ DESCRIERE A PROIECTULUI ȘI A SCHEMEI BLOC: 


### 1. INTRODUCERE

Proiectul intitulat "Estimarea dimensiunii/formei melanomului", dezvoltat în cadrul disciplinei "Prelucrarea imaginilor "  își propune dezvoltarea unui sistem automatizat pentru analiza imaginilor din domeniul medical, în cazul nostru, analiza imaginilor dermatoscopice care surprind leziuni cutanate ale pielii numite MELANOAME în scopul diagnosticării cancerului și a formelor sale.
Prin prelucrarea  imaginilor, așa cum spune și titlul disciplinei, urmărim extragerea unor caracteristici relevante ce ne pot ajuta în identificarea diagnosticului, precum aria, perimetrul, simetria și coeficientul de circularitate a leziunii.

### 2.

În schema bloc realizată mai sus, sunt punctate etapele parcurse de noi pentru realizarea acestui proiect.

### 2.1.

Primul pas în realizarea temei constă în analiza unui set de date – imagini medicale, unde sunt surprinse diverse tipuri de melanoame. Aceste imagini poartă numele de fotografii dermatoscopice și sunt capturate cu ajutorul unei camere digitale, sau cu ajutorul unui dermatoscop. Pentru a putea prelucra direct imaginile, ele vor trebui transpuse în diferite formate acceptate: jpeg, png, jpg etc.
Imaginile sunt utilizate ca input pentru sistemul de prelucrare și pentru aplicația în sine ce urmează a fi dezvoltată.

### 2.2. PROCESAREA IMAGINILOR
  Reprezintă componenta esențială pentru extragerea unor informații relevante și corecte. Aceasta se împarte în 3 mari subetape:

a) Preprocesare:
-> scop: accentuarea caracteristicilor pentru analiză/redare;
-> una dintre cele mai utilizate metode pentru îmbunătățire se realizează în domeniul spațial unde lucrăm cu matricea de pixeli;
-> în domeniul spațial putem aplica operații punctuale precum: accentuarea contrastului, limitarea culorilor, binarizarea, negativarea, operațiuni de tip fereastră, corecția gamma, conversia color-greyscale;

b) Segmentare:
-> scop: separarea zonei afectate pe care vrem să o analizăm (melanomul) de pielea sănătoasă;
-> metode: segmentare bazată pe praguri, algoritmi de detecție a conturului;

c) Postprocesarea:
-> scop: rafinarea rezultatului segmentării și corectarea erorilor rămase;
-> aplicăm operații precum: netezirea conturului, umplerea golurilor, eliminarea zonelor nerelevante investigării noastre;

### 3. Analiza: EXTRAGEREA CARACTERISTICILOR
  În urma etapei de segmentare, unde am obținut caracteristicile corecte, vom trece la analiza leziunii pentru a estima dimensiunea și forma.
Estimarea dimensiunii melanomului analizat se poate face prin:
-> calculul ariei (numărul total de pixeli incluși în zona afectată);
-> calculul perimetrului (lungimea conturului zonei segmentate);

Analiza formei se poate face prin:
-> evidențierea conturului;
-> analiza simetriei și a circularității, pentru care vom utiliza coeficientul de circularitate calculat pe baza formulei:
C = (4π * Aria) / Perimetru^2;
-> în urma documentației medicale studiate, se observă faptul că acest coeficient este important în diagnostic, ceea ce înseamnă că:
dacă C ≈ 1, formă rotundă, regulată ⇒ melanom benign,iar dacă C < 0.7, formă neregulată ⇒ forma melanomului este una suspectă în domeniu și necesită investigații suplimentare;

### 4. INTERPRETAREA REZULTATELOR
  Obiectivele urmărite sunt:
-> compararea valorilor obținute cu datele de referință;
-> identificarea regularității / neregularității conturului;
-> emiterea unor etichete descriptive: melanom suspect, leziune regulată;
Această etapă   reprezintă un sprijin major pentru diagnosticul medical;

### 5. RAPORT FINAL
  La finalul proiectului, după scrierea codului și modificările făcute asupra lui și a imaginilor folosite din setul de date, se generează un raport descriptiv care include:
-> imaginea originală, imaginea segmentată, conturul evidențiat, valorile calculate pentru arie, perimetru și coeficient de formă, concluziile interpretate pe baza rezultatelor.
Aceste rezultate pot fi folosite de către cadrele medicale pentru a completa investigațiile și pentru a monitoriza evoluția leziunilor cutanate.

### 6. CONCLUZIE
  Proiectul propune un sistem eficient de prelucrare a imaginilor dermatoscopice pentru diagnosticarea / analiza formei melanomului. Prin integrarea unor metode specifice și a operațiilor aplicate imaginilor, obținem rezultate utile pentru un diagnostic rapid și precis.


