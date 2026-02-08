##### QBR_Blog_3_Dash_App.py #####
# Dash Application to visualize NFL QBR and Passer Rating statistics over time #

### Import Libraries ###
import pandas as pd
import numpy as np
from dash import html, dcc, dash, callback, Input, Output, State, dash_table
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

### Read in Dataframe ###
df = pd.read_csv('qbr3_df.csv')

# Sort names of QBs (last name) and Teams #
names_list = df.name.unique()
sorted_names = sorted(names_list, key=lambda x: x.split()[1]) # makes it easier to search QBs

teams_list = df.Tm.unique()
sorted_teams = sorted(teams_list) # makes it easier to search Teams

### Application Contents ###

## Left Tab Contents (Individual QB Analysis) ##
content1 = html.Div(children=[
        html.Div([html.Br()]),

        html.Div(children="Choose a Quarterback to Analyze"),

        html.Div([html.Br()]),

        # Dropdown to choose QB #
        html.Div(children=[dcc.Dropdown(id = 'qb_dropdown', 
                     options=[{'label':i, 'value':i} for i in sorted_names],
                     placeholder = 'Select a Quarterback',
                     searchable=True,
                     persistence = True,
                     style = {"background-color":"#151515", 'color':'Grey'})]),

        html.Div([html.Br()]),

        # Dash Table that takes data and columns from qb_summary_table Callback #
        html.Div(children=[dash_table.DataTable(id='table', style_cell_conditional=[{'textAlign':'left'}],
            style_header = {"background-color":"#151515"}, style_data={'color':'White', 'backgroundColor':'Black'})])

        ])

# Line Graph of average QBR and Passer Rating per year by individual QB (shown on right-hand side of the screen) #
content1_b = html.Div(children=[dcc.Graph(id='graph', style={'display': 'inline-block'})])

## Right Tab Contents (Team QB Analysis) ##
content2 = html.Div(children=[
        html.Div([html.Br()]),

        html.Div(children="Choose a Team to Analyze"),

        html.Div([html.Br()]),

        # Dropdown to choose Team #
        html.Div(children=[dcc.Dropdown(id = 'team_dropdown', 
                     options=[{'label':i, 'value':i} for i in sorted_teams],
                     placeholder = 'Select a Team',
                     searchable=True,
                     persistence = True,
                     style = {"background-color":"#151515", 'color':'Grey'})]),

        html.Div([html.Br()]),

        # Dash Table that takes data and columns from qb_summary_table Callback #
        html.Div(children=[dash_table.DataTable(id='team-table', style_cell_conditional=[{'textAlign':'left'}],
            style_header = {"background-color":"#151515"}, style_data={'color':'White', 'backgroundColor':'Black'})])

    ])

# Line Graph of average QBR and Passer Rating per year by Team (shown on left-hand side of the screen)
content2_b = html.Div(children=[dcc.Graph(id='team-graph', style={'display': 'inline-block'})])


### Initiate application ###
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY], title = 'QBR vs. Passer Rating')
app.config.suppress_callback_exceptions = True

## Create Application Layout with Content established above ##
app.layout = html.Div([
    html.Div([dcc.Location(id="url"),

    html.Div([html.Br()]),

    html.H1(children='QBR Data Visualization', style={'textAlign':'center'}),

    html.Div([html.Br()]),

    # Two tab options, one for QB and one for Team comparisons #
    dcc.Tabs(id="tabs", value='qb-tab', children=[
        dcc.Tab(label='Quarterback Comparison', value='qb-tab'),
        dcc.Tab(label='Team Comparison', value='team-tab'),
    ], colors={
        "border": "Black",
        "primary": "Black",
        "background": "Grey"}),

    html.Div(id='tabs-output')

])])

### Tabs Callback (QB or Teams) ###
@callback(Output('tabs-output', 'children'),
              Input('tabs', 'value'))

def render_content(tab):
    if tab == 'qb-tab':

        return html.Div(children=[dbc.Row([
        dbc.Col(
            dbc.Row([content1])),
        dbc.Col(
            dbc.Row([content1_b]))], 
        )])

    elif tab == 'team-tab':

        return html.Div(children=[dbc.Row([
        dbc.Col(
            dbc.Row([content2])),
        dbc.Col(
            dbc.Row([content2_b]))], 
        )])

