import os
import qrcode
import numpy as np
from vcsd.decryptor import Decryptor

cwd = os.getcwd()
dec = Decryptor()

# text stored in the qr code
test_correct_data="test"

# # numpy array with the qr that is generated from the message
test_correct_extracted_QR_matrix_path = os.path.join(cwd, "tests", "data", "qr_matrix_with_word_test_as_content.npy")
test_correct_extracted_QR_matrix = np.load(test_correct_extracted_QR_matrix_path)
# numpy array with a transparencies pair that contain que qr code
test_trans_A_matrix_path = os.path.join(cwd, "tests", "data", "trans_A_matrix_test.npy")
test_trans_A_matrix = np.load(test_trans_A_matrix_path)
test_trans_B_matrix_path = os.path.join(cwd, "tests", "data", "trans_B_matrix_test.npy")
test_trans_B_matrix = np.load(test_trans_B_matrix_path)

# QR code extraction from transparencies TEST
def test_extract_qr_from_transparences():
    extracted_QR_matrix = dec.extract_qr_from_transparences(test_trans_A_matrix, test_trans_B_matrix)
    assert np.array_equal(test_correct_extracted_QR_matrix, extracted_QR_matrix)

# Data extraction from QR code TEST
def test_extract_data_from_qr_matrix():
    extracted_data, im_qr_extracted = dec.extract_data_from_qr_matrix(test_correct_extracted_QR_matrix)
    assert np.array_equal(test_correct_data, extracted_data)
