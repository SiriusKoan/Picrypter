from expand_matrix import M
from scipy.linalg import null_space
import numpy as np
from PIL import Image

def encrypt(image, password, size):
    key = convert_password_into_key(np.array([ord(c) for c in password]), len(password))
    matrix = make_transform_matrix(key)
    image = np.array(Image.frombytes("RGBA", size, image))
    encrypted_image = transform_image(image, matrix)
    encrypted_image = Image.fromarray(encrypted_image)
    return encrypted_image

def decrypt(image, password, size):
    key = convert_password_into_key(np.array([ord(c) for c in password]), len(password))
    matrix = make_transform_matrix(key)
    matrix = numpy.linalg.inv(matrix)
    image = np.array(Image.frombytes("RGBA", size, image))
    decrypted_image = transform_image(image, matrix)
    decrypted_image = Image.fromarray(decrypted_image)
    return decrypted_image

def convert_password_into_key(password, length):
    submatrix = M[:, :length]
    return submatrix @ password


def make_transform_matrix(key):
    LEN = 100
    start, end = LEN, LEN*2
    encrypt_matrix = np.array(key[0:LEN])
    encrypt_matrix = encrypt_matrix.reshape(LEN, 1)
    
    while end <= 6000:
        a_col = np.array(key[start:end])
        tmp_mat = np.c_[encrypt_matrix, a_col]
        check = check_independent(tmp_mat)
        if check:
            encrypt_matrix = tmp_mat
        start += LEN
        end += LEN
    return encrypt_matrix


def check_independent(matrix):
    ns = null_space(matrix)
    return bool(ns)


def transform_image(image, matrix):
    size = image.shape
    LEN = matrix.shape[0]
    start_c, end_c, start_r, end_r = 0, LEN, 0, LEN
    while end_c <= size[0]:
        start_r, end_r = 0, LEN
        while end_r <= size[1]:
            for i in range(image.shape[2]):
                image[start_c:end_c, start_r:end_r, i] = image[start_c:end_c, start_r:end_r, i] @ matrix
            start_r += LEN
            end_r += LEN
        start_c += LEN
        end_c += LEN
    return image