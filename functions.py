from expand_matrix import M
from scipy.linalg import null_space
import numpy as np

def encrypt(image, password):
    key = convert_password_into_key(np.array([ord(c) for c in password]), len(password))
    matrix = make_transform_matrix(key)
    encrypted_image = transform_image(image, matrix)
    return encrypted_image

def decrypt(image, password):
    key = convert_password_into_key(password)
    matrix = make_transform_matrix(key)
    matrix = numpy.linalg.inv(matrix)
    decrypted_image = transform_image(image, matrix)
    return decrypted_image

def convert_password_into_key(password, length):
    submatrix = M[:, :length]
    return submatrix @ password


def make_transform_matrix(key):
    LEN = 100
    start, end = 0, LEN
    encrypt_matrix = np.array()
    encrypt_matrix = np.reshape(LEN*1, dtype='i')
    while end <= 6000:
        a_col = key[start:end]
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
                image[start_c:end_c, start_r: end_r, i] = image[start_c:end_c, start_r: end_r, i] @ matrix
            start_r += LEN
            end_r += LEN
        start_c += LEN
        end_c += LEN
    return image