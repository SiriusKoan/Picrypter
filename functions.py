from expand_matrix import M
from scipy.linalg import null_space
import numpy as np
import PIL import Image

def encrypt(image, password):
    key = convert_password_into_key(np.array([ord(c) for c in password]), len(password))
    matrix = make_transform_matrix(key)
    encrypted_image = transform_image(image, matrix)
    encrypted_image = Image.fromarray(encrypted_image)
    return encrypted_image


def decrypt(image, password):
    key = convert_password_into_key(password)
    matrix = make_transform_matrix(key)
    matrix = numpy.linalg.inv(matrix)
    decrypted_image = transform_image(image, matrix)
    decrypted_image = Image.fromarray(decrypted_image)
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
    return matrix @ image
