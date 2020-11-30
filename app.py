import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
#os.chdir('C://Users/admin/Documents/Python2/LoanAnalytics/loan_analytics')
from loan_analytics.main import *
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import time
#os.chdir('C://Users/admin/Documents/Python2/LoanAnalytics/loan_analytics')
from controls import col_names, col_names_with_contributions, empty_schedule_df
from controls import create_base_barplot, create_base_piechart, clean_contributors, create_loan_form
from controls import create_summary_label

# setup app with stylesheets
external_stylesheets = 'https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/minty/bootstrap.min.css'
app = dash.Dash(external_stylesheets=[external_stylesheets])
#app = dash.Dash(external_stylesheets=[dbc.themes.SANDSTONE])
app.config.suppress_callback_exceptions = True



summary_selector_options = [
        {"label": "All Loans", "value": "all"},
        {"label": "Loan 1", "value": "0"},
        {"label": "Loan 2", "value": "1"},
        {"label": "Loan 3", "value": "2"}
    ]


 
tabs = dbc.Tabs(
    [
        dbc.Tab(create_loan_form(0), label="Loan 1", id='tab_0'),
        dbc.Tab(create_loan_form(1), label="Loan 2", id='tab_1'),
        dbc.Tab(create_loan_form(2), label="Loan 3", id='tab_2'),
    ],
    id='loan_tabs'
)

button_for_all_loans = dbc.Row(
    [
     dbc.Col(
         dbc.Button("Calculate", outline=False, color="primary", id='button_calculate', block=True, size="lg"),
         width=4
         ),
     dbc.Col(
         dbc.Button("Clear All", outline=False, color="danger", id='button_clear_all', block=True, size='lg'),
         width=4
         )
     ],
    align='center',
    justify='center',
    style={'margin-top':'30px'}
)







i=0

button_show_table= dbc.Button("Show amortization schedule table ▼", 
                              outline=True, color="info", 
                              block=True, size="mg", 
                              style={'font-weight': 'bold'},
                              id='button_show_table_'+str(i), 
                              )

empty_table = dbc.Table.from_dataframe(empty_schedule_df, 
                                       striped=True, bordered=True, hover=True,
                                       style={'overflowY': 'scroll'})
    



summary_selector = dbc.Select(
    id="summary_selector",
    options=[
        {"label": "All Loans", "value": "0"},
        {"label": "Loan 1", "value": "1"},
        {"label": "Loan 2", "value": "2", "disabled": True},
        {"label": "Loan 3", "value": "3", "disabled": True}
    ],
    value='0'
)


schedule_card = dbc.Card(
    [

     dbc.Row(dbc.Col(summary_selector, width=2), 
             justify='begin', 
             align='center', 
             style={'margin-bottom':'15px'}),
        
     dbc.Row(
         [
            dbc.Col(create_summary_label('Total Principal Paid', 'total_paid_text_'+str(i)), width=4),
            dbc.Col(create_summary_label('Total Interest Paid', 'total_interest_text_'+str(i)), width=4),
            dbc.Col(create_summary_label('Time to Loan Termination', 'time_text_'+str(i)), width=4)
             ],
         justify='around',
         align='begin',
             ),
     
     dbc.Row(
         [
             dbc.Col(
                 [
                     dbc.FormGroup(
                         [
                             html.H5('Schedule Plot', 
                                     style={'text-align':'center', 'margin-top':'40px', 'margin-bottom':'20px','font-weight': 'bold', 'fontColor': '#008CBA'}),
                             dcc.Graph(figure=create_base_barplot(), id='barplot_'+str(i), style={'height':300}),
                             ]
                         )
                     
                     ], 
                 width=4),
             dbc.Col(
                 [
                     dbc.FormGroup(
                         [
                             html.H5('Payment Proportion', 
                                     style={'text-align':'center', 'margin-top':'40px', 'margin-bottom':'20px','font-weight': 'bold', 'fontColor': '#008CBA'}),
                             dcc.Graph(figure=create_base_piechart(), id='pie_chart_'+str(i), style={'height':300}),
                             ]
                         )
                     ]
                 , width=4
                 ),
             dbc.Col(
                 [
                     dbc.FormGroup(
                         [
                             html.H5('Contributor Imapcts', 
                                     id='impact_plot_title', 
                                     style={'text-align':'center', 'margin-top':'40px', 'margin-bottom':'20px','font-weight': 'bold', 'fontColor': '#008CBA'}),
                             dbc.Row(dcc.RadioItems(
                                 options=
                                 [
                                     {'label': 'Duration', 'value': 'duration'},
                                     {'label': 'Interest', 'value': 'interest'},
                                     ],
                                 value='duration',
                                 labelStyle={'display': 'inline-block', 'margin-right':'10px'},
                                 id = 'impact_barplot_selector_' + str(i)
                                 ),
                                 justify='center',
                                 ),
                             dcc.Graph(id='impact_barplot_'+str(i), style={'height':300}),
                             ]
                         )
                     ], 
                 width=4)
             ],
         justify='around',
         align='begin'),
     
     dbc.Row(
         [dbc.Col(button_show_table, width=4)],
         justify='begin',
         align='begin'
         ),
     
     dbc.Row(
         [dbc.Col([dbc.Collapse(dbc.FormGroup([empty_table], id='schedule_table_'+str(i)), 
                                id='collapse_table_'+str(i))])],
         style={'margin-top': '15px'}
         )
     ], 
    body=True)
    
