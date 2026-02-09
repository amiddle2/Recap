import sqlite3
from pathlib import Path

import flet as ft
import platformdirs

from src.add_question import add_question
from src.edit_questions import edit_questions
from src.flashcards import flashcards
from src.quiz import quiz

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
        correct_answer TEXT NOT NULL,
        wrong_answer1 TEXT NOT NULL,
        wrong_answer2 TEXT NOT NULL,
        wrong_answer3 TEXT NOT NULL
        );
        """
    )
    conn.commit()
    add_question_tab = add_question(page, conn)
    edit_questions_tab = edit_questions(page, conn)
    flashcards_tab = flashcards(page, conn)
    quiz_tab = quiz(page, conn)
    tabs = ft.Tabs(
        tabs=[add_question_tab, edit_questions_tab, flashcards_tab, quiz_tab],
    )

    page.add(tabs)


ft.app(main)
