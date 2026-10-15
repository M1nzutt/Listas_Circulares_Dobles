from dataclasses import dataclass


@dataclass(frozen=True)
class OdysseyChampion:
    name: str
    role: str
    specialty: str
    greeting: str
    hint_prefix: str


CHARACTERS = [
    OdysseyChampion('Yasuo', 'Capitán', 'Observación', 'Mantén la calma. Cada detalle cuenta.', 'Observa con atención: '),
    OdysseyChampion('Jinx', 'Experta en improvisación', 'Experimentación', '¿Qué podría salir mal? ¡Probemos!', 'Idea loca: '),
    OdysseyChampion('Sona', 'Intérprete', 'Patrones', 'Una señal silenciosa puede decirlo todo.', 'Patrón detectado: '),
    OdysseyChampion('Ziggs', 'Inventor', 'Tecnología', '¡Ese sistema está pidiendo una reparación!', 'Diagnóstico técnico: '),
    OdysseyChampion('Malphite', 'Protector', 'Resistencia', 'Vamos paso a paso. Lo lograremos.', 'Una pista sencilla: '),
]