schedule_tab = dbc.Tab(schedule_card, label='Summary', id='schedule_tab_'+str(i))




app.layout = dbc.Container(
    [
        dcc.Store(id="loan_data0"),
        dcc.Store(id="loan_data1"),
        dcc.Store(id="loan_data2"),
        dcc.Store(id="loan_data3"),
        dcc.Store(id="loan_data4"),
        dcc.Store(id='loan_data_all'),
        dbc.Row(
            html.H2("Loan Calculator",
                    style={'text-align':'center', 'margin-top':'30px', 'margin-bottom':'10px','font-weight': 'bold', 'fontColor': '#008CBA'}),
            align='center',
            justify='center'
            ),
        dbc.Row(
            [
                html.Br(),
                html.P(['This loan calculator will help you determine the monthly payments on a loan. ',
                        'Simply enter the loan amount, term and interest rate in the fields below and click calculate. ',
                        html.Br(),
                        html.P('This calculator can be used for mortgage, auto, or any other fixed loan types.')],
                       style={'text-align':'center'}),
             ],
            align='center',
            justify='center'
            ),
        dbc.Row(
            [
                dbc.Col([tabs, 
                         button_for_all_loans], md=3),
                dbc.Col(dbc.Tabs([schedule_tab], 
                                 id='schedule_tabs', 
                                 active_tab = 'tab-0',
                                 persistence=True, 
                                 persistence_type='memory'), md=9)
                ],
            align="begin",
            justify='center',
          #  style={'height':'60vh'}
        ),
    ],
    id="main-container",
    style={"display": "flex", "flex-direction": "column"},
    fluid=True
)



# Show contribution form
for i in range(3):
    @app.callback(
        Output("contribution_form_"+str(i), "is_open"),
        [Input("button_show_contribution_"+str(i), "checked")],
    )
    
    def toggle_collapse(checked):
        return checked



@app.callback(
    Output("summary_selector", "options"),
    [Input("button_include_"+str(i), "checked") for i in range(3)],
)

def update_summary_selector(checked1, checked2, checked3):
        
    selector = [True] + [checked1, checked2, checked3]
    options = [summary_selector_options[i] for i, s in enumerate(selector) if s == True] 
    
    return options



