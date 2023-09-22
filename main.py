from time import sleep

import flet as ft


def main(page: ft.Page):

    page.add(
        ft.Text("Hello!")
    )

    sleep(3)
    page.window_visible = True
    page.update()

ft.app(target=main, view=ft.AppView.FLET_APP_HIDDEN)