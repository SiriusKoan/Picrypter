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
    pass


def check_independent(matrix, vector):
    pass


def transform_image(image, matrix):
    pass
