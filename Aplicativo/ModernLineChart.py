from flet import (
    LineChart,
    LineChartDataPoint,
    LineChartData,
    Container,
    UserControl,
    colors,
    ChartAxis,
    alignment,
    LinearGradient,
    ChartCirclePoint,
    Animation,
    ChartPointLine,
)

class ModernLineChart(UserControl):
    def __init__(self, max_x_range=10):
        super().__init__()

        self.contador = 0
        self.max_x_range = max_x_range

        self.line_chart = LineChartData(
            color=colors.GREEN,
            stroke_width=2,
            stroke_cap_round=True,
            selected_below_line=ChartPointLine(
                width=0.5,
                color="white54",
                dash_pattern=[2, 4]
            ),
            point=True,
            curved=True,
            below_line_gradient=LinearGradient(
                begin=alignment.top_center,
                end=alignment.bottom_center,
                colors=[
                    colors.with_opacity(0.25, colors.GREEN),
                    "transparent"
                ]
            ),
            data_points=[
                LineChartDataPoint(
                    x=0,
                    y=0,
                    point=ChartCirclePoint(
                        radius=5,
                        color="white"
                    )
                ),
            ]
        )

        self.line_chart2 = LineChartData(
            color=colors.RED,
            stroke_width=2,
            stroke_cap_round=True,
            selected_below_line=ChartPointLine(
                width=0.5,
                color="white54",
                dash_pattern=[2, 4]
            ),
            point=True,
            curved=True,
            below_line_gradient=LinearGradient(
                begin=alignment.top_center,
                end=alignment.bottom_center,
                colors=[
                    colors.with_opacity(0.25, colors.RED),
                    "transparent"
                ]
            ),
            data_points=[
                LineChartDataPoint(x=0, y=0),
            ]
        )

        self.chart = LineChart(
            tooltip_bgcolor=colors.with_opacity(1, colors.WHITE),
            expand=True,
            animate=Animation(1000,"easeOut"),
            # min_y=0,
            # max_y=10,
            # min_x=0,
            # max_x=10,
            left_axis=ChartAxis(labels_size=40, labels_interval=10), #title=Text("asd")
            bottom_axis=ChartAxis(labels_size=40, labels_interval=1),
            data_series=[
                self.line_chart,
                self.line_chart2
            ]
        )

        self.cont_main = Container(
            expand=True,
            alignment=alignment.center,
            content=self.chart,
            #bgcolor="black"
        )

    def build(self):
        return self.cont_main

    def draw_points(self, x_value=None, y_value=None):
        # Verificamos el valor X
        try:
            x_value = float(x_value)
        except:
            x_value = None

        if x_value == None:
            self.contador = self.contador + 1
            x_value = self.contador

        # Limite de valores en x
        if len(self.line_chart.data_points) > self.max_x_range:
            self.line_chart.data_points.pop(0)

        # Verificamos el valor y
        try:
            y_value = float(y_value)
            # Añadimos los puntos nuevos
            self.line_chart.data_points.append(
                LineChartDataPoint(
                    x=x_value,
                    y=y_value,
                    point=ChartCirclePoint(
                        radius=5,
                        color="green"
                    )
                )
            )
            self.chart.update()
        except Exception as e:
            print("No se puede convertir Y en float y por tanto no se graficara")
            print(e)

    def draw_points2(self, x_value=None, y_value=None):
        # Verificamos el valor X
        try:
            x_value = float(x_value)
        except:
            x_value = None

        if x_value == None:
            x_value = self.contador

        # Limite de valores en x
        if len(self.line_chart2.data_points) > self.max_x_range:
            self.line_chart2.data_points.pop(0)

        # Verificamos el valor y
        try:
            y_value = float(y_value)
            # Añadimos los puntos nuevos
            self.line_chart2.data_points.append(
                LineChartDataPoint(
                    x=x_value,
                    y=y_value,
                    point=ChartCirclePoint(
                        radius=5,
                        color="red"
                    )
                )
            )
            self.chart.update()
        except:
            print("No se puede convertir Y en float y por tanto no se graficara")

