import sqlite3

import flet as ft


def add_question(page: ft.Page, conn: sqlite3.Connection):
    # SQLite Conn
    cur = conn.cursor()

    # Add Questions Tab
    question_input = ft.TextField(hint_text="Enter Question", width=600)
    correct_input = ft.TextField(hint_text="Enter Correct Answer", width=600)

    warning_text1 = ft.Text("")
    success_text1 = ft.Text("Successfully added Question")
    success_text1.visible = False

    def add_question(e):
        success_text1.visible = False
        sql = """
            INSERT INTO questions (question, correct_answer)
            VALUES (?, ?);
        """
        if question_input.value and correct_input.value:
            warning_text1.value = ""
            page.update()
            cur.execute(
                sql,
                (
                    question_input.value,
                    correct_input.value,
                ),
            )
            conn.commit()
            question_input.value = ""
            correct_input.value = ""
            success_text1.visible = True
            page.update()
        else:
            warning_text1.value = "Please fill out all fields"
            page.update()

    add_button = ft.ElevatedButton("Add Question", on_click=add_question)

    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        padding=40,
        content=ft.Container(
            width=600,
            content=ft.Column(
                controls=[
                    question_input,
                    correct_input,
                    add_button,
                    warning_text1,
                    success_text1,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
        ),
    )