### Content 1 QB Summary Table ###
@callback(
       Output('table','data'),
       Output('table', 'columns'), # outputs data and columns of data table
       Input('qb_dropdown','value')
       )

def qb_summary_table(value):

    # Subset dataframe by quarterback selected #
    qb_df = df[df.name.isin([value])]

    # Find average QBR and Passer Rating grouped by Year #
    mean_gb = qb_df.groupby('Year')[['TOTAL QBR','Rate']].mean()
    mean_gb = mean_gb.reset_index()

    # Find number of games played by quarterback per year #
    num_games = qb_df.groupby('Year')[['Rate']].count()
    num_games = num_games.reset_index()

    # Merge the mean and count dataframes into one merged_gb #
    merged_gb = mean_gb.merge(num_games, how='inner', on='Year')

    # Set column names #
    merged_gb.columns = ['Year','QBR','Passer Rating','Num Games']

    # Show all results to the second decimal place #
    merged_gb['QBR'] = merged_gb['QBR'].map('{:.2f}'.format)
    merged_gb['Passer Rating'] = merged_gb['Passer Rating'].map('{:.2f}'.format)

    # Format data as a dictionary to populate dash_table #
    data = merged_gb.to_dict('records')

    # Format columns to populate dash_table #
    columns = [{'name': col, 'id': col} for col in merged_gb.columns]

    # Return the data and column names needed for dash_table #
    return data, columns

### Content 1 QB Line Graph ###
@callback(
    Output('graph','figure'), 
    Input('qb_dropdown','value')
    )

def update_line_chart(value):
    # Subset dataframe by quarterback selected #
    qb_df = df[df.name.isin([value])]

    # Find average QBR and Passer Rating grouped by Year #
    mean_gb = qb_df.groupby('Year')[['TOTAL QBR','Rate']].mean()
    mean_gb = mean_gb.reset_index()

    # Find number of games played by quarterback per year #
    num_games = qb_df.groupby('Year')[['Rate']].count()
    num_games = num_games.reset_index()

    # Merge the mean and count dataframes into one merged_gb #
    merged_gb = mean_gb.merge(num_games, how='inner', on='Year')

    # Set column names #
    merged_gb.columns = ['Year','QBR','Passer Rating','Num Games']

    # Show all results to the second decimal place #
    merged_gb['QBR'] = merged_gb['QBR'].map('{:.2f}'.format).astype(float)
    merged_gb['Passer Rating'] = merged_gb['Passer Rating'].map('{:.2f}'.format).astype(float)

    # Create subplot with secondary axis #
    subplot_fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Initital QBR figure #
    fig = px.line(merged_gb, x="Year", y="QBR", markers=True)
    fig.update_yaxes(range = [0,100])
    fig.update_layout(xaxis={'tickformat':'d'})

    # Secondary Passer Rating figure #
    fig1 = px.line(merged_gb, x="Year", y="Passer Rating", markers=True)
    fig1.update_yaxes(range = [0,159])
    fig1.update_layout(xaxis={'tickformat':'d'})
    fig1.update_traces(yaxis="y2")

    #Add the initial and secondary figures to the subplot figure to create one figure #
    subplot_fig.add_traces(fig.data + fig1.data)

    if value is None:
        title_name = 'QBR and Passer Rating Over Time'
    else:
        title_name = "{} QBR and Passer Rating Over Time".format(value)

    subplot_fig.update_layout(title_text=title_name, title_x=0.5, yaxis=dict(title="QBR"), yaxis2=dict(title="Passer Rating"), 
                              xaxis_title="Year", xaxis={'tickformat':'d'}, legend_title=value, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font_color = 'White')
    subplot_fig.update_xaxes(nticks=merged_gb.shape[0])

    # RECOLOR so as not to have overlapping colors #
    subplot_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))

    # Add a Legend #     
    subplot_fig['data'][0]['showlegend']=True
    subplot_fig['data'][0]['name']='QBR'
    subplot_fig['data'][1]['showlegend']=True
    subplot_fig['data'][1]['name']='Passer Rating'

    return subplot_fig

