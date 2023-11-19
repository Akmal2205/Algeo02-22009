import cv2
import numpy as np
import os


def calculate_hsv_histogram(image):
    # Normalisasi nilai BGR ke [0, 1]
    B = image[:, :, 0] / 255.0
    G = image[:, :, 1] / 255.0
    R = image[:, :, 2] / 255.0

    maxc = np.maximum.reduce([R, G, B])
    minc = np.minimum.reduce([R, G, B])

    delta = maxc - minc

    Hue = np.copy(delta)
    conditional1 = np.logical_and(maxc == B, Hue != 0)
    conditional2 = np.logical_and(maxc == G, Hue != 0)
    conditional3 = np.logical_and(maxc == R, Hue != 0)

    
    Hue[conditional1] = 60.0 * (((R[conditional1] - G[conditional1]) / delta[conditional1]) + 4)
    Hue[conditional2] = 60.0 * (((B[conditional2] - R[conditional2]) / delta[conditional2]) + 2)
    Hue[conditional3] = 60.0 * (((G[conditional3] - B[conditional3]) / delta[conditional3]) % 6)

    Saturation = np.copy(maxc)
    conditional = np.where(maxc != 0)
    Saturation[conditional] = (delta[conditional] / maxc[conditional])

    Value = np.copy(maxc)

    return Hue, Saturation, Value

    

def createHistogram(h,s,v):
# Hitung histogram menggunakan np.histogram
    hist_hue, _ = np.histogram(h.flatten(), bins=16, range=(0, 180))
    hist_saturation, _ = np.histogram(s.flatten(), bins=16, range=(0, 1))
    hist_value, _ = np.histogram(v.flatten(), bins=16, range=(0, 1))

    #normalisasi Histogram
    if np.linalg.norm(hist_hue) != 0:
        hist_hue = hist_hue / np.linalg.norm(hist_hue)

    if np.linalg.norm(hist_saturation) != 0:
        hist_saturation = hist_saturation / np.linalg.norm(hist_saturation)

    if np.linalg.norm(hist_value) != 0:
        hist_value = hist_value / np.linalg.norm(hist_value)

    histogram = np.concatenate([hist_hue, hist_saturation, hist_value])


    return histogram

def calculate_block_histogram(image,h,s,v,x,y,z):
    # Mendapatkan dimensi atau ukuran gambar
    height, width, _ = image.shape

    similarity = 0
    height //= 4
    width //= 4

    for i in range(0, 4):
        for j in range(0, 4):
            # Memotong blok dari gambar yang sudah diubah ke HSV
            block_hue = h[i*height:(i+1)*height, j*width:(j+1)*width]
            block1_hue = x[i*height:(i+1)*height, j*width:(j+1)*width]
            block_saturation = s[i*height:(i+1)*height, j*width:(j+1)*width]
            block1_saturation = y[i*height:(i+1)*height, j*width:(j+1)*width]
            block_value = v[i*height:(i+1)*height, j*width:(j+1)*width]
            block1_value = z[i*height:(i+1)*height, j*width:(j+1)*width]
            # Hitung histogram tiap blok
            block_histogram = createHistogram(block_hue, block_saturation,block_value)
            block1_histogram = createHistogram(block1_hue,block1_saturation,block1_value)
            similarity += cosine_similarity_vector(block_histogram, block1_histogram)

    similarity /= 16.0

    return similarity

def cosine_similarity_vector(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    similarity = dot_product / (norm_a * norm_b)
    return similarity

def process_color_dataset(input_image, dataset_folder):
    #vMendapatkan ukuran atau size dari input image
    height, width, _ = input_image.shape
    # Inisialisasi list untuk menyimpan hasil pencocokan
    similarity_scores = []

    input_hue, input_saturation, input_value = calculate_hsv_histogram(input_image)
    i = 1
    # Proses pencocokan dengan dataset gambar
    for filename in os.listdir(dataset_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            dataset_image_path = os.path.join(dataset_folder, filename)
            dataset_image = cv2.imread(dataset_image_path)

            # Resize(sesuaikan) gambar dataset agar sesuai dengan ukuran gambar input
            resized_image = cv2.resize(dataset_image, (width, height))

            # Mendapatkan HSV dataset
            dataset_hue, dataset_saturation, dataset_value = calculate_hsv_histogram(resized_image)
            # Memproses nilai cosine_similarity per bok (4x4) lalu dirata2 dengan 16
            similarity = calculate_block_histogram(input_image, input_hue, input_saturation, input_value, dataset_hue, dataset_saturation, dataset_value)

            #Dihitung presentase
            similarity = similarity*100
            # Simpan hasil pencocokan sebagai dictionary dalam endpoint
            if(similarity > 60.0):
                similarity_scores.append({
                    "id": i,  
                    "persentase": round(similarity,3),  # di bulatkan 3 angka dibelakang koma
                    "img": 'http://127.0.0.1:8000/media/dataset/'+filename,  # menyimpan img dalam link static URL
                    "durasi": 0  #nilai durasi di default ke-0
                })
                i += 1

    # Mengurutkan hasil 
    sorted_results = sorted(similarity_scores, key=lambda x: x['persentase'], reverse=True)


    return sorted_results