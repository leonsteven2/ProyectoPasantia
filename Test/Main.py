import flet
from flet import Page, app, Row, AppBar, Column, Container, Icon, icons, Text, colors, FontWeight

if __name__ == "__main__":
  def main(page: Page):
    page.title = "Example"
    page.window_maximized = True
    page.padding = 0
    page.window_left = 1000
    #page.theme_mode = flet.ThemeMode.LIGHT

    # Creamos el App Bar (el recuadro gris superior de la interfaz)
    app_bar = AppBar(
      leading=Icon(icons.SCHEMA),
      title=Text("Laboratorio Humedad", weight=FontWeight.BOLD),
      center_title=False,
      bgcolor=colors.SURFACE_VARIANT

    )
    page.appbar = app_bar

    # Creamos la columna de informacion
    col_informacion = Column(
      expand=2,
      controls=[
        Container(
          expand=1,
          bgcolor="blue",
          content=Text("Hola"),
          alignment=flet.alignment.center
        ),
      ]
    )

    # Creamos la columna de graficas
    col_graficas = Column(
      expand=5,
      controls=[
        Container(
          expand=1,
          bgcolor="pink",
          content=Text("Col graficas"),
          alignment=flet.alignment.center
        ),
      ]
    )

    # Creamos la columna de indicadores
    col_indicadores = Column(
      expand=2,
      controls=[
        Container(
          expand=1,
          bgcolor="grey",
          content=Text("Indicadores"),
          alignment=flet.alignment.center
        ),
      ]
    )

    row_principal = Row(
      expand=1,
      controls=[
        col_informacion,
        col_graficas,
        col_indicadores,
        col_graficas
      ]
    )

    page.add(
      row_principal
    )
    page.update()

  app(target=main)

