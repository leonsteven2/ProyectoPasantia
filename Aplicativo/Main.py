import time

import flet
from flet import AlertDialog, FilePicker, FilePickerResultEvent, ProgressBar, CircleAvatar, Dropdown, dropdown, Icon, Page, NavigationRail, FloatingActionButton, NavigationRailDestination, padding, \
    IconButton, TextStyle, Slider, TextThemeStyle, FontWeight, TextAlign, colors, TextCapitalization, Theme, UserControl, Container, icons, \
    ElevatedButton, DataTable, DataColumn, DataRow, DataCell, SafeArea, Checkbox, Text, Column, TextField, Row, ImageFit, TextButton
from time import sleep
import serial

import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart


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

def SliderAndTextfield(label, suffix):
    slider = Slider(expand=3, active_color="white")
    textfield = TextField(label=label, expand=1, value="0", suffix_text=suffix)
    return textfield, slider


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
                    border_radius=30,
                    expand=2,
                    alignment=flet.alignment.center,
                    image_src="C:\\Users\\USER\PycharmProjects\ProyectoPasantia\Aplicativo\Assets\InenPortada.png",
                    image_fit=ImageFit.COVER,
                ),
                Container(
                    border_radius=30,
                    gradient=flet.LinearGradient(
                        begin=flet.alignment.center,
                        end=flet.alignment.bottom_center,
                        colors=[colors.BLACK, "#08396a"]
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
                    Text("Welcome Back",weight=FontWeight.BOLD, style=TextThemeStyle.HEADLINE_MEDIUM, color=colors.WHITE),
                    Row(
                        controls=[
                            flet.Image(
                                width=120,
                                height=120,
                                src=f"Assets/LogoPrincipal.svg"),
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
                            TextButton(text="Forgot Password", width=140, on_click=self.open_dlg_modal)
                        ]
                    ),
                    Row(controls=[self.lbl_user_or_password_incorrect], alignment=flet.MainAxisAlignment.CENTER),
                    Row(
                        controls=[
                            ElevatedButton(
                                content=Text(value="Login", weight=FontWeight.BOLD, style=TextThemeStyle.BODY_LARGE, color="red"),
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
                            TextButton(text="Create account here", width=160)
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
        if self.caja_password.value == "123" and self.caja_username.value == "ADMIN":
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


class SetpointBox(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        # Creamos la caja de setpoint
        self.txt_RH_Pc, slider_RH_Pc = SliderAndTextfield(label="RH @Pc", suffix="%")
        slider_RH_Pc.on_change = lambda e: self.slider_value_to_text_field(e, textfield=self.txt_RH_Pc)

        self.txt_RH_PcTc, slider_RH_PcTc = SliderAndTextfield(label="RH @PcTc", suffix="%")
        slider_RH_PcTc.on_change = lambda e: self.slider_value_to_text_field(e, textfield=self.txt_RH_PcTc)

        self.txt_sat_pressure, slider_sat_pressure = SliderAndTextfield(label="Sat. Press.", suffix="psi")
        slider_sat_pressure.on_change = lambda e: self.slider_value_to_text_field(e, textfield=self.txt_sat_pressure)

        self.txt_sat_temp, slider_sat_temp = SliderAndTextfield(label="Sat. Temp", suffix="°C")
        slider_sat_temp.on_change = lambda e: self.slider_value_to_text_field(e, textfield=self.txt_sat_temp)

        self.txt_flow_rate, slider_flow_rate = SliderAndTextfield(label="Flow Rate", suffix="l/m")
        slider_flow_rate.on_change = lambda e: self.slider_value_to_text_field(e, textfield=self.txt_flow_rate)

        self.row_caja_setpoint = Row(
            expand=1,
            controls=[
                Column(
                    expand=1,
                    controls=[
                        Text("Setpoint!",
                             style=TextThemeStyle.TITLE_LARGE,
                             weight=FontWeight.BOLD
                             ),
                        Row(
                            expand=1,
                            controls=[
                                self.txt_RH_Pc,
                                slider_RH_Pc,
                                self.txt_RH_PcTc,
                                slider_RH_PcTc,
                                self.txt_sat_pressure,
                                slider_sat_pressure
                            ]
                        ),
                        Row(
                            expand=1,
                            controls=[
                                self.txt_sat_temp,
                                slider_sat_temp,
                                self.txt_flow_rate,
                                slider_flow_rate,
                                ElevatedButton("Enviar Valores", expand=4)
                            ]
                        )
                    ]
                )
            ],
        )

    def build(self):
        pass
        return self.row_caja_setpoint

    def slider_value_to_text_field(self, event, textfield):
        y = 1 + ((100-1)/(1))*(event.control.value)
        textfield.value = str(round(y,2))
        self.page.update(self)


class DeviceComunication(UserControl):
    def __init__(self, titulo, default_baud, page, data, grafica=None):
        super().__init__()
        self.titulo = titulo
        self.default_baud = default_baud
        self.page = page
        self.data = data
        self.grafica = grafica

        # Creamos la barra de progreso para la comunicación serial
        self.progress_bar = ProgressBar(
            expand=1,
            value=0,
            color="amber",
            bgcolor="#eeeeee"
        )
        # Creamos los botones para guardar y exportar datos
        self.btn_iniciar_registro_datos = ElevatedButton(
            "Iniciar registro",
            expand=1
        )
        # hide all dialogs in overlay
        save_file_dialog = FilePicker(on_result=self.save_file_result)
        self.page.overlay.extend([save_file_dialog])

        self.btn_guardar_datos_excel =  ElevatedButton(
            "Save file",
            icon=icons.SAVE,
            on_click=lambda _: save_file_dialog.save_file(file_name="HOLA")
        )
        # Creamos la fila que contiene al progress bar y los botones de guardado de datos
        self.row_progress_bar_and_buttons = Row(
            controls=[self.progress_bar, self.btn_guardar_datos_excel]
        )

        # Creamos la etiqueta de ayuda al usuario para la comunicación serial
        self.txt_user_help = Text(
            value="Click para empezar comunicación serial",
            color="yellow",
            style=TextThemeStyle.LABEL_LARGE
        )

        # Creamos la fila que contiene el Dropdown de Baud y PortCOM
        self.drop_PORT = Dropdown(
                            expand=1,
                            dense=True,
                            label="PORT",
                            hint_text="Puerto COM",
                            color="blue",
                            text_style=TextStyle(weight=FontWeight.BOLD),
                            options=[
                                dropdown.Option("COM1"),
                                dropdown.Option("COM2"),
                                dropdown.Option("COM3"),
                                dropdown.Option("COM4"),
                                dropdown.Option("COM5"),
                                dropdown.Option("COM6"),
                                dropdown.Option("COM7"),
                                dropdown.Option("COM8"),
                                dropdown.Option("COM9"),
                                dropdown.Option("COM10"),
                            ],
                        )
        self.drop_BAUD = Dropdown(
                            expand=1,
                            value=self.default_baud,
                            dense=True,
                            label="Baud",
                            color="blue",
                            text_style=TextStyle(weight=FontWeight.BOLD),
                            options=[
                                dropdown.Option("1200"),
                                dropdown.Option("2400"),
                                dropdown.Option("4800"),
                                dropdown.Option("9600"),
                                dropdown.Option("19200"),
                                dropdown.Option("38400"),
                                dropdown.Option("57600"),
                                dropdown.Option("115200"),
                            ]
                        )
        self.row_baud_port = Row(
                    controls=[
                        self.drop_PORT,
                        self.drop_BAUD,
                        IconButton(icon=icons.SEND_SHARP, on_click=self.establecer_conexion_serial, icon_color="yellow")
                    ]
                )

        # Creamos el título de la Caja de Setpoint
        self.lbl_setpoint = Text("Setpoint!",
                             style=TextThemeStyle.TITLE_LARGE,
                             weight=FontWeight.BOLD
                             )

        # Creamos las tablas para los diferentes equipos
        if self.data == "Thunder":
            self.txt_RH_Pc_setpoint = Text("0")
            self.txt_RH_Pc_actual = Text("0")

            self.txt_RH_PcTc_setpoint = Text("0")
            self.txt_RH_PcTc_actual = Text("0")

            self.txt_saturation_pressure_setpoint = Text("0")
            self.txt_saturation_pressure_actual = Text("0")

            self.txt_chamber_pressure_setpoint = Text("-")
            self.txt_chamber_pressure_actual = Text("0")

            self.txt_saturation_temp_setpoint = Text("0")
            self.txt_saturation_temp_actual = Text("0")

            self.txt_chamber_temp_setpoint = Text("-")
            self.txt_chamber_temp_actual = Text("0")




            self.txt_flow_rate_setpoint = Text("0")
            self.txt_flow_rate_actual = Text("0")

            self.data_table = DataTable(
                expand=1,
                columns=[
                    DataColumn(Text("Parámetro")),
                    DataColumn(Text("Mag.")),
                    DataColumn(Text("Setpoint"), numeric=True),
                    DataColumn(Text("Actual"), numeric=True),
                ],
                rows=[
                    DataRow(
                        cells=[
                            DataCell(Text("%RH")),
                            DataCell(Text("%Pc")),
                            DataCell(self.txt_RH_Pc_setpoint),
                            DataCell(self.txt_RH_Pc_actual)
                        ]
                    ),
                    DataRow(
                        cells=[
                            DataCell(Text("%RH")),
                            DataCell(Text("%PcTc")),
                            DataCell(self.txt_RH_PcTc_setpoint),
                            DataCell(self.txt_RH_PcTc_actual),
                        ]
                    ),
                    DataRow(
                        cells=[
                            DataCell(Text("Saturación")),
                            DataCell(Text("Psi")),
                            DataCell(self.txt_saturation_pressure_setpoint),
                            DataCell(self.txt_saturation_pressure_actual),
                        ]
                    ),
                    DataRow(
                        cells=[
                            DataCell(Text("Cámara")),
                            DataCell(Text("Psi")),
                            DataCell(self.txt_chamber_pressure_setpoint),
                            DataCell(self.txt_chamber_pressure_actual),
                        ]
                    ),
                    DataRow(
                        cells=[
                            DataCell(Text("Saturación")),
                            DataCell(Text("°C")),
                            DataCell(self.txt_saturation_temp_setpoint),
                            DataCell(self.txt_saturation_temp_actual),
                        ]
                    ),
                    DataRow(
                        cells=[
                            DataCell(Text("Cámara")),
                            DataCell(Text("°C")),
                            DataCell(self.txt_chamber_temp_setpoint),
                            DataCell(self.txt_chamber_temp_actual),
                        ]
                    ),
                    DataRow(
                        cells=[
                            DataCell(Text("Flow")),
                            DataCell(Text("l/m")),
                            DataCell(self.txt_flow_rate_setpoint),
                            DataCell(self.txt_flow_rate_actual),
                        ]
                    ),
                ],
                column_spacing=30,
            )

        if self.data == "473":
            self.txt_RH_473_actual = Text("0")
            self.txt_DewPoint_473_actual = Text("0")
            self.txt_ExternalTemp_473_actual = Text("0")

            self.data_table = DataTable(
                expand=1,
                columns=[
                    DataColumn(Text("Parámetro")),
                    DataColumn(Text("Mag.")),
                    DataColumn(Text("Actual"), numeric=True),
                ],
                rows=[
                    DataRow(
                        cells=[
                            DataCell(Text("Relative Humidity")),
                            DataCell(Text("%")),
                            DataCell(self.txt_RH_473_actual),
                        ]
                    ),
                    DataRow(
                        cells=[
                            DataCell(Text("Dew Point")),
                            DataCell(Text("°C")),
                            DataCell(self.txt_DewPoint_473_actual),
                        ]
                    ),
                    DataRow(
                        cells=[
                            DataCell(Text("External Temp")),
                            DataCell(Text("°C")),
                            DataCell(self.txt_ExternalTemp_473_actual),
                        ]
                    ),
                ],
                column_spacing=30,
            )

        if self.data == "Fluke":
            self.txt_temp1_actual = Text("0")
            self.txt_temp2_actual = Text("0")

            self.txt_RH1_actual = Text("0")
            self.txt_RH2_actual = Text("0")

            self.data_table = DataTable(
                expand=1,
                columns=[
                    DataColumn(Text("Parámetro")),
                    DataColumn(Text("Mag.")),
                    DataColumn(Text("Sensor 1"), numeric=True),
                    DataColumn(Text("Sensor 2"), numeric=True),
                ],
                rows=[
                    DataRow(
                        cells=[
                            DataCell(Text("Temperatura")),
                            DataCell(Text("°C")),
                            DataCell(self.txt_temp1_actual),
                            DataCell(self.txt_temp2_actual),
                        ]
                    ),
                    DataRow(
                        cells=[
                            DataCell(Text("Humedad Relativa")),
                            DataCell(Text("%")),
                            DataCell(self.txt_RH1_actual),
                            DataCell(self.txt_RH2_actual),
                        ]
                    ),

                ],
                column_spacing=30,
            )

        # Creamos la columna principal que contiene el título, configuracion serial y tablas
        self.col_main = Column(
            expand=1,
            spacing=15,
            scroll=flet.ScrollMode.HIDDEN,
            #alignment=flet.MainAxisAlignment.CENTER,
            controls=[
                Row(controls=[
                    Text(value=self.titulo, text_align=TextAlign.CENTER, weight=FontWeight.BOLD,
                         style=TextThemeStyle.TITLE_LARGE)],
                    alignment=flet.MainAxisAlignment.CENTER
                ),
                self.row_baud_port,
                Row(
                    controls=[
                        self.txt_user_help,
                    ],
                    alignment=flet.MainAxisAlignment.CENTER
                ),
                self.row_progress_bar_and_buttons,
                Row(
                    controls=[
                        self.data_table
                    ],
                    alignment=flet.MainAxisAlignment.CENTER
                )
            ]
        )

        # Creamos la fila que contiene toda la MainInterface
        self.row_main = Row(
            expand=1,
            controls=[
                Container(
                    # bgcolor=colors.BLUE_GREY_900,
                    bgcolor=colors.GREY_900,
                    padding=padding.all(10),
                    expand=1,
                    content=self.col_main

                )
            ]
        )

    def build(self):
        pass
        return self.row_main

    def save_file_result(self, e: FilePickerResultEvent):
        save_file_path = e.path if e.path else "Cancelled!"
        name_file = save_file_path.split("\\")
        print(f'Path: {save_file_path}\nFile name: {name_file[-1]}')

    def establecer_conexion_serial(self, event):
        conexion_satisfactoria = False
        # Cambiamos el color
        if self.drop_PORT.value != None:
            self.progress_bar.color = "amber"
            self.progress_bar.value = None
            self.txt_user_help.value = f"Conectando por {self.drop_PORT.value} ..."
            self.txt_user_help.color = None
            self.page.update(self)
            sleep(3)
            try:
                self.comunicacion_serial = serial.Serial(str(self.drop_PORT.value), int(self.drop_BAUD.value))
                conexion_satisfactoria = True
            except Exception as e:
                error = str(e).split("(")
                self.progress_bar.value = 1
                self.progress_bar.color = "red"
                self.txt_user_help.value = error[0]
                self.txt_user_help.color = "red"
        else:
            self.progress_bar.value = 1
            self.progress_bar.color = "red"
            self.txt_user_help.value = "Seleccione el puerto COM"
            self.txt_user_help.color = "red"
            self.drop_PORT.autofocus = True

        if conexion_satisfactoria:
            self.row_baud_port.visible = False
            # self.progress_bar.value = 1
            # self.progress_bar.color = "green"
            self.txt_user_help.value = f"Conectado a {self.drop_PORT.value} - {self.drop_BAUD.value}"
            self.txt_user_help.color = "green"

            # Escondemos la barra de progreso y mostramos los botones de registro de datos
            self.progress_bar.visible = False
            #self.row_progress_bar_and_buttons.controls.append(self.btn_iniciar_registro_datos)
            #self.row_progress_bar_and_buttons.controls.append(self.btn_guardar_datos_excel)

            self.page.update(self)

            if self.data == "Thunder":
                self.adquisicion_datos_thunder()

            if self.data == "473":
                self.adquisicion_datos_473()

            if self.data == "Fluke":
                self.adquisicion_datos_fluke()


        self.page.update(self)

    def adquisicion_datos_thunder(self):
        while True:
            try:
                # Enviamos el mensaje para recibir los valores actuales
                mensaje = "?\r"
                self.comunicacion_serial.write(mensaje.encode())
                mensaje_desde_thunder = self.comunicacion_serial.readline().decode().strip().split(",")
                self.txt_RH_Pc_actual.value = str(mensaje_desde_thunder[0])
                self.txt_RH_PcTc_actual.value = str(mensaje_desde_thunder[1])
                self.txt_saturation_pressure_actual.value = str(mensaje_desde_thunder[2])
                self.txt_chamber_pressure_actual.value = str(mensaje_desde_thunder[3])
                self.txt_saturation_temp_actual.value = str(mensaje_desde_thunder[4])
                self.txt_chamber_temp_actual.value = str(mensaje_desde_thunder[5])
                self.txt_flow_rate_actual.value = str(mensaje_desde_thunder[6])

                # Enviamos el mensaje para recibir los valores de setpoint
                mensaje = "?SP\r"
                self.comunicacion_serial.write(mensaje.encode())
                mensaje_desde_thunder = self.comunicacion_serial.readline().decode().strip().split(",")
                self.txt_RH_Pc_setpoint.value = str(mensaje_desde_thunder[0])
                self.txt_RH_PcTc_setpoint.value = str(mensaje_desde_thunder[1])
                self.txt_saturation_pressure_setpoint.value = str(mensaje_desde_thunder[2])
                self.txt_saturation_temp_setpoint.value = str(mensaje_desde_thunder[3])
                self.txt_flow_rate_actual.value = str(mensaje_desde_thunder[4])
                # mensaje_serial = self.comunicacion_serial.readline().decode().strip()
                # self.txt_RH_Pc_actual.value = str(mensaje_serial)
                # self.grafica.graficar_en_tiempo_real(event=None, value1=self.txt_RH_Pc_actual.value, value2=self.txt_RH_Pc_actual.value)
                self.page.update(self)
            except Exception as e:
                self.conexion_serial_fallida(error=e)
                break

    def adquisicion_datos_473(self):
        while True:
            try:
                mensaje = "RH?\r"
                self.comunicacion_serial.write(mensaje.encode())
                mensaje_desde_473 = self.comunicacion_serial.readline().decode().strip()
                self.txt_RH_473_actual.value = str(mensaje_desde_473)

                mensaje = "DP?\r"
                self.comunicacion_serial.write(mensaje.encode())
                mensaje_desde_473 = self.comunicacion_serial.readline().decode().strip()
                self.txt_DewPoint_473_actual.value = str(mensaje_desde_473)

                mensaje = "Tx?\r"
                self.comunicacion_serial.write(mensaje.encode())
                mensaje_desde_473 = self.comunicacion_serial.readline().decode().strip()
                self.txt_ExternalTemp_473_actual.value = str(mensaje_desde_473)

                self.page.update(self)
                time.sleep(2)
            except Exception as e:
                self.conexion_serial_fallida(error=e)
                break

    def adquisicion_datos_fluke(self):
        while True:
            try:
                mensaje_desde_fluke = self.comunicacion_serial.readline().decode()
                mensaje_desde_fluke = mensaje_desde_fluke.split(",")
                self.txt_temp1_actual.value = mensaje_desde_fluke[1].strip()
                self.txt_temp2_actual.value = mensaje_desde_fluke[5].strip()
                self.txt_RH1_actual.value = mensaje_desde_fluke[3].strip()
                self.txt_RH2_actual.value = mensaje_desde_fluke[7].strip()
                # mensaje_serial = self.comunicacion_serial.readline().decode().strip()
                # self.txt_RH_Pc_actual.value = str(mensaje_serial)
                # self.grafica.graficar_en_tiempo_real(event=None, value1=self.txt_RH_Pc_actual.value, value2=self.txt_RH_Pc_actual.value)
                self.page.update(self)
            except Exception as e:
                self.conexion_serial_fallida(error=e)
                break

    def conexion_serial_fallida(self, error):
        self.row_baud_port.visible = True
        str_error = str(error).split("(")
        self.progress_bar.visible = True
        self.progress_bar.value = 1
        self.progress_bar.color = "red"
        self.txt_user_help.value = str_error[0]
        self.txt_user_help.color = "red"


class GraficaIndependiente(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        fig, self.ax = plt.subplots()
        self.datos_x = [0]
        self.datos_y = [0]
        self.contador = 0
        self.ax.plot(
            self.datos_y,
            linestyle="--",
            color="green",
            linewidth=5,
            marker="o",
            markersize=20,
            label="Actual",
        )
        # plt.legend(fontsize=30)
        # ax.set_ylabel("Valor", fontsize=30, color="red")
        self.ax.tick_params(axis='both', labelsize=30, labelcolor="white")
        self.ax.grid()
        fig.set_figwidth(20)
        # plt.xlabel("# Medición")
        # plt.ylabel("Valor")
        #self.plt_chart = MatplotlibChart(fig, transparent=True, isolated=True, expand=True)
        self.plt_chart = MatplotlibChart(fig, transparent=True, isolated=True, expand=1)


    def build(self):
        self.row_chart = Row(
            expand=1,
            controls=[
                self.plt_chart,
                IconButton(icon=icons.START)
            ]
        )
        return self.row_chart

    def graficar_en_tiempo_real(self, event, value1, value2):
        self.contador = self.contador + 1
        if len(self.datos_x) >= 15:
            self.datos_x.pop(0)
            self.datos_y.pop(0)
        self.datos_x.append(self.contador)
        self.datos_y.append(int(value1))
        self.ax.clear()
        self.ax.plot(
            self.datos_x,
            self.datos_y,
            linestyle="--",
            color="green",
            linewidth=5,
            marker="o",
            markersize=20,
            label="Actual",
        )

        self.ax.plot(
            [self.datos_x[0],self.datos_x[-1]],
            [50,50],
            linestyle="--",
            color="red",
            linewidth=5,
            label="Setpoint",
        )

        self.ax.tick_params(axis='both', labelsize=30, labelcolor="white")
        self.ax.grid()
        self.plt_chart.update()


class Dashboard(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        # Creamos la gráfica
        self.row_chart_setpoint_and_actual = GraficaIndependiente(page=self.page)

        # Creamos las cajas de configuración serial para cada dispositivo
        self.caja_configuracion_serial_thunder = DeviceComunication(titulo="Thunder Scientific", default_baud="2400",
                                                               page=self.page, data="Thunder", grafica=self.row_chart_setpoint_and_actual)
        self.caja_configuracion_serial_dew473 = DeviceComunication(titulo="Dew Point Mirror - 473", default_baud="9600",
                                                              page=self.page, data="473")
        self.caja_configuracion_serial_fluke = DeviceComunication(titulo="Fluke - DewK ", default_baud="9600",
                                                             page=self.page, data="Fluke")

        self.container_all_serial_configuration = Container(
            bgcolor="#2D2F31",
            padding=padding.all(5),
            expand=1,
            content=Column(
                controls=[
                    Text(""),
                    Row(
                        controls=[
                            CircleAvatar(
                                content=Icon(icons.PERSON, size=45),
                                color=colors.BLUE_GREY_700,
                                bgcolor=colors.BLUE_GREY_100,
                                width=60,
                                height=60
                            )
                        ],
                        alignment=flet.MainAxisAlignment.CENTER
                    ),
                    NavigationRail(
                        selected_index=1,
                        group_alignment=-0.9,
                        bgcolor=colors.TRANSPARENT,
                        expand=1,
                        extended=True,
                        destinations=[
                            NavigationRailDestination(
                                # padding=padding.only(left=5),
                                icon=icons.HOME,
                                # icon=Icon(icons.HOME),
                                label_content=Text("Home", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
                            ),
                            NavigationRailDestination(
                                # padding=padding.only(left=5),
                                icon=icons.DASHBOARD,
                                label_content=Text("Panel", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
                            ),
                            NavigationRailDestination(
                                # padding=padding.only(left=5),
                                icon=icons.PERSON,
                                label_content=Text("Admin", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
                            ),
                            NavigationRailDestination(
                                # padding=padding.only(left=5),
                                icon=icons.SETTINGS,
                                label_content=Text("Settings", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
                            ),
                        ],
                        # on_change=lambda e: print("Selected destination:", e.control.selected_index)
                        # on_change=self.destination_changed
                    ),
                    Row(
                        controls=[
                            TextButton(
                                content=Row(
                                    controls=[
                                        Icon(icons.LOGOUT_OUTLINED, color=colors.WHITE),
                                        Text("Logout", weight=FontWeight.BOLD, style=TextThemeStyle.BODY_LARGE,
                                             color=colors.WHITE)
                                    ]
                                ),
                                on_click=self.return_to_login_page,
                            )
                        ],
                        alignment=flet.MainAxisAlignment.CENTER
                    ),
                    Text("")

                ],
            )
        )

        self.container_dashboard = Container(
            expand=7,
            content=Column(
                spacing=5,
                controls=[
                    Container(
                        bgcolor=colors.BLACK87,
                        expand=1,
                        content=SetpointBox(page=self.page),
                        padding=padding.all(10),
                    ),
                    Row(
                        spacing=5,
                        expand=3,
                        controls=[
                            Container(
                                expand=2,
                                content=self.caja_configuracion_serial_thunder
                            ),
                            Column(
                                expand=3,
                                spacing=5,
                                controls=[
                                    Row(
                                        spacing=5,
                                        expand=8,
                                        controls=[
                                            Container(
                                                expand=1,
                                                content=self.caja_configuracion_serial_dew473,
                                            ),
                                            Container(
                                                expand=1,
                                                content=self.caja_configuracion_serial_fluke
                                            ),
                                        ]
                                    ),
                                    Container(
                                        padding = padding.only(right=10),
                                        expand=4,
                                        bgcolor=colors.BLACK87,
                                        content=self.row_chart_setpoint_and_actual
                                    )
                                ]
                            )

                        ],

                    )
                ]
            )
        )
        self.container_main = Container(
            content=Row(
                controls=[
                    self.container_all_serial_configuration,
                    self.container_dashboard
                ],
                spacing=5,
            )
        )

    def build(self):
        pass
        return self.container_main

    def return_to_login_page(self, event):
        self.page.go("/")


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
        # page.theme_mode = flet.ThemeMode.LIGHT
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
            if page.route == "/sensores": #and login_interface.login_successful:
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
        #page.theme = Theme(font_family="Oswald Bold")
        def save_file_result(e: FilePickerResultEvent):
            save_file_path = e.path if e.path else "Cancelled!"
            print(save_file_path)



        page.window_maximized = True

        main_interface = Dashboard(page)
        login_interface = LoginInterface(page)
        page.on_route_change = route_change
        # page.go(page.route)
        page.go("/sensores")

    flet.app(target=main)  # view=flet.WEB_BROWSER
