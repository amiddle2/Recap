import flet as ft
import sqlalchemy.orm as orm

from src.tables.question import Questions


def add_question(page: ft.Page, db: orm.Session):

    # Add Questions Tab
    question_input = ft.TextField(hint_text="Enter Question", width=600)
    correct_input = ft.TextField(hint_text="Enter Correct Answer", width=600)

    warning_text1 = ft.Text("")
    success_text1 = ft.Text("Successfully added Question")
    success_text1.visible = False

    def add_question(e):
        success_text1.visible = False
        if question_input.value and correct_input.value:
            warning_text1.value = ""
            page.update()
            new_question = Questions(
                question=question_input.value, correct_answer=correct_input.value
            )
            db.add(new_question)
            db.commit()
            db.refresh(new_question)
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
