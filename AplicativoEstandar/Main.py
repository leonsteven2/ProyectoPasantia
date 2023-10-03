import flet
from flet import Page, Container, app
from LoginInterface import LoginInterface

def main(page: Page):
    def route_change(route):
        page.views.clear()
        print("Cambio de ruta")

        if page.route == "/login":
            page.views.append(
                flet.View(
                    "/",
                    [
                        Container(
                            expand=True,
                            content=row_login_interface
                        )
                    ]

                )
            )
        if page.route == "/dashboard":  # and login_interface.login_successful:
            page.views.append(
                flet.View(
                    "/dashboard",
                    [
                        Container(
                            width=100,
                            height=100,
                            bgcolor="red"
                        )
                    ]
                )
            )

        page.update()

    page.title = "Aplicativo General"
    page.window_maximized = True
    page.window_left = 1000
    page.window_min_width = 1200
    page.window_min_height = 700
    #page.theme_mode = flet.ThemeMode.LIGHT

    page.on_route_change = route_change

    # Creamos la interfaz de login
    row_login_interface = LoginInterface(page=page)
    page.go("/login")


app(target=main, assets_dir="assets")