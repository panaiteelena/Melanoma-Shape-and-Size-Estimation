# Titlu proiect : ESTIMAREA FORMEI SI DIMENSIUNII UNUI MELANOM
# Metrici: IoU, Dice(F1), Raport Arie
# Masuratori: Arie(px), Perimetru(px), Circularitate


### PREPROCESARE(imbunatatirea calitatii imaginii) eliminand regiuni din img ce pot afecta segmentarea ###
    # 1.Conversie la grayscale +  eliminare zgomot(filtru gaussian)
    # 2.Eliminarea firelor de par ( remove_hair) - prin inpainting


### SEGMENTARE (izolarea regiunii corespunzatoare leziunii de fundal) ###
    # Functie : segmentare Otsu


### POST-PROCESARE (rafinarea mastii obtinute in urma segmentarii) ###
    #   1) Eliminare vigneta (umbrele ce apar in colturile imaginii )
    #           Metoda- flood fill(pornind din colturi)
    #           functie : remove_vignette

    #   2) Operatii morfologice OPEN/CLOSE (cv2.morphologyEx ...)
    #           - elimina petele de dimensiuni mici si umple golurile din interiorul leziunii

    #   3) Eliminare pete pigmentare (pastreaza obiectele localizate central)
    #       - functie : keep_central_components(..)


import os
import math
import cv2
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

try:
    matplotlib.use('TkAgg')
except:
    pass

IMAGE_FOLDER = "imagini"
GT_FOLDER = "masti"

# Functii ajutatoare

def binarize_mask(mask):
    """Transforma o imagine (masca) intr-o masca binara: 0/255 + varianta booleana."""
    if mask is None:
        return None, None
    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    _, mask_u8 = cv2.threshold(mask,
                               127,
                               255,
                               cv2.THRESH_BINARY)
    mask_bool = (mask_u8 > 0)
    return mask_u8, mask_bool


def calc_metrics(pred_mask, gt_mask):
    """
    Calcul IoU, Dice(F1), Raport Arie intre masca obtinuta si GT.
    Returnam valorile brute (intersectie, reuniune, arii) pentru macro-average.
    """
    _, p = binarize_mask(pred_mask)
    _, g = binarize_mask(gt_mask)

    if p is None or g is None:
        return 0.0, 0.0, 0.0, 0, 0, 0, 0

    inter = int(np.logical_and(p, g).sum())
    union = int(np.logical_or(p, g).sum())
    area_p = int(p.sum())
    area_g = int(g.sum())

    if union > 0:
        iou = inter / union
    else:
        0.0

    if (area_p + area_g) > 0:
        dice = (2 * inter) / (area_p + area_g)
    else:
        0.0

    if area_g > 0:
        ratio = area_p / area_g
    else:
        0.0

    return float(iou), float(dice), float(ratio), inter, union, area_p, area_g


