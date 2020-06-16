import os
import qrcode
import random
import numpy as np
from PIL import Image

import vcsd.util as util

# TODO docstring for CvedEncryptor class
class Encryptor():
    '''
    '''


    def apply_encryption(self, data, save_im_gen_QR=False, path_im_QR="", save_ims_gen_trans=False, path_im_A="", path_im_B=""):
        """Obtains the data hidden in two transparencies
        
        Perform all the steps needed to retrieve the data encrypted in two transparencies by visual-crypt

        Parameters
        ----------
        data: str
            The text to be encoded in the QR code
        save_ims_gen_QR: bool, default=False
            Whether to save the generated QR or not (location by default is current directory)
        path_im_QR: str
            Absolute path where the image file of the qr code generated will be stored
        save_ims_gen_trans: bool, default=False
            Whether to save the generated transparencies or not (location by default is current directory)
        path_im_A: str
            Absolute path where the image (in .png format) of the transparence A genereted will be stored
        path_im_B: str
            Absolute path where the image (in .png format) of the transparence B generated will be stored
        
        Returns
        -------
        trans_A: ndarray
            Transparence A, a 2D array computed from the QR code
        trans_B: ndarray
            Transparence B, a 2D array computed from the QR cod
        """
        # 1 - Generate QR code from the text specified
        qr_code_matrix, im_qr_code = self.generate_qr(data)
        if(save_im_gen_QR):
            # correct the image name
            util.save_im(im_qr_code, path_im_QR, im_name="/qr_code_gen.png")

        # 2 - Generate 2 transparences from a qr_code object obtained
        trans_A, trans_B = self.generate_transparences(qr_code_matrix)
        if(save_ims_gen_trans):
            im_A = util.gen_image_from_transparence(trans_A)
            im_B = util.gen_image_from_transparence(trans_B)
            # correct the images names
            util.save_im(im=im_A, path_im=path_im_A, im_name="/trans_A_gen.png")   
            util.save_im(im=im_B, path_im=path_im_B, im_name="/trans_B_gen.png")

        return trans_A, trans_B


    def generate_qr(self, data):
        """Generate QR code from the text specified
        
        Generate a matrix with the QR code that contains the text specified in the arguments

        Parameters
        ----------
        data: str
            The text to be added in the QR code

        Returns
        -------
        qr_code_matrix: ndarray
            QR code matrix, a 2D array representing the QR code
        im_qr_code: object
            Image object with the generated QR code, instance of the PIL Image class
        """
        qr_code = qrcode.QRCode(border=0)
        qr_code.add_data(data)
        qr_code.make(fit=True)
        im_qr_code = qr_code.make_image()
        qr_code_matrix = np.array(qr_code.get_matrix()).astype(int)
           
        return qr_code_matrix, im_qr_code


    def generate_transparences(self, qr_code_matrix):
        """Generate 2 transparences from a qr_code object
        
        Generate 2 transparences (trans_A and trans_B) from a qr_code object.
        If the qr code consist on a matrix of size (n x n), the size of the transparences is the double: N = 2*n, (N x N).

        Parameters
        ----------
        qr_code_matrix: ndarray
            QR code matrix, a 2D array representing the QR code

        Returns
        -------
        trans_A: ndarray
            Transparence A, a 2D array computed from the QR code
        trans_B: ndarray
            Transparence B, a 2D array computed from the QR code
        """
        trans_A = np.zeros([x * 2 for x in qr_code_matrix.shape], dtype=qr_code_matrix.dtype)
        trans_B = np.zeros([x * 2 for x in qr_code_matrix.shape], dtype=qr_code_matrix.dtype)
        
        it = np.nditer(trans_A, flags=['multi_index'])
        submatrix_size = 2
        
        while not it.finished:
            ri = it.multi_index[0] % submatrix_size
            rj = it.multi_index[1] % submatrix_size
            
            random_bin = np.reshape(np.random.randint(2, size=submatrix_size**2), (submatrix_size,submatrix_size))
            
            if ri == 0 and rj == 0:
                start_row    = it.multi_index[0]
                end_row      = it.multi_index[0] + submatrix_size
                start_column = it.multi_index[1]
                end_column   = it.multi_index[1] + submatrix_size
                qr_row    = int(start_row/2)
                qr_column = int(start_column/2)
                
                if qr_code_matrix[qr_row, qr_column] == 0:
                    trans_A[start_row:end_row, start_column:end_column] = random_bin
                    trans_B[start_row:end_row, start_column:end_column] = random_bin
                else:
                    trans_A[start_row:end_row, start_column:end_column] = random_bin
                    random_bin_inv = np.where(random_bin==0, 1, 0)
                    trans_B[start_row:end_row, start_column:end_column] = random_bin_inv 
                    
            it.iternext()

        return trans_A, trans_B
    
    
    # TODO create apply_distortion
    # def apply_distortion(trans_A, trans_B):
    #     return dist_trans_A, dist_trans_B
    

    # TODO create apply_LSB
    # def apply_LSB(dist_trans_A, dist_trans_B):
    #     return steg_A, steg_B