for i in range(3):
    @app.callback(
        Output("loan_data"+str(i), "data"),
        [Input("button_calculate", "n_clicks"),
         Input("button_include_"+str(i), "checked"),
         Input('principal_'+str(i), 'value'),
         Input('interest_rate_'+str(i), 'value'),
         Input('payment_'+str(i), 'value'), 
         Input('extra_payment_'+str(i), 'value'),
         Input('contributor_input_{}_{}'.format(i, 0), 'value'),
         Input('contributor_input_{}_{}'.format(i, 1), 'value'),
         Input('contributor_input_{}_{}'.format(i, 2), 'value'),
         Input('contribution_input_{}_{}'.format(i, 0), 'value'),
         Input('contribution_input_{}_{}'.format(i, 1), 'value'),
         Input('contribution_input_{}_{}'.format(i, 2), 'value')],
    )
    
    
    def store_data(button_calculate, button_include, principal, rate, payment, extra_payment,
                        p1, p2, p3, c1, c2, c3):
        
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
        
        if ('button_calculate' in changed_id):
        
        
            contributors = clean_contributors([p1, p2, p3])
            contributions = [c1, c2, c3]
    
            
            contributions_sum = sum(contributions)
    
            loan = compute_schedule(principal, rate, payment, extra_payment+contributions_sum)
            schedule_df = pd.DataFrame(loan.schedule.values(), columns=col_names).to_dict()
            
            
            loan_impacts = compute_loan_contribution(principal, rate, payment, extra_payment, contributions)
            loan_impacts_df = pd.DataFrame(loan_impacts.results[1:], columns=loan_impacts.results[0]).to_dict()
                                                 
            return {'schedule': schedule_df, 'loan_impacts': loan_impacts_df, 
                    'principal': principal, 'rate': rate, 'payment': payment, 'extra_payment': extra_payment, 
                    'contributions': contributions, 'contributors': contributors}
        
        else:
        
            return dash.no_update


for i in range(3):
    @app.callback(
        [
            Output("button_include_"+str(i), "checked"),
            ],
        [
             Input('principal_'+str(i), 'value'),
             Input('interest_rate_'+str(i), 'value'),
             Input('payment_'+str(i), 'value'), 
            ]
        )        
    
    def check_include_button(principal, rate, payment):
        
        if (principal !=0 ) | (rate != 0) | (payment != 0):
            return [True]



@app.callback(
    [ Output("loan_data_all", "data")],
    [
     Input("button_calculate", "n_clicks"),
     Input("button_include_0", "checked"),
     Input("button_include_1", "checked"),
     Input("button_include_2", "checked"),
     ],
     [State("loan_data"+str(0), "data"),
      State("loan_data"+str(1), "data"),
      State("loan_data"+str(2), "data")
      ]
     )


def store_data_to_all(button_calculate, 
                      include0, include1, include2, 
                      data0, data1, data2):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    include_list = [include0, include1, include2]
    data_list = [data0, data1, data2]
    
    if 'button_calculate' in changed_id:  
    
        loan_id = []
        loan_list = []
        time = []
        principal = []
        interest = []
        contributions = []
        
        for i in range(len(include_list)):
            
            
            if include_list[i]:
                data = data_list[i]
                contributions_sum = sum(data['contributions'])
                loan = compute_schedule(data['principal'], data['rate'], data['payment'], 
                                        data['extra_payment']+contributions_sum)
                loan_list.append(loan)
                loan_id.append(i)
                time.append(loan.time_to_loan_termination)
                principal.append(loan.total_principal_paid)
                interest.append(loan.total_interest_paid)
                contributions.append(contributions_sum)
                
        loan_portfolio = compute_portfolio_schedule(loan_list)
        schedule_df = pd.DataFrame(loan_portfolio.schedule.values(), columns=col_names).to_dict()
        
        
        return [{'schedule':schedule_df, 'loan_id': loan_id, 
                'principal': principal, 'interest':interest, 'time':time, 
                'contributions': contributions}]
                


i=0
#for i in range(3):

@app.callback(
     [Output('total_paid_text_'+str(i), "children"),
      Output('total_interest_text_'+str(i), 'children'), 
      Output('time_text_'+str(i), 'children'),
      ],
     [Input("button_calculate", "n_clicks"),
      Input("summary_selector", "value")],
     [State("loan_data0", "data"),
      State("loan_data1", "data"),
      State("loan_data2", "data"),
      State("loan_data_all", "data")],
      prevent_initial_call=True
)


