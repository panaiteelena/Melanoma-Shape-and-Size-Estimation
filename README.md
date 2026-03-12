# Melanoma Shape and Size Estimation 

This project, developed for the "Image Processing" discipline at the Gheorghe Asachi Technical University of Iași, aims to create an automated system for analyzing dermoscopic images. The primary objective is to identify and evaluate skin lesions (melanomas) to support a faster and more objective medical diagnosis.By utilizing advanced image processing techniques, the system extracts key morphological features—such as Area, Perimeter, and Circularity—which are critical in distinguishing between benign lesions and suspicious melanomas.

---

##  Introduction & Objectives
The system is designed to automate the medical analysis of skin lesions to aid in cancer diagnosis. By processing dermoscopic images, we extract key characteristics such as **Area**, **Perimeter**, and **Circularity** to identify the nature of the lesion

---

##  Processing Pipeline (Block Diagram)
The project follows a rigorous flow consisting of three main stages

### 1. Preprocessing
* **Color to Grayscale:** Converting the image to simplify analysis
* **Gaussian Filter:** Applied for noise reduction
* **Black-Hat Transform:** Highlighting dark structures (like hairs) for removal
* **Inpainting:** Removing artifacts (hairs/scales) and filling the gaps to focus solely on the skin lesion

### 2. Segmentation
* **Otsu Segmentation:** Automatically separating the lesion from healthy skin based on thresholding

### 3. Post-processing
* **Flood Fill & Morphological Operations:** Used to refine the segmented mask (by removing the vignette from dermatoscopical images) and fill internal gaps
* **Connected Components:** Identifying and isolating the specific lesion area

---

##  Feature Extraction & Medical Interpretation
From the final refined mask, we extract the following morphological descriptors:
* **Area ($A$):** Total pixel count of the affected area
* **Perimeter ($P$):** The length of the lesion's contour
* **Circularity Coefficient ($C$):** Calculated as $$C = \frac{4\pi \cdot Area}{Perimeter^2}$$
    * **$C \approx 1$:** Regular shape, typically indicating a **benign** lesion.
    * **$C < 0.7$:** Irregular shape, suggesting a **suspicious** melanoma that requires further investigation.

---

##  Dataset & Performance Results
* **Dataset:** ISIC Challenge Dataset containing 65 dermoscopic images in RGB format
* **Evaluation Metrics:** Performance was measured against Ground-Truth masks using IoU, Dice and aria raport coefficients

| Metric | Initial Value (Mean) | Final Value (Mean) |
| :--- | :---: | :---: |
| **IoU (Intersection over Union)** | 0.62812 | **0.71937**|
| **Dice Coefficient** | 0.74282  | **0.81652** |

The results highlight that post-processing significantly improves the accuracy of the segmentation

---

##  Final Report & Conclusions
The project generates a descriptive report including the original image, the segmented mask, highlighted contours, and calculated values. This serves as a major support tool for medical professionals in monitoring skin lesion evolution

---

##  Authors
* **Aciocârlănoaei Georgiana** - Group 1310A 
* **Panaite Elena - Alexandra** - Group 1309B 

**Institution:** "Gheorghe Asachi" Technical University of Iași
[Poster - Estimarea formei si dimensiunii unui melanom.pdf](https://github.com/user-attachments/files/25928398/Poster.-.Estimarea.formei.si.dimensiunii.unui.melanom.pdf)

