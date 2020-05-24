import os
import cv2
import qrcode
import numpy as np
from PIL import Image

# TODO docstring for CvedDecryptor class
class CvedDecryptor():
    emojis = {
        "check_mark_button":    "\U00002705",
        "cross_mark":           "\U0000274C",
        "magnifying_glass":     "\U0001F50D"
    }

    # qr_code_size: qr_code_version
    qr_size_version_dict = {
        21:  1,  	 25:  2,  	 29:  3,  	 33:  4,  	 37:  5,  	
        41:  6,  	 45:  7,  	 49:  8,  	 53:  9,  	 57:  10,  	
        61:  11,  	 65:  12,  	 69:  13,  	 73:  14,  	 77:  15,  	
        81:  16,  	 85:  17,  	 89:  18,  	 93:  19,  	 97:  20,  	
        101: 21,  	 105: 22,  	 109: 23,  	 113: 24,  	 117: 25,  	
        121: 26,  	 125: 27,  	 129: 28,  	 133: 29,  	 137: 30,  	
        141: 31,  	 145: 32,  	 149: 33,  	 153: 34,  	 157: 35,  	
        161: 36,  	 165: 37,  	 169: 38,  	 173: 39,  	 177: 40
    }

    def save_im(self, im, path_im, im_name="/image_gen.png"):
        """Save an image file from an image object
        
        Save a file with an image generated from an incoming image object

        Parameters
        ----------
        im: object
            Image object, instance of the PIL Image class
        path_im: str
            Absolute path where to store the qr image file
        im_name: str, default="/image_gen.png"
            Name for the generated file
        """
        if(path_im==""):
            try:
                dirpath = os.getcwd() + im_name
                im.save(dirpath, 'png')
                print(self.emojis["check_mark_button"] + f" Image successfully saved at {dirpath}")
            except:
                print(self.emojis["cross_mark"] + " Unable to correctly save the image")
        else:
            try:
                im.save(path_im, 'png')
                print(self.emojis["check_mark_button"] + f" Image successfully saved at {path_im}")
            except:
                print(self.emojis["cross_mark"] + " Unable to find the path specified")


    def load_im(self, path_im=""):
        """Load an image file 

        Load an image file (in .png format) and return it as a PIL Image object

        Parameters
        ----------
        path_im: str
            Absolute path where the image (in .png format) is stored

        Returns
        -------
        im: object
            Image object, instance of the PIL Image class
        """
        if(path_im!=""):
            try:
                im = Image.open(path_im, mode="r")
                print(self.emojis["check_mark_button"] + f" Image successfully loaded from {path_im}")
                return im
            except:
                print(self.emojis["cross_mark"] + f" Unable to correctly load the image from {path_im}")
        else:
            print(self.emojis["cross_mark"] + " The path to the image was not provided")


    def gen_transparence_from_image(self, im):
        """Generate transparence 2D array from an image
        
        Generate a transparence (2D numpy array) from an image object (ready to be saved or plotted) 

        Parameters
        ----------
        im: object
            Image object, instance of the PIL Image class
        
        Returns
        -------
        trans: ndarray
            Transparence, a 2D array computed from the QR code
        """
        trans_rgb = np.array(im)
        trans = trans_rgb.mean(axis=2).astype(int)
        trans = (trans/255).astype(int)
        return trans


    def load_and_validate_trans(self, path_im_A="", path_im_B=""):
        """
        """

        # load images with transparencies
        im_trans_A = self.load_im(path_im=path_im_A)
        im_trans_B = self.load_im(path_im=path_im_B) 
        
        # extract binary matrices
        trans_A = self.gen_transparence_from_image(im_trans_A)
        trans_B = self.gen_transparence_from_image(im_trans_B)
        
        # determine version of the hidden qr code
        if(len(trans_A) == len(trans_B)):
            print(emojis["check_mark_button"] + " Loaded transparences are equally sized")
            qr_size = round(len(trans_A)/2)
            detected_version = qr_size_version_dict[qr_size]
            print(emojis["magnifying_glass"] + f" Loaded transparences correspond to a QR code version {detected_version}")
        else:
            print(emojis["cross_mark"] + f" There is size mismatch between both transparencies: {trans_A.shape} and {trans_B.shape}. They need to be equally sized")
            
        return trans_A, trans_B


    # TODO create extract_LSB
    # def extract_LSB(steg_A, steg_B):
    #     return dist_trans_A, dist_trans_B
    

    # TODO create clean_distortion
    # def clean_distortion(dist_trans_A, dist_trans_B):
    #     return trans_A, trans_B

    
    def extract_qr_from_transparences(self, trans_A, trans_B):
        """
        """

        # recover QR code matrix applying visual criptography   
        qr_rec_XOR = trans_A != trans_B
        submatrix_size = 2
        qr_matrix_rec = qr_rec_XOR[::submatrix_size, ::submatrix_size]

        return qr_matrix_rec


    # TODO create extract_text_from_qr
    # def extract_text_from_qr(qr_code):
    #   return text

    def extract_data_from_qr_matrix(self, qr_matrix_rec, save_im=False, path_im_QR_rec=""):
        """
        """

        # convert that matrix into qr_code object
        qr_version = qr_size_version_dict[len(qr_matrix_rec)]
        qr_code = qrcode.QRCode(version=qr_version, border=1)
        qr_code.make(fit=True)
        qr_code.modules = qr_matrix_rec
        
        # obtain image object with the qr code extracted
        im_qr_extracted = qr_code.make_image()

        # this should be separated in other function (maybe the composed ones)
        if(save_im):
            self.save_im(im=im_qr_extracted, path_im=path_im_QR_rec)
        
        # use cv2 to extract the data from the qr image object
        im_qr_extracted = np.asarray(im_qr_extracted.convert('RGB'))
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(im_qr_extracted)
        
        return data