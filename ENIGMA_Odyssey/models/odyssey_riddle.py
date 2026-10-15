from dataclasses import dataclass, field
from typing import List


@dataclass
class OdysseyRiddle:
    id: str
    title: str
    narrative: str
    question: str
    answer: str
    hint: str
    category: str = "Código"
    choices: List[str] = field(default_factory=list)

    def validate(self) -> None:
        if not all([self.id.strip(), self.title.strip(), self.question.strip(), self.answer.strip()]):
            raise ValueError("ID, título, pregunta y respuesta son obligatorios.")

    def matches(self, attempt: str) -> bool:
        def normalized(value: str) -> str:
            import unicodedata
            import re
            text = unicodedata.normalize('NFKD', value.strip().casefold())
            text = ''.join(char for char in text if not unicodedata.combining(char))
            return re.sub(r'\s+', ' ', text)
        return normalized(attempt) == normalized(self.answer)
