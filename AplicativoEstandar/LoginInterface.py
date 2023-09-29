from flet import app, SafeArea, UserControl, TextAlign, Page, RoundedRectangleBorder, ButtonStyle, ElevatedButton, TextThemeStyle, Checkbox, MainAxisAlignment, Image, Column, icons, alignment, LinearGradient, MainAxisAlignment, FontWeight, TextCapitalization, Icon, TextStyle, colors, AlertDialog, Text, TextField, TextButton, Row, Container, ImageFit

def CajaTextoConIcono(label, src_image, password, icon):
    icon_caja = Icon(
        name=icon,
        color=colors.WHITE,
        size=30,
    )
    txt_caja = TextField(
        label=label,
        expand=1,
        label_style=TextStyle(
            color=colors.WHITE,
            weight=FontWeight.BOLD,
        ),
        text_style=TextStyle(
            color=colors.AMBER,
            weight=FontWeight.BOLD,
        ),
        border_radius=15,
        capitalization=TextCapitalization.CHARACTERS,
        password=password,
        can_reveal_password=password,
        border_color=colors.WHITE,
        bgcolor="#1c84cb",
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
            actions=[
                TextButton("Send", on_click=self.close_dlg),
                TextButton("Close", on_click=self.close_dlg),
            ],
            actions_alignment=MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!")
        )

    def build(self):

        self.row_interfaz = Row(
            expand=True,
            controls=[
                Container(
                    border_radius=30,
                    expand=2,
                    alignment=alignment.center,
                    image_src="Assets\InenPortada.png",
                    image_fit=ImageFit.COVER,
                ),
                Container(
                    border_radius=30,
                    gradient=LinearGradient(
                        begin=alignment.center,
                        end=alignment.bottom_center,
                        colors=[colors.BLACK, "#08396a"]
                    ),
                    expand=1,
                    content=self.Container_Login_Password(),
                    alignment=alignment.top_center
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
                alignment=MainAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    Text("Welcome Back",weight=FontWeight.BOLD, style=TextThemeStyle.HEADLINE_MEDIUM, color=colors.WHITE),
                    Row(
                        controls=[
                            Image(
                                width=120,
                                height=120,
                                src=f"Assets/LogoPrincipal.svg"),
                        ],
                        alignment=MainAxisAlignment.CENTER
                    ),
                    Row([self.caja_username]),
                    Row([self.caja_password]),
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        spacing=30,
                        controls=[
                            Checkbox(label="Remember Password", expand=1),
                            TextButton(text="Forgot Password", width=140, on_click=self.open_dlg_modal)
                        ]
                    ),
                    Row(controls=[self.lbl_user_or_password_incorrect], alignment=MainAxisAlignment.CENTER),
                    Row(
                        controls=[
                            ElevatedButton(
                                content=Text(value="Login", weight=FontWeight.BOLD, style=TextThemeStyle.BODY_LARGE, color="red"),
                                expand=1,
                                color=colors.RED_ACCENT_700,
                                bgcolor=colors.WHITE,
                                style=ButtonStyle(
                                    overlay_color=colors.BLACK,
                                    shape=RoundedRectangleBorder(radius=10),
                                ),
                                on_click=self.user_and_password_validate,
                            )
                        ],
                    ),
                    Row(
                        alignment=MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            Text("Dont you have account?", expand=1.2, text_align=TextAlign.CENTER),
                            TextButton(text="Create account here", width=160)
                        ]
                    ),

                ],

            ),
            alignment=alignment.top_center,

        )
        return container

    def user_and_password_validate(self, e):
        self.caja_password.value = "123"
        self.caja_username.value = "ADMIN"
        if self.caja_password.value == "123" and self.caja_username.value == "ADMIN":
            self.login_successful = True
            self.page.go("/dashboard")
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

