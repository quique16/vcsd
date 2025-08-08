import os
import qrcode
import numpy as np
from vcsd.encryptor import Encryptor
from vcsd.decryptor import Decryptor

cwd = os.getcwd()
enc = Encryptor()
dec = Decryptor()

# text stored in the qr code
test_correct_data="test"

# numpy array with the qr that is generated from the message
test_correct_generated_qr_path = os.path.join(cwd, "tests", "data", "qr_matrix_with_word_test_as_content.npy")
test_correct_generated_qr_matrix = np.load(test_correct_generated_qr_path)


# QR code generation TEST
def test_generate_qr():
    generated_qr, im_qr_code = enc.generate_qr(data=test_correct_data)
    assert np.array_equal(test_correct_generated_qr_matrix, generated_qr)

# Generation of transparencies from QR code TEST
def test_generate_transparences():
    # regardless of the content of the QR code trans_A and trans_B vary in every iteration
    # (the relationship between them is what remaings constant)
    # in order to test the proper generation of them, the recovery needs to be performed as well
    trans_A, trans_B = enc.generate_transparences(test_correct_generated_qr_matrix)
    extracted_QR_matrix = dec.extract_qr_from_transparences(trans_A, trans_B)
    # ensure transparencies are twice the size of the original QR
    qr_h, qr_w = test_correct_generated_qr_matrix.shape
    assert trans_A.shape == (qr_h * 2, qr_w * 2)
    assert trans_B.shape == (qr_h * 2, qr_w * 2)

    # ensure transparencies contain only binary values
    assert np.isin(trans_A, [0, 1]).all()
    assert np.isin(trans_B, [0, 1]).all()

    # it checks that what is recovered is the same as what was encrypted
    assert np.array_equal(test_correct_generated_qr_matrix, extracted_QR_matrix)
