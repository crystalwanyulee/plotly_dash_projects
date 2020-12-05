import os
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# drop down list for use in airport codes
from controls import city_df, airport_df, routes_df, airlines_df
from main import best_path, best_route_planner
from dash_extensions.callback import CallbackGrouper
#from dash_extensions.enrich import CallbackGrouper


cities_options = [{"label": col, "value": col} for col in city_df['City']]
cities = list(city_df.City.values)
color_dict = {'g': '#35b494', 'y': '#f7b025', 'r': '#ea5345', 'b': '#4264FB', 'title': '#595959'}
city_dict = {city:i for i, city in enumerate(city_df['City'])}
id_to_city = {i: city for i, city in enumerate(city_df['City'])}
city_df['Text_Position'] = 'top right'
city_df.loc[city_df.City.isin(['Chicago', 'Portland', 'San Diego', 'San Antonio', 'Tampa', 'Baltimore']), 'Text_Position'] = 'bottom left'
routes_info = pd.read_csv('data/routes_info.csv')

node_to_color = {'Start': color_dict['g'], 'Destination': color_dict['y'], 'Intermediary': color_dict['b']}



def create_path_df(nodes, path, dist):
    path_df = city_df.set_index('City').loc[path].reset_index()
    path_df['Node'] = 'Intermediary'
    path_df.loc[path_df.City == path[0], 'Node'] = 'Start'
    path_df.loc[path_df.City == path[-1], 'Node'] = 'Destination'
    
    return path_df


def create_base_map():
    fig = go.Figure(go.Scattergeo(
                    mode = "markers+text",
                    lon = city_df["Longitude"],
                    lat = city_df["Latitude"], 
                    text = city_df['City'],
                    textposition = city_df['Text_Position'],
                    hoverinfo='text'))
    
    fig.update_layout(geo = dict(
                            scope='usa',
                            projection_scale=1, #this is kind of like zoom
                            center=dict(lat=39, lon=-94)),
                      showlegend=False,
                       margin={"r":0,"t":0,"l":0,"b":0})
    
    return fig



# setup app with stylesheets
app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])


