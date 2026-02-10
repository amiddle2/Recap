import random
import sqlite3

import flet as ft


def quiz(page: ft.Page, conn: sqlite3.Connection):
    cur = conn.cursor()

    correct_value = None
    index = 0
    qs = []
    q_count = 0
    correct_answers = 0

    # Radio options
    options = [ft.Radio(label="", value="") for _ in range(4)]

    question = ft.Text(visible=False)
    choices = ft.RadioGroup(content=ft.Column(options), visible=False)

    end_text = ft.Text("Quiz Completed!", visible=False)
    empty_warning = ft.Text("Quiz requires at least 4 questions", visible=False)

    next_button = ft.ElevatedButton("Next Question", visible=False)
    warning_text = ft.Text("Please select an answer before proceeding", visible=False)

    score_text = ft.Text()
    score_text.visible = False

    def reset_ui():
        choices.value = None
        end_text.visible = False

    def begin_quiz(e):
        nonlocal qs, q_count, index
        index = 0

        cur.execute("SELECT question, correct_answer FROM questions")
        qs = cur.fetchall()
        q_count = len(qs)

        if q_count < 4:
            empty_warning.visible = True
            page.update()
            return

        empty_warning.visible = False
        question.visible = True
        choices.visible = True
        begin_button.visible = False
        next_button.visible = True

        reset_ui()
        load_question()
        page.update()

    def load_question():
        nonlocal index, correct_value

        q, c = qs[index]
        index += 1

        # Get all possible answers
        cur.execute("SELECT correct_answer FROM questions")
        all_answers = [row[0] for row in cur.fetchall()]
        all_answers.remove(c)

        wrong_answers = random.sample(all_answers, 3)

        answers = [(c, True)] + [(w, False) for w in wrong_answers]
        random.shuffle(answers)

        question.value = q

        for i, (text, is_correct) in enumerate(answers):
            options[i].label = text
            options[i].value = text
            if is_correct:
                correct_value = text

        choices.value = None

    def check_answer():
        nonlocal correct_answers
        if choices.value == correct_value:
            correct_answers += 1

    def next_question(e):
        nonlocal correct_answers

        if not choices.value:
            warning_text.visible = True
            page.update()
            return
        warning_text.visible = False
        check_answer()

        if index < q_count:
            reset_ui()
            load_question()
        else:
            question.visible = False
            choices.visible = False
            next_button.visible = False
            end_text.visible = True
            score_text.visible = True
            percentage = correct_answers / q_count if q_count != 0 else 0
            score_text.value = f"Score: {(percentage * 100):.2f}%"

        page.update()

    begin_button = ft.ElevatedButton("Take Quiz", on_click=begin_quiz)
    next_button.on_click = next_question

    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        padding=40,
        content=ft.Container(
            width=600,
            content=ft.Column(
                controls=[
                    begin_button,
                    empty_warning,
                    question,
                    choices,
                    next_button,
                    end_text,
                    score_text,
                    warning_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
        ),
    )
