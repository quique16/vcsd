from VisioCrypt.encryptor import Encryptor
from VisioCrypt.decryptor import Decryptor
import VisioCrypt.util as util


def apply_encryption(data, save_im_gen_QR=False, path_im_QR="", save_ims_gen_trans=False, path_im_A="", path_im_B=""):
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
    enc = Encryptor()
    # 1 - Generate QR code from the text specified
    qr_code_matrix, im_qr_code = enc.generate_qr(data)
    if(save_im_gen_QR):
        # correct the image name
        util.save_im(im_qr_code, path_im_QR, im_name="qr_code_gen.png")

    # 2 - Generate 2 transparences from a qr_code object obtained
    trans_A, trans_B = enc.generate_transparences(qr_code_matrix)
    if(save_ims_gen_trans):
        im_A = util.gen_image_from_transparence(trans_A)
        im_B = util.gen_image_from_transparence(trans_B)
        # correct the images names
        util.save_im(im=im_A, path_im=path_im_A, im_name="trans_A_gen.png")   
        util.save_im(im=im_B, path_im=path_im_B, im_name="trans_B_gen.png")

    return trans_A, trans_B


def apply_decryption(trans_A=None, trans_B=None, load_from_files=False, path_im_A="", path_im_B="", save_im_extracted_QR=False, path_im_extracted_QR=""):
    """Obtains the data hidden in two transparencies
    
    Perform all the steps needed to retrieve the data encrypted in two transparencies by visual-crypt

    Parameters
    ----------
    save_im_extracted_QR: bool, default=False
        Whether to save recovered QR or not (location by default is current directory)
    path_im_A: str
        Absolute path where the image (in .png format) of the transparence A is stored
    path_im_B: str
        Absolute path where the image (in .png format) of the transparence B is stored
    save_im_extracted_QR: bool, default=False
        Whether to save recovered QR or not (location by default is current directory)
    path_im_extracted_QR: str
        Absolute path where to store the image file of the qr code extracted

    Returns
    -------
    data: str
        Text data extracted from the QR code
    """
    dec = Decryptor()

    # transparence pair load and validation
    if(load_from_files):
        # 1 - Load transparencies from the images
        trans_A_rec, trans_B_rec = util.load_trans_pair(path_im_A=path_im_A, path_im_B=path_im_B)
        # 2 - Check if the pair of transparencies is valid
        valid = util.validate_trans_pair(trans_A_rec, trans_B_rec)
    else:
        # 1 - Take transparencies from the function parameters
        trans_A_rec = trans_A
        trans_B_rec = trans_B
        # 2 - Check if the pair of transparencies is valid
        valid = util.validate_trans_pair(trans_A_rec, trans_B_rec)
    
    # transparence pair decryption
    if(valid):
        # 3 - Extract the QR code encoded in the transparencies
        qr_matrix_rec = dec.extract_qr_from_transparences(trans_A_rec, trans_B_rec)
        # 4 - Extract the data encoded in the QR code
        data, im_qr_extracted  = dec.extract_data_from_qr_matrix(qr_matrix_rec)
        if(save_im_extracted_QR):
            util.save_im(im=im_qr_extracted, path_im=path_im_extracted_QR, im_name="QR_rec.png")
        
        return data
