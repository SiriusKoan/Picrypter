import numpy as np

def encrypt(image, password):
    key = convert_password_into_key(password)
    matrix = make_transform_matrix(key)
    encrypted_image = transform_image(image, matrix)
    return encrypted_image


def decrypt(image, password):
    key = convert_password_into_key(password)
    matrix = make_transform_matrix(key)
    # make inverse
    decrypted_image = transform_image(image, matrix)
    return decrypted_image


def convert_password_into_key(password):
    pass


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
    pass


def transform_image(image, matrix):
    
