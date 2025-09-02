import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
from pathlib import Path

# --- Load CSV (robust path logic) ---
def load_spacex_csv(filename="spacex_launch_dash.csv"):
    base = Path(__file__).resolve().parent if '__file__' in globals() else Path.cwd()
    for p in [base/filename, base.parent/filename, base/"data"/filename]:
        if p.exists():
            print(f"Loading: {p}")
            return pd.read_csv(p)
    raise FileNotFoundError("CSV not found")

spacex_df = load_spacex_csv()
PAYLOAD_COL = 'Payload Mass (kg)'   # <- make sure this matches your CSV exactly

# --- App + layout ---
app = dash.Dash(__name__)

options = [{'label': 'All Sites', 'value': 'ALL'}] + \
          [{'label': s, 'value': s} for s in spacex_df['Launch Site'].unique()]

app.layout = html.Div([
    dcc.Dropdown(
        id='site-dropdown',
        options=options,
        value='ALL',
        searchable=True,
        placeholder='Select a Launch Site'
    ),
    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[spacex_df[PAYLOAD_COL].min(), spacex_df[PAYLOAD_COL].max()]
    ),
    dcc.Graph(id='success-pie-chart'),
    dcc.Graph(id='success-payload-scatter-chart')
])

# --- Callback: dropdown + slider -> pie chart ---
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_pie(selected_site, payload_range):
    low, high = payload_range
    # filter by payload range first
    dff = spacex_df[(spacex_df[PAYLOAD_COL] >= low) & (spacex_df[PAYLOAD_COL] <= high)]

    if selected_site == 'ALL':
        # successes per site (sum of class 0/1 == #success)
        agg = dff.groupby('Launch Site', as_index=False)['class'].sum()
        fig = px.pie(
            agg, names='Launch Site', values='class',
            title='Total Success Launches By Site (filtered by payload)'
        )
    else:
        dff = dff[dff['Launch Site'] == selected_site]
        counts = dff['class'].value_counts().reindex([1, 0], fill_value=0)
        pie_df = counts.rename(index={1: 'Success', 0: 'Failure'}).reset_index()
        pie_df.columns = ['Outcome', 'Count']
        fig = px.pie(
            pie_df, names='Outcome', values='Count',
            title=f'Total Success Launches for site {selected_site} (filtered by payload)'
        )
    return fig

# Column names used below – make sure they match your CSV exactly
PAYLOAD_COL = 'Payload Mass (kg)'
SITE_COL    = 'Launch Site'
CLASS_COL   = 'class'
BOOSTER_CAT = 'Booster Version Category'

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range

    # filter by payload range first
    dff = spacex_df[(spacex_df[PAYLOAD_COL] >= low) & (spacex_df[PAYLOAD_COL] <= high)]

    # then (optionally) by site
    if selected_site != 'ALL':
        dff = dff[dff[SITE_COL] == selected_site]
        title = f'Payload vs Success for site {selected_site}'
    else:
        title = 'Correlation between Payload and Success for All Sites'

    fig = px.scatter(
        dff,
        x=PAYLOAD_COL,
        y=CLASS_COL,
        color=BOOSTER_CAT,
        hover_data=[SITE_COL, BOOSTER_CAT, PAYLOAD_COL],
        title=title,
        labels={CLASS_COL: 'Class (0=Fail, 1=Success)', PAYLOAD_COL: 'Payload Mass (kg)'}
    )
    # keep y-axis at 0/1 to make the success/failure band clear
    fig.update_yaxes(tickmode='array', tickvals=[0, 1], range=[-0.2, 1.2])

    return fig


if __name__ == '__main__':
    app.run(debug=True)
