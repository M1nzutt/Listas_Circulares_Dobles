# ENIGMA: Odyssey

Aventura narrativa de investigación espacial en español. Proyecto académico de fans **no oficial** inspirado en la temática Odyssey de League of Legends. No incluye imágenes oficiales de Riot; el arte espacial incluido es original y generado para este ejercicio.

## Abrir en Windows con VS Code

1. Extrae el ZIP y abre la **carpeta interior** `ENIGMA_Odyssey` (la que contiene `main.py`).
2. Abre Terminal > New Terminal.
3. Ejecuta:

```powershell
py -m pip install -r requirements.txt
py main.py
```

Si `py` no está disponible, sustituye `py` por `python`.

## Juego

- Escoge Yasuo, Jinx, Sona, Ziggs o Malphite en tarjetas.
- Escoge uno de los tres episodios: Señal perdida, El núcleo de Ora, La sombra de Rhaast.
- Lee la **bitácora de misión a la izquierda**; los datos necesarios para la respuesta aparecen en el relato.
- Resuelve el acertijo de la derecha, solicita una pista o consulta estaciones anteriores.
- Solo podrás avanzar cuando resuelvas el acertijo actual. El circuito es circular al completar la misión.
- El tiempo límite y el progreso aparecen durante la partida.
- El modo administrador permite crear, editar y eliminar salas/acertijos y comprueba los enlaces.

## Arquitectura

- `models/`: OdysseyChampion, OdysseyMission, OdysseyRiddle
- `structures/riddle_circuit.py`: RiddleCircuit + RiddleStation; estructura circular doble enlazada real, sin listas Python para implementar los enlaces.
- `controllers/`: MissionDirector y MissionArchitect
- `services/`: MissionArchive y CaptainLog (guardado JSON)
- `views/odyssey_console.py`: EnigmaOdysseyApp, frontend CustomTkinter en español
- `assets/`: arte espacial original del proyecto

Todos los nombres de clases están relacionados con el dominio ENIGMA, y el código usa identificadores en inglés.

## Pruebas

```powershell
py -m unittest discover -s tests -v
```

## Guardados

La app guarda contenido y progreso en `%USERPROFILE%\.enigma_odyssey`. Si ejecutaste una versión anterior, sus misiones antiguas pueden permanecer en `rooms.json`. Para recuperar **las misiones narrativas nuevas**, cierra la aplicación, haz una copia de seguridad y renombra `rooms.json` (ej. `rooms_anterior.json`). Al abrir de nuevo se cargarán los nuevos capítulos. El progreso anterior, si lo hay, seguirá separado en otro archivo.

## Nota

El frontend se ha actualizado y las 7 pruebas automatizadas pasan. La visualización en Windows depende de las fuentes y escala de pantalla; no se ha verificado visualmente en el equipo del usuario.
