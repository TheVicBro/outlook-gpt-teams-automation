from dataclasses import dataclass

@dataclass
class CompletionResponse:
    payload: str = ""
    message: str = ""
    err: str = ""