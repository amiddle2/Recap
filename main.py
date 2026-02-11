from pathlib import Path

import flet as ft
import platformdirs

from src.core.database import init_db
from src.tabs.add_question import add_question
from src.tabs.edit_questions import edit_questions
from src.tabs.flashcards import flashcards
from src.tabs.home import home
from src.tabs.quiz import quiz
from src.tabs.settings import settings
from src.tabs.study import study

# Get user-specific data directory
data_dir = Path(platformdirs.user_data_dir("Recap", "YourCompanyName"))
data_dir.mkdir(parents=True, exist_ok=True)

DB_PATH = data_dir / "recap.db"


def main(page: ft.Page):
    page.title = "Recap"
    Session = init_db(DB_PATH)
    db = Session()

    tabs = ft.Tabs(
        tabs=[
            ft.Tab(text="Home", content=home()),
            ft.Tab(text="Add Questions", content=ft.Container()),
            ft.Tab(text="Edit Questions", content=ft.Container()),
            ft.Tab(text="Flashcards", content=ft.Container()),
            ft.Tab(text="Study", content=ft.Container()),
            ft.Tab(text="Quiz", content=ft.Container()),
            ft.Tab(text="Settings", content=settings(page)),
        ],
        expand=True,
    )

    def on_tab_change(e):
        idx = tabs.selected_index
        match idx:
            case 0:
                tabs.tabs[idx].content = home()
            case 1:
                tabs.tabs[idx].content = add_question(page, db)
            case 2:
                tabs.tabs[idx].content = edit_questions(page, db)
            case 3:
                tabs.tabs[idx].content = flashcards(page, db)
            case 4:
                tabs.tabs[idx].content = study(page, db)
            case 5:
                tabs.tabs[idx].content = quiz(page, db)
            case 6:
                tabs.tabs[idx].content = settings(page)

        tabs.update()

    # Attach the event handler
    tabs.on_change = on_tab_change

    page.add(tabs)


ft.app(main)
