import time
import pymysql
import flet
import credenciales
from flet import AlertDialog, FilePicker, FilePickerResultEvent, ProgressBar, CircleAvatar, Dropdown, dropdown, Icon, Page, NavigationRail, NavigationRailDestination, padding, \
    IconButton, TextStyle, Slider, TextThemeStyle, FontWeight, TextAlign, colors, TextCapitalization, UserControl, Container, icons, \
    ElevatedButton, DataTable, DataColumn, DataRow, DataCell, SafeArea, Checkbox, Text, Column, TextField, Row, ImageFit, TextButton
from time import sleep, strftime
import serial
import pandas as pd

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
                    image_src="Assets\InenPortada.png",
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
        self.bool_enviar_datos = False

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

        self.btn_enviar_setpoint = ElevatedButton(
            "Enviar Valores",
            expand=4,
            on_click=self.enviar_setpoint,
            disabled=True
        )

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
                                self.btn_enviar_setpoint
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

    def enviar_setpoint(self, event):
        self.btn_enviar_setpoint.disabled = True
        self.btn_enviar_setpoint.text = "Enviando..."
        self.btn_enviar_setpoint.update()
        self.bool_enviar_datos = True
        sleep(2)
        self.btn_enviar_setpoint.disabled = False
        self.btn_enviar_setpoint.text = "Enviar Valores"
        self.btn_enviar_setpoint.update()

    def activar_boton_enviar(self):
        self.btn_enviar_setpoint.disabled = False
        self.btn_enviar_setpoint.update()


