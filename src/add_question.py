import sqlite3

import flet as ft


def add_question(page: ft.Page, conn: sqlite3.Connection):
    # SQLite Conn
    cur = conn.cursor()

    # Add Questions Tab
    question_input = ft.TextField(hint_text="Enter Question", width=600)
    correct_input = ft.TextField(hint_text="Enter Correct Answer", width=600)
    wrong_input1 = ft.TextField(hint_text="Enter First Wrong Answer", width=600)
    wrong_input2 = ft.TextField(hint_text="Enter Second Wrong Answer", width=600)
    wrong_input3 = ft.TextField(hint_text="Enter Third Wrong Answer", width=600)

    warning_text1 = ft.Text("")
    success_text1 = ft.Text("Successfully added Question")
    success_text1.visible = False

    def add_question(e):
        success_text1.visible = False
        sql = """
            INSERT INTO questions (question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3)
            VALUES (?, ?, ?, ?, ?);
        """
        if (
            question_input.value
            and correct_input.value
            and wrong_input1.value
            and wrong_input2.value
            and wrong_input3.value
        ):
            warning_text1.value = ""
            page.update()
            cur.execute(
                sql,
                (
                    question_input.value,
                    correct_input.value,
                    wrong_input1.value,
                    wrong_input2.value,
                    wrong_input3.value,
                ),
            )
            conn.commit()
            question_input.value = ""
            correct_input.value = ""
            wrong_input1.value = ""
            wrong_input2.value = ""
            wrong_input3.value = ""
            success_text1.visible = True
            page.update()
        else:
            warning_text1.value = "Please fill out all fields"
            page.update()

    add_button = ft.ElevatedButton("Add Question", on_click=add_question)

    add_question_tab = ft.Tab(
        "Add Question",
        content=ft.Column(
            [
                question_input,
                correct_input,
                wrong_input1,
                wrong_input2,
                wrong_input3,
                add_button,
                warning_text1,
                success_text1,
            ]
        ),
    )

    return add_question_tab
