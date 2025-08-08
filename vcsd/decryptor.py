import os
import cv2
import qrcode
import numpy as np
from PIL import Image

import vcsd.util as util

# TODO docstring for Decryptor class
class Decryptor():
    """
    """


    # TODO create extract_LSB
    # def extract_LSB(steg_A, steg_B):
    #     return dist_trans_A, dist_trans_B
    

    # TODO create clean_distortion
    # def clean_distortion(dist_trans_A, dist_trans_B):
    #     return trans_A, trans_B

    
    def extract_qr_from_transparences(self, trans_A, trans_B):
        """Extract the QR code from a pair of transparencies
        
        Extract a qr code matrix (2D numpy array) from a pair of transparencies.
        If the size of the transparencies is (N x N), the extracted qr code will consist on a matrix of size (n x n), n = N/2.

        Parameters
        ----------
        trans_A: ndarray
            Transparence A, a 2D array computed from the QR code
        trans_B: ndarray
            Transparence B, a 2D array computed from the QR code
        
        Returns
        -------
        qr_matrix_rec: ndarray
            QR code matrix, a 2D array representing the QR code
        """
        # recover QR code matrix applying visual criptography   
        qr_rec_XOR = trans_A != trans_B
        submatrix_size = 2
        qr_matrix_rec = qr_rec_XOR[::submatrix_size, ::submatrix_size]

        return qr_matrix_rec


    def extract_data_from_qr_matrix(self, qr_matrix_rec):
        """Extract the data from the QR code specified
        
        Extract the text data from the QR code matrix specified

        Parameters
        ----------
        qr_matrix_rec: ndarray
            QR code matrix, a 2D array representing the QR code

        Returns
        -------
        data: str
            The text data extracted from the QR code
        im_qr_extracted: object
            Image object with the recovered QR code, instance of the PIL Image class
        """
        # convert that matrix into qr_code object
        qr_version = util.QR_SIZE_VERSION_DICT[len(qr_matrix_rec)]
        qr_code = qrcode.QRCode(version=qr_version, border=1)
        qr_code.make(fit=True)
        qr_code.modules = qr_matrix_rec
        
        # obtain image object with the qr code extracted
        im_qr_extracted = qr_code.make_image()
        
        # use cv2 to extract the data from the qr image object
        im_qr_extracted_arr = np.asarray(im_qr_extracted.convert('RGB'))
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(im_qr_extracted_arr)
        # sometimes images are not properly detected by cv2
        # rotating the image 90 degrees helps in most of the cases
        if(data==''):
            im_qr_extracted_arr = np.rot90(im_qr_extracted_arr)
            data, bbox, straight_qrcode = detector.detectAndDecode(im_qr_extracted_arr)

        return data, im_qr_extracted
