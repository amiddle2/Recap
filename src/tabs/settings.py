import json

import flet as ft

SETTINGS_FILE = r"C:\Users\dmiddleton\Projects\Recap\src\utils\settings.json"


def settings(page: ft.Page):
    with open(SETTINGS_FILE, "r") as file:
        data = json.load(file)
        dark_mode_initial = data["settings"].get("dark_mode", False)

    dark_mode_switch = ft.Switch(label="Dark Mode", value=dark_mode_initial)

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if dark_mode_switch.value else ft.ThemeMode.LIGHT
        )
        page.update()

    dark_mode_switch.on_change = toggle_theme

    def save_settings(e):
        data["settings"]["dark_mode"] = dark_mode_switch.value
        with open(SETTINGS_FILE, "w") as file:
            json.dump(data, file, indent=4)
        save_notif.visible = True
        page.update()

    save_button = ft.ElevatedButton("Save Settings", on_click=save_settings)

    save_notif = ft.Text("Settings saved successfully!")
    save_notif.visible = False

    page.theme_mode = ft.ThemeMode.DARK if dark_mode_initial else ft.ThemeMode.LIGHT

    return ft.Container(
        expand=True,
        padding=40,
        content=ft.Container(
            width=600,
            content=ft.Column(
                controls=[dark_mode_switch, save_button, save_notif],
                spacing=20,
            ),
        ),
    )
