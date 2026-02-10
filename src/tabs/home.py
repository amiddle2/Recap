import flet as ft


def home():
    greeting_text = ft.Text("Welcome to Recap!")
    explanation_text = ft.Text(
        "Here you can create and edit questions, and quiz yourself with questions or flashcards!"
    )

    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        padding=40,
        content=ft.Container(
            width=600,
            content=ft.Column(
                controls=[
                    greeting_text,
                    explanation_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
        ),
    )
