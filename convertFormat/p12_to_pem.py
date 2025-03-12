from fastapi import FastAPI, UploadFile, File, HTTPException, Form
import subprocess
import os

app = FastAPI()

UPLOAD_DIR = "certificates"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Crear directorio para almacenar certificados

# Endpoint para recibir .p12 y convertirlo en .pem
@app.post("/convert/p12-to-pem/")
async def convert_p12_to_pem(file: UploadFile = File(...), password: str = Form(...)):
    try:
        # Guardar el archivo .p12 temporalmente
        p12_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(p12_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Definir la ruta de salida del archivo .pem
        pem_path = p12_path.replace(".p12", ".pem")

        # Comando para convertir .p12 a .pem usando OpenSSL
        command = [
            "openssl", "pkcs12",
            "-in", p12_path,
            "-out", pem_path,
            "-nodes",
            "-password", f"pass:{password}"
        ]

        # Ejecutar el comando
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Verificar errores
        if result.returncode != 0:
            raise HTTPException(status_code=500, detail=f"Error en la conversión: {result.stderr}")

        return {"message": "Conversión exitosa", "pem_file": pem_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/extract/pem/")
async def extract_pem(file: UploadFile = File(...)):
    try:
        pem_path = os.path.join(UPLOAD_DIR, file.filename)
        
        # Leer contenido del archivo .pem
        with open(pem_path, "r") as pem_file:
            pem_content = pem_file.read()

        # Separar clave privada y certificado
        private_key = []
        certificate = []
        inside_private = False
        inside_cert = False

        for line in pem_content.split("\n"):
            if "BEGIN PRIVATE KEY" in line:
                inside_private = True
            if "END PRIVATE KEY" in line:
                inside_private = False
                private_key.append(line)
            
            if "BEGIN CERTIFICATE" in line:
                inside_cert = True
            if "END CERTIFICATE" in line:
                inside_cert = False
                certificate.append(line)

            if inside_private:
                private_key.append(line)
            elif inside_cert:
                certificate.append(line)

        # Guardar clave privada y certificado en archivos separados
        private_key_path = pem_path.replace(".pem", "_private.pem")
        certificate_path = pem_path.replace(".pem", "_cert.pem")

        with open(private_key_path, "w") as pk_file:
            pk_file.write("\n".join(private_key))

        with open(certificate_path, "w") as cert_file:
            cert_file.write("\n".join(certificate))

        return {
            "message": "Extracción exitosa",
            "private_key": private_key_path,
            "certificate": certificate_path
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))