class DeviceComunication(UserControl):
    def __init__(self, titulo, default_baud, page, data, grafica=None, setpoint=None):
        super().__init__()
        self.titulo = titulo
        self.default_baud = default_baud
        self.page = page
        self.data = data
        self.grafica = grafica
        self.setpoint_box = setpoint

        # Creamos la barra de progreso para la comunicación serial
        self.progress_bar = ProgressBar(
            value=0,
            color="amber",
            bgcolor="#eeeeee"
        )

        # Creamos los botones para guardar y exportar datos
        self.bool_registrar_datos = False
        self.btn_iniciar_registro_datos = ElevatedButton(
            "Registrar",
            expand=1,
            on_click=lambda _: self.registrar_datos(),
            bgcolor="green",
            color="white"
        )
        # hide all dialogs in overlay
        save_file_dialog = FilePicker(on_result=self.save_file_result)
        self.page.overlay.extend([save_file_dialog])
        self.btn_guardar_datos =  ElevatedButton(
            ".csv",
            icon=icons.SAVE,
            disabled=True,
            color="black",
            bgcolor="white",
            on_click=lambda _: save_file_dialog.save_file(file_name="datos.csv", allowed_extensions=["csv"])
        )
        # Creamos el boton para resetear los datos del dataframe
        self.btn_reset_dataframe = IconButton(
            icon=icons.RESTART_ALT,
            icon_color="white",
            disabled=True,
            on_click=self.resetear_dataframe
        )
        # self.btn_reset_dataframe = ElevatedButton(
        #     "Reset",
        #     disabled=True,
        #     on_click=self.resetear_dataframe
        # )
        # Creamos el botón para salir de la conexión
        self.btn_exit = IconButton(
            bgcolor=colors.RED_400,
            icon=icons.EXIT_TO_APP_ROUNDED,
            icon_color="white",
            on_click=lambda _: self.conexion_serial_fallida("Proceso finalizado")
        )

        # Creamos el botón para enviar datos a la nube
        self.btn_send_data_cloud = IconButton(
            icon=icons.CLOUD_UPLOAD,
            icon_color="white",
            disabled=True,
            on_click=self.enviar_datos_a_mysql
        )

        # Creamos la fila que contiene al progress bar y los botones de guardado de datos
        self.row_data_buttons = Row(
            visible=False,
            controls=[
                self.btn_iniciar_registro_datos,
                self.btn_guardar_datos,
                self.btn_reset_dataframe,
                self.btn_send_data_cloud,
                self.btn_exit
            ]
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
                            color="white",
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
                            color="white",
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


            self.df_datos_thunder = pd.DataFrame(columns=[
                'id_equipo', 'fecha', 'hora',
                'rh_pc_sp', 'rh_pc', 'unit_rh_pc',
                'rh_pctc_sp', 'rh_pctc', 'unit_pctc',
                'satur_pressure_sp', 'satur_pressure', 'unit_satur_pressure',
                'chmbr_pressure', 'unit_chmbr_pressure',
                'satur_temp_sp', 'satur_temp', 'unit_satur_temp',
                'chmbr_temp', 'unit_chmbr_temp',
                'flow_sp', 'flow', 'unit_flow'
            ])

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

            self.df_datos_473 = pd.DataFrame(columns=['RH', 'DewPoint', 'Ext. Temp'])

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

            self.df_datos_fluke = pd.DataFrame(columns=['Temp1', 'RH1', 'Temp2', 'RH2'])

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

        # Creamos un indice general para los dataframe
        self.dataframe_indice = 0

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
                    alignment=flet.MainAxisAlignment.CENTER,
                ),
                self.progress_bar,
                self.row_data_buttons,
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
        if self.data == "Thunder":
            self.df_datos_thunder.to_csv(save_file_path, index=False)
        if self.data == "473":
            self.df_datos_473.to_csv(save_file_path, index=False)
        if self.data == "Fluke":
            self.df_datos_fluke.to_csv(save_file_path, index=False)

    def establecer_conexion_serial(self, event):
        conexion_satisfactoria = False
        # Cambiamos el color
        if self.drop_PORT.value != None:
            self.progress_bar.color = "amber"
            self.progress_bar.value = None
            self.txt_user_help.value = f"Conectando por {self.drop_PORT.value} ..."
            self.txt_user_help.color = None
            self.page.update(self)
            sleep(2)
            try:
                self.comunicacion_serial = serial.Serial(
                    str(self.drop_PORT.value),
                    int(self.drop_BAUD.value),
                    timeout=1
                )
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
            self.row_data_buttons.visible = True
            # self.progress_bar.value = 1
            # self.progress_bar.color = "green"
            self.txt_user_help.value = f"Conectado a {self.drop_PORT.value} - {self.drop_BAUD.value}"
            self.txt_user_help.color = "green"

            # Escondemos la barra de progreso y mostramos los botones de registro de datos
            self.progress_bar.visible = False


            self.page.update(self)

            if self.data == "Thunder":
                self.adquisicion_datos_thunder()

            if self.data == "473":
                self.adquisicion_datos_473()

            if self.data == "Fluke":
                self.adquisicion_datos_fluke()


        self.page.update(self)

    def adquisicion_datos_thunder(self):
        #self.setpoint_box.activar_boton_enviar()
        self.setpoint_box.btn_enviar_setpoint.disabled = False
        self.setpoint_box.btn_enviar_setpoint.update()
        while True:
            sleep(2)
            try:
                if self.setpoint_box.bool_enviar_datos == False:
                    # Enviamos el mensaje para recibir los valores actuales
                    mensaje = "?\r"
                    self.comunicacion_serial.write(mensaje.encode())
                    try:
                        mensaje_desde_thunder = self.comunicacion_serial.readline().decode().strip().split(",")
                    except:
                        print("No pudo leer o splitear")
                        continue
                    try:
                        self.txt_RH_Pc_actual.value = str(mensaje_desde_thunder[0])
                        self.txt_RH_PcTc_actual.value = str(mensaje_desde_thunder[1])
                        self.txt_saturation_pressure_actual.value = str(mensaje_desde_thunder[2])
                        self.txt_chamber_pressure_actual.value = str(mensaje_desde_thunder[3])
                        self.txt_saturation_temp_actual.value = str(mensaje_desde_thunder[4])
                        self.txt_chamber_temp_actual.value = str(mensaje_desde_thunder[5])
                        self.txt_flow_rate_actual.value = str(mensaje_desde_thunder[6])
                    except:
                        continue

                    # Enviamos el mensaje para recibir los valores de setpoint
                    mensaje = "?SP\r"

                    try:
                        self.comunicacion_serial.write(mensaje.encode())
                        mensaje_desde_thunder = self.comunicacion_serial.readline().decode().strip().split(",")
                        self.txt_RH_Pc_setpoint.value = str(mensaje_desde_thunder[0])
                        self.txt_RH_PcTc_setpoint.value = str(mensaje_desde_thunder[1])
                        self.txt_saturation_pressure_setpoint.value = str(mensaje_desde_thunder[2])
                        self.txt_saturation_temp_setpoint.value = str(mensaje_desde_thunder[3])
                        self.txt_flow_rate_setpoint.value = str(mensaje_desde_thunder[4])
                    except:
                        continue

                else:

                    # Enviar datos
                    if float(self.setpoint_box.txt_RH_Pc.value) > 1:
                        mensaje = f"R1={self.setpoint_box.txt_RH_Pc.value}\r"
                        self.enviar_setpoint(mensaje=mensaje)
                    sleep(2)

                    if float(self.setpoint_box.txt_RH_PcTc.value) > 1:
                        mensaje = f"R2={self.setpoint_box.txt_RH_PcTc.value}\r"
                        self.enviar_setpoint(mensaje=mensaje)
                    sleep(2)

                    if float(self.setpoint_box.txt_sat_pressure.value) > 1:
                        mensaje = f"PS={self.setpoint_box.txt_sat_pressure.value}\r"
                        self.enviar_setpoint(mensaje=mensaje)
                    sleep(2)

                    if float(self.setpoint_box.txt_sat_temp.value) > 1:
                        mensaje = f"TS={self.setpoint_box.txt_sat_temp.value}\r"
                        self.enviar_setpoint(mensaje=mensaje)
                    sleep(2)

                    if float(self.setpoint_box.txt_flow_rate.value) > 1:
                        mensaje = f"FS={self.setpoint_box.txt_flow_rate.value}\r"
                        self.enviar_setpoint(mensaje=mensaje)
                    sleep(2)

                    self.setpoint_box.bool_enviar_datos = False


                # Guardamos en el dataframe si se presiono el boton registrar
                try:
                    if self.bool_registrar_datos:

                        hora = strftime("%H:%M:%S")
                        fecha = strftime("20%y-%m-%d")
                        self.dataframe_indice = self.df_datos_thunder.shape[0] + 1
                        self.df_datos_thunder.loc[self.dataframe_indice] = [
                            "1207906",fecha, hora,
                            self.txt_RH_Pc_setpoint.value, self.txt_RH_Pc_actual.value, "%HR",
                            self.txt_RH_PcTc_setpoint.value, self.txt_RH_PcTc_actual.value, "%HR",
                            self.txt_saturation_pressure_setpoint.value, self.txt_saturation_pressure_actual.value, "psi",
                            self.txt_chamber_pressure_actual.value, "psi",
                            self.txt_saturation_temp_setpoint.value, self.txt_saturation_temp_actual.value, "C",
                            self.txt_chamber_temp_actual.value, "C",
                            self.txt_flow_rate_setpoint.value, self.txt_flow_rate_actual.value, "l/m"


                        ]
                        self.txt_user_help.value = f"Datos registrados: {self.dataframe_indice}"
                        self.txt_user_help.color = "green"
                except Exception as e:
                    print(f'Error: {e}')

                try:
                    self.grafica.graficar_en_tiempo_real(value1=self.txt_RH_Pc_actual.value, value2=self.txt_RH_Pc_setpoint.value)
                except Exception as e:
                    print(f"No se pudo graficar: {e}")

                self.col_main.update()

            except Exception as e:
                print(e)
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

    def enviar_setpoint(self, mensaje):
        print("Esta es la funcion enviar_setpoint")
        try:
            self.comunicacion_serial.write(mensaje.encode())
            self.txt_user_help.value = f'Setpoint Enviado: {mensaje}'
            self.txt_user_help.color = "yellow"

        except Exception as e:
            self.txt_user_help.value = f'No se pudo enviar Setpoint.'
            self.txt_user_help.color = "red"
        self.txt_user_help.update()


    def conexion_serial_fallida(self, error):
        self.comunicacion_serial.close()
        self.row_data_buttons.visible = False
        self.row_baud_port.visible = True
        list_error = str(error).split("(")
        self.progress_bar.visible = True
        self.progress_bar.value = 1
        self.progress_bar.color = "red"

        if list_error[0] == "list index out of range":
            self.txt_user_help.value = "Proceso finalizado"
        else:
            self.txt_user_help.value = list_error[0]
        self.txt_user_help.color = "red"

        self.btn_iniciar_registro_datos.text = "Registrar"
        self.bool_registrar_datos = False

        self.page.update(self)

    def registrar_datos(self):
        if self.btn_iniciar_registro_datos.text == "Registrar":
            self.bool_registrar_datos = True

            self.btn_iniciar_registro_datos.text = "Detener"
            self.btn_iniciar_registro_datos.bgcolor = "red"

            self.btn_guardar_datos.disabled = True
            self.btn_reset_dataframe.disabled = True
            self.btn_send_data_cloud.disabled = True
            print("bool en true")
        else:
            self.bool_registrar_datos = False

            self.btn_iniciar_registro_datos.text = "Registrar"
            self.btn_iniciar_registro_datos.bgcolor = "green"

            if self.dataframe_indice > 0:
                self.btn_guardar_datos.disabled = False
                self.btn_reset_dataframe.disabled = False
                self.btn_send_data_cloud.disabled = False
        self.page.update(self)

    def resetear_dataframe(self, event):
        if self.data == "Thunder":
            self.df_datos_thunder.drop(self.df_datos_thunder.index, inplace=True)
        if self.data == "473":
            self.df_datos_473.drop(self.df_datos_473.index, inplace=True)
        if self.data == "Fluke":
            self.df_datos_fluke.drop(self.df_datos_fluke.index, inplace=True)
        self.dataframe_indice = 0
        self.btn_guardar_datos.disabled = True
        self.btn_reset_dataframe.disabled = True
        self.txt_user_help.value = "Datos registrados: 0"
        self.page.update(self)

    def enviar_datos_a_mysql(self, e):
        # Accedemos a la base de datos en mysql
        try:
            database = pymysql.connect(
                host=credenciales.host,
                user=credenciales.user,
                password=credenciales.password,
                database=credenciales.database,
            )
            cursor = database.cursor()

            if self.data == "Thunder":
                lista = self.df_datos_thunder
                comando_sql = "insert into lab_humedad values "
                for i in range(0, len(lista)):
                    separator = "," if i < (len(lista) - 1) else ";"
                    comando_sql = comando_sql + f"\n('{lista['id_equipo'].iloc[i]}','{lista['fecha'].iloc[i]}','{lista['hora'].iloc[i]}','" \
                                                f"{lista['rh_pc_sp'].iloc[i]}','{lista['rh_pc'].iloc[i]}','{lista['unit_rh_pc'].iloc[i]}','" \
                                                f"{lista['rh_pctc_sp'].iloc[i]}','{lista['rh_pctc'].iloc[i]}','{lista['unit_pctc'].iloc[i]}','" \
                                                f"{lista['satur_pressure_sp'].iloc[i]}','{lista['satur_pressure'].iloc[i]}','{lista['unit_satur_pressure'].iloc[i]}','" \
                                                f"{lista['chmbr_pressure'].iloc[i]}','{lista['unit_chmbr_pressure'].iloc[i]}','" \
                                                f"{lista['satur_temp_sp'].iloc[i]}','{lista['satur_temp'].iloc[i]}','{lista['unit_satur_temp'].iloc[i]}','" \
                                                f"{lista['chmbr_temp'].iloc[i]}','{lista['unit_chmbr_temp'].iloc[i]}','" \
                                                f"{lista['flow_sp'].iloc[i]}','{lista['flow'].iloc[i]}','{lista['unit_flow'].iloc[i]}'){separator}"

                print(comando_sql)
                cursor.execute(comando_sql)
                database.commit()
                self.txt_user_help.value = "Datos enviados a MYSQL"
                self.txt_user_help.update()

        except Exception as e:
            print(e)
            self.txt_user_help.value = e
            self.txt_user_help.color = "red"

