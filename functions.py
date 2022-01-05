from matrix import M
from scipy.linalg import null_space
import numpy as np
from PIL import Image
from io import BytesIO

MOD = 257
M_size = 5000 # maximum 6000 

def modular_inv(a, b, x, y):
    d = a
    if b != 0:
        d = modular_inv(b, a % b, y, x)[0]
        y[0] -= (a//b) * x[0]
    else:
        x[0], y[0] = 1, 0
    return [d, x]

def encrypt(image, password):
    key = convert_password_into_key(np.array([ord(c) % 12 for c in password]), len(password))
    matrix = make_transform_matrix(key)
    image = np.array(Image.open(BytesIO(image)))
    encrypted_image = transform_image(image, matrix, 1)
    print("enc:\n", encrypted_image)
    encrypted_image = Image.fromarray(encrypted_image)
    print(encrypted_image, dir(encrypted_image))
    f = BytesIO()
    encrypted_image.save(f, "PNG")
    return f.getvalue()

def decrypt(image, password):
    key = convert_password_into_key(np.array([ord(c) % 12 for c in password]), len(password))
    matrix = make_transform_matrix(key)

    DET = int(np.round(np.linalg.det(matrix)))
    if DET % MOD == 0:
        DET = 1
    inv_det = modular_inv(DET, MOD, [0], [0])[1][0]
    inv_det = (inv_det + MOD) % MOD
    print("inv_det: ", inv_det, "DET: ", DET)

    print("before inv:\n", matrix)
    # inverse matrix
    matrix = matrix.astype('int64')
    matrix = np.array([[matrix[1, 1], -matrix[0, 1]], [-matrix[1, 0], matrix[0, 0]]])
    matrix *= inv_det
    matrix %= MOD

    image = np.array(Image.open(BytesIO(image)))
    print("dec:\n", image)

    decrypted_image = transform_image(image, matrix, 0)
    decrypted_image = Image.fromarray(decrypted_image)
    f = BytesIO()
    decrypted_image.save(f, "PNG")
    return f.getvalue()

def convert_password_into_key(password, length):
    print("password: ", password)
    submatrix = M[:M_size, :length]
    submatrix = submatrix @ password
    print("submatrix: ", submatrix)
    print("size", submatrix.shape)
    return submatrix


def make_transform_matrix(key):
    LEN = 10
    start, end = LEN, LEN*2
    encrypt_matrix = np.array(key[0:LEN])
    print("key123: ", key)
    encrypt_matrix = encrypt_matrix.reshape(LEN, 1)
    cnt = 1
    while end < M_size:
        a_col = np.array(key[start:end])
        tmp_mat = np.c_[encrypt_matrix, a_col]
        check = check_independent(tmp_mat)
        if not check:
            encrypt_matrix = tmp_mat
            cnt += 1
        if cnt == 2:
            break
        start += LEN
        end += LEN
    encrypt_matrix = encrypt_matrix.transpose() @ encrypt_matrix
    print("encrypted matrix:\n", encrypt_matrix.shape)

    return encrypt_matrix

def check_independent(matrix):
    ns = null_space(matrix)
    return bool(ns.any())


def transform_image(image, matrix, flag):
    # flag == 1: encrypted
    print("before image:\n", image)
    image = image.astype('int64')
    size = image.shape
    LEN = matrix.shape[0]
    start_c, end_c, start_r, end_r = 0, LEN, 0, LEN
    if not flag:
        for i in range(size[0]):
            for j in range(size[1]):
                for k in range(3):
                    if image[i, j, k] != 0:
                        image[i, j ,k] += 1
    while end_c <= size[0]:
        start_r, end_r = 0, LEN
        while end_r <= size[1]:
            for i in range(3):
                image[start_c:end_c, start_r:end_r, i] = image[start_c:end_c, start_r:end_r, i] @ matrix
            start_r += LEN
            end_r += LEN
        start_c += LEN
        end_c += LEN
    print("middle image:\n", image)
    for i in range(size[0]):
        for j in range(size[1]):
            # only RGB, alpha neglected (hence .jpg is supported)
            for k in range(3):
                image[i, j, k] %= MOD
                if flag and image[i, j, k] > 0:
                    image[i, j, k] -= 1
    
    image = image.astype('uint8')
    print("after image:\n", image)
    return image