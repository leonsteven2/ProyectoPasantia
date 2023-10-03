from flet import Page, app, DataTable, ScrollMode, Divider, DataCell, DataRow, DataColumn, border, TextField, MaterialState, ButtonStyle, NavigationRail, VerticalDivider, CrossAxisAlignment, TextButton, NavigationRailDestination, padding, CircleAvatar, Row, Column, TextThemeStyle, alignment, FontWeight, ElevatedButton, TextAlign, MainAxisAlignment, UserControl, ThemeMode, Container, AppBar, Icon, Text, IconButton, icons, colors

from pandas import DataFrame
from plotly.express import line
from flet.plotly_chart import PlotlyChart

def container_graphics(expansion=1):
    df = DataFrame(columns=["value, setpoint"])

    print(type(df))
    data = {
        "x": [1,2,3,4,5],
        "y": [10,20,15,30,11]
    }

    data2 = {
        "x": [1, 0, 5, 3, 1],
        "y": [1, 2, 1, 3, 100]
    }

    chart1 = line(x=data["x"],y=data["y"], markers=True)

    cont_graphics = Container(
        bgcolor="#3B3B3B",
        expand=expansion,
        alignment=alignment.center,
        content=Column(
            horizontal_alignment="center",
            controls=[
                Text("Gráficas", style=TextThemeStyle.HEADLINE_SMALL, weight=FontWeight.BOLD, color="white"),
                PlotlyChart(chart1, expand=True)
            ]
        )
    )
    return cont_graphics

def container_data_monitoreo(expansion=1):
    def data_row(parameter, value, unit):
        data_row = DataRow(
            cells=[
                DataCell(Text(parameter)),
                DataCell(Text(value)),
                DataCell(Text(unit))
            ]
        )
        return data_row

    cont_data_monitoreo = Container(
        expand=expansion,
        padding=padding.only(top=10, left=10, right=10),
        bgcolor="#3B3B3B",
        alignment=alignment.top_center,
        content=Column(
            scroll=ScrollMode.HIDDEN,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                Text("Monitoreo de Datos", style=TextThemeStyle.HEADLINE_SMALL, weight=FontWeight.BOLD, color="white"),
                DataTable(
                    columns=[
                        DataColumn(Text("Parámetro", weight=FontWeight.BOLD)),
                        DataColumn(Text("Valor",weight=FontWeight.BOLD),numeric=True),
                        DataColumn(Text("Unidad", weight=FontWeight.BOLD)),
                    ],
                    rows=[
                        data_row("Patron","0","NaN"),
                        data_row("Equipo1", "0","NaN"),
                        data_row("Equipo2", "0","NaN"),
                        data_row("Temperatura", "0", "°C"),
                        data_row("Humedad", "0", "%"),
                        data_row("Presión", "0", "°atm")
                    ]
                ),
            ]
        )
    )
    return cont_data_monitoreo

def container_information(expansion=1):
    def data_row(parameter, description):
        data_row = DataRow(
            cells=[
                DataCell(Text(parameter)),
                DataCell(Text(description)),
            ]
        )
        return data_row

    cont_info = Container(
        expand=expansion,
        padding=padding.only(top=10, left=10, right=10),
        bgcolor="#3B3B3B",
        alignment=alignment.top_center,
        content=Column(
            scroll=ScrollMode.HIDDEN,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                Text("Información", style=TextThemeStyle.HEADLINE_SMALL, weight=FontWeight.BOLD, color="white"),
                DataTable(
                    columns=[
                        DataColumn(Text("Parámetros", weight=FontWeight.BOLD)),
                        DataColumn(Text("Descripción")),
                    ],
                    rows=[
                        data_row("Equipo","Dewk Point Mirror"),
                        data_row("Modelo", "473"),
                        data_row("Serie", "12345-6"),
                        data_row("Salida", "Analógico/Digital")
                    ]
                ),
            ]
        )
    )
    return cont_info

def top_container(expansion=1):
    btn_style = ButtonStyle(
        color="white",
        bgcolor={MaterialState.HOVERED: "#65B744", "": "#8B8B8B"},
        shadow_color="white"
    )

    cont_top = Container(
        bgcolor="#3B3B3B",
        #bgcolor="#1F1F1F",
        #bgcolor=colors.TRANSPARENT,
        padding=padding.only(left=25, right=25),
        expand=expansion,
        content=Row(
            controls=[
                Text("Laboratorio Presión", style=TextThemeStyle.HEADLINE_SMALL, weight=FontWeight.BOLD),
                Row(
                    expand=1,
                    alignment=MainAxisAlignment.END,
                    controls=[
                        ElevatedButton("Información", style=btn_style),
                        ElevatedButton("Monitoreo", style=btn_style),
                        ElevatedButton("Control", style=btn_style),
                        VerticalDivider(),
                        ElevatedButton("Laboratorios", bgcolor="white", color="green")
                    ],

                )
            ]
        )
    )
    return cont_top

