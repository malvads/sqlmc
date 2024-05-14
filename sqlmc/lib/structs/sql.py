from dataclasses import dataclass

@dataclass
class SqlInjectionReport:
    error: bool
    db: str
