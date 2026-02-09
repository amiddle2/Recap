import sqlite3
from pathlib import Path

import flet as ft
import platformdirs

from src.add_question import add_question
from src.edit_questions import edit_questions
from src.flashcards import flashcards
from src.home import home
from src.study import study

# Get user-specific data directory
data_dir = Path(platformdirs.user_data_dir("Recap", "YourCompanyName"))
data_dir.mkdir(parents=True, exist_ok=True)

DB_PATH = data_dir / "recap.db"


def main(page: ft.Page):
    page.title = "Recap"
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        correct_answer TEXT NOT NULL
        );
        """
    )
    conn.commit()

    tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Home", content=home()),
            ft.Tab(text="Add", content=ft.Container()),
            ft.Tab(text="Edit", content=ft.Container()),
            ft.Tab(text="Flashcards", content=ft.Container()),
            ft.Tab(text="Study", content=ft.Container()),
        ],
        expand=True,
    )

    def on_tab_change(e):
        idx = tabs.selected_index
        if idx == 0:
            tabs.tabs[0].content = home()
        elif idx == 1:
            tabs.tabs[1].content = add_question(page, conn)
        elif idx == 2:
            tabs.tabs[2].content = edit_questions(page, conn)
        elif idx == 3:
            tabs.tabs[3].content = flashcards(page, conn)
        elif idx == 4:
            tabs.tabs[4].content = study(page, conn)
        tabs.update()

    # Attach the event handler
    tabs.on_change = on_tab_change

    page.add(tabs)


ft.app(main)
