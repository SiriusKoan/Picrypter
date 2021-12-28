from expand_matrix import M
from scipy.linalg import null_space
import numpy as np
from PIL import Image
from io import BytesIO

def encrypt(image, password):
    key = convert_password_into_key(np.array([ord(c) - 45 for c in password]), len(password))
    matrix = make_transform_matrix(key)
    image = np.array(Image.open(BytesIO(image)))
    encrypted_image = transform_image(image, matrix)
    encrypted_image = Image.fromarray(encrypted_image)
    print(encrypted_image, dir(encrypted_image))
    f = BytesIO()
    encrypted_image.save(f, "PNG")
    return f.getvalue()

def decrypt(image, password):
    key = convert_password_into_key(np.array([ord(c) - 45 for c in password]), len(password))
    matrix = make_transform_matrix(key)
    matrix = np.linalg.inv(matrix)
    print("inverse: ", matrix)
    image = np.array(Image.open(BytesIO(image)))
    decrypted_image = transform_image(image, matrix)
    decrypted_image = Image.fromarray(decrypted_image)
    f = BytesIO()
    decrypted_image.save(f, "PNG")
    return f.getvalue()

def convert_password_into_key(password, length):
    
    size = M.shape
    for i in range(size[0]):
        for j in range(size[1]):
                M[i,j] = 1
    
    submatrix = M[:600, :length]
    # print("submatrix: ", submatrix @ password)
    return submatrix @ password


def make_transform_matrix(key):
    LEN = 1
    start, end = LEN, LEN*2
    encrypt_matrix = np.array(key[0:LEN])
    encrypt_matrix = encrypt_matrix.reshape(LEN, 1)
    
    while end <= 600:
        a_col = np.array(key[start:end])
        tmp_mat = np.c_[encrypt_matrix, a_col]
        check = check_independent(tmp_mat)
        print("encrypted matrix: ", encrypt_matrix)
        # print(np.linalg.det(tmp_mat.transpose() @ tmp_mat))
        if not check:
            print("tmp: ", tmp_mat)
            encrypt_matrix = tmp_mat
        start += LEN
        end += LEN
    encrypt_matrix = encrypt_matrix.transpose() @ encrypt_matrix
    print("encrypted matrix: ", encrypt_matrix)
    print(np.linalg.det(encrypt_matrix))
    # print(encrypt_matrix)
    print(encrypt_matrix.shape)
    return encrypt_matrix


def check_independent(matrix):
    ns = null_space(matrix)
    # print(ns)
    return bool(ns.any())


def transform_image(image, matrix):
    image = image.astype('float64')
    size = image.shape
    LEN = matrix.shape[0]
    start_c, end_c, start_r, end_r = 0, LEN, 0, LEN
    while end_c <= size[0]:
        start_r, end_r = 0, LEN
        while end_r <= size[1]:
            for i in range(image.shape[2]):
                # print(image[start_c:end_c, start_r:end_r, i], matrix)
                image[start_c:end_c, start_r:end_r, i] = image[start_c:end_c, start_r:end_r, i] @ matrix
            start_r += LEN
            end_r += LEN
        start_c += LEN
        end_c += LEN
    print("before %")
    print(image)
    # for i in range(size[0]):
    #     for j in range(size[1]):
    #         for k in range(size[2]):
    #             image[i,j,k] %= 256
    print("after %")
    print(image)
    image = image.astype('uint8')
    return image