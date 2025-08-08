# vcsd

Paquete de **criptografía visual** orientado a ocultar mensajes de texto en un
código QR, generando dos transparencias que al superponerse revelan el
contenido.

## Instalación

1. Clona este repositorio y entra en él:

   ```bash
   git clone https://github.com/<usuario>/vcsd.git
   cd vcsd
   ```

2. Instala el paquete con `pip`:

   ```bash
   python -m pip install .
   ```

   Si se quiere realizar una instalación editable para desarrollo puede
   usarse:

   ```bash
   python -m pip install -e .
   ```

## Uso

El módulo `vcsd.main` ofrece funciones de alto nivel para cifrar y descifrar
mensajes. El flujo básico consta de dos pasos: generar las transparencias a
partir del texto y recuperar el mensaje desde ellas.

### Cifrado

```python
from vcsd.main import apply_encryption

trans_A, trans_B = apply_encryption(
    "mensaje secreto",
    save_ims_gen_trans=True,
    path_im_A="trans_A.png",
    path_im_B="trans_B.png",
)
```

El ejemplo anterior genera un código QR con el texto especificado y produce dos
transparencias (`trans_A.png` y `trans_B.png`). Al superponerlas se puede
recuperar el mensaje original.

### Descifrado

```python
from vcsd.main import apply_decryption

mensaje = apply_decryption(trans_A=trans_A, trans_B=trans_B)
print(mensaje)  # imprime: "mensaje secreto"
```

También es posible cargar las transparencias desde archivos:

```python
mensaje = apply_decryption(
    load_from_files=True,
    path_im_A="trans_A.png",
    path_im_B="trans_B.png",
)
```

## Estructura del paquete

```
vcsd/
├── encryptor.py  # Genera el QR y las transparencias
├── decryptor.py  # Recupera el mensaje a partir de las transparencias
└── main.py       # Funciones de alto nivel (apply_encryption, apply_decryption)
```

