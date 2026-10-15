import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
from PIL import Image
from pathlib import Path

from controllers.mission_architect import MissionArchitect
from controllers.mission_director import MissionDirector
from models.odyssey_champion import CHARACTERS
from models.odyssey_mission import OdysseyMission
from services.mission_archive import MissionArchive
from services.captain_log import CaptainLog

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')
BG = '#080D1D'
PANEL = '#141F36'
ACCENT = '#9674E7'
GOLD = '#EEC48B'


class EnigmaOdysseyApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('ENIGMA: Odyssey — Proyecto académico no oficial')
        self.geometry('1120x740')
        self.minsize(870, 610)
        self.configure(fg_color=BG)
        self.repo = MissionArchive()
        self.progress_repo = CaptainLog()
        self.rooms = self.repo.load()
        self.progress = self.progress_repo.load()
        self.character = CHARACTERS[0]
        self.game = None
        self._timer_job = None
        self._images = {}
        self.show_home()
        self.protocol('WM_DELETE_WINDOW', self._close)

    def _close(self):
        self.save_progress()
        if self._timer_job:
            self.after_cancel(self._timer_job)
        self.destroy()

    def clear(self):
        if self._timer_job:
            self.after_cancel(self._timer_job)
            self._timer_job = None
        for child in self.winfo_children():
            child.destroy()

    def label(self, parent, text, size=15, color='white', weight='normal', **kwargs):
        return ctk.CTkLabel(parent, text=text, font=('Segoe UI', size, weight), text_color=color, wraplength=kwargs.pop('wraplength', 780), **kwargs)

    def btn(self, parent, text, command, color=ACCENT, text_color=BG, **kwargs):
        return ctk.CTkButton(parent, text=text, command=command, fg_color=color, hover_color='#C1A6FF',
                             text_color=text_color, font=('Segoe UI', 14, 'bold'), height=kwargs.pop('height', 41), **kwargs)

    def header(self, subtitle=''):
        nav = ctk.CTkFrame(self, fg_color=PANEL, height=65, corner_radius=0)
        nav.pack(fill='x')
        self.label(nav, '✦  ENIGMA: ODYSSEY', 23, GOLD, 'bold').pack(side='left', padx=28, pady=15)
        self.label(nav, subtitle, 12, '#AAB3CA').pack(side='right', padx=24)

    def content(self):
        frame = ctk.CTkScrollableFrame(self, fg_color=BG, corner_radius=0)
        frame.pack(fill='both', expand=True, padx=30, pady=20)
        return frame

    def artwork(self, name, size):
        key = (name, size)
        if key not in self._images:
            image = Image.open(Path(__file__).resolve().parent.parent / 'assets' / name)
            self._images[key] = ctk.CTkImage(light_image=image, dark_image=image, size=size)
        return self._images[key]

    def eyebrow(self, parent, text):
        self.label(parent, text, 12, GOLD, 'bold').pack(anchor='w', pady=(0, 10))

    def show_home(self):
        self.save_progress()
        self.clear()
        self.header('MORNING STAR   /   TRANSMISIÓN ABIERTA')
        main = self.content()
        hero = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=20)
        hero.pack(fill='x', pady=(0, 22))
        hero_image = ctk.CTkLabel(hero, text='', image=self.artwork('hero.png', (970, 325)))
        hero_image.pack(fill='x', padx=9, pady=9)
        self.label(main, '01    /    ELIGE TU TRIPULANTE', 13, GOLD, 'bold').pack(anchor='w', pady=(0, 9))
        self.label(main, 'Cinco maneras de investigar. Una misma galaxia en peligro.', 15, '#B8C9E3').pack(anchor='w', pady=(0, 13))
        roster = ctk.CTkFrame(main, fg_color='transparent')
        roster.pack(fill='x', pady=(0, 23))
        self.character_cards = {}
        glyphs = ['⚔', '✦', '♫', '⚙', '◆']
        for idx, champion in enumerate(CHARACTERS):
            selected = champion.name == self.character.name
            card = ctk.CTkFrame(roster, fg_color='#283957' if selected else PANEL,
                                border_color=GOLD if selected else '#31415A', border_width=2 if selected else 1, corner_radius=14)
            card.grid(row=0, column=idx, sticky='nsew', padx=(0, 9))
            roster.grid_columnconfigure(idx, weight=1, uniform='champions')
            self.label(card, glyphs[idx], 36, GOLD if selected else '#9EAADA', 'bold').pack(pady=(15, 3))
            self.label(card, champion.name.upper(), 15, 'white', 'bold').pack()
            self.label(card, champion.specialty, 11, '#B4C3DE').pack(pady=(3, 10))
            self.btn(card, 'ELEGIDO' if selected else 'ELEGIR', lambda n=champion.name: self.choose_character(n),
                     color=GOLD if selected else '#36466D', text_color=BG if selected else 'white', height=32).pack(fill='x', padx=10, pady=(0, 12))
        self.label(main, '02    /    ELIGE TU DESTINO', 13, GOLD, 'bold').pack(anchor='w', pady=(0, 12))
        for index, room in enumerate(self.rooms):
            card = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=17, border_width=1, border_color='#35435F')
            card.pack(fill='x', pady=8)
            ctk.CTkLabel(card, text='', image=self.artwork(f'mission_{index%3+1}.png', (260, 112))).pack(side='left', padx=10, pady=10)
            info = ctk.CTkFrame(card, fg_color='transparent')
            info.pack(side='left', fill='both', expand=True, padx=15, pady=10)
            self.label(info, room.title.upper(), 19, 'white', 'bold').pack(anchor='w')
            self.label(info, room.description, 12, '#B8C9E3', wraplength=480, justify='left').pack(anchor='w', pady=5)
            self.label(info, f'{room.difficulty.upper()}   ·   {len(room.puzzles)} ESTACIONES   ·   {room.minutes} MIN', 11, GOLD, 'bold').pack(anchor='w')
            self.btn(card, 'INVESTIGAR  →', lambda r=room: self.start_game(r), width=140).pack(side='right', padx=16)
        footer = ctk.CTkFrame(main, fg_color='transparent')
        footer.pack(fill='x', pady=23)
        self.btn(footer, '⚙  ARCHIVO DEL ADMINISTRADOR', self.show_admin, color='#283653', text_color='white', width=310).pack(side='left')
        self.label(footer, 'Proyecto académico de fans · No oficial', 11, '#8899B9').pack(side='right')

    def choose_character(self, name):
        self.character = next(c for c in CHARACTERS if c.name == name)
        self.show_home()

    def _on_character(self, name):
        self.character = next(c for c in CHARACTERS if c.name == name)
        self.character_info.configure(text=f'{self.character.role} · {self.character.specialty} — «{self.character.greeting}»')

    def save_progress(self):
        if self.game:
            key = f'{self.game.character.name}:{self.game.room.id}'
            self.progress[key] = self.game.snapshot()
            try:
                self.progress_repo.save(self.progress)
            except OSError as exc:
                messagebox.showerror('Guardado', str(exc))

    def start_game(self, room):
        self.save_progress()
        key = f'{self.character.name}:{room.id}'
        saved = self.progress.get(key)
        if saved and (len(saved.get('solved', [])) == len(room.puzzles) or saved.get('elapsed', 0) >= room.minutes*60):
            if messagebox.askyesno('Nueva partida', 'Hay una partida terminada o sin tiempo. ¿Comenzar de nuevo?'):
                saved = None
            else:
                return
        self.game = MissionDirector(room, self.character, saved)
        self.show_game()

    def show_game(self):
        self.clear()
        game = self.game
        self.header(f'{game.character.name.upper()}    /    {game.room.title.upper()}')
        main = self.content()
        top = ctk.CTkFrame(main, fg_color='transparent')
        top.pack(fill='x', pady=(0, 13))
        self.btn(top, '←  VOLVER A LA NAVE', self.show_home, color='#283653', text_color='white', width=185).pack(side='left')
        self.timer_label = self.label(top, '', 17, GOLD, 'bold')
        self.timer_label.pack(side='right')
        self.label(main, 'EXPEDIENTE DE MISIÓN     /     TRANSMISIÓN IMPERIAL', 12, GOLD, 'bold').pack(anchor='w', pady=(4, 10))
        panels = ctk.CTkFrame(main, fg_color='transparent')
        panels.pack(fill='both', expand=True)
        panels.grid_columnconfigure(0, weight=5)
        panels.grid_columnconfigure(1, weight=6)
        story = ctk.CTkFrame(panels, fg_color='#111C31', corner_radius=18, border_width=1, border_color='#34455F')
        story.grid(row=0, column=0, sticky='nsew', padx=(0, 9))
        self.label(story, '◈  BITÁCORA DEL MORNING STAR', 12, GOLD, 'bold').pack(anchor='w', padx=20, pady=(24, 16))
        self.label(story, game.room.title, 23, 'white', 'bold', wraplength=390).pack(anchor='w', padx=20)
        self.label(story, game.room.description, 13, '#ADBFDA', wraplength=370, justify='left').pack(anchor='w', padx=20, pady=(10, 18))
        ctk.CTkFrame(story, height=2, fg_color='#394960').pack(fill='x', padx=20, pady=(0, 17))
        self.label(story, 'REGISTRO RECUPERADO', 12, GOLD, 'bold').pack(anchor='w', padx=20)
        self.narrative_label = self.label(story, '', 15, '#E6EAF7', wraplength=370, justify='left')
        self.narrative_label.pack(anchor='w', padx=20, pady=(12, 18))
        self.label(story, 'MENSAJE DE LA TRIPULACIÓN', 12, GOLD, 'bold').pack(anchor='w', padx=20, pady=(12, 4))
        self.dialogue_label = self.label(story, '', 13, '#B8A7EB', wraplength=370, justify='left')
        self.dialogue_label.pack(anchor='w', padx=20, pady=(8, 25))
        terminal = ctk.CTkFrame(panels, fg_color='#18243B', corner_radius=18, border_width=1, border_color='#4C5D83')
        terminal.grid(row=0, column=1, sticky='nsew', padx=(9, 0))
        self.step_label = self.label(terminal, '', 12, GOLD, 'bold')
        self.step_label.pack(anchor='w', padx=22, pady=(25, 10))
        self.puzzle_title = self.label(terminal, '', 25, 'white', 'bold', wraplength=430)
        self.puzzle_title.pack(anchor='w', padx=22)
        self.label(terminal, 'PROTOCOLO DE SEGURIDAD', 11, '#86DADB', 'bold').pack(anchor='w', padx=22, pady=(24, 7))
        self.question_label = self.label(terminal, '', 16, '#F0F2FA', 'bold', wraplength=420, justify='left')
        self.question_label.pack(anchor='w', padx=22, pady=(5, 21))
        self.answer_entry = ctk.CTkEntry(terminal, height=47, placeholder_text='Introduce el código o respuesta', fg_color='#0D1528', border_color='#54719A')
        self.answer_entry.pack(fill='x', padx=22)
        self.answer_entry.bind('<Return>', lambda _event: self.submit_answer())
        self.btn(terminal, 'VERIFICAR ACCESO  →', self.submit_answer).pack(fill='x', padx=22, pady=(14, 7))
        self.btn(terminal, '◈  CONSULTAR PISTA', self.show_hint, color='#334465', text_color='white').pack(fill='x', padx=22, pady=5)
        self.feedback = self.label(terminal, '', 13, GOLD, wraplength=420, justify='left')
        self.feedback.pack(anchor='w', padx=22, pady=(14, 25))
        lower = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=14)
        lower.pack(fill='x', pady=(18, 5))
        self.btn(lower, '← ANTERIOR', self.go_previous, color='#32415F', text_color='white', width=150).pack(side='left', padx=15, pady=15)
        self.btn(lower, 'SIGUIENTE →', self.go_next, width=150).pack(side='right', padx=15, pady=15)
        center = ctk.CTkFrame(lower, fg_color='transparent')
        center.pack(side='left', fill='both', expand=True, padx=8)
        self.progress_label = self.label(center, '', 12, '#B8C9E3', 'bold')
        self.progress_label.pack(pady=(16, 6))
        self.progress_bar = ctk.CTkProgressBar(center, progress_color=GOLD, height=7)
        self.progress_bar.pack(fill='x', pady=(0, 17))
        self.refresh_game()
        self.tick()

    def refresh_game(self):
        game = self.game
        puzzle = game.puzzle
        count = len(game.chain)
        self.progress_label.configure(text=f'ESTACIONES DESCIFRADAS   {len(game.solved)} / {count}')
        self.progress_bar.set(len(game.solved) / max(1, count))
        self.step_label.configure(text=f'TERMINAL  {game.current+1:02} / {count:02}     ·     {puzzle.category.upper()}')
        self.puzzle_title.configure(text=puzzle.title)
        self.narrative_label.configure(text=puzzle.narrative)
        self.dialogue_label.configure(text=f'{game.character.name}: «{game.character.greeting}»')
        self.question_label.configure(text=puzzle.question)
        self.answer_entry.delete(0, 'end')
        self.feedback.configure(text='✓ Terminal descifrada. Puedes continuar.' if puzzle.id in game.solved else '')
        self.answer_entry.focus_set()

    def submit_answer(self):
        if self.game.expired:
            messagebox.showwarning('Tiempo agotado', 'Se agotó el tiempo de esta misión.')
            return
        correct = self.game.answer(self.answer_entry.get())
        self.feedback.configure(text='✓ Respuesta correcta. La ruta está desbloqueada.' if correct else '✗ Código incorrecto. Vuelve a intentarlo.')
        self.save_progress()
        self.progress_label.configure(text=f'PROGRESO · {len(self.game.solved)}/{len(self.game.chain)} acertijos completados')
        self.progress_bar.set(len(self.game.solved) / max(1, len(self.game.chain)))
        if correct and self.game.completed:
            messagebox.showinfo('MISIÓN COMPLETA', f'¡{self.game.character.name} completó {self.game.room.title}!\nTiempo: {self.game.elapsed//60:02}:{self.game.elapsed%60:02}\nPistas consultadas: {len(self.game.hints_used)}\nAhora puedes recorrer el circuito circular completo.')

    def show_hint(self):
        if self.game.expired:
            return
        self.feedback.configure(text=self.game.hint())
        self.save_progress()

    def go_next(self):
        if self.game.next():
            self.refresh_game()
            self.save_progress()
        else:
            self.feedback.configure(text='Resuelve esta estación para avanzar. El circuito se cierra al completar la misión.')

    def go_previous(self):
        if self.game.previous():
            self.refresh_game()
            self.save_progress()
        else:
            self.feedback.configure(text='No hay una estación anterior desbloqueada. Tras completar la misión, la navegación será circular.')

    def tick(self):
        game = self.game
        remaining = max(0, game.room.minutes * 60 - game.elapsed)
        self.timer_label.configure(text=f'TIEMPO · {remaining//60:02}:{remaining%60:02}' if not game.completed else f'COMPLETADA · {game.elapsed//60:02}:{game.elapsed%60:02}')
        if game.expired:
            self.feedback.configure(text='Tiempo agotado. Regresa al menú para reiniciar la misión.')
        if not game.completed and not game.expired:
            self._timer_job = self.after(1000, self.tick)
        else:
            self._timer_job = None

    def show_admin(self):
        self.save_progress()
        self.clear()
        self.header('PANEL DE ADMINISTRACIÓN // EDICIÓN LOCAL')
        main = self.content()
        self.btn(main, '← MENÚ PRINCIPAL', self.show_home, color='#394665', text_color='white', width=185).pack(anchor='w', pady=(0, 16))
        self.label(main, 'Gestión de expedientes y estaciones', 26, 'white', 'bold').pack(anchor='w', pady=8)
        self.label(main, 'Los cambios se guardan en tu equipo. Cada sala tiene una lista circular doble independiente.', 13, '#BFC8DF').pack(anchor='w', pady=(0, 16))
        line = ctk.CTkFrame(main, fg_color='transparent')
        line.pack(fill='x', pady=5)
        self.room_var = tk.StringVar(value=self.rooms[0].id if self.rooms else '')
        self.room_menu = ctk.CTkOptionMenu(line, values=[r.id for r in self.rooms] or ['—'], variable=self.room_var,
                                            command=lambda _: self._render_admin_list(), width=250)
        self.room_menu.pack(side='left', padx=(0, 12))
        self.btn(line, '+ NUEVA SALA', self.add_room, width=155).pack(side='left', padx=5)
        self.btn(line, 'EDITAR SALA', self.edit_room, color='#415075', text_color='white', width=155).pack(side='left', padx=5)
        self.btn(line, 'BORRAR SALA', self.delete_room, color='#713D55', text_color='white', width=155).pack(side='left', padx=5)
        self.admin_list = ctk.CTkFrame(main, fg_color='transparent')
        self.admin_list.pack(fill='x', pady=12)
        self._render_admin_list()

    def chosen_room(self):
        return next((r for r in self.rooms if r.id == self.room_var.get()), None)

    def _render_admin_list(self):
        for child in self.admin_list.winfo_children():
            child.destroy()
        room = self.chosen_room()
        if not room:
            self.label(self.admin_list, 'Crea una sala para comenzar.', 14).pack(anchor='w')
            return
        chain = MissionArchitect.chain(room)
        status = 'CIRCUITO ÍNTEGRO ✓' if chain.validate_links() else 'ERROR DE ENLACES'
        self.label(self.admin_list, f'{room.title} · {len(chain)} estaciones · {status}', 17, GOLD, 'bold').pack(anchor='w', pady=10)
        for index, puzzle in enumerate(chain):
            line = ctk.CTkFrame(self.admin_list, fg_color=PANEL)
            line.pack(fill='x', pady=4)
            self.label(line, f'{index+1:02} · {puzzle.title} — {puzzle.category}', 14).pack(side='left', padx=14, pady=13)
            self.btn(line, 'BORRAR', lambda i=index: self.delete_puzzle(i), color='#713D55', text_color='white', width=80).pack(side='right', padx=5)
            self.btn(line, 'EDITAR', lambda i=index: self.edit_puzzle(i), color='#415075', text_color='white', width=80).pack(side='right', padx=5)
        self.btn(self.admin_list, '+ AÑADIR ACERTIJO', self.add_puzzle, width=210).pack(anchor='w', pady=15)
        self.label(self.admin_list, 'Los enlaces último ↔ primero se mantienen también después de insertar o borrar.', 12, '#98A7C1').pack(anchor='w')

    def _ask(self, title, label, initial=''):
        return simpledialog.askstring(title, label, initialvalue=initial, parent=self)

    def _room_inputs(self, room=None):
        title = self._ask('Sala', 'Título de la sala:', room.title if room else '')
        if title is None: return None
        description = self._ask('Sala', 'Descripción:', room.description if room else '')
        if description is None: return None
        difficulty = self._ask('Sala', 'Dificultad:', room.difficulty if room else 'Media')
        if difficulty is None: return None
        minutes = simpledialog.askinteger('Sala', 'Tiempo límite en minutos:', initialvalue=room.minutes if room else 15,
                                           minvalue=1, maxvalue=240, parent=self)
        if minutes is None: return None
        if not title.strip():
            messagebox.showerror('Validación', 'El título no puede estar vacío.')
            return None
        return title.strip(), description.strip(), difficulty.strip(), minutes

    def add_room(self):
        values = self._room_inputs()
        if not values: return
        import uuid
        room = OdysseyMission(str(uuid.uuid4())[:8], *values, [])
        self.rooms.append(room)
        self._save_admin(room.id)

    def edit_room(self):
        room = self.chosen_room()
        if not room: return
        values = self._room_inputs(room)
        if not values: return
        room.title, room.description, room.difficulty, room.minutes = values
        self._save_admin(room.id)

    def delete_room(self):
        room = self.chosen_room()
        if room and messagebox.askyesno('Borrar sala', f'¿Eliminar «{room.title}» y todos sus acertijos?'):
            self.rooms.remove(room)
            self._save_admin(self.rooms[0].id if self.rooms else '')

    def _puzzle_inputs(self, puzzle=None):
        fields = [('Título', 'title'), ('Contexto narrativo', 'narrative'), ('Pregunta', 'question'),
                  ('Respuesta correcta', 'answer'), ('Pista', 'hint'), ('Categoría', 'category')]
        values = {}
        for label, key in fields:
            value = self._ask('Editar acertijo', label + ':', getattr(puzzle, key, '') if puzzle else ('Código' if key == 'category' else ''))
            if value is None: return None
            values[key] = value.strip()
        if not values['title'] or not values['question'] or not values['answer']:
            messagebox.showerror('Validación', 'Título, pregunta y respuesta son obligatorios.')
            return None
        return values

    def add_puzzle(self):
        room = self.chosen_room()
        if not room: return
        values = self._puzzle_inputs()
        if not values: return
        position = simpledialog.askinteger('Posición', f'Insertar en posición (1 a {len(room.puzzles)+1}):',
                                            initialvalue=len(room.puzzles)+1, minvalue=1, maxvalue=len(room.puzzles)+1, parent=self)
        if position is None: return
        try:
            MissionArchitect.insert(room, position-1, MissionArchitect.make_puzzle(**values))
            self._save_admin(room.id)
        except ValueError as exc:
            messagebox.showerror('Validación', str(exc))

    def edit_puzzle(self, index):
        room = self.chosen_room()
        puzzle = room.puzzles[index]
        values = self._puzzle_inputs(puzzle)
        if not values: return
        from models.odyssey_riddle import OdysseyRiddle
        try:
            MissionArchitect.update(room, index, OdysseyRiddle(id=puzzle.id, **values))
            self._save_admin(room.id)
        except ValueError as exc:
            messagebox.showerror('Validación', str(exc))

    def delete_puzzle(self, index):
        room = self.chosen_room()
        if messagebox.askyesno('Borrar acertijo', f'¿Eliminar «{room.puzzles[index].title}»?'):
            MissionArchitect.delete(room, index)
            self._save_admin(room.id)

    def _save_admin(self, selected_id):
        try:
            self.repo.save(self.rooms)
        except (OSError, ValueError) as exc:
            messagebox.showerror('Error al guardar', str(exc))
            self.rooms = self.repo.load()
            self.show_admin()
            return
        self.room_menu.configure(values=[r.id for r in self.rooms] or ['—'])
        self.room_var.set(selected_id or '—')
        self._render_admin_list()
