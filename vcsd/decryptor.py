import os
import qrcode
import numpy as np
from PIL import Image

# TODO docstring for CvedDecryptor class
class CvedDecryptor():
    emojis = {
        "check_mark_button":    "\U00002705",
        "cross_mark":           "\U0000274C"
    }


    def load_trans_im(self, path_im_A="", path_im_B=""):
        """Load the image files of a transparence pair 
        
        Load the image files of a transparence pair (A and B) return them as Image objects

        Parameters
        ----------
        path_im_A: str
            Absolute path where the .png file containing transparence A is stored
        path_im_B: str
            Absolute path where the .png file containing transparence B is stored

        Returns
        -------
        im_trans_A: object
            Image object containning transparence A, instance of the PIL Image class
        im_trans_B: object
            Image object containning transparence B, instance of the PIL Image class
        """
        if(path_im_A!="" and path_im_B!=""):
            try:
                im_trans_A = Image.open(path_im_A, mode="r")
                im_trans_B = Image.open(path_im_B, mode="r")
                print(self.emojis["check_mark_button"] + f" Transparence A successfully loaded from {path_im_A}")
                print(self.emojis["check_mark_button"] + f" Transparence B successfully loaded from {path_im_B}")
                return im_trans_A, im_trans_B
            except:
                print(self.emojis["cross_mark"] + " Unable to correctly load the image/s")
        else:
            print(self.emojis["cross_mark"] + " One or more paths to the image/s were not provided")


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


    # TODO create extract_LSB
    # def extract_LSB(steg_A, steg_B):
    #     return dist_trans_A, dist_trans_B
    

    # TODO create clean_distortion
    # def clean_distortion(dist_trans_A, dist_trans_B):
    #     return trans_A, trans_B
    

    # TODO create extract_qr_from_transparences
    # def extract_qr_from_transparences(trans_A, trans_B):
    #     return qr_code
    

    # TODO create extract_text_from_qr
    # def extract_text_from_qr(qr_code):
    #   return text