controls = dbc.Card(
    [
        html.H2("Route Planner"),
        dbc.FormGroup(
            [
                dbc.Label("Start City"),
                dcc.Dropdown(
                    options=cities_options,
                    multi=False, 
                    searchable=True,
                    id="start-city",
                ),
            ]
        ),
        dbc.FormGroup(
            [   dbc.Label("Intermediary City (*Optional)", style={'font-style': 'italic'}),
                dcc.Dropdown(
                    options=cities_options,
                    multi=True, 
                    searchable=True,
                    id="intermediary-city",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Destination City"),
                dcc.Dropdown(
                    options=cities_options,
                    multi=False, # Select one city at a time
                    searchable=True,
                    id="destination-city",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Fixed"),
                dcc.RadioItems(
                    id="path_selector",
                    options=[
                        {"label": " Order", "value": "order"},
                        {"label": " Start City", "value": "start"},
                        {"label": " Destination City", "value": "end"},
                        {"label": " Start & Destination", "value": "start_and_end"},
                        {"label": " None (find the shortest order)", "value": "none"},
                    ],
                    value="order",
                    labelStyle={"display": "inline-block", "margin-right": "15px"}
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Submit", outline=False, color="primary", id='button', block=True, size="lg"),
                    width=6
                    ),
                dbc.Col(
                    dbc.Button("Clear", outline=False, color="danger", id='button_clear', block=True, size='lg'),
                    width=6
                    )
                ],
            )
    ],
    body=True,
    style={'height': '50vh'}
)



map_card = dbc.Card(
    dbc.FormGroup(dcc.Graph(id="map", figure=create_base_map())),
    style={'height':'50vh'}
    )


small_labels = dbc.CardDeck([
                    dbc.Card([dbc.CardBody([
                                html.P('Distance', style={'text-align':'center'}), 
                                html.H4(id='distance_text', style={'text-align':'center', 'margin-top':'0px'})]
                            )]),
                    dbc.Card([dbc.CardBody([
                                html.P('# of Cities', style={'text-align':'center'}), 
                                html.H4(id='ncities_text', style={'text-align':'center'})]
                            )])
                    ]
                )


ariline_info = dbc.Card([dbc.FormGroup(small_labels),
                         dbc.FormGroup(id='trip_menu'),
                         dbc.FormGroup(id='table')],
                        body=True,
                        style={'height':'50vh'})





app.layout = dbc.Container([
                dcc.Store(id="route_data"),
                dbc.Row([
                        dbc.Col(controls, md=3),
                        dbc.Col(map_card, md=6),
                        dbc.Col(ariline_info, md=3)
                    ],
                    justify = 'center',
                    align="center",
                    style={'margin-top': '30px', 'margin-bottom': '30px', 'height': '60%'}
                    ),
                dbc.Row(
                        dbc.Col([dbc.CardDeck(id='city_info')]),
                    justify='center',
                    align="center",
                    )
                ],
                id="main-container",
                style={"display": "flex", "flex-direction": "column"},
                fluid=True)



@app.callback(
    Output("intermediary-city", "options"),
    [Input("start-city", "value")],
)


def update_destination_options(start_city):
    
    inter_options = [{"label": col, "value": col} for col in city_df['City'] if col != start_city]   
    
    return inter_options




@app.callback(
    Output("destination-city", "options"),
    [Input("start-city", "value"),
     Input("intermediary-city", "value")],
)


def update_destination_options(start_city, inter_city):
    
    des_options = [{"label": col, "value": col} for col in city_df['City'] if (col != start_city) & (col not in inter_city)]   
    
    return des_options
    



@app.callback(
    [Output("start-city", "value"),
     Output("intermediary-city", "value"),
     Output("destination-city", "value")],
     Input('button_clear', 'n_clicks')
)

def clearDropDown(n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'button_clear' in changed_id:
    #if n_clicks != 0:
        return "", "", ""



@app.callback(
    [Output("map", "figure"),
     Output("route_data", 'data')],
    [   Input("start-city", "value"),
        Input("destination-city", "value"),
        Input("intermediary-city", "value"),
        Input("path_selector", "value"),
        Input('button', 'n_clicks')
    ],
)


def update_figure(source, destination, intermediaries, path_selected, submit_button):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    
    if 'button' in changed_id:
        
        if intermediaries is None:
            nodes_list = []
            
        else:
            nodes_list = [city for city in intermediaries]
        
        if path_selected == 'order':
            nodes, path, dist = best_path(source, destination, nodes_list)
            

            
        else:
            nodes_list = [source] + nodes_list + [destination]
            
            if path_selected == 'none':
                nodes, path, dist = best_route_planner(nodes_list, start_fixed=False, end_fixed=False)
                
            elif path_selected == 'start':
                nodes, path, dist = best_route_planner(nodes_list, start_fixed=True, end_fixed=False)
                
            if path_selected == 'end':
                nodes, path, dist = best_route_planner(nodes_list, start_fixed=False, end_fixed=True)
                
            else:
                nodes, path, dist = best_route_planner(nodes_list, start_fixed=False, end_fixed=True)     
        
        
        path_df = create_path_df(nodes, path, dist)
        fig = go.Figure(go.Scattergeo(
                        mode = "lines",
                        lon = path_df["Longitude"],
                        lat = path_df["Latitude"],
                        showlegend=False))
        
                        
        for n in path_df['Node'].unique():
            df = path_df[path_df['Node'] == n]
            fig.add_trace(go.Scattergeo(lat=df["Latitude"], 
                                            lon=df["Longitude"], 
                                            mode='markers',
                                            name=n,
                                            marker=dict(size= 8, 
                                                        color=node_to_color[n],  
                                                        opacity=1,
                                                        line=dict(
                                                            color=node_to_color[n],
                                                            width=2),
                                                        symbol='circle'
                                                       ), 
                                            showlegend=True))
            
        fig.add_trace(go.Scattergeo(lat=path_df["Latitude"], 
                                    lon=path_df["Longitude"], 
                                    mode='text',
                                    text = path_df['City'], 
                                    textposition = path_df['Text_Position'],
                                    hoverinfo='text',
                                    showlegend=False))
        
        
        fig.update_layout(geo = dict(
                                scope='usa',
                                projection_scale=1, #this is kind of like zoom
                                center=dict(lat=39, lon=-94)),
                                legend=dict(x=0.8,y=0.1),
                                showlegend=True,
                                margin={"r":0,"t":0,"l":0,"b":0})

    return fig, [nodes, path, dist]



@app.callback(
    [
        Output("distance_text", "children"),
        Output("ncities_text", "children")
     ],
    [   Input('route_data', 'data'),
        Input('button', 'n_clicks')
    ],
)

def update_texts(data, submit_button):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'button' in changed_id:    
        return data[2], len(data[0])



@app.callback(
    Output("trip_menu", "children"),
    [   Input('route_data', 'data'),
        Input('button', 'n_clicks')
    ],
)

def produce_airline_menu(data, submit_button):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'button' in changed_id:
        
        path = data[1]
        
        menu_items = []
        cities_options = [{"label": col, "value": col} for col in city_df['City']]
        
        for i in range(len(path)-1):
            start = path[i].capitalize()
            end = path[i+1].capitalize()
            label = '{0} → {1}'.format(start, end)
            value = '{0}_{1}'.format(city_dict[path[i]], city_dict[path[i+1]])
            menu_items.append({'label':label, 'value':value})

       
        trip_menu = [dbc.Label("Check Out Available Airlines"),
                     dcc.Dropdown(options=menu_items,
                                  multi=False, # Select one city at a time
                                  searchable=True,
                                  id='trip_buttons'
                                  )
                     ]
                    

        
        return trip_menu
    

@app.callback(
    Output("table", "children"),
    [
     Input('route_data', 'data'),
     Input("trip_buttons", "value")
     ]
)


def produce_airline_table(data, selected_trip):
    
    #table = html.P(selected_trip)
    
    path = data[1]    
    start = id_to_city[int(selected_trip.split('_')[0])]
    end = id_to_city[int(selected_trip.split('_')[1])]
    df = routes_info.loc[(routes_info['From'] == start) & (routes_info['To'] == end)].drop(['From', 'To'], axis=1)
    df.columns = ['Airline', 'From', 'To']
    table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True,
                                     style={'overflowY': 'scroll'})

    return table



@app.callback(
    Output("city_info", "children"),
    [   Input('route_data', 'data'),
        Input('button', 'n_clicks')
    ],
)


def produce_city_info(data, submit_button):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if 'button' in changed_id:
       
        picture_cards = []
        cities = [city for city in data[1]]
        df = city_df.set_index('City').loc[cities].reset_index()
        
        for i, row in df.iterrows(): 
            picture = dbc.Card(
                [
                    dbc.CardImg(src=row['Image'], top=False),
                    dbc.CardBody(
                        [
                            html.H4(row['City'], className="card-title"),
                            html.P('Population: {}'.format(row['Population'])),
                            html.P(row['Description'][:110] + '...'),
                            dbc.Button("Learn more", color="info", outline=True, size='sm',
                                       href=row['Tourism']),
                        ]
                    ),
                ],
                style={"width": "18rem"},
            )
            
            picture_cards.append(picture)
        
        return picture_cards




# Main
if __name__ == "__main__":
    #app.run_server(debug=True, use_reloader=False)
    app.run_server(debug=False)
