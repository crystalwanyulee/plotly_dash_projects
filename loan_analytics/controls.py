# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 17:24:32 2020

@author: admin
"""
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os
os.chdir('C://Users/admin/Documents/Python2/LoanAnalytics/loan_analytics')
from loan_analytics.main import *
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import time


col_names = ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment',
             'Applied Principal', 'Applied Interest', 'End Principal']

col_names_with_contributions = ['Payment Number', 'Begin Principal', 'Payment', 'Extra Payment', 'Contributions',
             'Applied Principal', 'Applied Interest', 'End Principal']



empty_schedule_df = pd.DataFrame([], columns=col_names_with_contributions)

subtitle_style = {'font-weight': 'bold', 'fontColor': '#262626'}


def create_base_barplot():
    schedule_df = pd.DataFrame([], columns=col_names)
    schedule_df['Payment Number'] = list(range(200))
    schedule_df.iloc[:, 1:] = 0

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig.add_trace(go.Bar(name='Applied Principal', 
                         x=schedule_df['Payment Number'], 
                         y=schedule_df['Applied Principal'], 
                         marker_color='#B2DBD5',
                        ), 
                         secondary_y=False)
    fig.add_trace(go.Bar(name='Applied Interest', x=schedule_df['Payment Number'], y=schedule_df['Applied Interest'], marker_color='#FABD62'), secondary_y=False)
    fig.add_trace(go.Scatter(name='Principal', x=schedule_df['Payment Number'], y=schedule_df['End Principal'], marker_color='#E7472E'), secondary_y=True)
    
    # Change the bar mode
    #fig.update_xaxes(type='category')
    fig.update_layout(barmode='stack',
                      yaxis=dict(range=[0, 5]),
                      margin={"r":1,"t":1,"l":1,"b":1},
                      plot_bgcolor='rgba(0,0,0,0)',
                      legend=dict(x=0.5, y=1.1, traceorder='normal',orientation="h",xanchor="center",
                                 font=dict(size=12)),
                   #   xaxis_title="Months",
                      yaxis_title="US Dollars",
                      font=dict(
                        #  family="Courier New, monospace",
                          size=12,
                      ),
                      hovermode="x unified"
                     )
    fig.update_traces(hovertemplate='%{y}')
    fig.update_xaxes(tickfont=dict(size=12))
    
    return fig

def create_base_piechart():
    fig = go.Figure(go.Pie(labels=['Empty'], values=[100], 
                           textinfo='label',
                           insidetextorientation='radial', marker_colors=['lightgrey']))
    fig.update_layout(margin={"r":1,"t":1,"l":1,"b":1}, showlegend=False)
    
    
    return fig


def clean_contributors(contributors_list):
    contributors_list = [c.strip() for c in contributors_list]

    repeated_names = []
    for name, count in Counter(contributors_list).items():
        if count > 1:
            repeated_names.append(name)

    for name in repeated_names:
        t = 1
        for i in range(len(contributors_list)):
            if contributors_list[i] == name:
                contributors_list[i] = '{} {}'.format(name, t)
                t+=1

    return contributors_list



def create_loan_form(loan_number):
    
    n = str(loan_number)
    input_principal = dbc.FormGroup(
                            [
                                dbc.Label("Principal", style=subtitle_style),
                                dbc.Input(type="number",
                                          id="principal_"+n,
                                          value=0)
                                ]
                            )
    
    input_interest_rate = dbc.FormGroup(
                            [
                                dbc.Label("Interest Rate", style=subtitle_style),
                                dbc.Input(type="number",
                                          id="interest_rate_"+n,
                                          value=0)
                                ]
                            )
    
    input_payment = dbc.FormGroup(
                            [
                                dbc.Label("Payment", style=subtitle_style),
                                dbc.Input(type="number",
                                          id="payment_"+n,
                                          value=0)
                                ]
                            )
    
    
    input_extra_payment = dbc.FormGroup(
                            [
                                dbc.Label("Extra Payment", style=subtitle_style),
                                dbc.Input(type="number",
                                          id="extra_payment_"+n,
                                          value=0)
                                ]
                            )
    
    

    
    
    basic_form1 = dbc.Row(
        [
         dbc.Col(input_principal, width=6),
         dbc.Col(input_interest_rate, width=6),
    
        ],
        justify='around', 
        align='center',
        style={'margin-top':'15px'}
    )
    
    basic_form2 = dbc.Row(
        [
         dbc.Col(input_payment, width=6),
         dbc.Col(input_extra_payment, width=6)
    
        ],
        justify='around', 
        align='center',
        style={'margin-top':'15px'}
    )
    
    

    
    contribution_rows_list = []    
    
    contribution_row = dbc.Row(
        [   
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Row(dbc.Label("Contributor"), justify='center', style=subtitle_style),
                        dbc.Input(
                            value='Contributor 1',
                            type="text",
                            id="contributor_input_{}_{}".format(loan_number, 0),
                        ),
                    ]
                ),
             #   align='end',
                width=6,
            ),
            dbc.Col(
                dbc.FormGroup(
                    [
                        dbc.Row(dbc.Label("Contribution"), justify='center', style=subtitle_style),
                        dbc.Input(
                            value=0,
                            type="number",
                            id="contribution_input_{}_{}".format(loan_number, 0),
                        ),
                    ]
                ),
              #  align='end',
                width=6,
            ),
        ],
        justify='center', 
        align='center',
        style={'margin-top':'15px'}
    )
    
    contribution_rows_list.append(contribution_row)
    
    
    for nrows in range(1, 3):
        new_row = dbc.Row(
            [   
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Input(
                                value='Contributor {}'.format(nrows+1),
                                type="text",
                                id="contributor_input_{}_{}".format(loan_number, nrows),
                                placeholder="Enter email",
                            ),
                        ]
                    ),
                    width=6,
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Input(
                                value=0,
                                type="number",
                                id="contribution_input_{}_{}".format(loan_number, nrows),
                                ),
                            ]
                        ),
                    width=6,
                    )
                ],
            
            justify='center', 
            align='center',
            id='contribution_row_{}_{}'.format(loan_number, nrows),
        )
        
        contribution_rows_list.append(new_row)
    

    
    button_for_each_loan = dbc.Row(
        [
        # dbc.Col(
         #    dbc.Button("+ Add Loan", outline=True, color="info", block=True, size="sg",
         #               id='button_add_'+n),
          #   width=4
           #  ),
         dbc.Col(
             dbc.Button("Clear", outline=True, color="danger", block=True, size='sg', 
                        id='button_clear_'+n),
             width=3
             )
         ],
        align='center',
        justify='end',
        style={'margin-top':'10px', 'margin-bottom':'20px'}
    )
    
    
    button_show_contribution = dbc.Row(
        [
         dbc.Col(
             dbc.Button("Show Contribution Options ▼", outline=True, color="info", 
                        id='button_show_contribution_'+n, 
                        block=True, size="mg", 
                        style={'font-weight': 'bold'}),
             #width=
             ),
         ],
        align='center',
        justify='begin',
        style={'margin-top':'30px', 'margin-bottom':'20px'}
    )
  
    button_show_contribution = dbc.FormGroup(
        [
         dbc.Checkbox(id='button_show_contribution_'+n),
         dbc.Label("Add Contributors", html_for="standalone-checkbox"),
         ])   
    
    
    button_include_loan = dbc.FormGroup(
        [
         dbc.Checkbox(id='button_include_'+n),
         dbc.Label("Included", html_for="standalone-checkbox"),
         ])  
    
    
    form = dbc.FormGroup(
        [ 
#         button_for_each_loan,
         button_include_loan,
         basic_form1,
         basic_form2,
         button_show_contribution,
         dbc.Collapse(contribution_rows_list, id='contribution_form_'+n),
         ], 
    #    body=True
    )
    
    return form



def create_summary_label(label, id_name):
    
    summary_label = dbc.Card(
                        [
                            html.P(label, 
                                   style={'text-align':'center', 'margin-top':'0px', 'margin-bottom':'0px'}), 
                            html.H4('0', id=id_name, 
                                    style={'text-align':'center', 'margin-top':'10px', 'margin-bottom':'0px','font-weight': 'bold', 'fontColor': '#404040'})
                            ],
                        body=True
                        )
    
    return summary_label