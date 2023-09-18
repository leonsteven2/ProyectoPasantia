import flet
from flet import AlertDialog, Icon, Page, NavigationRail, FloatingActionButton, NavigationRailDestination, padding, IconButton, TextStyle, FontWeight, TextAlign, colors, TextCapitalization, Theme, UserControl, Container, icons, ElevatedButton, SafeArea, Checkbox, Text, Column, TextField, Row, ImageFit, TextButton


def CajaTextoConIcono(label, src_image, password, icon):
    icon_caja = Icon(
        name=icon,
        color=colors.WHITE,
        size=30,
    )
    txt_caja = TextField(
                label=label,
                #height=50,
                expand=1,
                label_style=TextStyle(
                    color=colors.WHITE,
                    weight=FontWeight.BOLD,
                ),
                # text_align=TextAlign.JUSTIFY,
                text_style=TextStyle(
                    color=colors.AMBER,
                    weight=FontWeight.BOLD,
                ),
                border_radius=15,
                capitalization=TextCapitalization.CHARACTERS,
                password=password,
                can_reveal_password=password,
                border_color=colors.WHITE,
                bgcolor=colors.PINK_ACCENT_700,
                autofocus=True
            )
    return Row(controls=[icon_caja, txt_caja], expand=1)


class LoginInterface(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.cont_password_incorrect = 0
        self.dlg_modal_send_email = AlertDialog(
            modal=True,
            title=Text("Send New Password"),
            content=TextField(label="Email", suffix=Text("@gmail.com")),

            # Column(
            #     # controls=[
            #     #     Text("Ingrese su correo", size=15),
            #     #     # TextField(label="Email", suffix=Text("@gmail.com")),
            #     #     # Text("Se", size=15, color=colors.RED_500),
            #     #     # Text("ASD", size=15, color=colors.RED_500, text_align=flet.TextAlign.CENTER),
            #     # ]
            # ),
            actions=[
                TextButton("Send", on_click=self.close_dlg),
                TextButton("Close", on_click=self.close_dlg),
            ],
            actions_alignment=flet.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )

    def build(self):

        self.row_interfaz = Row(
            controls=[
                Container(
                    border_radius=15,
                    expand=2,
                    alignment=flet.alignment.center,
                    image_src=f'https://i.pinimg.com/originals/0e/b1/56/0eb15636563ecc2920056a5dd6e496c5.gif',
                    image_fit=ImageFit.COVER,
                ),
                Container(
                    border_radius=15,
                    gradient=flet.LinearGradient(
                        begin=flet.alignment.center,
                        end=flet.alignment.bottom_center,
                        colors=[colors.BLACK, colors.PINK_900]
                    ),
                    expand=1,
                    content=self.Container_Login_Password(),
                    alignment=flet.alignment.top_center
                )
            ],
            spacing=3,
        )
        return self.row_interfaz

    def Container_Login_Password(self):
        self.caja_username = CajaTextoConIcono(
                        label="Username",
                        src_image=f'https://cdn-icons-png.flaticon.com/128/6172/6172285.png',
                        password=False,
                        icon=icons.PERSON,
                    )
        self.caja_password = CajaTextoConIcono(
                        label="Password",
                        src_image=f'https://cdn-icons-png.flaticon.com/128/9397/9397489.png',
                        password=True,
                        icon=icons.SECURITY
                    )
        self.lbl_user_or_password_incorrect = Text(
            value="",
            color=colors.RED,
            size=17
        )
        container = Container(
            width=375,
            padding=20,
            content=Column(
                alignment=flet.MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    Text("Welcome Back Steven", size=30, color=colors.WHITE),
                    Row(
                        controls=[
                            flet.Image(
                                width=120,
                                height=120,
                                src=f"C:/Users/USER/Downloads/logonice (1).svg"),
                        ],
                        alignment=flet.MainAxisAlignment.CENTER
                    ),
                    Row([self.caja_username]),
                    Row([self.caja_password]),
                    Row(
                        alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                        spacing=30,
                        controls=[
                            Checkbox(label="Remember Password", expand=1),
                            TextButton(text="Forgot Password", width=120, on_click=self.open_dlg_modal)
                        ]
                    ),
                    Row(controls=[self.lbl_user_or_password_incorrect], alignment=flet.MainAxisAlignment.CENTER),
                    Row(
                        controls=[
                            ElevatedButton(
                                content=Text(value="Login", size=20),
                                expand=1,
                                color=colors.RED_ACCENT_700,
                                bgcolor=colors.WHITE,
                                style=flet.ButtonStyle(
                                    overlay_color=colors.BLACK,
                                    shape=flet.RoundedRectangleBorder(radius=10),
                                ),
                                on_click=self.user_and_password_validate,
                            )
                        ],
                    ),
                    Row(
                        alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text("Dont you have account?", expand=1.2, text_align=flet.TextAlign.CENTER),
                            TextButton(text="Create account here", width=145)
                        ]
                    ),

                ],

            ),
            alignment=flet.alignment.top_center,

        )
        return container

    def user_and_password_validate(self, e):
        self.caja_password.value = "123"
        self.caja_username.value = "ADMIN"
        if self.caja_password.value == "123" and self.caja_username.value =="ADMIN":
            self.login_successful = True
            self.page.go("/sensores")
        else:
            print("Datos de ingreso incorrectos")
            self.cont_password_incorrect += 1
            self.login_successful = False
            self.lbl_user_or_password_incorrect.value = f"Incorrect user or password ({self.cont_password_incorrect})"
            self.page.update(self)

    def send_email_to_recovery_password(self):
        pass

    def open_dlg_modal(self, e):
        print("Entra a open dlg modal")
        self.page.dialog = self.dlg_modal_send_email
        self.dlg_modal_send_email.open = True
        self.page.update()

    def close_dlg(self, e):
        self.dlg_modal_send_email.open = False
        self.page.update()


