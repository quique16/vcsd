import os
import numpy as np
from PIL import Image
import pytest

from vcsd.decryptor import Decryptor


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
dec = Decryptor()

# text stored in the QR code
test_correct_data = "test"

# numpy array with the QR that is generated from the message
test_correct_extracted_QR_matrix_path = os.path.join(
    DATA_DIR, "qr_matrix_with_word_test_as_content.npy"
)
test_correct_extracted_QR_matrix = np.load(test_correct_extracted_QR_matrix_path)
# numpy array with a pair of transparencies that contain the QR code
test_trans_A_matrix_path = os.path.join(DATA_DIR, "trans_A_matrix_test.npy")
test_trans_A_matrix = np.load(test_trans_A_matrix_path)
test_trans_B_matrix_path = os.path.join(DATA_DIR, "trans_B_matrix_test.npy")
test_trans_B_matrix = np.load(test_trans_B_matrix_path)

# QR code extraction from transparencies TEST
def test_extract_qr_from_transparences():
    extracted_QR_matrix = dec.extract_qr_from_transparences(test_trans_A_matrix, test_trans_B_matrix)
    assert np.array_equal(test_correct_extracted_QR_matrix, extracted_QR_matrix)


def test_extract_qr_from_transparences_invalid_shapes():
    trans_A = np.zeros((2, 2), dtype=int)
    trans_B = np.zeros((3, 3), dtype=int)
    with pytest.raises(ValueError):
        dec.extract_qr_from_transparences(trans_A, trans_B)

# Data extraction from QR code TEST
def test_extract_data_from_qr_matrix():
    extracted_data, im_qr_extracted = dec.extract_data_from_qr_matrix(
        test_correct_extracted_QR_matrix
    )
    assert np.array_equal(test_correct_data, extracted_data)
    assert isinstance(im_qr_extracted.get_image(), Image.Image)


def test_extract_data_from_qr_matrix_invalid_size():
    invalid_qr = np.zeros((22, 22), dtype=int)
    with pytest.raises(KeyError):
        dec.extract_data_from_qr_matrix(invalid_qr)
