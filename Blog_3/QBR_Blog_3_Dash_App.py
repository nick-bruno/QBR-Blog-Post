##### QBR Blog 3 - Dash Application #####

### Import Libraries ###
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

### Initiate application ###t
app = dash.Dash(__name__)
#
df = pd.read_csv('qbr3_df.csv')

app.layout = html.Div(children=[
        html.H1(children='QBR Data Visualization'),
        html.Div(children="Choose a Quarterback to Analyze"),
        # Dropdown Menu
        dcc.Dropdown(id = 'qb_dropdown', 
                     options=[{'label':i, 'value':i} for i in df.name.unique().tolist()],
                     value='Peyton Manning',
                     searchable=True),
        html.Div(id='qb-dropdown-output'),
#        dash_table.DataTable(
#                df.to_dict('records'),
#                [{"name": i, "id": i} for i in df.columns]
#)
        ])
        
@app.callback(
    dash.dependencies.Output('qb-dropdown-output', 'children'),
    [dash.dependencies.Input('qb_dropdown', 'value')]
)

def update_output(value):
    return f'You have selected {value}'

#@app.callback(
#        dash.dependencies.Output('qb-dropdown-output','children'),
#        [dash.dependencies.Input('qb-dropdown','value')]
#    )
#
#def qb_summary_table(value):
#
#    summary_table = dash_table.DataTable(
#                    df.to_dict('records'),
#                    [{"name": i, "id": i} for i in df.columns]
#                    )
#    return summary_table

if __name__ == '__main__':
    app.run_server(port=8000, host="0.0.0.0", debug=True)
##    app.run_server(debug=False,
##                   port=8000)
#    app.run_server(
#            host="0.0.0.0")