# Melanoma Shape and Size Estimation (Estimarea formei și dimensiunii unui melanom)

[cite_start]This project, developed for the **"Image Processing"** discipline [cite: 3][cite_start], focuses on the automated analysis of dermoscopic images to identify and evaluate skin lesions (melanomas)[cite: 7]. [cite_start]The goal is to provide a faster and more objective diagnostic tool by extracting relevant morphological features[cite: 7, 9].

---

## 📖 Introduction & Objectives
[cite_start]The system is designed to automate the medical analysis of skin lesions to aid in cancer diagnosis[cite: 7]. [cite_start]By processing dermoscopic images, we extract key characteristics such as **Area**, **Perimeter**, and **Circularity** to identify the nature of the lesion[cite: 17, 38].

---

## ⚙️ Processing Pipeline (Block Diagram)
[cite_start]The project follows a rigorous flow consisting of three main stages[cite: 8, 25]:

### 1. Preprocessing
* [cite_start]**Color to Grayscale:** Converting the image to simplify analysis[cite: 30].
* [cite_start]**Gaussian Filter:** Applied for noise reduction[cite: 33].
* [cite_start]**Black-Hat Transform & Inpainting:** Used to remove artifacts such as hairs and enhance lesion features[cite: 34, 35].

### 2. Segmentation
* [cite_start]**Otsu Segmentation:** Automatically separating the lesion from healthy skin based on thresholding[cite: 31].

### 3. Post-processing
* [cite_start]**Flood Fill & Morphological Operations:** Used to refine the segmented mask and fill internal gaps[cite: 32, 36].
* [cite_start]**Connected Components:** Identifying and isolating the specific lesion area[cite: 37].

---

## 📊 Feature Extraction & Medical Interpretation
[cite_start]From the final refined mask, we extract the following morphological descriptors[cite: 38]:
* [cite_start]**Area ($A$):** Total pixel count of the affected area[cite: 17, 38].
* [cite_start]**Perimeter ($P$):** The length of the lesion's contour[cite: 17, 39].
* [cite_start]**Circularity Coefficient ($C$):** Calculated as $$C = \frac{4\pi \cdot Area}{Perimeter^2}$$[cite: 40].
    * **$C \approx 1$:** Regular shape, typically indicating a **benign** lesion.
    * **$C < 0.7$:** Irregular shape, suggesting a **suspicious** melanoma that requires further investigation.

---

## 📈 Dataset & Performance Results
* [cite_start]**Dataset:** ISIC Challenge Dataset containing 65 dermoscopic images in RGB format[cite: 19, 20, 21].
* [cite_start]**Evaluation Metrics:** Performance was measured against Ground-Truth masks using IoU and Dice coefficients[cite: 11, 12, 13].

| Metric | Initial Value (Mean) | Final Value (Mean) |
| :--- | :---: | :---: |
| **IoU (Intersection over Union)** | [cite_start]0.62812 [cite: 43] | [cite_start]**0.71937** [cite: 43] |
| **Dice Coefficient** | [cite_start]0.74282 [cite: 43] | [cite_start]**0.81652** [cite: 43] |

[cite_start]The results highlight that post-processing significantly improves the accuracy of the segmentation[cite: 46, 47].

---

## 🏆 Final Report & Conclusions
[cite_start]The project generates a descriptive report including the original image, the segmented mask, highlighted contours, and calculated values[cite: 45]. [cite_start]This serves as a major support tool for medical professionals in monitoring skin lesion evolution[cite: 45].

---

## 👥 Authors
* [cite_start]**Aciocârlănoaei Georgiana** - Group 1310A [cite: 48]
* [cite_start]**Panaite Elena - Alexandra** - Group 1309B [cite: 48]

[cite_start]**Institution:** "Gheorghe Asachi" Technical University of Iași[cite: 1, 2, 5].
