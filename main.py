from pathlib import Path
import sqlite3

import flet as ft
from src.add_question import add_question
from src.edit_questions import edit_questions
from src.flashcards import flashcards
from src.quiz import quiz

# Create a database file in the user's home directory
DB_PATH = Path.home() / ".recap" / "recap.db"

# Ensure the directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def main(page: ft.Page):
    page.title = "Recap"
    conn = sqlite3.connect(DB_PATH)
    add_question_tab = add_question(page, conn)
    edit_questions_tab = edit_questions(page, conn)
    flashcards_tab = flashcards(page, conn)
    quiz_tab = quiz(page, conn)
    tabs = ft.Tabs(
        tabs=[add_question_tab, edit_questions_tab, flashcards_tab, quiz_tab],
    )

    page.add(tabs)


ft.app(main)
