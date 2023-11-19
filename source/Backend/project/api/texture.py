import numpy as np
import os
import cv2
import time

def calculate_cooccurrence_matrix(grayscale : np.ndarray) :
    # fungsi untuk mendapatkan cooccurence matrix dari sebuah grayscale dengan distance=1 dan theta=0 

    # declare matrix cooccurrence_matrix yang berdimensi 256x256 dengan tipe elemennya float dan semuanya diinisialisasi dengan nilai 0
    cooccurrence_matrix = np.zeros((256, 256), dtype=float)
    rows = len(grayscale)
    cols = len(grayscale[0])

    # memeriksa setiap pasangan elemen pada matrix grayscale dan melakukan increment pada cooccurrence_matrix
    for i in range (rows) :
        for j in range (cols-1) :
            nl = grayscale[i][j]
            nr = grayscale[i][j+1]
            cooccurrence_matrix[nl][nr] += 1   

    # declare nilai baris dan kolom matrix cooccurrence
    rows_comatr = np.max(grayscale)
    cols_comatr = rows_comatr

    # mengganti nilai matrix cooccurrence dengan hasil penjumlahan matrix cooccurrence dengan matrix transposenya sendiri
    cooccurrence_matrix = cooccurrence_matrix + cooccurrence_matrix.transpose()

    # mendapatkan hasil jumlah dari setiap elemen dalam matrix cooccurrence
    sum_elmt = np.sum(cooccurrence_matrix)

    # membagi setiap elemen matrix cooccurrence dengan sum_elmt nya
    for i in range (rows_comatr) :
        for j in range (cols_comatr) :
            cooccurrence_matrix[i][j] = cooccurrence_matrix[i][j]/sum_elmt
    
    return cooccurrence_matrix

def get_contrast(gray):
    # mendapatkan nilai contrast dari grayscale
    i, j = np.indices(gray.shape)
    return np.sum(gray * ((i - j) ** 2))

def get_homogeneity(gray):
    # mendapatkan nilai homogeneity dari grayscale
    i, j = np.indices(gray.shape)
    return np.sum(gray / (1 + (i - j) ** 2))

def get_entropy(gray) :
     # mendapatkan nilai entropy dari grayscale
    entropy = 0
    rows = len(gray)
    cols = len(gray[0])
    
    for i in range (rows) :
        for j in range (cols) :
            if (gray[i][j] != 0) :
                entropy = entropy + (gray[i][j]*np.log10(gray[i][j]))
    return entropy*(-1)

def image_to_grayscale(image):
    # mengubah image menjadi grayscale
    return np.round(0.114 * image[:, :, 0] + 0.587 * image[:, :, 1] + 0.29 * image[:, :, 2]).astype(int)

def compare_images(image1, image2) :
    # membandingkan dua buah image. return berupa persentase kemiripan dua buah image tersebut

    # dapatkan grayscale dari image "img"
    grayscale1 = image_to_grayscale(image1)
    grayscale2 = image_to_grayscale(image2)

    # hitung cooccurrence matrix
    comatrix1 = calculate_cooccurrence_matrix(grayscale1)
    comatrix2 = calculate_cooccurrence_matrix(grayscale2)

    # mendapatkan nilai contrast, homogeneity, dan entropy dari image
    contrast1 = get_contrast(comatrix1)
    contrast2 = get_contrast(comatrix2)
    homogeneity1 = get_homogeneity(comatrix1)
    homogeneity2 = get_homogeneity(comatrix2)
    entropy1 = get_entropy(comatrix1)
    entropy2 = get_entropy(comatrix2)

    vectorA = np.array([contrast1,homogeneity1,entropy1])
    vectorB = np.array([contrast2,homogeneity2,entropy2])

    magnitude_of_A = np.linalg.norm(vectorA)
    magnitude_of_B = np.linalg.norm(vectorB)

    result = np.dot(vectorA,vectorB)/(magnitude_of_A*magnitude_of_B)
    return result*100

def process_texture_dataset(input_image, dataset_folder):
    
    grayscale1 = image_to_grayscale(input_image)
    # hitung cooccurrence matrix
    comatrix1 = calculate_cooccurrence_matrix(grayscale1)
    # mendapatkan nilai contrast, homogeneity, dan entropy dari input_image
    contrast1 = get_contrast(comatrix1)
    homogeneity1 = get_homogeneity(comatrix1)
    entropy1 = get_entropy(comatrix1)

    vectorA = np.array([contrast1,homogeneity1,entropy1])
    magnitude_of_A = np.linalg.norm(vectorA)

    # Inisialisasi list untuk menyimpan hasil pencocokan
    similarity_scores = []

    # Proses pencocokan dengan dataset gambar
    i = 0
    for filename in os.listdir(dataset_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            dataset_image_path = os.path.join(dataset_folder, filename)
            dataset_image = cv2.imread(dataset_image_path)

            grayscale2 = image_to_grayscale(dataset_image)
            # mendapatkan nilai contrast, homogeneity, dan entropy dari dataset
            comatrix2 = calculate_cooccurrence_matrix(grayscale2)
            contrast2 = get_contrast(comatrix2)
            homogeneity2 = get_homogeneity(comatrix2)
            entropy2 = get_entropy(comatrix2)

            vectorB = np.array([contrast2,homogeneity2,entropy2])
            magnitude_of_B = np.linalg.norm(vectorB)


            result = np.dot(vectorA,vectorB)/(magnitude_of_A*magnitude_of_B)
            result = result*100 #Dihitung presentase

            # Simpan hasil pencocokan sebagai dictionary untuk endpoint
            if(result > 60.0):
                similarity_scores.append({
                    "id": i,  
                    "persentase": round(result,3),  # di bulatkan 3 angka dibelakang koma
                    "img": 'http://127.0.0.1:8000/media/dataset/'+filename,  # menyimpan img dalam link static URL
                    "durasi": 0  #nilai durasi di default ke-0
                })
                i += 1

    # Mengurutkan hasil 
    sorted_results = sorted(similarity_scores, key=lambda x: x['persentase'], reverse=True)


    return sorted_results


 


# dataset_folder = 'dataset1'
# input_image = cv2.imread('1.jpg') 
# input1_image = cv2.imread('4.jpg') 
# t0 = time.time()
# # hasil = process_dataset(input_image, dataset_folder)
# print(compare_images(input_image, input1_image), "\n")
# t1 = time.time()
# exec = t1-t0
# # hasil[0]['durasi'] = exec
# print(exec,"\n")