def container_navigation_riel():
    def resize_navigation_riel(e):
        print("entra")
        nav_riel.extended = False if nav_riel.extended == True else True
        icon_resize_nav_riel.icon = icons.ARROW_FORWARD if icon_resize_nav_riel.icon == icons.ARROW_BACK else icons.ARROW_BACK
        icon_resize_nav_riel.update()
        nav_riel.update()

    nav_riel = NavigationRail(
        selected_index=1,
        group_alignment=-0.5,
        bgcolor=colors.TRANSPARENT,
        #bgcolor="red",
        expand=1,
        min_extended_width=170,
        min_width=80,
        extended=False,
        destinations=[
            NavigationRailDestination(
                icon=icons.HOME,
                # icon=Icon(icons.HOME),
                label_content=Text("Home", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
            ),
            NavigationRailDestination(
                icon=icons.DASHBOARD,
                label_content=Text("Panel", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
            ),
            NavigationRailDestination(
                icon=icons.NEWSPAPER,
                label_content=Text("Report", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS,
                label_content=Text("Settings", style=TextThemeStyle.BODY_LARGE, weight=FontWeight.BOLD),
            ),
        ],
        # on_change=lambda e: print("Selected destination:", e.control.selected_index)
        # on_change=self.destination_changed
    )

    icon_resize_nav_riel = IconButton(icons.ARROW_FORWARD, on_click=resize_navigation_riel)

    contenedor = Container(
        bgcolor="#3B3B3B",
        #padding=padding.all(5),
        alignment=alignment.center,
        content=Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                Text(""),
                Row(
                    controls=[
                        CircleAvatar(
                            content=Icon(icons.PERSON, size=45, color="#1F1F1F"),
                            color=colors.BLUE_GREY_700,
                            bgcolor=colors.BLUE_GREY_100,
                            width=60,
                            height=60,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                nav_riel,
                Row(
                    controls=[
                        icon_resize_nav_riel
                    ]
                ),
                Row(
                    controls=[
                        TextButton(
                            content=Row(
                                controls=[
                                    Icon(icons.LOGOUT_OUTLINED),
                                    Text("Salir", weight=FontWeight.BOLD, style=TextThemeStyle.BODY_LARGE)
                                ]
                            ),
                            #on_click=self.return_to_login_page,
                        )
                    ],
                    alignment=MainAxisAlignment.CENTER
                ),
                Text("")

            ],
        )
    )
    return contenedor

class Dashboard(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.page.padding = 0

        self.cont_navigation_riel = container_navigation_riel()

        self.row_main = Row(
            expand=1,
            spacing=1,
            controls=[
                self.cont_navigation_riel,
                Column(
                    expand=1,
                    spacing=1,
                    controls=[
                        top_container(expansion=1),
                        Row(
                            expand=10,
                            spacing=1,
                            controls=[
                                Column(
                                    expand=3,
                                    spacing=1,
                                    controls=[
                                        container_information(expansion=3),
                                        container_data_monitoreo(expansion=5)
                                    ]
                                ),
                                container_graphics(expansion=5),
                                Container(bgcolor="#3B3B3B", expand=3)
                            ]
                        )

                    ]
                )
            ]
        )

    def build(self):
        pass
        return self.row_main

    def check_item_clicked(self, e):
        e.control.checked = not e.control.checked
        self.page.update()

    def change_theme(self, e):
        self.page.theme_mode = ThemeMode.DARK if str(self.page.theme_mode) == "ThemeMode.LIGHT" else ThemeMode.LIGHT
        self.page.update()

    def encabezado_container(self, texto):
        encabezado = Text(
            texto,
            style=TextThemeStyle.HEADLINE_SMALL,
            weight=FontWeight.BOLD, color="red"
        )
        return encabezado

def main(page: Page):
    page.theme_mode = ThemeMode.DARK
    page.window_maximized = True

    dash = Dashboard(page=page)



    page.add(
        Container(
            expand=True,
            content=dash,
            padding=5,
        )
    )

app(target=main)