### Content 2 Team Summary Table ###
@callback(
       Output('team-table','data'),
       Output('team-table', 'columns'),
       Input('team_dropdown','value')
       )

def team_summary_table(value):
    # Subset dataframe by quarterback selected #
    qb_df = df[df.Tm.isin([value])]


    # Find average QBR and Passer Rating grouped by Year #
    mean_gb = qb_df.groupby('Year')[['TOTAL QBR','Rate']].mean()
    mean_gb = mean_gb.reset_index()

    # Find number of games played by quarterback per year #
    num_starters = qb_df.groupby('Year')[['name']].nunique()
    num_starters = num_starters.reset_index()

    # Merge the mean and count dataframes into one merged_gb #
    merged_gb = mean_gb.merge(num_starters, how='inner', on='Year')

    # Set column names #
    merged_gb.columns = ['Year','QBR','Passer Rating','Num QBs']

    # Show all results to the second decimal place #
    merged_gb['QBR'] = merged_gb['QBR'].map('{:.2f}'.format)
    merged_gb['Passer Rating'] = merged_gb['Passer Rating'].map('{:.2f}'.format)

    # Format data as a dictionary to populate dash_table #
    data = merged_gb.to_dict('records')

    # Format columns to populate dash_table #
    columns = [{'name': col, 'id': col} for col in merged_gb.columns]

    # Return the data and column names needed for dash_table #
    return data, columns

### Content 2 Team Line Graph ### 
@callback(
    Output('team-graph','figure'), 
    Input('team_dropdown','value')
    )

def update_team_line_chart(value):
    # Subset dataframe by quarterback selected #
    qb_df = df[df.Tm == value]
    
    # Find average QBR and Passer Rating grouped by Year #
    mean_gb = qb_df.groupby('Year')[['TOTAL QBR','Rate']].mean()
    mean_gb = mean_gb.reset_index()
    
    # Find number of games played by quarterback per year #
    num_games = qb_df.groupby('Year')[['Rate']].count()
    num_games = num_games.reset_index()
    
    # Merge the mean and count dataframes into one merged_gb #
    merged_gb = mean_gb.merge(num_games, how='inner', on='Year')
    
    # Set column names #
    merged_gb.columns = ['Year','QBR','Passer Rating','Num Games']
    
    # Show all results to the second decimal place #
    merged_gb['QBR'] = merged_gb['QBR'].map('{:.2f}'.format).astype(float)
    merged_gb['Passer Rating'] = merged_gb['Passer Rating'].map('{:.2f}'.format).astype(float)
    
    # Create subplot with secondary axis #
    subplot_fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig2 = px.line(merged_gb, x="Year", y="QBR", markers=True)
    fig2.update_yaxes(range = [0,100])
    fig2.update_layout(xaxis={'tickformat':'d'})
    
    fig1 = px.line(merged_gb, x="Year", y="Passer Rating", markers=True)
    fig1.update_yaxes(range = [0,159])
    fig1.update_layout(xaxis={'tickformat':'d'})
    
    fig1.update_traces(yaxis="y2")
    
    #Add the figs to the subplot figure #
    subplot_fig.add_traces(fig2.data + fig1.data)

    if value is None:
        title_name = 'QBR and Passer Rating Over Time'
    else:
        title_name = "{} QBR and Passer Rating Over Time".format(value)
    
    #FORMAT subplot figure #
    subplot_fig.update_layout(title_text=title_name, title_x=0.5, yaxis=dict(title="QBR"), 
                              yaxis2=dict(title="Passer Rating"), 
                              xaxis_title="Year", xaxis={'tickformat':'d'}, legend_title=value,
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              font_color = 'White')

    subplot_fig.update_xaxes(nticks=merged_gb.shape[0])
    
    # RECOLOR so as not to have overlapping colors #
    subplot_fig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
    
    # Add Legend #
    subplot_fig['data'][0]['showlegend']=True
    subplot_fig['data'][0]['name']='QBR'
    subplot_fig['data'][1]['showlegend']=True
    subplot_fig['data'][1]['name']='Passer Rating'
    
    return subplot_fig


# Run Server with local host to port 8000 #
if __name__ == '__main__':
    app.run_server(port=8000, host="0.0.0.0", debug=True)