class MainInterface(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.contador_icon_main = 0
        self.container_home_page = HomePage(self.page, "Texto de prueba")
        self.container_customers_page = CustomersPage(self.page)
        # Agregamos un audio a la interfaz accionado por el IconButton de Música
        self.audio1 = flet.Audio(
            src="C:\\Users\\USER\Downloads\MUSICA.mp3"
        )
        self.page.overlay.append(self.audio1)

    def build(self):
        self.container_principal = Container(
            bgcolor=colors.BLACK,
            expand=10
        )
        self.icon_main = IconButton(
            icon=icons.MUSIC_NOTE_SHARP,
            icon_size=40,
            icon_color=colors.WHITE,
            width=60,
            on_click=self.change_color_icon
        )
        container = Container(
            alignment=flet.alignment.top_center,
            border_radius=15,
            content=Column(
                spacing=5,
                controls=[
                    Container(
                        # margin=margin.only(left=50),
                        padding=padding.only(right=15, left=15),
                        # bgcolor=colors.PINK_900,
                        gradient=flet.LinearGradient(
                            begin=flet.alignment.top_center,
                            end=flet.alignment.bottom_center,
                            colors=[colors.PINK_900, colors.BLACK]
                        ),
                        expand=1,
                        content=Row(
                            controls=[
                                self.icon_main,
                                Text(
                                    value="Infinity",
                                    size=25,
                                    color=colors.WHITE,
                                    expand=1
                                ),
                                Text(
                                    value="",
                                    expand=3
                                ),
                                TextButton(text="Services", width=100),
                                TextButton(text="Projects", width=100),
                                TextButton(text="About", width=100),
                                ElevatedButton(
                                    content=Text(
                                        value="Contact",
                                        color=colors.WHITE
                                    ),
                                    bgcolor=colors.CYAN_400,
                                    style=flet.ButtonStyle(
                                        overlay_color=colors.CYAN_600,
                                    ),
                                    on_click=lambda e: self.page.go("/")
                                )
                            ]
                        )
                    ),
                    Container(
                        expand=10,
                        content=Row(
                            spacing=5,
                            controls=[
                                Container(
                                    expand=2,
                                    content=NavigationRail(
                                        #selected_index=0,
                                        group_alignment=-0.9,
                                        bgcolor=colors.BLACK87,
                                        extended=True,
                                        leading=FloatingActionButton(
                                            icon=icons.ADD,
                                            text="Agregar Dispositivo"
                                        ),
                                        destinations=[
                                            NavigationRailDestination(
                                                padding=padding.only(left=5),
                                                icon=icons.HOME,
                                                label_content=Text("Home", size=20),
                                            ),
                                            NavigationRailDestination(
                                                padding=padding.only(left=5),
                                                icon=icons.PEOPLE,
                                                label_content=Text("Customers", size=20),
                                            ),
                                            NavigationRailDestination(
                                                padding=padding.only(left=5),
                                                icon=icons.PRODUCTION_QUANTITY_LIMITS,
                                                label_content=Text("Products", size=20),
                                            ),
                                            NavigationRailDestination(
                                                padding=padding.only(left=5),
                                                icon=icons.NEWSPAPER,
                                                label_content=Text("Orders", size=20),
                                            ),
                                            NavigationRailDestination(
                                                padding=padding.only(left=5),
                                                icon=icons.REPORT,
                                                label_content=Text("Reports", size=20),
                                            ),
                                            NavigationRailDestination(
                                                padding=padding.only(left=5),
                                                icon=icons.PAN_TOOL,
                                                #label_content=Text("Tools", size=20),
                                            )
                                        ],
                                        #on_change=lambda e: print("Selected destination:", e.control.selected_index)
                                        on_change=self.destination_changed
                                    )
                                ),
                                self.container_principal,

                            ]
                        )
                    )
                ]
            )
        )
        return container

    def destination_changed(self, event):
        print(f'Selected Destination: {event.control.selected_index}')
        if str(event.control.selected_index) == "0":
            self.container_principal.content = self.container_home_page
        if str(event.control.selected_index) == "1":
            self.container_principal.content = self.container_customers_page
        self.page.update(self)

    def change_color_icon(self, e):
        self.contador_icon_main += 1
        if self.contador_icon_main == 1:
            self.icon_main.icon_color = colors.RED_800
            self.audio1.resume()
            self.page.update(self)
        if self.contador_icon_main == 2:
            self.icon_main.icon_color = colors.WHITE
            self.contador_icon_main = 0
            self.audio1.pause()
            self.page.update(self)


class CustomersPage(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.row_main = Row(
            controls=[
                ElevatedButton("asd", on_click=self.button_clicked),
            ],
        )
        self.container = Container(
            bgcolor=colors.BLACK,
            content=self.row_main,
            alignment=flet.alignment.center,
        )

    def build(self):
        pass
        return self.container

    def button_clicked(self, event):
        print("Presionado")
        self.row_main.controls.append(Text("Aquí estoy"))
        self.page.update(self)

class HomePage(UserControl):
    def __init__(self, page, texto):
        super().__init__()
        self.page = page
        self.texto = texto
        self.row_main = Row(
            controls=[
                ElevatedButton("asd", on_click=self.button_clicked),
            ]
        )
        self.container = Container(
            bgcolor=colors.BLUE,
            content=self.row_main,
            alignment=flet.alignment.center,
        )

    def build(self):
        pass
        return self.container

    def button_clicked(self, event):
        print("Presionado")
        self.row_main.controls.append(Text("Aquí estoy"))
        self.page.update(self)

if __name__ == "__main__":
    def main(page: Page):
        #page.theme_mode = flet.ThemeMode.LIGHT
        page.title = "Login Interface"

        def route_change(route):
            page.views.clear()
            print("Cambio de ruta")

            if page.route == "/":
                page.views.append(
                    flet.View(
                        "/",
                        [
                            SafeArea(
                                content=login_interface,
                                expand=True,
                            )
                        ]

                    )
                )
            if page.route == "/sensores" and login_interface.login_successful:
                page.views.append(
                    flet.View(
                        "/sensores",
                        [
                            SafeArea(
                                content=main_interface,
                                expand=True,
                            )
                        ]
                    )
                )
            page.update()

        page.fonts = {
            "Kanit": "https://raw.githubusercontent.com/google/fonts/master/ofl/kanit/Kanit-Bold.ttf",
            "Oswald Bold": "https://github.com/googlefonts/OswaldFont/raw/main/fonts/ttf/Oswald-Bold.ttf",
            "Oswald Medium": "https://github.com/googlefonts/OswaldFont/blob/main/fonts/ttf/Oswald-Medium.ttf",
        }
        page.theme = Theme(font_family="Oswald Bold")
        page.window_maximized = True

        main_interface = MainInterface(page)
        login_interface = LoginInterface(page)
        page.on_route_change = route_change
        page.go(page.route)

    flet.app(target=main)  # view=flet.WEB_BROWSER
