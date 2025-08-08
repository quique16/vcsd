import os
import numpy as np
from PIL import Image

from VisioCrypt.encryptor import Encryptor
from VisioCrypt.decryptor import Decryptor


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
enc = Encryptor()
dec = Decryptor()

# text stored in the QR code
test_correct_data = "test"

# numpy array with the QR that is generated from the message
test_correct_generated_qr_path = os.path.join(
    DATA_DIR, "qr_matrix_with_word_test_as_content.npy"
)
test_correct_generated_qr_matrix = np.load(test_correct_generated_qr_path)


# QR code generation TEST
def test_generate_qr():
    generated_qr, im_qr_code = enc.generate_qr(data=test_correct_data)
    # validate that the generated matrix matches the precomputed one
    assert np.array_equal(test_correct_generated_qr_matrix, generated_qr)
    # ensure only binary values are present
    assert np.isin(generated_qr, [0, 1]).all()
    # the returned image must be convertible to a PIL Image instance
    assert isinstance(im_qr_code.get_image(), Image.Image)

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

    # verify relationship of blocks depending on the original QR bit
    for i in range(0, trans_A.shape[0], 2):
        for j in range(0, trans_A.shape[1], 2):
            block_A = trans_A[i:i + 2, j:j + 2]
            block_B = trans_B[i:i + 2, j:j + 2]
            qr_bit = test_correct_generated_qr_matrix[i // 2, j // 2]
            if qr_bit == 0:
                assert np.array_equal(block_A, block_B)
            else:
                assert np.array_equal(block_A, 1 - block_B)

    # ensure that what is recovered is the same as what was encrypted
    assert np.array_equal(test_correct_generated_qr_matrix, extracted_QR_matrix)
