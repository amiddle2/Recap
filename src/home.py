import flet as ft


def home():
    greeting_text = ft.Text("Welcome to Recap!")
    explanation_text = ft.Text(
        "Here you can create and edit questions, and quiz yourself with questions or flashcards!"
    )

    home_tab = ft.Tab(content=ft.Column([greeting_text, explanation_text]))

    return home_tab.content
