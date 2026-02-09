import random
import sqlite3

import flet as ft


def study(page: ft.Page, conn: sqlite3.Connection):
    cur = conn.cursor()

    correct_value = None
    index = 0
    qs = []
    q_count = 0

    # Radio options
    options = [ft.Radio(label="", value="") for _ in range(4)]

    question = ft.Text(visible=False)
    choices = ft.RadioGroup(content=ft.Column(options), visible=False)
    correctness = ft.Text("", visible=False)

    end_text = ft.Text("All Questions Completed!", visible=False)
    empty_warning = ft.Text("Studying requires at least 4 questions", visible=False)

    check_answer_button = ft.ElevatedButton("Check Answer", visible=False)
    next_button = ft.ElevatedButton("Next Question", visible=False)

    def reset_ui():
        choices.value = None
        correctness.value = ""
        correctness.visible = False
        next_button.visible = False
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
        check_answer_button.visible = True
        begin_button.visible = False

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

    def check_answer(e):
        if choices.value is None:
            correctness.value = "Pick an answer first"
            correctness.visible = True
            page.update()
            return

        correctness.visible = True
        if choices.value == correct_value:
            correctness.value = "Correct!"
            next_button.visible = True
        else:
            correctness.value = "Incorrect"
            next_button.visible = False

        page.update()

    def next_question(e):
        if index < q_count:
            reset_ui()
            load_question()
        else:
            question.visible = False
            choices.visible = False
            check_answer_button.visible = False
            next_button.visible = False
            correctness.visible = False
            end_text.visible = True

        page.update()

    begin_button = ft.ElevatedButton("Study", on_click=begin_quiz)
    check_answer_button.on_click = check_answer
    next_button.on_click = next_question

    study_tab = ft.Tab(
        text="Study",
        content=ft.Column(
            [
                begin_button,
                empty_warning,
                question,
                choices,
                check_answer_button,
                correctness,
                next_button,
                end_text,
            ]
        ),
    )
    return study_tab.content
