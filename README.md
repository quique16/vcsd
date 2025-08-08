# CVSD

## Package structure

### Encryption module

```python
class Encryptor():
    def generate_qr(data):
        return qr_code
    def generate_transparences(qr_code):
        return trans_A, trans_B
    def apply_distortion(trans_A, trans_B):
        return dist_trans_A, dist_trans_B
    def apply_LSB(dist_trans_A, dist_trans_B):
        return steg_A, steg_B
```

### Decryption module

```python
class Decryptor():
    def extract_LSB(steg_A, steg_B):
        return dist_trans_A, dist_trans_B
    def clean_distortion(dist_trans_A, dist_trans_B):
        return trans_A, trans_B
    def extract_qr_from_transparences(trans_A, trans_B):
        return qr_matrix
    def extract_data_from_qr_matrix(qr_matrix):
        return data
```
