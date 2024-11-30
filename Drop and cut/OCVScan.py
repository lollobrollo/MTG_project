import cv2
import numpy as np
import matplotlib.pyplot as plt

def load_image(image_path):
    # Carica l'immagine
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Impossibile caricare l'immagine!")
    return image

def detect_edges(image):
    # Converti l'immagine in scala di grigi
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Applica un filtro Gaussiano per ridurre il rumore
    image = cv2.GaussianBlur(image, (5,5), 0)

    _, image = cv2.threshold(image, 20, 255, cv2.THRESH_BINARY)
    # Rileva i bordi con l'algoritmo di Canny
    edges = cv2.Canny(image, 150, 200)
    return edges

def find_card_contour(edges):
    # Trova i contorni
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Ordina i contorni per area in ordine decrescente e prendi i più grandi
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
    cont = []

    for contour in contours:
        # Approssima i contorni per ottenere un quadrilatero
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            cont.append(approx)
    
    if len(cont) > 0:
        cont = sorted(cont, key=cv2.contourArea, reverse=True)
        return cont[0]
    else:
        return None

def transform_card(image, card_contour):
    # Ordina i punti del contorno
    pts = card_contour.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")

    # Calcola le coordinate rettangolari
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # Definisci le dimensioni della carta
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Definisci i punti di destinazione per la trasformazione prospettica
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # Calcola la matrice di trasformazione prospettica
    M = cv2.getPerspectiveTransform(rect, dst)
    # Applica la trasformazione
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped


def crop_pic(image):
    tot_h = image.shape[0]
    tot_w = image.shape[1]

    h = round(tot_h/15)
    w = round(tot_w/5)
    return image[tot_h-h:, :w]



# Esegui il programma
image_path = 'D:\MTG_project\Drop and cut\Test_pic\pic8.jpg'
image = load_image(image_path)
edges = detect_edges(image)
card_contour = find_card_contour(edges)

if card_contour is not None:
    warped_card = transform_card(image, card_contour)
    warped_card = crop_pic(warped_card)
    cv2.imwrite('output.jpg', warped_card)

else:
    print("Contorno della carta non trovato.")

# plot the image with matplotlib with the edges
# plt.imshow(card_contour, cmap='gray')
# plt.show()

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# image = cv2.GaussianBlur(image, (3,3), 0)
# _, image = cv2.threshold(image, 15, 255, cv2.THRESH_BINARY)
# edges = cv2.Canny(image, 150, 200)
# contours = find_card_contour(image)
# contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

# for contour in contours:
#     cv2.drawContours(image, [contour], -1, (0, 255, 0), 3)

# plt.imshow(image, cmap='gray')
cv2.imwrite('output.jpg', image)
# plt.imshow(image, cmap='gray')
# plt.show()