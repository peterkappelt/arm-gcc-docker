"""
Fetch and unpack specific ARM GCC version
"""

from argparse import ArgumentParser
from tempfile import TemporaryDirectory
import tarfile
import requests
import os
import shutil

gcc_versions = {
    "x86_64": {
        "10.3-2021.10": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-x86_64-linux.tar.bz2?rev=78196d3461ba4c9089a67b5f33edf82a&hash=5631ACEF1F8F237389F14B41566964EC",
        "10-2020-q4-major": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-x86_64-linux.tar.bz2?revision=ca0cbf9c-9de2-491c-ac48-898b5bbc0443&rev=ca0cbf9c9de2491cac48898b5bbc0443&hash=0C735F2481B3EDAB54EF4E68321CE01F",
        "9-2019-q4-major": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2019q4/gcc-arm-none-eabi-9-2019-q4-major-x86_64-linux.tar.bz2?revision=108bd959-44bd-4619-9c19-26187abf5225&rev=108bd95944bd46199c1926187abf5225&hash=E367D388F6429B67D5D6BECF691B9521",
        "8-2018-q4-major": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/8-2018q4/gcc-arm-none-eabi-8-2018-q4-major-linux.tar.bz2?rev=ab7c81a3cba343beaf9de922098961dd&revision=ab7c81a3-cba3-43be-af9d-e922098961dd?product=Downloads,64-bit,,Linux,8-2018-q4-major",
    },
    "aarch64": {
        "10.3-2021.10": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10.3-2021.10/gcc-arm-none-eabi-10.3-2021.10-aarch64-linux.tar.bz2?rev=b748c39178c043b4915b04645d7774d8&hash=572217C8AFE83F1010753EA3E3A7EC2307DADD58",
        "10-2020-q4-major": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/10-2020q4/gcc-arm-none-eabi-10-2020-q4-major-aarch64-linux.tar.bz2?revision=cff794bc-3fb1-4c9c-934b-782886767324&rev=cff794bc3fb14c9c934b782886767324&hash=14BD0CC7D78E6D5E5FCF87DBB6D845C4A651BFD7",
        "9-2019-q4-major": "https://developer.arm.com/-/media/Files/downloads/gnu-rm/9-2019q4/gcc-arm-none-eabi-9-2019-q4-major-aarch64-linux.tar.bz2?revision=4583ce78-e7e7-459a-ad9f-bff8e94839f1&rev=4583ce78e7e7459aad9fbff8e94839f1&hash=C9B942D74CEA05FF9DE28380F267BB7D3F3B17A6",
    },
}

parser = ArgumentParser(
    description="Download and unpack arm-none-eabi-gcc to the current directory.\nThe script will output the folder where the compiler was extracted to."
)
parser.add_argument(
    "ARCH",
    help="Host architecture to fetch for. One of " + ", ".join(gcc_versions.keys()),
)
parser.add_argument(
    "GCC_VERSION",
    help="arm-none-eabi-gcc version to fetch. One of "
    + ", ".join(gcc_versions["x86_64"].keys()),
)

if __name__ == "__main__":
    args = parser.parse_args()
    requested_arch = args.ARCH
    requested_gcc_version = args.GCC_VERSION

    if not requested_arch in gcc_versions.keys():
        print("Unknown arch!")
        exit(1)

    if not requested_gcc_version in gcc_versions[requested_arch].keys():
        print("Unknown gcc version!")
        exit(1)

    with TemporaryDirectory() as tmp_dl, TemporaryDirectory() as tmp_tar:
        res = requests.get(gcc_versions[requested_arch][requested_gcc_version], stream=True)
        with open(f"{tmp_dl}/{requested_gcc_version}.tar.bz2", "wb") as fd:
            for chunk in res.iter_content(chunk_size=8192):
                fd.write(chunk)
        with tarfile.open(f"{tmp_dl}/{requested_gcc_version}.tar.bz2") as tar:
            tar.extractall(tmp_tar)

        extracted_folder = os.listdir(tmp_tar)[0]
        shutil.move(f"{tmp_tar}/{extracted_folder}", ".")

        print(extracted_folder)
