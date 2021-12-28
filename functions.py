from expand_matrix import M
from scipy.linalg import null_space

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
    pass


def check_independent(matrix):
    ns = null_space(matrix)
    return bool(ns)


def transform_image(image, matrix):
    return matrix @ image
