import sqlite3

import flet as ft


def flashcards(page: ft.Page, conn: sqlite3.Connection):
    cur = conn.cursor()

    fc_index = 0
    cur.execute("SELECT COUNT(*) FROM questions")
    card_count = cur.fetchall()[0][0]
    fc_warning = ft.Text()

    cur.execute("SELECT question, correct_answer FROM questions")
    cards = cur.fetchall()

    flashcard = ft.Card(
        content=ft.Container(
            width=600,
            height=400,
            padding=20,
            alignment=ft.alignment.center,
            content=ft.Text(
                value="" if card_count == 0 else cards[fc_index][0],
                size=24,
                text_align=ft.TextAlign.CENTER,
            ),
        ),
    )

    def update_card():
        nonlocal card_count
        flashcard.content.content.value = cards[fc_index][0] if card_count != 0 else ""
        page.update()

    def flip_card(e):
        nonlocal fc_index, cards
        question = cards[fc_index][0]
        answer = cards[fc_index][1]
        if flashcard.content.content.value == question:
            flashcard.content.content.value = answer
        elif flashcard.content.content.value == answer:
            flashcard.content.content.value = question
        else:
            flashcard.content.content.value = "Error: Card not Found"
        page.update()

    def next_card(e):
        nonlocal fc_index, card_count
        if fc_index < card_count - 1:
            fc_index += 1
            update_card()
        else:
            flashcard.visible = False
            fc_warning.visible = True
            fc_warning.value = "Flashcards Completed!"
            flip_button.visible = False
            next_card_button.visible = False
            restart_cards_button.visible = True
            page.update()

    def restart_cards(e):
        nonlocal fc_index
        fc_index = 0
        flashcard.visible = True
        fc_warning.visible = False
        flip_button.visible = True
        next_card_button.visible = True
        restart_cards_button.visible = False
        update_card()

    flip_button = ft.ElevatedButton("Flip Card", on_click=flip_card)
    next_card_button = ft.ElevatedButton("Next Card", on_click=next_card)
    restart_cards_button = ft.ElevatedButton("Restart", on_click=restart_cards)
    restart_cards_button.visible = False

    flashcards_tab = ft.Tab(
        "Flashcards",
        content=ft.Column(
            [
                ft.Container(height=50),
                flashcard,
                flip_button,
                next_card_button,
                fc_warning,
                restart_cards_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    return flashcards_tab.content
