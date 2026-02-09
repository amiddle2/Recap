import random
import sqlite3

import flet as ft


def quiz(page: ft.Page, conn: sqlite3.Connection):

    cur = conn.cursor()

    correct_value = None

    option1 = ft.Radio(label="", value="")
    option2 = ft.Radio(label="", value="")
    option3 = ft.Radio(label="", value="")
    option4 = ft.Radio(label="", value="")

    options = [option1, option2, option3, option4]

    question = ft.Text()
    choices = ft.RadioGroup(content=ft.Column(options))
    correctness = ft.Text("")
    end_text = ft.Text("Quiz Complete!")
    end_text.visible = False

    question.visible = False
    choices.visible = False
    check_answer_button = ft.ElevatedButton("Check Answer")
    check_answer_button.visible = False
    next_button = ft.ElevatedButton("Next Question")
    next_button.visible = False
    empty_warning = ft.Text("No Questions Made")
    empty_warning.visible = False
    page.update()
    index = 0
    q_count = None
    qs = None

    def begin_quiz(e):
        nonlocal q_count, qs, index
        correct_value = None
        index = 0

        cur.execute(
            "SELECT question, correct_answer, wrong_answer1, wrong_answer2, wrong_answer3 FROM questions"
        )
        questions = cur.fetchall()
        question_count = len(questions)
        qs = questions
        q_count = question_count
        if question_count > 0:
            end_text.visible = False
            correctness.visible = False
            next_button.visible = False
            begin_button.visible = False
            question.visible = True
            choices.visible = True
            check_answer_button.visible = True
            empty_warning.visible = False
            page.update()
            load_question()
        else:
            empty_warning.visible = True
            page.update()

    def load_question():
        nonlocal index, correct_value, qs
        q, c, w1, w2, w3 = qs[index]

        question.value = q
        answers = [(c, True), (w1, False), (w2, False), (w3, False)]

        random.shuffle(answers)

        for i, (text, is_correct) in enumerate(answers):
            options[i].label = text
            options[i].value = text

            if is_correct:
                correct_value = text

        choices.value = None
        page.update()
        index += 1

    def check_answer(e):
        correctness.visible = True
        if choices.value is None:
            return

        if choices.value == correct_value:
            correctness.value = "Correct!"
            next_button.visible = True
        else:
            correctness.value = "Incorrect"
            next_button.visible = False
        page.update()

    def next_question(e):
        nonlocal index
        if index < q_count:
            # Next question
            load_question()
            next_button.visible = False
            correctness.visible = False
        else:
            # No more questions
            question.visible = False
            choices.visible = False
            correctness.visible = False
            next_button.visible = False
            check_answer_button.visible = False
            end_text.visible = True
        page.update()

    check_answer_button.on_click = check_answer
    next_button.on_click = next_question
    begin_button = ft.ElevatedButton("Begin Quiz", on_click=begin_quiz)

    quiz_tab = ft.Tab(
        "Quiz",
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

    return quiz_tab
