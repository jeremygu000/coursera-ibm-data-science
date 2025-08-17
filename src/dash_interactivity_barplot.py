import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Read the airline data into pandas dataframe
airline_data =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

# Create a dash application layout
app = dash.Dash(__name__)

# Get the layout of the application and adjust it.
# Create an outer division using html.Div and add title to the dashboard using html.H1 component
# Add a html.Div and core input text component
# Finally, add graph component.
app.layout = html.Div(children=[ html.H1('Airline Performance Dashboard',style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
                                # id: input-year, which is a unique identifier for this specific input field. The default value for this input field will be set to 2010, and the type of input will be a number.
                                # style parameter for the dropdown: Here within it we define height of the input box to be 50px and font-size to be 35px to make the text larger and more readable.
                                html.Div(["Input Year: ", dcc.Input(id='input-year', value='2010', type='number', style={'height':'50px', 'font-size': 35}),], 
                                # style parameter for the whole division: Now assign font-size as 40 .
                                style={'font-size': 40}),
                                html.Br(),
                                html.Br(),
                                html.Div(dcc.Graph(id='bar-plot')),
                                ])

# In Python, @app.callback is a decorator used in the Dash framework to specify that a function should be called when an input component changes its value.The Input and Output functions are used to define the inputs and outputs of a callback function.
# The core idea of this application is to get year as user input(input function) and update the dashboard(output function) in real-time with the help of callback function.

# Input() function takes two parameters:
# component-id with the value input-year, which is the ID of the input dropdown.
# component_property being accessed is the value property, which represents the year entered by the user.

# Output()function takes two parameters:
# component-id with the value line-plot, which is the id of the output.
# component_property being modified is the figure property, which specifies the data and layout of the line plot.
@app.callback(Output('bar-plot', 'figure'),
               Input('input-year', 'value'))
# Add computation to callback function and return graph
def get_graph(entered_year):
    # Select data based on the entered year
    df =  airline_data[airline_data['Year']==int(entered_year)]
    
    # Group the data by Month and compute the average over arrival delay time.
    bar_data = df.groupby('DestState')['Flights'].sum().reset_index()


    #         Month  ArrDelay
    # 0      1  3.909091
    # 1      2  8.000000
    # 2      3  9.357143
    # 3      4  0.594937
    # 4      5  0.976471
    # print(line_data.head())

    # Create a bar plot
    fig = go.Figure(data=go.Bar(x=bar_data['DestState'], y=bar_data['Flights'], marker=dict(color='blue')))
    fig.update_layout(title='Flights to Destination State', xaxis_title='DestState', yaxis_title='Flights')

    return fig

# Run the app
if __name__ == '__main__':
    app.run()