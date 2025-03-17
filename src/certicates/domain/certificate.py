from dataclasses import dataclass

@dataclass
class Certificate:
    id: int
    name: str
    storage_url: str
    private_key_url: str
    public_cert_url: str
