import subprocess
from pathlib import Path

class OpenSSLAdapter:
    @staticmethod
    def convert_p12_to_pem(p12_path: str, pem_path: str, password: str):
        command = [
            "openssl", "pkcs12",
            "-in", p12_path,
            "-out", pem_path,
            "-nodes",
            "-password", f"pass:{password}"
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Error en OpenSSL: {result.stderr}")
        return pem_path