def shape_features(mask):
    """
    Descriptori geometrici: extrasi din masca binara
      - Arie: numar pixeli albi din masca
      - Perimetru: lungimea conturului cel mai mare
      - Circularitate: 4*pi*A / P^2
    """
    mask_u8, mask_bool = binarize_mask(mask)
    if mask_u8 is None:
        return 0.0, 0.0, 0.0

    area = float(mask_bool.sum())

    contours, _ = cv2.findContours(mask_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return area, 0.0, 0.0

    cnt = max(contours, key=cv2.contourArea)
    perimeter = float(cv2.arcLength(cnt, True))

    if perimeter > 0:
        circularity = (4 * math.pi * area) / (perimeter ** 2)
    else:
        0.0

    return area, perimeter, circularity


# PREPROCESARE: eliminare par (black-hat + inpaint)

def remove_hair(gray, kernel_size=17, inpaint_radius=3, dilate_iters=1):
    """
    Elimina firele de par (linii subtiri inchise) aplicand:
      - black-hat pentru evidentierea liniilor intunecate
      - dilatare -> acopera grosimea firului
      - inpaint -> umple firele
    """
    if gray is None:
        return gray

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                       (kernel_size, kernel_size))

    blackhat = cv2.morphologyEx(gray,
                                cv2.MORPH_BLACKHAT,
                                kernel)

    _, hair_mask = cv2.threshold(blackhat,
                                 0,
                                 255,
                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    if dilate_iters > 0:
        hair_mask = cv2.dilate(hair_mask,
                               np.ones((3, 3), np.uint8),
                               iterations=dilate_iters)

    gray_clean = cv2.inpaint(gray, hair_mask,
                             inpaint_radius,
                             cv2.INPAINT_TELEA)

    return gray_clean


# POSTPROCESARE (functia este aplicata pe masca binara obtinuta dupa aplicarea metodei Otsu)

def remove_vignette(mask_u8, corner_size=35):
    """
    Eliminam umbrele ce apar in colturi.
    Aplicam metoda flood fill in colturi pe zona alba pentru a obtine culoarea neagra
    """
    if mask_u8 is None:
        return mask_u8

    h, w = mask_u8.shape[:2]
    cs = int(corner_size)

    # verificam daca exista alb in colturi
    corners = [
        mask_u8[0:cs, 0:cs],
        mask_u8[0:cs, w - cs:w],
        mask_u8[h - cs:h, 0:cs],
        mask_u8[h - cs:h, w - cs:w]
    ]
    if all(np.count_nonzero(c) == 0 for c in corners):
        return mask_u8

    out = mask_u8.copy()
    flood_mask = np.zeros((h + 2, w + 2), np.uint8)

    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    # puncte din interiorul coltului
    seeds += [
        (cs // 2, cs // 2),
        (w - cs // 2 - 1, cs // 2),
        (cs // 2, h - cs // 2 - 1),
        (w - cs // 2 - 1, h - cs // 2 - 1)
    ]

    for sx, sy in seeds:
        if 0 <= sx < w and 0 <= sy < h and out[sy, sx] == 255:
            cv2.floodFill(out,
                          flood_mask,
                          (sx, sy),
                          0)

    return out



# POSTPROCESARE (Eliminarea petelor pigmentare): pastram componenta de interes din imagine(zona cu melanomul)
def keep_central_components(mask_u8, min_area=500, center_frac=0.75, max_components=4):
    """
    Pastreaza componentele albe:
      - destul de mari (min_area)
      - din zona centrala (center_frac)
      - maxim max_components (pentru a reduce petele)
    """
    if mask_u8 is None:
        return mask_u8

    bw = (mask_u8 > 0).astype(np.uint8)
    num, labels, stats, centroids = cv2.connectedComponentsWithStats(bw, connectivity=8)

    if num <= 1:
        return mask_u8

    h, w = mask_u8.shape[:2]
    cx0, cy0 = w / 2.0, h / 2.0

    half_w = (w * center_frac) / 2.0
    half_h = (h * center_frac) / 2.0

    x_min, x_max = cx0 - half_w, cx0 + half_w
    y_min, y_max = cy0 - half_h, cy0 + half_h

    candidates = []
    for lbl in range(1, num):
        area = stats[lbl, cv2.CC_STAT_AREA]
        if area < min_area:
            continue
        cx, cy = centroids[lbl]
        if x_min <= cx <= x_max and y_min <= cy <= y_max:
            candidates.append((area, lbl))

    # daca nu gasim nimic central, pastram cea mai mare componenta
    if not candidates:
        biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        out = np.zeros_like(mask_u8)
        out[labels == biggest] = 255
        return out

    # Sortam descrescator dupa arie si pastram primele max_components
    candidates.sort(reverse=True, key=lambda x: x[0])
    out = np.zeros_like(mask_u8)
    for _, lbl in candidates[:max_components]:
        out[labels == lbl] = 255

    return out


# Pipeline complet  pentru o imagine

def segmentare_leziune(image_bgr):
    """
    Returneaza:
      gray              - grayscale original
      preproc_img       - imagine dupa preprocesare (remove_hair)
      mask_raw          - masca dupa segmentare Otsu (bruta)
      mask_final        - masca dupa postprocesare (finala)
    """
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # 1) Eliminam firele de par (pe grayscale)
    preproc_img = remove_hair(gray, kernel_size=17, inpaint_radius=3, dilate_iters=1)

    # 2) Filtru Gaussian + Segmentare Otsu
    blur = cv2.GaussianBlur(preproc_img, (5, 5), 0)
    _, mask_raw = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 3) Eliminare vigneta (doar daca exista alb in colturi)
    mask_final = remove_vignette(mask_raw, corner_size=35)

    # daca devine goala
    if np.count_nonzero(mask_final) == 0 and np.count_nonzero(mask_raw) > 0:
        mask_final = mask_raw.copy()

    # 4) Eliminare pete ( deschidere )
    mask_final = cv2.morphologyEx(
        mask_final,
        cv2.MORPH_OPEN,
        cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)),
        iterations=1
    )

    # 5) Pastreaza componente centrale (fara unire)
    mask_final = keep_central_components(mask_final, min_area=500, center_frac=0.75, max_components=4)

    # 6) Inchidere  (umplere goluri)
    mask_final = cv2.morphologyEx(mask_final,
                                  cv2.MORPH_CLOSE,
                                  np.ones((5, 5), np.uint8),
                                  iterations=1)

    return gray, preproc_img, mask_raw, mask_final

# MAIN: iteram prin imagini, calculam metrici, export Excel, slider

# lista imagini
image_files = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
if not image_files:
    print("Nu s-au gasit imagini in folderul 'imagini'.")
    raise SystemExit

processed_images = []
results = []
# iterare prin toate imaginile
for file_name in image_files:
    image_path = os.path.join(IMAGE_FOLDER, file_name)
    base_name = os.path.splitext(file_name)[0]

    # cautam mastile GT
    gt_candidates = [
        os.path.join(GT_FOLDER, base_name + "_Segmentation.png"),
        os.path.join(GT_FOLDER, base_name + "_segmentation.png"),
        os.path.join(GT_FOLDER, base_name + ".png"),
    ]
    gt_path = next((p for p in gt_candidates if os.path.exists(p)), None)

    image = cv2.imread(image_path)
    if image is None:
        continue

    # pipeline (cu etape)
    gray, preproc_img, mask_raw, my_mask = segmentare_leziune(image)

    # Ground Truth
    if gt_path:
        gt_mask = cv2.imread(gt_path, cv2.IMREAD_GRAYSCALE)
        if gt_mask is None:
            gt_mask = np.zeros_like(my_mask)
        else:
            gt_mask = cv2.resize(gt_mask,
                                 (my_mask.shape[1], my_mask.shape[0]),
                                 interpolation=cv2.INTER_NEAREST)
    else:
        gt_mask = np.zeros_like(my_mask)

    # Metrici (pe masca finala)
    iou, dice, ratio, _, _, _, _ = calc_metrics(my_mask, gt_mask)

    # Shape features
    area_my, per_my, circ_my = shape_features(my_mask)
    area_gt, per_gt, circ_gt = shape_features(gt_mask)

    # tabel per imagine
    results.append({
        "Imagine": file_name,
        "IoU": iou,
        "Dice": dice,
        "Raport_Arie": ratio,
        "Arie_obtinuta_px": area_my,
        "Arie_GT_px": area_gt,
        "Perimetru_obtinut_px": per_my,
        "Perimetru_GT_px": per_gt,
        "Circularitate_obtinuta": circ_my,
        "Circularitate_GT": circ_gt
    })

    # date pentru slider
    processed_images.append({
        "name": file_name,
        "original": cv2.cvtColor(image, cv2.COLOR_BGR2RGB),
        "preproc": preproc_img,   # imagine dupa preprocesare (gray)
        "seg_raw": mask_raw,      # masca bruta
        "post": my_mask,          # masca finala
        "gt": gt_mask,            # ground truth

        "IoU": iou,
        "Dice": dice,
        "Raport": ratio,

        "Arie_obtinuta_px": area_my,
        "Arie_GT_px": area_gt,
        "Perimetru_obtinut_px": per_my,
        "Perimetru_GT_px": per_gt,
        "Circularitate_obtinuta": circ_my,
        "Circularitate_GT": circ_gt
    })

if not processed_images:
    print("Nu exista imagini ce pot fi procesate. Verifica continutul folder-elor.")
    raise SystemExit


### CSV (tip tabel) cu TOATE imaginile###
tabel = pd.DataFrame(results) # creeaza DataFrame Pandas (un tabel) cu toate rezultatele
                           # fiecare rand corespunde unei imagini
                           # fiecare coloana metricele, caracteristicile de forma, numele img

# converteste continutul coloanelor la float + rotunjeste la 4 zecimale
for c in ["IoU",
          "Dice",
          "Raport_Arie",
          "Arie_obtinuta_px",
          "Arie_GT_px",
          "Perimetru_obtinut_px",
          "Perimetru_GT_px",
          "Circularitate_obtinuta",
          "Circularitate_GT"]:
    tabel[c] = tabel[c].astype(float).round(4)

### SUMMARY – doar MACRO AVERAGE
# MACRO AVERAGE = media metricelor calculata peste toate imaginile

summary_df = pd.DataFrame([{
    "IoU_macro_mean": round(float(tabel["IoU"].mean()), 4),
    "Dice_macro_mean": round(float(tabel["Dice"].mean()), 4),
    "Raport_Arie_macro_mean": round(float(tabel["Raport_Arie"].mean()), 4),
    "Numar_imagini": int(len(tabel))
}])

print("\nREZUMAT GLOBAL AL METRICILOR (MACRO-AVERAGE)\n")
print(summary_df)

### Salvare CSV

tabel.to_csv("rezultate_melanom_per_image.csv", index=False)
summary_df.to_csv("rezultate_melanom_summary.csv", index=False)

print("\nCSV salvate:")
print(" - rezultate_melanom_per_image.csv")
print(" - rezultate_melanom_summary.csv\n")


 # Slider
fig, axes = plt.subplots(1, 5, figsize=(28, 6))
plt.subplots_adjust(bottom=0.3)

def show_images(idx):
    data = processed_images[idx]

    for ax in axes:
        ax.clear()

    axes[0].imshow(data["original"])
    axes[0].set_title("Original")
    axes[0].axis("off")

    axes[1].imshow(data["preproc"], cmap="gray")
    axes[1].set_title("Dupa Preprocesare")
    axes[1].axis("off")

    axes[2].imshow(data["seg_raw"], cmap="gray")
    axes[2].set_title("Dupa Segmentare Otsu")
    axes[2].axis("off")

    axes[3].imshow(data["post"], cmap="gray")
    axes[3].set_title("Dupa Postprocesare")
    axes[3].axis("off")

    axes[4].imshow(data["gt"], cmap="gray")
    axes[4].set_title("Ground Truth")
    axes[4].axis("off")

    fig.suptitle(
        f"{data['name']}\n"
        f"IoU={data['IoU']:.4f} | "
        f"Dice={data['Dice']:.4f} | "
        f"Raport_Arie={data['Raport']:.4f}\n"
        f"Arie obtinuta={data['Arie_obtinuta_px']:.0f} px | "
        f"Arie GT={data['Arie_GT_px']:.0f} px\n"
        f"Perimetru obtinut={data['Perimetru_obtinut_px']:.1f} px | "
        f"Perimetru GT={data['Perimetru_GT_px']:.1f} px\n"
        f"Circularitate obtinuta={data['Circularitate_obtinuta']:.4f} | "
        f"Circularitate GT={data['Circularitate_GT']:.4f}",
        fontsize=11,
        color="darkblue"
    )
    fig.canvas.draw_idle()

show_images(0)

ax_slider = plt.axes([0.25, 0.1, 0.5, 0.03])
slider = Slider(ax_slider, 'Imagine', 0, len(processed_images) - 1, valinit=0, valstep=1)
slider.on_changed(lambda v: show_images(int(v)))

plt.show()