def update_summary(button_calculate, selector, data0, data1, data2, data_all):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    data_list = [data0, data1, data2, data_all]
    
 #   if button_calculate: 
    if selector == 'all':
        selector = -1
    else:
        selector = int(selector)
                
    schedule_df = pd.DataFrame(data_list[selector]['schedule'])   
    
    t1 = '{:,.0f}'.format(schedule_df.loc[(schedule_df['Payment Number'] == 1), 'Begin Principal'].values[0])
    t2 = '{:,.0f}'.format(schedule_df['Applied Interest'].sum())
    t3 = len(schedule_df)

    return t1, t2, t3

#else:
   # dash.no_update
        


i=0
#for i in range(3):

@app.callback(
     [Output('schedule_table_'+str(i), "children")],
     [Input("button_calculate", "n_clicks"),
      Input("summary_selector", "value")],
     [State("loan_data0", "data"),
      State("loan_data1", "data"),
      State("loan_data2", "data"),
      State("loan_data_all", "data")],
      prevent_initial_call=True
)


def update_table(button_calculate, selector, data0, data1, data2, data_all):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    data_list = [data0, data1, data2, data_all]
    
#    if button_calculate:
    
    if selector == 'all':
        selector = -1  
        
    else:
        selector = int(selector)
    
    schedule_df = pd.DataFrame(data_list[selector]['schedule'])             
    schedule_df[['Begin Principal', 'Applied Principal', 'Applied Interest', 'End Principal']] = schedule_df[['Begin Principal', 'Applied Principal', 'Applied Interest', 'End Principal']].applymap(lambda x: '{:,.2f}'.format(x))
    schedule_df['Contributions'] = sum(data_list[selector]['contributions'])
    schedule_df['Extra Payment'] = schedule_df['Extra Payment'] - schedule_df['Contributions']
    schedule_df = schedule_df[col_names_with_contributions]
    
    table = dbc.Table.from_dataframe(schedule_df, striped=True, bordered=True, hover=True)
        
    return [table]

#else:
    #dash.no_update

        

i=0
#for i in range(3):
@app.callback(
     [Output('barplot_'+str(i), "figure")],
     [Input("button_calculate", "n_clicks"),
      Input("summary_selector", "value")],
     [State("loan_data0", "data"),
      State("loan_data1", "data"),
      State("loan_data2", "data"),
      State("loan_data_all", "data")],
     prevent_initial_call=True
)


def update_barplot(button_calculate, selector, data0, data1, data2, data_all):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    data_list = [data0, data1, data2, data_all]
    
 #   if button_calculate:
    
    if selector == 'all':
        selector = -1  
        
    else:
        selector = int(selector)  
        
    schedule_df = pd.DataFrame(data_list[selector]['schedule'])
    cols_adjust = ['Begin Principal', 'Applied Principal', 'Applied Interest']
    schedule_df[cols_adjust] = schedule_df[cols_adjust].applymap(lambda x: '{:,.2f}'.format(x))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(name='Applied Principal', 
                         x=schedule_df['Payment Number'], 
                         y=schedule_df['Applied Principal'], 
                         marker_color='#C1E1DC'), 
                  secondary_y=False)
    
    fig.add_trace(go.Bar(name='Applied Interest', 
                         x=schedule_df['Payment Number'], 
                         y=schedule_df['Applied Interest'], 
                         marker_color='#FDD475'), 
                  secondary_y=False)
    
    fig.add_trace(go.Scatter(name='Principal', 
                             x=schedule_df['Payment Number'], 
                             y=schedule_df['End Principal'], 
                             marker_color='#E7472E'), 
                  secondary_y=True)
    
    fig.update_layout(barmode='stack',
                      margin={"r":1,"t":1,"l":1,"b":1},
                      plot_bgcolor='rgba(0,0,0,0)',
                      legend=dict(x=0.5, y=1.1, traceorder='normal',orientation="h",xanchor="center",
                                 font=dict(size=12)),
                      xaxis_title="Time",
                      yaxis_title="US Dollars",
                      font=dict(size=12),
                      hovermode="x unified")
    
 #   fig.update_layout(yaxis=dict(range=[0,schedule_df['End Principal'].max()*1.1]), secondary_y=True)
    
    fig.update_traces(hovertemplate='%{y}')
    fig.update_xaxes(tickfont=dict(size=12))
    
    return [fig]

#else:
  #  dash.no_update



