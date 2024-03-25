# Import packages 
import plotly.express as px
import pandas as pd
import numpy as np
from dash import Dash, html , dcc, Output, Input, dash_table

# Define the data
df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Canada.csv')
df.set_index('Country', inplace=True) # set country as an index
df.index.name = None                  # remove the name of index
df.rename(index={'United Kingdom of Great Britain and Northern Ireland':'United Kingdom'}, inplace=True)

# Initialize the app
app = Dash(__name__)
server = app.server 
# App layout
app.layout = html.Div([
    html.H1(children='The dashboard layout for the Number of Immigrants from other countries in the world to Canada',
             style={'textAlign': 'center', 'color':'Red' }),
    html.H3(children='We are going to create a new line dashboard for the Number of immigrated countries'),
    html.H4(children='Please select upto 5 countries form the list below'),
    html.Hr(),
    dcc.Dropdown(options=[{'label':country, 'value':country} for country in df.index],
                 value=['India','China'],
                 multi=True,
                 id='country_names'),
    dcc.Graph(figure={}, id='compotation_graph'),
    html.Div([
        dcc.Graph(figure={}, id='pie-chart-group'),          
        dcc.Graph(figure={}, id='bar-chart')
        ], style={'display':'flex'})
    
   
])

# Build callbacks
@app.callback(
    [Output(component_id='bar-chart', component_property='figure'),
    Output(component_id='pie-chart-group', component_property='figure'),
    Output(component_id='compotation_graph', component_property='figure')],
    [Input(component_id='country_names', component_property='value')],
)

def update_graph(value_chosen):
    value_chosen= (value_chosen + [])[:5]
    data = df.loc[value_chosen,np.arange(1980,2014).astype(str)]
    data = data.transpose().reset_index()
    fig_1 = px.line(data, x='index', y=value_chosen,
                    title='The number of immigrants has increased year after year',
                    labels={'index':'Years', 'value':'Number of immigrated'})
    
    data_pie = df.loc[value_chosen,'Total']
    fig_2 = px.pie(data_pie, names=value_chosen,values=data_pie.values,
                   title=f'Present with pie chart {value_chosen}')
    fig_3 = px.bar(data, x='index', y=value_chosen,barmode='group',
                    title='The number of immigrants has increased year after year',
                    labels={'index':'Years', 'value':'Number of immigrated'})
    

    return fig_1, fig_2, fig_3



  

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
