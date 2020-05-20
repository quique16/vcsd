import os
import qrcode
import random
import numpy as np
from PIL import Image

# TODO docstring for CvedEncryptor class
class CvedEncryptor():
    emojis = {
        "check_mark_button":    "\U00002705",
        "cross_mark":           "\U0000274C"
    }

    def gen_image_from_transparence(self, trans):
        """Generate an image from a transparence 2D array
        
        Generate an image object (ready to be saved or plotted) from a transparence (2D numpy array)

        Parameters
        ----------
        trans: ndarray
            Transparence, a 2D array computed from the QR code
        
        Returns
        -------
        im: object
            Image object
        """
        trans_im = np.expand_dims(255*trans, axis=2)
        trans_im = np.where(trans_im==[255], [255,255,255], [0,0,0]).astype(np.uint8)
        im = Image.fromarray(trans_im)
        return im


    def save_image(self, im, path_im, im_name="/image_gen.png"):
        """Save an image file from an image object
        
        Save a file with an image generated from an incoming image object

        Parameters
        ----------
        im: object
            Image object
        path_im: str
            Absolute path where to store the qr image file
        im_name: str, default="/image_gen.png"
            Name for the generated file
        """
        if(path_im==""):
            try:
                dirpath = os.getcwd() + im_name
                im.save(dirpath)
                print(self.emojis["check_mark_button"] + f" Image successfully saved at {dirpath}")
            except:
                print(self.emojis["cross_mark"] + " Unable to correctly save the image")
        else:
            try:
                im.save(path_im)
                print(self.emojis["check_mark_button"] + f" Image successfully saved at {path_im}")
            except:
                print(self.emojis["cross_mark"] + " Unable to find the path specified")
    

    def generate_qr(self, text, save_im=False, path_im=""):
        """Generate QR code from the text specified
        
        Generate a QR code object containing the text specified in the arguments

        Parameters
        ----------
        text: str
            The text to be added in the QR code
        save_im: bool, default=False
            Whether to save QR or not (location by default ir current directory)
        path_im: str
            Absolute path where to store the qr image file

        Returns
        -------
        qr_code: object
            QR code python object, instance of the qrcode class
        """
        qr_code = qrcode.QRCode()
        qr_code.add_data(text)
        qr_code.make(fit=True)
        im = qr_code.make_image()
        if(save_im):
            self.save_image(im, path_im, im_name="/qr_code_gen.png")        
        return qr_code


    def generate_transparences(self, qr_code, save_ims=False, path_im_A="", path_im_B=""):
        """Generate 2 transparences from a qr_code object
        
        Generate 2 transparences (trans_A and trans_B) from a qr_code object. If the qr code consist on a matrix of size (n x n), the size of the transparences is the double: N = 2*n, (N x N).

        Parameters
        ----------
        qr_code: object
            QR code python object, instance of the qrcode class

        Returns
        -------
        trans_A: ndarray
            Transparence A, a 2D array computed from the QR code
        trans_B: ndarray
            Transparence B, a 2D array computed from the QR code
        """
        qr_code_matrix = np.array(qr_code.get_matrix()).astype(int)
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
        
        if(save_ims):
            im_A = self.gen_image_from_transparence(trans_A)
            im_B = self.gen_image_from_transparence(trans_B)
            self.save_image(im_A, path_im_A, im_name="/trans_A_gen.png")   
            self.save_image(im_B, path_im_B, im_name="/trans_B_gen.png")

        return trans_A, trans_B
    
    
    # TODO create apply_distortion
    # def apply_distortion(trans_A, trans_B):
    #     return dist_trans_A, dist_trans_B
    

    # TODO create apply_LSB
    # def apply_LSB(dist_trans_A, dist_trans_B):
    #     return steg_A, steg_B
