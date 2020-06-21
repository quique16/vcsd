"""Utility functions"""

import os
import numpy as np
from PIL import Image


EMOJIS = {
    "check_mark_button":    "\U00002705",
    "cross_mark":           "\U0000274C",
    "magnifying_glass":     "\U0001F50D",
    "detective":            "\U0001F575"
}

# key: value
# qr_code_size: qr_code_version
QR_SIZE_VERSION_DICT = {
    21:  1,  	 25:  2,  	 29:  3,  	 33:  4,  	 37:  5,  	
    41:  6,  	 45:  7,  	 49:  8,  	 53:  9,  	 57:  10,  	
    61:  11,  	 65:  12,  	 69:  13,  	 73:  14,  	 77:  15,  	
    81:  16,  	 85:  17,  	 89:  18,  	 93:  19,  	 97:  20,  	
    101: 21,  	 105: 22,  	 109: 23,  	 113: 24,  	 117: 25,  	
    121: 26,  	 125: 27,  	 129: 28,  	 133: 29,  	 137: 30,  	
    141: 31,  	 145: 32,  	 149: 33,  	 153: 34,  	 157: 35,  	
    161: 36,  	 165: 37,  	 169: 38,  	 173: 39,  	 177: 40
}



### Image object helpers ###


def gen_image_from_transparence(trans):
    """Generate an image from a transparence 2D array
    
    Generate an image object (ready to be saved or plotted) from a transparence (2D numpy array)

    Parameters
    ----------
    trans: ndarray
        Transparence, a 2D array computed from the QR code
    
    Returns
    -------
    im: object
        Image object, instance of the PIL Image class
    """
    trans_im = np.expand_dims(255*trans, axis=2)
    trans_im = np.where(trans_im==[255], [255,255,255], [0,0,0]).astype(np.uint8)
    im = Image.fromarray(trans_im)
    return im


def gen_transparence_from_image(im):
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



### SAVE ###


def save_im(im, path_im, im_name="image_gen.png"):
    """Save an image file from an image object
    
    Save a file with an image generated from an incoming image object

    Parameters
    ----------
    im: object
        Image object, instance of the PIL Image class
    path_im: str
        Absolute path where to store the qr image file
    im_name: str, default="image_gen.png"
        Name for the generated file
    """
    if(path_im==""):
        try:
            dirpath = os.path.join(os.getcwd(), im_name)
            im.save(dirpath, 'png')
            print(EMOJIS["check_mark_button"] + f" Image successfully saved at '{dirpath}'")
        except:
            print(EMOJIS["cross_mark"] + f" Unable to correctly save the image at '{dirpath}'")
    else:
        try:
            im.save(path_im, 'png')
            print(EMOJIS["check_mark_button"] + f" Image successfully saved at '{path_im}'")
        except FileNotFoundError as fnf_error:
            print(EMOJIS["cross_mark"], fnf_error)
        except:
            print(EMOJIS["cross_mark"] + f" Unable to save the image at the path specified: '{path_im}'")



### LOAD ###


def load_im(path_im=""):
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
            print(EMOJIS["check_mark_button"] + f" Image successfully loaded from '{path_im}'")
            return im
        except FileNotFoundError as fnf_error:
            print(EMOJIS["cross_mark"], fnf_error)
        except:
            print(EMOJIS["cross_mark"] + f" Unable to correctly load the image from '{path_im}'")
    else:
        print(EMOJIS["cross_mark"] + " The path to the image was not provided")


def load_trans_pair(path_im_A="", path_im_B=""):
    """Load the image files of the pair of transparencies

    Load the image files (in .png format) of the pair of transparencies and extract the 2D arrays with the transparences.
    If checks are successful return each transpacencie of the pair as a 2D numpy array.

    Parameters
    ----------
    path_im_A: str
        Absolute path where the image (in .png format) of the transparence A is stored
    path_im_B: str
        Absolute path where the image (in .png format) of the transparence B is stored

    Returns
    -------
    trans_A: ndarray
        Transparence A, a 2D array computed from the QR code
    trans_B: ndarray
        Transparence B, a 2D array computed from the QR code
    """
    # load images with transparencies
    im_trans_A = load_im(path_im=path_im_A)
    im_trans_B = load_im(path_im=path_im_B) 
    
    if(im_trans_A and im_trans_B):
        try:
            # extract binary matrices
            trans_A = gen_transparence_from_image(im_trans_A)
            trans_B = gen_transparence_from_image(im_trans_B)
        except:
            print(EMOJIS["cross_mark"] + f" Unable to properly extract the transparencies information from the loaded images")
            print(EMOJIS["detective"]  + f" Probably one or both of them have incorrect format")
        return trans_A, trans_B


def validate_trans_pair(trans_A, trans_B):
    """Validate the arrays of the pair of transparencies

    Validate if the 2D arrays for the transparencies are equal sized and check the version of the QR code they contain.
    Return a boolean containing the result of the validation (True is valid, False otherwise).

    Parameters
    ----------
    trans_A: ndarray
        Transparence A, a 2D array computed from the QR code
    trans_B: ndarray
        Transparence B, a 2D array computed from the QR code

    Returns
    -------
    is_valid: bool
        True if the pair of transparences is considered valid, False otherwise.
    """
    is_valid = False
    if(trans_A.any() and trans_B.any()):
        # determine version of the hidden qr code
        if((len(trans_A) == len(trans_B)) and (trans_A!=trans_B).any()):
            print(EMOJIS["check_mark_button"] + " Loaded transparences are equally sized and different")
            qr_size = round(len(trans_A)/2)
            detected_version = QR_SIZE_VERSION_DICT[qr_size]
            print(EMOJIS["magnifying_glass"] + f" Loaded transparences correspond to a QR code version {detected_version}")
            is_valid = True
            return is_valid
        elif((trans_A==trans_B).all()):
            print(EMOJIS["cross_mark"] + f" Both transparencies are equal, no data can be extracted from two equal transparencies")
            return is_valid
        else:
            print(EMOJIS["cross_mark"] + f" There is size mismatch between both transparencies: {trans_A.shape} and {trans_B.shape}. They need to be equally sized")
            return is_valid
    else:
        print(EMOJIS["cross_mark"] + f" Unable to recognise the transparence/s provided")
        return is_valid
   