i=0
#for i in range(3):
@app.callback(
     [Output('pie_chart_'+str(i), "figure")],
     [
      Input("button_calculate", "n_clicks"),
      Input("summary_selector", "value"),
      Input("button_show_contribution_"+str(0), "checked"),
      Input("button_show_contribution_"+str(1), "checked"),
      Input("button_show_contribution_"+str(2), "checked")
      ],
     [
      State("loan_data0", "data"),
      State("loan_data1", "data"),
      State("loan_data2", "data"),
      State("loan_data_all", "data")
      ],
      prevent_initial_call=True
)


def update_piechart(button_calculate, selector, check0, check1, check2,
                    data0, data1, data2, data_all, 
                   ):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    data_list = [data0, data1, data2, data_all]
    check_list = [check0, check1, check2]
    
    
   # if button_calculate:
    if selector == 'all':
        selector = -1  
        
        data = data_list[selector]
        payers = ['Loan {}'.format(i+1) for i in data['loan_id']]
        all_payment = np.array(data['principal'])
        all_payment = all_payment/all_payment.sum()
        
        fig = go.Figure(go.Pie(labels=payers, 
                               values=all_payment, 
                               textinfo='label+percent',
                               textposition = 'outside',
                               sort=False,
                               insidetextorientation='radial', 
                               marker_colors=['#C1E1DC', '#FEEB94', '#E4EA8C'], 
                               hole=.4))
        
        fig.update_layout(margin={"r":1,"t":1,"l":1,"b":1},
                          showlegend=False)
        
        return [fig]
        
    else:
        selector = int(selector)  
        check = check_list[selector]
        
        contributions = np.array(data_list[selector]['contributions'])
        idx = contributions.nonzero()[0]
        contributions = [contributions[i] for i in idx]
        contributors = [data_list[selector]['contributors'][i] for i in idx]
        payment = data_list[selector]['payment']
        extra_payment = data_list[selector]['extra_payment']
        
        if check:
            
            all_payment = np.array([payment, extra_payment]+contributions)
            all_payment = all_payment/all_payment.sum()
            payers = ['My Payment', 'My Extra Payment', 'Contributor 1', 'Contributor 2', 'Contributor 3']
            
        
        else:
            all_payment = np.array([payment, extra_payment])
            all_payment = all_payment/all_payment.sum()
            payers = ['My Payment', 'My Extra Payment']
        
        fig = go.Figure(go.Pie(labels=payers, 
                               values=all_payment, 
                               textinfo='label+percent',
                               textposition = 'outside',
                               sort=False,
                               insidetextorientation='radial', 
                               marker_colors=['#FFCCAC', '#FDD475', '#C1E1DC', '#FEEB94', '#E4EA8C'], 
                               hole=.4))
        
        fig.update_layout(margin={"r":1,"t":1,"l":1,"b":1},
                          showlegend=False)
        
        return [fig]
 #   else:
     #   dash.no_update
        
     
@app.callback(
    Output('impact_plot_title', 'children'),
    Input("summary_selector", "value")
    )

def update_impact_plot_title(summary_selector):
    if summary_selector == 'all':
        return 'Loan Comparison'
    else:
        return 'Contributor Imapcts'
    
