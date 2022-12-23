from dataclasses import dataclass

@dataclass
class User:
    cpf: str
    liveness_required: dict