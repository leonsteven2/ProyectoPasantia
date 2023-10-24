from flet import (
    app,
    BoxShadow,
    alignment,
    ShadowBlurStyle,
    border,
    MainAxisAlignment,
    FilePicker,
    FilePickerResultEvent,
    ProgressBar,
    CircleAvatar,
    Dropdown,
    dropdown,
    Icon,
    Page,
    NavigationRail,
    NavigationRailDestination,
    padding,
    IconButton,
    TextStyle,
    Slider,
    TextThemeStyle,
    FontWeight,
    TextAlign,
    colors,
    ScrollMode,
    UserControl,
    Container,
    icons,
    ElevatedButton,
    DataTable,
    DataColumn,
    DataRow,
    DataCell,
    SafeArea,
    Text,
    Column,
    TextField,
    Row,
    TextButton,
)
import pymysql
from time import sleep, strftime
from datetime import datetime, timedelta
import serial
from pandas import DataFrame
from xlwings import apps
import keyboard

from ModernLineChart import ModernLineChart
import credenciales


def CajaTextoConIcono(label, src_image=None, password=None, icon=None, valor=None):
    icon_caja = Icon(
        name=icon,
        color=colors.WHITE,
        size=30,
    )
    txt_caja = TextField(
        label=label,
        value=valor,
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

class Dashboard(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        # Creamos la gráfica
        self.chart_thunder = ModernLineChart(max_x_range=15)

        # Creamos la caja de setpoint
        self.setpoint_box = SetpointBox(page=self.page)

        # Creamos las cajas de configuración serial para cada dispositivo
        self.caja_configuracion_serial_thunder = DeviceComunication(titulo="Thunder Scientific", default_baud="9600",
                                                               page=self.page, data="Thunder", grafica=self.chart_thunder, setpoint=self.setpoint_box)
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
                        alignment=MainAxisAlignment.CENTER
                    ),
                    NavigationRail(
                        selected_index=0,
                        group_alignment=-0.8,
                        bgcolor=colors.TRANSPARENT,
                        expand=1,
                        min_extended_width=170,
                        min_width=80,
                        extended=False,
                        destinations=[
                            NavigationRailDestination(
                                icon=icons.DASHBOARD,
                                label_content=Text("Panel", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
                            ),
                            NavigationRailDestination(
                                icon=icons.SETTINGS,
                                label_content=Text("Settings", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
                            ),
                        ],
                        on_change=self.destination_changed
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
                        alignment=MainAxisAlignment.CENTER
                    )

                ],
            )
        )
        self.container_panel = Column(
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
                                    padding = padding.only(top=15, right=10),
                                    expand=4,
                                    #clip_behavior=ClipBehavior.HARD_EDGE,
                                    bgcolor=colors.BLACK87,
                                    content=self.chart_thunder
                                )
                            ]
                        )

                    ],

                )
            ]
        )

        self.container_dashboard = Container(
            expand=7,
            content=self.container_panel
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

        # Creamos la caja de settings
        self.cont_settings = Settings(self.page)

    def build(self):
        pass
        return self.container_main

    def return_to_login_page(self, event):
        self.page.go("/")

    def destination_changed(self, e):
        if e.control.selected_index == 0:
            self.container_dashboard.content = self.container_panel

        if e.control.selected_index == 1:
            self.container_dashboard.content = self.cont_settings
        self.page.update(self)


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
        self.tiempo_muestreo = 2

        # Variables de tiempo para bucles
        self.minutos_actual = None
        self.segundos_actual = None

        # Variables para exportar a excel en tiempo real
        self.contador_excel_HR = 0
        self.contador_excel_temp = 0
        self.bool_exportar_excel = False
        self.bool_HR_excel = False
        self.bool_Temp_excel = False
        self.actual_row_excel = None
        self.actual_column_excel = None
        self.actual_sheet_excel = None

        self.actual_row_excel_2 = None
        self.actual_column_excel_2 = None
        self.actual_sheet_excel_2 = None
        keyboard.hook(self.detect_keyboard_command)

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
        # Ocultamos los diálogos en el Overlay
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
        # Creamos el botón para resetear los datos del dataframe
        self.btn_reset_dataframe = IconButton(
            icon=icons.RESTART_ALT,
            icon_color="white",
            disabled=True,
            on_click=self.resetear_dataframe
        )
        # Creamos el botón para salir de la comunicación serial
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
            value="Digite el tiempo de muestreo:",
            color="yellow",
            style=TextThemeStyle.LABEL_LARGE,
        )
        # Creamos el campo de texto para introducir el tiempo
        self.txt_time_period = TextField(value=2, suffix_text="seg", expand=1)

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
        self.lbl_setpoint = Text(
            "Setpoint!",
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

            self.datos_mysql_thunder = [
                'fecha', 'hora',
                'rh_pc_sp', 'rh_pc', 'unit_rh_pc',
                'rh_pctc_sp', 'rh_pctc', 'unit_pctc',
                'satur_pressure_sp', 'satur_pressure', 'unit_satur_pressure',
                'chmbr_pressure', 'unit_chmbr_pressure',
                'satur_temp_sp', 'satur_temp', 'unit_satur_temp',
                'chmbr_temp', 'unit_chmbr_temp',
                'flow_sp', 'flow', 'unit_flow',
                'id_equipo']

            self.df_datos_thunder = DataFrame(columns=self.datos_mysql_thunder)

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
            # Escondemos boton de mysql
            self.btn_send_data_cloud.visible = False

            # Variables internas
            self.txt_RH_473_actual = Text("0")
            self.txt_DewPoint_473_actual = Text("0")
            self.txt_ExternalTemp_473_actual = Text("0")

            self.df_datos_473 = DataFrame(columns=['hora','fecha','RH', 'DewPoint', 'Ext. Temp'])

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
            # Escondemos boton de mysql
            self.btn_send_data_cloud.visible = False

            # Variables internas
            self.txt_temp1_actual = Text("0")
            self.txt_temp2_actual = Text("0")

            self.txt_RH1_actual = Text("0")
            self.txt_RH2_actual = Text("0")

            self.df_datos_fluke = DataFrame(columns=['hora','fecha','Temp1', 'RH1', 'Temp2', 'RH2'])

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

        # Creamos un índice general para los dataframe
        self.dataframe_indice = 0

        # Creamos la columna principal que contiene el título, configuracion serial y tablas
        self.col_main = Column(
            expand=1,
            spacing=15,
            scroll=ScrollMode.HIDDEN,
            controls=[
                Row(controls=[
                    Text(value=self.titulo, text_align=TextAlign.CENTER, weight=FontWeight.BOLD,
                         style=TextThemeStyle.TITLE_LARGE)],
                    alignment=MainAxisAlignment.CENTER
                ),
                self.row_baud_port,
                Row(
                    controls=[
                        self.txt_user_help,
                        self.txt_time_period
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                self.progress_bar,
                self.row_data_buttons,
                Row(
                    controls=[
                        self.data_table
                    ],
                    alignment=MainAxisAlignment.CENTER
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
        bool_tiempo_muestreo = False
        # Verificamos si el tiempo de muestreo fue digitado correctamente
        try:
            self.tiempo_muestreo = int(self.txt_time_period.value)
            bool_tiempo_muestreo = True
        except:
            bool_tiempo_muestreo = False


        # Validamos que exista un puerto COM
        if self.drop_PORT.value != None and bool_tiempo_muestreo:
            self.progress_bar.color = "amber"
            self.progress_bar.value = None
            self.txt_user_help.value = f"Conectando por {self.drop_PORT.value} ..."
            self.txt_user_help.color = None
            self.txt_time_period.visible = False
            self.page.update(self)
            sleep(1)
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
            sleep(self.tiempo_muestreo)
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
                    sleep(1)

                    if float(self.setpoint_box.txt_RH_PcTc.value) > 1:
                        mensaje = f"R2={self.setpoint_box.txt_RH_PcTc.value}\r"
                        self.enviar_setpoint(mensaje=mensaje)
                    sleep(1)

                    if float(self.setpoint_box.txt_sat_pressure.value) > 1:
                        mensaje = f"PS={self.setpoint_box.txt_sat_pressure.value}\r"
                        self.enviar_setpoint(mensaje=mensaje)
                    sleep(1)

                    if float(self.setpoint_box.txt_sat_temp.value) > 1:
                        mensaje = f"TS={self.setpoint_box.txt_sat_temp.value}\r"
                        self.enviar_setpoint(mensaje=mensaje)
                    sleep(1)

                    if float(self.setpoint_box.txt_flow_rate.value) > 1:
                        mensaje = f"FS={self.setpoint_box.txt_flow_rate.value}\r"
                        self.enviar_setpoint(mensaje=mensaje)
                    sleep(1)

                    self.setpoint_box.bool_enviar_datos = False


                # Guardamos en el dataframe si se presiono el boton registrar
                try:
                    if self.bool_registrar_datos:

                        hora = strftime("%H:%M:%S")
                        fecha = strftime("20%y-%m-%d")
                        self.dataframe_indice = self.df_datos_thunder.shape[0] + 1
                        self.df_datos_thunder.loc[self.dataframe_indice] = [
                            fecha, hora,
                            self.txt_RH_Pc_setpoint.value, self.txt_RH_Pc_actual.value, "%HR",
                            self.txt_RH_PcTc_setpoint.value, self.txt_RH_PcTc_actual.value, "%HR",
                            self.txt_saturation_pressure_setpoint.value, self.txt_saturation_pressure_actual.value, "psi",
                            self.txt_chamber_pressure_actual.value, "psi",
                            self.txt_saturation_temp_setpoint.value, self.txt_saturation_temp_actual.value, "C",
                            self.txt_chamber_temp_actual.value, "C",
                            self.txt_flow_rate_setpoint.value, self.txt_flow_rate_actual.value, "l/m", "L0038"
                        ]
                        self.txt_user_help.value = f"Datos registrados: {self.dataframe_indice}"
                        self.txt_user_help.color = "green"
                except Exception as e:
                    print(f'Error: {e}')

                # Graficar
                try:
                    self.grafica.draw_points(y_value=self.txt_RH_Pc_actual.value)
                    self.grafica.draw_points2(y_value=self.txt_RH_Pc_setpoint.value)

                except Exception as e:
                    print(f"No se pudo graficar: {e}")

                self.col_main.update()

            except Exception as e:
                print(e)
                self.conexion_serial_fallida(error=e)
                break

    def adquisicion_datos_473(self):
        tiempo_futuro = datetime.now()
        bool_aux = True

        while True:
            if self.bool_registrar_datos or self.bool_HR_excel or self.bool_Temp_excel:
                tiempo_actual = datetime.now()

                if self.bool_HR_excel and self.contador_excel_HR == 0 and not self.bool_Temp_excel:
                    bool_aux = True

                if self.bool_Temp_excel and self.contador_excel_temp == 0 and not self.bool_HR_excel:
                    bool_aux = True

                if tiempo_futuro.strftime('%H:%M:%S') == tiempo_actual.strftime('%H:%M:%S') or bool_aux:
                    tiempo_futuro = tiempo_actual + timedelta(seconds=int(self.tiempo_muestreo))
                    bool_aux = False

                    try:
                        mensaje = "RH?\r"
                        self.comunicacion_serial.write(mensaje.encode())
                        mensaje_desde_473 = self.comunicacion_serial.readline().decode()
                        try:
                            self.txt_RH_473_actual.value = str(mensaje_desde_473).strip()
                        except:
                            pass

                        mensaje = "DP?\r"
                        self.comunicacion_serial.write(mensaje.encode())
                        mensaje_desde_473 = self.comunicacion_serial.readline().decode()
                        try:
                            self.txt_DewPoint_473_actual.value = str(mensaje_desde_473).strip()
                        except:
                            pass

                        mensaje = "Tx?\r"
                        self.comunicacion_serial.write(mensaje.encode())
                        mensaje_desde_473 = self.comunicacion_serial.readline().decode()
                        try:
                            self.txt_ExternalTemp_473_actual.value = str(mensaje_desde_473).strip()
                        except:
                            pass

                        self.page.update(self)
                        # Guardamos en el dataframe si se presiono el boton registrar
                        try:
                            if self.bool_registrar_datos:
                                # Registro de datos en el dataframe
                                hora = strftime("%H:%M:%S")
                                fecha = strftime("20%y-%m-%d")
                                self.dataframe_indice = self.df_datos_473.shape[0] + 1
                                self.df_datos_473.loc[self.dataframe_indice] = [
                                    hora,
                                    fecha,
                                    self.txt_RH_473_actual.value,
                                    self.txt_DewPoint_473_actual.value,
                                    self.txt_ExternalTemp_473_actual.value
                                ]
                        except:
                            pass

                        # Registro de datos en el Excel
                        try:
                            # Envió de datos
                            app = apps.active
                            if app and self.bool_HR_excel:
                                if self.contador_excel_HR == 0:
                                    self.actual_row_excel = app.selection.row
                                    self.actual_column_excel = app.selection.column
                                    self.actual_sheet_excel = app.selection.sheet
                                self.actual_sheet_excel.range(self.actual_row_excel + self.contador_excel_HR, self.actual_column_excel).value = self.txt_RH_473_actual.value
                                self.contador_excel_HR += 1
                                if self.contador_excel_HR == 5:
                                    self.bool_HR_excel = False
                                    self.contador_excel_HR = 0

                            if app and self.bool_Temp_excel:
                                if self.contador_excel_temp == 0:
                                    self.actual_row_excel_2 = app.selection.row
                                    self.actual_column_excel_2 = app.selection.column
                                    self.actual_sheet_excel_2 = app.selection.sheet
                                self.actual_sheet_excel_2.range(self.actual_row_excel_2 + self.contador_excel_temp, self.actual_column_excel_2).value = self.txt_ExternalTemp_473_actual.value
                                self.contador_excel_temp += 1
                                if self.contador_excel_temp == 5:
                                    self.bool_Temp_excel = False
                                    self.contador_excel_temp = 0

                                # self.actual_sheet_excel.range(celda_activa.row + self.contador_excel,
                                #                           celda_activa.column + 1).value = self.txt_DewPoint_473_actual.value
                                # self.actual_sheet_excel.range(celda_activa.row + self.contador_excel,
                                #                           celda_activa.column + 2).value = self.txt_ExternalTemp_473_actual.value


                        except Exception as e:
                            print(e)

                        # Se muestra el registro
                        self.txt_user_help.value = f"Registro: {self.dataframe_indice} - Excel (HR = {self.bool_HR_excel}) (Temp = {self.bool_Temp_excel})"
                        self.txt_user_help.color = "green"
                        self.txt_user_help.update()

                    except Exception as e:
                        self.conexion_serial_fallida(error=e)
                        break


            sleep(1)



    def adquisicion_datos_fluke(self):
        while True:
            sleep(self.tiempo_muestreo)
            try:
                mensaje = "READ? \r"
                self.comunicacion_serial.write(mensaje.encode())
                mensaje_desde_fluke = self.comunicacion_serial.readline().decode()

                try:
                    mensaje_desde_fluke = mensaje_desde_fluke.strip().split(",")
                    if mensaje_desde_fluke[0] == "READ?":
                        continue
                    self.txt_temp1_actual.value = mensaje_desde_fluke[0].strip()
                    self.txt_temp2_actual.value = mensaje_desde_fluke[1].strip()
                    self.txt_RH1_actual.value = mensaje_desde_fluke[2].strip()
                    self.txt_RH2_actual.value = mensaje_desde_fluke[3].strip()
                except Exception as e:
                    print(f"Error en split o strip de fluke: {e}")

                self.page.update(self)

                # Guardamos datos
                # Guardamos en el dataframe si se presiono el boton registrar
                try:
                    if self.bool_registrar_datos:
                        hora = strftime("%H:%M:%S")
                        fecha = strftime("20%y-%m-%d")
                        self.dataframe_indice = self.df_datos_fluke.shape[0] + 1
                        self.df_datos_fluke.loc[self.dataframe_indice] = [
                            hora,
                            fecha,
                            mensaje_desde_fluke[0].strip(),
                            mensaje_desde_fluke[1].strip(),
                            mensaje_desde_fluke[2].strip(),
                            mensaje_desde_fluke[3].strip(),
                        ]
                        self.txt_user_help.value = f"Datos registrados: {self.dataframe_indice}"
                        self.txt_user_help.color = "green"
                        self.txt_user_help.update()
                except:
                    pass

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
        self.txt_time_period.visible = True
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
        self.btn_iniciar_registro_datos.bgcolor = "green"
        self.bool_registrar_datos = False

        self.bool_exportar_excel = False
        self.contador_excel_HR = 0
        self.contador_excel_temp = 0

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
                table_name = "lab_humedad"

                df = self.df_datos_thunder

                comando_mysql_inicio = f"INSERT INTO {table_name}\n("
                for dato in self.datos_mysql_thunder:
                    comando_mysql_inicio += dato + ","
                comando_mysql_inicio = comando_mysql_inicio[:-1] + ")\n"

                comando_mysql_final = f"VALUES\n"
                for i in range(0, len(df)):
                    comando_mysql_final = comando_mysql_final + "("
                    for dato in self.datos_mysql_thunder:
                        comando_mysql_final += f"'{df[dato].iloc[i]}'" + ","
                    comando_mysql_final = comando_mysql_final[:-1] + ""
                    comando_mysql_final += "),\n"

                comando_mysql_final = comando_mysql_final[:-2] + ";"

                comando_sql = comando_mysql_inicio + comando_mysql_final

                cursor.execute(comando_sql)
                database.commit()

                self.txt_user_help.value = "Datos enviados a MYSQL"
                self.txt_user_help.update()

        except Exception as e:
            print(e)
            self.txt_user_help.value = e
            self.txt_user_help.color = "red"

    def detect_keyboard_command(self, e):

        if e.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('ctrl') and keyboard.is_pressed('mayusculas') and keyboard.is_pressed('H'):
            self.bool_HR_excel = True if self.bool_HR_excel == False else False
            print(self.bool_HR_excel)
            self.contador_excel_HR = 0 if self.bool_HR_excel == False else self.contador_excel_HR

        if e.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('ctrl') and keyboard.is_pressed('mayusculas') and keyboard.is_pressed('T'):
            self.bool_Temp_excel = True if self.bool_Temp_excel == False else False
            self.contador_excel_temp = 0 if self.bool_Temp_excel == False else self.contador_excel_temp








class Settings(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

        # Caja de MYSQL Database
        self.txt_host = CajaTextoConIcono(label="HOST", icon=icons.HOME, valor="192.168.20.63")
        self.txt_user = CajaTextoConIcono(label="USER", icon=icons.PERSON, valor="inenDB_ca")
        self.txt_password = CajaTextoConIcono(label="PASSWORD", password=True, icon=icons.SECURITY, valor="INEN@4636server")
        self.txt_database = CajaTextoConIcono(label="DATABASE", icon=icons.DATASET, valor="db_test_inen")

        self.cont_mysql_settings = Container(
            width=300,
            height=450,
            padding=padding.all(25),
            shadow=BoxShadow(
                spread_radius=0,
                blur_radius=5,
                color="white",
                blur_style=ShadowBlurStyle.OUTER,
            ),
            border_radius=25,
            border=border.all(width=3, color="white"),
            bgcolor=colors.with_opacity(opacity=0.75, color="black"),
            content=Column(
                horizontal_alignment="center",
                controls=[
                    Text("MYSQL Database", color="yellow", weight="w700", style=TextThemeStyle.HEADLINE_SMALL),
                    self.txt_host,
                    self.txt_user,
                    self.txt_password,
                    self.txt_database,
                    ElevatedButton("Guardar", color="white", on_click=self.save_mysql_configuration, icon=icons.CHECK, icon_color="white")
                ]
            )
        )

        # Contenedor principal
        self.cont_main = Container(
            #bgcolor="blue",
            alignment=alignment.center,
            expand=True,
            content=Row(
                alignment="center",
                expand=1,
                spacing=25,
                controls=[
                    self.cont_mysql_settings,
                ]
            ),
        )

    def build(self):
        return self.cont_main

    def save_mysql_configuration(self, e):
        credenciales.host = self.txt_host.controls[1].value
        credenciales.user = self.txt_user.controls[1].value
        credenciales.password = self.txt_password.controls[1].value
        credenciales.database = self.txt_database.controls[1].value
        e.control.icon_color = "green"
        e.control.color = "green"
        e.control.update()
        sleep(1)
        e.control.icon_color = "white"
        e.control.color = "white"
        e.control.update()


if __name__ == "__main__":
    def main(page: Page):
        page.title = "Laboratorio de Humedad"
        page.window_left = 1000
        page.window_frameless = True
        page.window_maximized = True
        page.window_min_width = 1200
        page.window_min_height = 700

        dashboard_interface = Dashboard(page)

        page.add(
            SafeArea(
                content=dashboard_interface,
                expand=True,
            )
        )

    app(target=main, assets_dir="assets")
