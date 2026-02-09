import sqlite3

import flet as ft


def edit_questions(page: ft.Page, conn: sqlite3.Connection):
    cur = conn.cursor()

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
            sql = "SELECT question FROM questions WHERE question LIKE ?"
            search_term = f"%{question_search.value}%"

            cur.execute(sql, (search_term,))
            questions = cur.fetchall()

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
        if update_question.value:
            cur.execute(
                "UPDATE questions SET question = ? WHERE question = ?",
                (update_question.value, dropdown.value),
            )
        if update_correct.value:
            cur.execute(
                "UPDATE questions SET correct_answer = ? WHERE question = ?",
                (update_correct.value, dropdown.value),
            )

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
        conn.commit()

    delete_message = ft.Text()

    def delete_question(e):
        if not dropdown.value:
            return

        sql = "DELETE FROM questions WHERE question = ?"
        cur.execute(sql, (dropdown.value,))
        conn.commit()
        delete_message.value = "Question Successfully Deleted"
        page.update()

    delete_button = ft.ElevatedButton("Delete Question", on_click=delete_question)
    delete_button.visible = False

    edit_button.text = "Confirm Changes"
    edit_button.on_click = edit_question

    edit_questions_tab = ft.Tab(
        "Edit Questions",
        content=ft.Column(
            [
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
            ]
        ),
    )

    return edit_questions_tab.content
