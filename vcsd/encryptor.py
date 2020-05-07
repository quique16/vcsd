import os
import qrcode

# TODO docstring for CvedEncryptor class
class CvedEncryptor():


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
            dirpath = os.getcwd() + im_name
            im.save(dirpath)
        else:
            try:
                im.save(path_im)
            except:
                print("Unable to find the path specified")
    

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
        qr_code: str
            QR code python object, instance of the qrcode class
        """
        qr_code = qrcode.QRCode()
        qr_code.add_data(text)
        qr_code.make(fit=True)
        im = qr_code.make_image()
        if(save_im):
            self.save_image(im, path_im, im_name="/qr_code_gen.png")        
        return qr_code


    # TODO create generate_transparences
    # def generate_transparences(qr_code):
    #     return trans_A, trans_B
    
    
    # TODO create apply_distortion
    # def apply_distortion(trans_A, trans_B):
    #     return dist_trans_A, dist_trans_B
    

    # TODO create apply_LSB
    # def apply_LSB(dist_trans_A, dist_trans_B):
    #     return steg_A, steg_B
