"""Encrypt and decrypt a message in memory."""

from visiocrypt import apply_encryption, apply_decryption


def main() -> None:
    message = "hello world"
    trans_a, trans_b = apply_encryption(message)
    recovered = apply_decryption(trans_a, trans_b)
    print(f"Original: {message}")
    print(f"Recovered: {recovered}")


if __name__ == "__main__":
    main()
