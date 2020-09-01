import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

df = pd.read_csv('client-location-data.csv')

app = dash.Dash(__name__)
server=app.server
app.layout = html.Div(children=[
    
    html.Div([
        html.A(
            html.Img(
                src="https://alariss.com/wp-content/uploads/2019/07/On-Light@3x.png",
                style={'float': 'left',
                    'height': '65px',
                    'paddingLeft':'20px'}
            ), href="https://alariss.com"),
        html.H1(children=[
                "Alariss Client Map"],
             style={'paddingLeft': '37%',
                'color':'navy',
                'fontFamily':'Arial',
                'fontSize':42,
                'paddingTop':'5px',
                'paddingBottom':'5px'})
    ], style={'borderBottom':'1px solid Black',
    'backgroundColor':'white'}),
    
    html.Div(children=[
        html.Label('Industries', style={
            'fontFamily':'Arial',
            'color':'Black',
            'fontSize':24,
            'paddingLeft':'150px'}),
        dcc.Dropdown(id='dropdown', style={
            'color':'Black',
            'marginTop':'10px',
            'fontSize':18,
            'paddingLeft':'150px',
            'fontFamily':'Arial',
            'width':'250px'},
            options=[
                {'label': 'All', 'value': 'All'},
                {'label': 'Business', 'value': 'Business'},
                {'label': 'Education', 'value': 'Education'},
                {'label': 'Engineering & Tech', 'value': 'Engineering/Tech'}
            ],
            value='All',
            searchable=False,
            clearable=False
        ),

        dcc.Graph(id='map')
         
    ], style={
    'margin':'50px 20px 0px',
    "backgroundColor":'white'
    })  
])

@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('dropdown', 'value')])

def update_figure(industry):
    #print(industry)
    hover_data = []
    hover_color = ""
    opacity = .8
    if industry == "Engineering/Tech":
        hover_data = {'Latitude':False, 'Longitude':False, 'Engineering/Tech':True}
        hover_color = '#3cee11'
        opacity = .8
    elif industry == "Business":
        hover_data = {'Latitude':False, 'Longitude':False, 'Business':True}
        hover_color = '#ec1713'
        opacity = .7
    elif industry == "Education":
        hover_data= {'Latitude':False, 'Longitude':False,'Education':True}
        hover_color = '#e60cf3'
        opacity = .8
    else:
        hover_data = {'Latitude':False, 'Longitude':False, 'All':False, 'Engineering/Tech':True, 'Business':True, 'Education':True}
        hover_color = "#1ecbe1"

    df2 = df.copy()
    df2 = df2[df2[industry] > 0]

    fig = px.scatter_geo(df2,
        lat="Latitude",
        lon="Longitude",
        hover_name="City",
        opacity=opacity,
        color_discrete_sequence=[hover_color],
        size=industry,
        size_max=30,
        hover_data=hover_data,
        height = 500,
    )

    fig.update_geos(
        showcoastlines=True, coastlinecolor="#B2DBFF",
        showland=True, landcolor="white",
        showlakes=True, lakecolor="white",
        showocean=True, oceancolor="#0B1746",
        showcountries=True, countrycolor="#B2DBFF"
        #fitbounds="locations"
        )

    fig.update_layout(
        #title = 'Alariss Global Clients',
        #title_font_size = 24,
        hoverlabel=dict(
            bgcolor="navy",
            font_size=16),
    )

    fig.update_traces(marker=dict(sizemin=5))
    # fig.show()

    return fig

if __name__ == '__main__':
    app.run_server(debug=False)