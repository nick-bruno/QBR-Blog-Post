##### QBR Blog 3 - Dash Application #####

### Import Libraries ###
import pandas as pd
import numpy as np
import dash
from dash import html, dcc, dash, callback, Input, Output, State, dash_table
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
#from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

### Initiate application ###
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True

# # the style arguments for the sidebar. We use position:fixed and a fixed width
# SIDEBAR_STYLE = {
#     "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "16rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
# }

# # the styles for the main content position it to the right of the sidebar and
# # add some padding.
# CONTENT_STYLE = {
#     "margin-left": "18rem",
#     "margin-right": "2rem",
#     "padding": "2rem 1rem",
# }

### Read in Dataframe ###
df = pd.read_csv('qbr3_df.csv')

# Sort list of quarterbacks by Last Name #
names_list = df.name.unique()
sorted_names = sorted(names_list, key=lambda x: x.split()[1]) # makes it easier to search QBs

teams_list = df.Tm.unique()
sorted_teams = sorted(teams_list) # makes it easier to search Teams

### Set application layout ###
app.layout = html.Div(children=[
        html.H1(children='QBR Data Visualization', style={'textAlign':'center'}),
        html.Div(children="Choose a Quarterback to Analyze"),

        html.Div(children=[dcc.Dropdown(id = 'qb_dropdown', 
                     options=[{'label':i, 'value':i} for i in sorted_names],
                     placeholder = 'Select a Quarterback',
                     #value='Peyton Manning',
                     searchable=True)]),


        # Break between Dropdown and QB Summary table #
        html.Div([html.Br()]),

        # Dash Table that takes data and columns from qb_summary_table Callback #
        html.Div(children=[dash_table.DataTable(id='table')]),

        # Break #
        html.Div([html.Br()]),

        # Line Plot #
        dcc.Graph(id='graph'),

        html.Div([html.Br()]),

        html.Div(children="Choose a Team to Analyze"),

        html.Div(children=[dcc.Dropdown(id = 'team_dropdown', 
                     options=[{'label':i, 'value':i} for i in sorted_teams],
                     placeholder = 'Select a Team',
                     searchable=True)]),
                     #multi=True)]),

        html.Div([html.Br()]),

        # Dash Table that takes data and columns from qb_summary_table Callback #
        html.Div(children=[dash_table.DataTable(id='team-table')]),

        html.Div([html.Br()]),

        # Line Plot #
        dcc.Graph(id='team-graph'),


        ])
        
# @callback(
#     Output('qb-dropdown-output', 'children'),
#     Input('qb_dropdown', 'value')
# )

# def update_output(value):
#     return f'You have selected {value}'

@callback(
       Output('table','data'),
       Output('table', 'columns'),
       Input('qb_dropdown','value')
       )

def qb_summary_table(value):

    # Subset dataframe by quarterback selected
    qb_df = df[df.name.isin([value])]

    # Find average QBR and Passer Rating grouped by Year
    mean_gb = qb_df.groupby('Year')[['TOTAL QBR','Rate']].mean()
    mean_gb = mean_gb.reset_index()

    # Find number of games played by quarterback per year
    num_games = qb_df.groupby('Year')[['Rate']].count()
    num_games = num_games.reset_index()

    # Merge the mean and count dataframes into one merged_gb
    merged_gb = mean_gb.merge(num_games, how='inner', on='Year')

    # Set column names
    merged_gb.columns = ['Year','QBR','Passer Rating','Num Games']

    # Show all results to the second decimal place
    merged_gb['QBR'] = merged_gb['QBR'].map('{:.2f}'.format)
    merged_gb['Passer Rating'] = merged_gb['Passer Rating'].map('{:.2f}'.format)

    # Format data as a dictionary to populate dash_table
    data = merged_gb.to_dict('records')

    # Format columns to populate dash_table
    columns = [{'name': col, 'id': col} for col in merged_gb.columns]

    # Return the data and column names needed for dash_table
    return data, columns

@callback(
    Output('graph','figure'), 
    Input('qb_dropdown','value')
    )

