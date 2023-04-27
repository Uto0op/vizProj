import dash
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, callback, Input, Output, dash_table
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import glob
import os
import pandas
import plotly.figure_factory as ff
import util


dash.register_page(__name__)

# App layout
layout = html.Div([
    html.Div([html.Br()], style={'display':'inline-block', 'width':'5%'}),
      html.Div([
        html.H3("Settings"),
        html.Br(),
        html.Div([
        html.H5('Query ID'),
            dcc.Dropdown(
                id="qid",
                options=util.get_querys(),
                value=util.get_querys()[0],
                placeholder='Select a query by id',
                style={'color': '#191970'},
                clearable=False,
        ),
        html.Br(),
        html.H5('Sort By'),
            dcc.Dropdown(
                id="sort",
                options=["Latency", "Docs Touched", "Postings Scored", "Doc. Block Decodes", "Freq. Block Decodes"],
                value = "Latency",
                placeholder='Sort by',
                style={'color': '#191970'},
                clearable=False,
        ),
           ], 
        style={'width': '60%', 'align-items': 'center'}),
        html.Br(),
        html.H4('Query Terms'),
        html.P(id='qterms'),
        html.H4("Filters"),
        html.H5('Algorithm'),
        dcc.Checklist(['WAND', 'BMW', 'MaxScore'],
                      ['WAND', 'BMW', 'MaxScore'],
                      id='algo-type',
                      #inline = True,
                      style={'color':'#191970'},
                      labelStyle={'display': 'block'}),
        html.Br(),
        html.H5('Order'),
        dcc.Checklist(['Random', 'BP'],
                      ['Random', 'BP'],
                      id='order-type',
                      style={'color':'#191970'},
                      labelStyle={'display': 'block'}),
 
        html.Br(),
        html.H5('Thresh'),
        dcc.Checklist(['None', 'QK', 'Oracle'], 
                      ['None', 'QK', 'Oracle'], 
                      id='threshold-type',
                      style={'color':'#191970'},
                      labelStyle={'display': 'block'}),
        html.Br(),
        html.H5('Ranker'),
        dcc.Checklist(['BM25', 'BM25-T5', 'DeepImpact'],
                      ['BM25', 'BM25-T5', 'DeepImpact'],
                      id='ranker-type',
                      style={'color':'#191970'},
                      labelStyle={'display': 'block'}),

     ],
      style={'display': 'inline-block', 'width':'15%', 'vertical-align':'top', 'align-items':'center', 'justify-content':'center'}), # end options
      html.Div([
        html.H3("Query-Level Statistics"),
        dcc.Graph(id="configs"),
        ], style={'width': '20%', 'display': 'inline-block', 'align-items': 'center', 'vertical-align':'top'}),
])

# Sort configurations
def get_sort_column(sort_metric):
  if sort_metric == "Latency":
    sort_idx = 8
  elif sort_metric == "Docs Touched":
    sort_idx = 4
  elif sort_metric == "Postings Scored":
    sort_idx = 5
  elif sort_metric == "Doc. Block Decodes":
    sort_idx = 6
  elif sort_metric == "Freq. Block Decodes":
    sort_idx = 7
  else: #unreachable
    sort_idx = -1
  return sort_idx



@callback(
    Output("configs", "figure"),
    Input('sort', 'value'),
    Input('qid', 'value'),
    Input('algo-type', 'value'),
    Input('order-type', 'value'),
    Input('threshold-type', 'value'),
    Input('ranker-type', 'value'))
def tabulate_term_info(sort_metric, qid, algos, orders, thresholds, rankers):

  labels = ["Algorithm", "Order", "Threshold", "Ranker", "Docs Touched", "Postings Scored", "Doc. Block Decodes", "Freq. Block Decodes", "Latency"]
  rows = []

  # Generate every possible configuration
  for algo in algos:
    for order in orders:
      for threshold in thresholds:
        for ranker in rankers:
          latency, docs_scored, postings_scored, dblock_decodes, fblock_decodes = util.get_performance_info(qid, algo, order, threshold, ranker)
          values = [algo, order, threshold, ranker, docs_scored, postings_scored, dblock_decodes, fblock_decodes, latency]
          rows.append(values)
  
  sort_idx = get_sort_column(sort_metric)
  rows = sorted(rows,key=lambda l:l[sort_idx], reverse=True) 
  transposed_lists = list(map(list, zip(*rows)))
  # Build the figure
  fig = go.Figure(data=[go.Table(header=dict(values=labels, font_size=15), cells=dict(values=[util.stringify_list(x) for x in transposed_lists], font_size=14, height=30))])
  fig.update_layout(margin=dict(r=5, l=5, t=5, b=5), height=1200, width=1400)
  return fig


@callback(
    Output('qterms', 'children'),
    Input('qid', 'value')
    )
def get_query_info(qid):
  return util.get_query_info(qid, "DeepImpact")[2]


