import flet as ft
import sqlalchemy.orm as orm

from src.tables.question import Questions


def edit_questions(page: ft.Page, db: orm.Session):

    question_search = ft.TextField(hint_text="Search for a question", width=600)
    warning_text2 = ft.Text("")
    dropdown = ft.Dropdown(value="", width=600)
    dropdown.visible = False
    warning_text3 = ft.Text("")

    update_question = ft.TextField(hint_text="New Question", width=600)
    update_correct = ft.TextField(hint_text="New Correct Answer", width=600)

    update_question.visible = False
    update_correct.visible = False

    edit_button = ft.ElevatedButton()
    edit_button.visible = False
    page.update()

    def search_questions(e):
        if question_search.value:
            search_term = f"%{question_search.value}%"

            questions = (
                db.query(Questions.question)
                .filter(Questions.question.like(search_term))
                .all()
            )

            if questions:
                dropdown.options = [ft.dropdown.Option(q[0]) for q in questions]
                dropdown.visible = True
                dropdown.value = dropdown.options[0].key
                warning_text2.value = ""

                update_question.visible = True
                update_correct.visible = True

                edit_button.visible = True
                delete_button.visible = True
            else:
                dropdown.options = []
                warning_text2.value = "No questions found that match your search"
        else:
            dropdown.options = []
            warning_text2.value = "Please enter a search term"

        page.update()

    search_button = ft.ElevatedButton("Search", on_click=search_questions)

    def edit_question(e):
        if dropdown.value:
            question_obj = (
                db.query(Questions).filter(Questions.question == dropdown.value).first()
            )

            if question_obj:
                if update_question.value:
                    question_obj.question = update_question.value

                if update_correct.value:
                    question_obj.correct_answer = update_correct.value

                db.commit()
                db.refresh(question_obj)

        if not any(
            val
            for val in (
                update_question.value,
                update_correct.value,
            )
        ):
            warning_text3.value = "Please enter the value to be edited"
        else:
            warning_text3.value = "Question altered successfully"
        page.update()

    delete_message = ft.Text()

    def delete_question(e):
        if not dropdown.value:
            return

        question_obj = (
            db.query(Questions).filter(Questions.question == dropdown.value).first()
        )

        if question_obj:
            db.delete(question_obj)
            db.commit()

            delete_message.value = "Question Successfully Deleted"
            page.update()

    delete_button = ft.ElevatedButton("Delete Question", on_click=delete_question)
    delete_button.visible = False

    edit_button.text = "Confirm Changes"
    edit_button.on_click = edit_question

    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        padding=40,
        content=ft.Container(
            width=600,
            content=ft.Column(
                controls=[
                    question_search,
                    dropdown,
                    search_button,
                    warning_text2,
                    update_question,
                    update_correct,
                    warning_text3,
                    edit_button,
                    delete_button,
                    delete_message,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
        ),
    )
