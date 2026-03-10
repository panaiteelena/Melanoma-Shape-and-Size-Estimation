# <ins>_TITLU  : ESTIMAREA DIMENSIUNII/FORMEI MELANOMULUI</ins>_

## TABEL CU ANALIZA LITERATURII DE SPECIALITATE :



| Autor(i) / An | Titlul articolului / proiectului | Aplicație / Domeniu | Tehnologii utilizate | Metodologie / Abordare | Rezultate | Limitări | Comentarii suplimentare |
|----------------|----------------------------------|----------------------|-----------------------|--------------------------|------------|-------------|----------------------------|
| **Fakhre Alam, Asad Ullah, Dilwar Shah (2025)** | *Artificial Intelligence in Melanoma Detection: a review of current technologies and future directions* | Medicină, diagnostic cancer de piele | Camere pentru captură imagine, biblioteci AI, TensorFlow, Python, OpenCV | Utilizarea rețelelor neuronale convoluționale (CNN) pentru extragerea trăsăturilor și segmentarea leziunii | Metrici: Dice coefficient, Jaccard index, accuracy, precision | Seturi de date insuficient diverse (tonuri de piele, rezoluție variabilă) | Analiză detaliată a tehnologiilor moderne de detecție AI în dermatologie |
| **Muhammad Mateen, Shaukat Hayat, Fizzah Arshad, Yeong-Hyeon Gu, Mugahed A. Al-antari (2024)** | *Hybrid Deep Learning Framework for Melanoma Diagnosis Using Dermoscopic Medical Images* | Segmentare + clasificare benign vs. malign | U-Net, Inception ResNet v2, TensorFlow | Segmentare → extragere trăsături → clasificare → optimizare | ISIC2020: 98.65% acuratețe, 99.20% sensibilitate, 98.03% specificitate | Posibile biaisuri de date, complexitate mare, consum ridicat de resurse | Performanțe superioare altor metode, dar implementare complexă |
| **Marios Papadakis, Alexandros Paschos, Andreas Manios, Percy Lehmann, Georgios Manios, Hubert Zirngibl (2021)** | *Computer-aided clinical image analysis for non-invasive assessment of tumor thickness in cutaneous melanoma* | Diagnostic non-invaziv al grosimii melanomului | Software de procesare imagine RGB | Analiză culoare (R,G,B): range, deviație standard, skewness; extragere descriptori geometrici: arie, diametru, perimetru, circularitate, excentricitate, rază medie | Măsurători geometrice și cromatice precise | Imagini 2D clinice, fără adâncime | Precizie ridicată pentru estimarea formei melanomului |
| **GeeksforGeeks (2025)** | *Measure Size of an Object Using Python OpenCV* | Analiză imagini medicale, măsurare dimensiuni leziuni | Python, OpenCV (cv2), NumPy | 1. Încărcare imagine → 2. Conversie grayscale → 3. Threshold → 4. Contururi → 5. Arie → 6. Scalare în unități reale → 7. Afișare rezultate | Dimensiune obiect în unități reale (cm²) + contur vizibil | Forme complexe sau margini nedefinite pot da erori | Cod simplu, ușor de adaptat pentru măsurarea dimensiunilor melanomului |
| **Adrian Rosebrock (2021)** | *OpenCV Shape Detection* | Procesare imagini, recunoaștere forme geometrice | Python, OpenCV, imutils | Detecție contururi (cv2.findContours) + aproximare (cv2.approxPolyDP); clasificare după numărul de colțuri și raportul de aspect | Detecție precisă a formelor geometrice simple | Funcționează doar cu contururi clare, fără zgomot; nu oferă segmentare semantică | Bază pentru analiză geometrică a leziunilor simple |
| **Sovit Rath (2021)** | *Contour Detection using OpenCV (Python/C++)* | Procesare imagini, segmentare, recunoaștere obiecte | Python, OpenCV | Detecție contururi (cv2.findContours, cv2.drawContours); moduri CHAIN_APPROX_SIMPLE și NONE | Segmentare precisă prim-plan/fundal; cod exemplu pentru diverse tipuri de imagini | Eficiență scăzută pentru fundal zgomotos sau forme complexe | Explică clar principiile segmentării bazate pe contururi în OpenCV |



## SCHEMA BLOC A PROIECTULUI :
<img width="1731" height="3123" alt="schema_bloc" src="https://github.com/user-attachments/assets/9dd30d00-b28e-4d4d-9733-ffa5676d2a7c" />




## SCURTĂ DESCRIERE A PROIECTULUI ȘI A COMPONENTELOR CARE APAR ÎN SCHEMA BLOC : 


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


