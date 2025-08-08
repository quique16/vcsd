# VisioCrypt

**Visual cryptography** package designed to hide text messages inside a QR
code, generating two transparencies that reveal the content when overlaid.

## Installation

1. Clone this repository and enter it:

   ```bash
   git clone https://github.com/<user>/VisioCrypt.git
   cd VisioCrypt
   ```

2. Install the package with `pip`:

   ```bash
   python -m pip install .
   ```

   For an editable installation for development you can use:

   ```bash
   python -m pip install -e .
   ```

## Usage

The `VisioCrypt.main` module provides high-level functions for encrypting and
decrypting messages. The basic workflow consists of two steps: generating the
transparencies from the text and recovering the message from them.

### Encryption

```python
from VisioCrypt.main import apply_encryption

trans_A, trans_B = apply_encryption(
    "secret message",
    save_ims_gen_trans=True,
    path_im_A="trans_A.png",
    path_im_B="trans_B.png",
)
```

The example above generates a QR code with the specified text and produces two
transparencies (`trans_A.png` and `trans_B.png`). When they are overlaid, the
original message can be recovered.

### Decryption

```python
from VisioCrypt.main import apply_decryption

message = apply_decryption(trans_A=trans_A, trans_B=trans_B)
print(message)  # prints: "secret message"
```

It is also possible to load the transparencies from files:

```python
message = apply_decryption(
    load_from_files=True,
    path_im_A="trans_A.png",
    path_im_B="trans_B.png",
)
```

## Package structure

```
VisioCrypt/
├── encryptor.py  # Generates the QR and the transparencies
├── decryptor.py  # Recovers the message from the transparencies
└── main.py       # High-level functions (apply_encryption, apply_decryption)
```

