"""Save generated transparencies and decrypt from the saved files."""

from VisioCrypt import apply_encryption, apply_decryption


def main() -> None:
    message = "hello world"
    apply_encryption(
        message,
        save_ims_gen_trans=True,
        path_im_A="trans_A.png",
        path_im_B="trans_B.png",
    )
    recovered = apply_decryption(
        load_from_files=True,
        path_im_A="trans_A.png",
        path_im_B="trans_B.png",
    )
    print(f"Original: {message}")
    print(f"Recovered: {recovered}")


if __name__ == "__main__":
    main()