i=0
#for i in range(3):
@app.callback(
     [Output('impact_barplot_'+str(i), "figure")],
     [
      Input("button_calculate", "n_clicks"),
      Input("summary_selector", "value"),
      Input('impact_barplot_selector_' + str(i), 'value'),
      Input("button_show_contribution_"+str(0), "checked"),
      Input("button_show_contribution_"+str(1), "checked"),
      Input("button_show_contribution_"+str(2), "checked")
      ],
     [State("loan_data0", "data"),
      State("loan_data1", "data"),
      State("loan_data2", "data"),
      State("loan_data_all", "data")],
     prevent_initial_call=True
)
    
    
def update_impact_chart(button_calculate, summary_selector, selector, 
                        check0, check1, check2, 
                        data0, data1, data2, data_all):
    
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    data_list = [data0, data1, data2, data_all]
    check_list = [check0, check1, check2]
    
   # if button_calculate: 
    if summary_selector == 'all':
        summary_selector = -1  
        check= False
        
        
    else:
        summary_selector = int(summary_selector)
        check = check_list[summary_selector]
  
    data = data_list[summary_selector]
    
    
    if (check) & (summary_selector != -1):
        
        loan_impacts_df = pd.DataFrame(data['loan_impacts'])
        loan_impacts_df = loan_impacts_df.iloc[2:]
        loan_impacts_df['contributions'] = data['contributions']
        loan_impacts_df['contributors'] =  data['contributors']
        loan_impacts_df = loan_impacts_df.loc[loan_impacts_df['contributions']!=0]

        if selector == 'duration':
            fig = go.Figure(go.Bar(x=loan_impacts_df['MIDuration'],
                                    y=loan_impacts_df['contributors'] ,
                                    marker_color=['#C1E1DC', '#FEEB94', '#E4EA8C'],
                                    orientation='h',
                                   width=.5,
                                    text=loan_impacts_df['contributors'] ,
                                   textposition='auto',
                                    name='Duration'))
            fig.update_layout(showlegend=False, 
                              plot_bgcolor='rgba(0,0,0,0)',
                              xaxis_title='Duration',
                              margin={"r":1,"t":1,"l":1,"b":1},
                             )
            
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='silver')
            fig.update_yaxes(showgrid=False, showticklabels=False)

        
            return [fig]
        
        elif selector == 'interest':
            fig = go.Figure(go.Bar(x=loan_impacts_df['MIInterest'],
                                    y=loan_impacts_df['contributors'] ,
                                    marker_color=['#C1E1DC', '#FEEB94', '#E4EA8C'],
                                    orientation='h',
                                    width=.5,
                                    text=loan_impacts_df['contributors'] ,
                                    textposition='auto',
                                    name='Duration'))
            fig.update_layout(showlegend=False, 
                              plot_bgcolor='rgba(0,0,0,0)',
                              yaxis_showticklabels=False,
                              xaxis_title='Duration',
                              margin={"r":1,"t":1,"l":1,"b":1},
                             )
            
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='silver')
            fig.update_yaxes(showgrid=False, showticklabels=False)

        
            return [fig]
        
    elif (not check)  & (summary_selector == -1):
        time = data['time']
        interest = data['interest']
        loan_name = ['Loan {}'.format(i+1) for i in data['loan_id']]
    
        if selector == 'duration':
            fig = go.Figure(go.Bar(x=time,
                                   y=loan_name,
                                   marker_color=['#C1E1DC', '#FEEB94', '#E4EA8C'],
                                   orientation='h',
                                   width=.5,
                                   text=loan_name,
                                   textposition='auto',
                                   name='Duration'))
            fig.update_layout(showlegend=False, 
                              plot_bgcolor='rgba(0,0,0,0)',
                              xaxis_title='Duration',
                              margin={"r":1,"t":1,"l":1,"b":1}, 
                             )
            
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='silver')
            fig.update_yaxes(showgrid=False, showticklabels=False)

        
            return [fig]
        
        elif selector == 'interest':
            fig = go.Figure(go.Bar(x=interest,
                                   y=loan_name,
                                   marker_color=['#C1E1DC', '#FEEB94', '#E4EA8C'],
                                   orientation='h',
                                   width=.5,
                                   text=loan_name,
                                   textposition='auto',
                                   name='Duration'))
            fig.update_layout(showlegend=False, 
                              plot_bgcolor='rgba(0,0,0,0)',
                              yaxis_showticklabels=False,
                              xaxis_title='Duration',
                              margin={"r":1,"t":1,"l":1,"b":1}, 
                             )
            
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='silver')
            fig.update_yaxes(showgrid=False, showticklabels=False)

        
            return [fig]
        
    else:
        dash.no_update
            
   # else:
     #   dash.no_update

i=0
# Show amortization table
#for i in range(3):
@app.callback(
    Output("collapse_table_"+str(i), "is_open"),
    [Input("button_show_table_"+str(i), "n_clicks")],
    [State("collapse_table_"+str(i), "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# Main
if __name__ == "__main__":
    #app.run_server(debug=True, use_reloader=False)
    app.run_server(debug=False, use_reloader=False)
