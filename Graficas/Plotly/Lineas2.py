import plotly.express as px
import pandas as pd

df = pd.DataFrame(dict(
    x = [0,1],
    y = [0,1]
))
fig = px.line(df, x="x", y="y", title="Unsorted Input")
fig.show()

