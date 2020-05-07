import os
import qrcode
from vcsd.encryptor import CvedEncryptor as enc

# really important to properly instanciate the class
encoder = enc()

# initial code for testing qr code generation and image save
encoder.generate_qr("hola mundo, que tal?")
encoder.generate_qr("hola mundo, que tal?", save_im=True)
encoder.generate_qr("hola mundo, que tal?", save_im=True, path_im="/Users/eiglesias/Desktop/ey/image.png")
encoder.generate_qr("hola mundo, que tal?", save_im=True, path_im="/Users/eiglesias/Desktop/eo/image.png")

# future tests will need to be per function