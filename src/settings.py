import flet as ft


def settings(page: ft.Page):
    def toggle_dark_mode(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if dark_mode_switch.value else ft.ThemeMode.LIGHT
        )
        page.update()

    dark_mode_switch = ft.Switch(
        label="Dark Mode", value=False, on_change=toggle_dark_mode
    )

    settings_tab = ft.Tab(content=ft.Column([dark_mode_switch]))

    return settings_tab.content