class GraficaIndependiente(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        self.float1 = 0
        self.float2 = 0

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

    def graficar_en_tiempo_real(self, value1, value2):
        try:
            self.float1 = float(value1)
            self.float2 = float(value2)
        except:
            print("No se puede convertir a float")

        self.contador = self.contador + 1
        if len(self.datos_x) >= 15:
            self.datos_x.pop(0)
            self.datos_y.pop(0)
        self.datos_x.append(self.contador)
        self.datos_y.append(self.float1)
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
            [self.float2,self.float2],
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

        # Creamos la caja de setpoint
        self.setpoint_box = SetpointBox(page=self.page)

        # Creamos las cajas de configuración serial para cada dispositivo
        self.caja_configuracion_serial_thunder = DeviceComunication(titulo="Thunder Scientific", default_baud="9600",
                                                               page=self.page, data="Thunder", grafica=self.row_chart_setpoint_and_actual, setpoint=self.setpoint_box)
        self.caja_configuracion_serial_dew473 = DeviceComunication(titulo="Dew Point Mirror - 473", default_baud="9600",
                                                              page=self.page, data="473")
        self.caja_configuracion_serial_fluke = DeviceComunication(titulo="Fluke - DewK ", default_baud="9600",
                                                             page=self.page, data="Fluke")

        self.container_user_options = Container(
            bgcolor="#2D2F31",
            padding=padding.only(top=30, left=5, right=5, bottom=30),
            content=Column(
                horizontal_alignment="center",
                controls=[
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
                        min_extended_width=170,
                        min_width=80,
                        extended=False,
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
                                icon=icons.NEWSPAPER,
                                label_content=Text("Report", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
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
                    )

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
                        content=self.setpoint_box,
                        padding=padding.all(10),
                    ),
                    Row(
                        spacing=5,
                        expand=3,
                        controls=[
                            Container(
                                expand=1,
                                content=self.caja_configuracion_serial_thunder
                            ),
                            Column(
                                expand=2,
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
                    self.container_user_options,
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
        page.title = "Login Interface"
        #page.theme = flet.theme.Theme(color_scheme_seed="pink")
        theme = flet.Theme()
        theme.page_transitions.windows = flet.PageTransitionTheme.CUPERTINO
        page.theme = theme
        page.window_left = 1000
        page.window_frameless = True
        page.window_maximized = True
        page.window_min_width = 1200
        page.window_min_height = 700

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
                                content=dashboard_interface,
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

        dashboard_interface = Dashboard(page)
        login_interface = LoginInterface(page)
        page.on_route_change = route_change
        # page.go(page.route)
        page.go("/sensores")

    flet.app(target=main, assets_dir="assets")  # view=flet.WEB_BROWSER