def update_line_chart(value):
    # Subset dataframe by quarterback selected
    qb_df = df[df.name.isin([value])]

    # Find average QBR and Passer Rating grouped by Year
    mean_gb = qb_df.groupby('Year')[['TOTAL QBR','Rate']].mean()
    mean_gb = mean_gb.reset_index()

    # Find number of games played by quarterback per year
    num_games = qb_df.groupby('Year')[['Rate']].count()
    num_games = num_games.reset_index()

    # Merge the mean and count dataframes into one merged_gb
    merged_gb = mean_gb.merge(num_games, how='inner', on='Year')

    # Set column names
    merged_gb.columns = ['Year','QBR','Passer Rating','Num Games']

    # Show all results to the second decimal place
    merged_gb['QBR'] = merged_gb['QBR'].map('{:.2f}'.format).astype(float)
    merged_gb['Passer Rating'] = merged_gb['Passer Rating'].map('{:.2f}'.format).astype(float)

    # Create subplot with secondary axis
    subplot_fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig = px.line(merged_gb, x="Year", y="QBR", markers=True)
    fig.update_yaxes(range = [0,100])
    fig.update_layout(xaxis={'tickformat':'d'})

    fig1 = px.line(merged_gb, x="Year", y="Passer Rating", markers=True)
    fig1.update_yaxes(range = [0,159])
    fig1.update_layout(xaxis={'tickformat':'d'})

    fig1.update_traces(yaxis="y2")

    #Add the figs to the subplot figure
    subplot_fig.add_traces(fig.data + fig1.data)

    #FORMAT subplot figure
    subplot_fig.update_layout(title="QBR and Passer Rating Over Time", yaxis=dict(title="QBR"), yaxis2=dict(title="Passer Rating"), 
                              xaxis_title="Year", xaxis={'tickformat':'d'}, legend_title=value)
    subplot_fig.update_xaxes(nticks=merged_gb.shape[0])

    #RECOLOR so as not to have overlapping colors
    subplot_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    subplot_fig['data'][0]['showlegend']=True
    subplot_fig['data'][0]['name']='QBR'
    subplot_fig['data'][1]['showlegend']=True
    subplot_fig['data'][1]['name']='Passer Rating'

    return subplot_fig

@callback(
       Output('team-table','data'),
       Output('team-table', 'columns'),
       Input('team_dropdown','value')
       )

def team_summary_table(value):

    # Subset dataframe by quarterback selected
    qb_df = df[df.Tm.isin([value])]

    # Find average QBR and Passer Rating grouped by Year
    mean_gb = qb_df.groupby('Year')[['TOTAL QBR','Rate']].mean()
    mean_gb = mean_gb.reset_index()

    # Find number of games played by quarterback per year
    num_starters = qb_df.groupby('Year')[['name']].nunique()
    num_starters = num_starters.reset_index()

    # Merge the mean and count dataframes into one merged_gb
    merged_gb = mean_gb.merge(num_starters, how='inner', on='Year')

    # Set column names
    merged_gb.columns = ['Year','QBR','Passer Rating','Num QBs']

    # Show all results to the second decimal place
    merged_gb['QBR'] = merged_gb['QBR'].map('{:.2f}'.format)
    merged_gb['Passer Rating'] = merged_gb['Passer Rating'].map('{:.2f}'.format)

    # Format data as a dictionary to populate dash_table
    data = merged_gb.to_dict('records')

    # Format columns to populate dash_table
    columns = [{'name': col, 'id': col} for col in merged_gb.columns]

    # Return the data and column names needed for dash_table
    return data, columns

@callback(
    Output('team-graph','figure'), 
    Input('team_dropdown','value')
    )

def update_line_chart(value):
    # Subset dataframe by quarterback selected
    qb_df = df[df.Tm.isin([value])]

    # Find average QBR and Passer Rating grouped by Year
    mean_gb = qb_df.groupby('Year')[['TOTAL QBR','Rate']].mean()
    mean_gb = mean_gb.reset_index()

    # Find number of games played by quarterback per year
    num_games = qb_df.groupby('Year')[['Rate']].count()
    num_games = num_games.reset_index()

    # Merge the mean and count dataframes into one merged_gb
    merged_gb = mean_gb.merge(num_games, how='inner', on='Year')

    # Set column names
    merged_gb.columns = ['Year','QBR','Passer Rating','Num Games']

    # Show all results to the second decimal place
    merged_gb['QBR'] = merged_gb['QBR'].map('{:.2f}'.format).astype(float)
    merged_gb['Passer Rating'] = merged_gb['Passer Rating'].map('{:.2f}'.format).astype(float)

    # Create subplot with secondary axis
    subplot_fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig = px.line(merged_gb, x="Year", y="QBR", markers=True)
    fig.update_yaxes(range = [0,100])
    fig.update_layout(xaxis={'tickformat':'d'})

    fig1 = px.line(merged_gb, x="Year", y="Passer Rating", markers=True)
    fig1.update_yaxes(range = [0,159])
    fig1.update_layout(xaxis={'tickformat':'d'})

    fig1.update_traces(yaxis="y2")

    #Add the figs to the subplot figure
    subplot_fig.add_traces(fig.data + fig1.data)

    #FORMAT subplot figure
    subplot_fig.update_layout(title="QBR and Passer Rating Over Time", yaxis=dict(title="QBR"), yaxis2=dict(title="Passer Rating"), 
                              xaxis_title="Year", xaxis={'tickformat':'d'}, legend_title=value)
    subplot_fig.update_xaxes(nticks=merged_gb.shape[0])

    #RECOLOR so as not to have overlapping colors
    subplot_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    subplot_fig['data'][0]['showlegend']=True
    subplot_fig['data'][0]['name']='QBR'
    subplot_fig['data'][1]['showlegend']=True
    subplot_fig['data'][1]['name']='Passer Rating'

    return subplot_fig

# Run Server with local host to port 8000
if __name__ == '__main__':
    app.run_server(port=8000, host="0.0.0.0", debug=True)