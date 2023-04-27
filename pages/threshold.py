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
    #html.Img(src='assets/logo.png'),
    #html.H1('Threshold analysis', style={'textAlign':'center', 'color': '#0000CD', 'font-weight':'bold'}),
    # This is a hack for padding
      #html.Div([html.Br()], style={'display':'inline-block', 'width':'5%'}),
      dbc.Row(
          [
              dbc.Col(
                  [
                      html.Div([
                           html.H4("Settings"),
                           html.Br(),
                           html.Div([
                           html.H6('Query ID'),
                               dcc.Dropdown(
                                   id="qid",
                                   options=util.get_querys(),
                                   value=util.get_querys()[0],
                                   placeholder='Select a query by id',
                                   style={'color': '#4169E1'},
                                   clearable=False,
                           )], 
                           style={'width': '60%', 'align-items': 'center'}),
                           html.Br(),
                           html.H6('Algorithm'),
                           dcc.RadioItems(['WAND', 'BMW', 'MaxScore'],
                                       id='algo-type', value = 'WAND',
                                          #inline = True,
                                       style={'color':'#4169E1'},
                                      labelStyle={'display': 'block'}),
                           html.Br(),
                           html.H6('Order'),
                           dcc.RadioItems(['Random', 'BP'],
                                      id='order-type', value = "Random",
                                      style={'color':'#4169E1'},
                                      labelStyle={'display': 'block'}),
                          html.Br(),
                          html.H6('Thresh'),
                          dcc.RadioItems(['None', 'QK', 'Oracle'], 
                                     id='threshold-type', value = "None",
                                     style={'color':'#191970'},
                                     labelStyle={'display': 'block'}),
                           
                           html.Br(),
                           html.H6('Ranker'),
                           dcc.RadioItems(['BM25', 'BM25-T5', 'DeepImpact'],
                                      id='ranker-type', value = "BM25",
                                      style={'color':'#191970'},
                                      labelStyle={'display': 'block'}),
                      ])
                      #style={'display': 'inline-block', 'width':'30%', 'vertical-align':'top', 'align-items':'center', 'justify-content':'center'}), # end options
                      #width = {'size' : 10, 'offset' : 1},
                      ],
                      width = {'offset':1},
                      align = 'start',
                  ),
              
              dbc.Col(
                  [
                      dbc.Row(
                          [
                              dbc.Col([html.H4("Query Data"), dcc.Graph(id="qstats")]),
                                       #style={'width': '20%', 'display': 'inline-block', 'align-items': 'center', 'vertical-align':'top'}),),
                              
                              dbc.Col([html.H4("Term Data"), dcc.Graph(id="tstats")]),
                                       #style={'width': '20%', 'display': 'inline-block', 'align-items': 'center', 'vertical-align':'top'}),),
                          ],
                          justify = 'center'
                          ),
                        
                      html.Div([html.H4("Query Trace"),dcc.Graph(id="compare-single"),])
                               #style={'margin-left':'50px', 'width': '800px',  'display': 'inline-block', 'align-items': 'center', 'justify-content': 'center', 'vertical-align':'top'}), #end flex container
                  ],
                  width = {'offset':0},
                  
                  ),
                  
              ],
              align = 'center',
              
          ),
      
      #html.Div([html.Br()], style={'display':'inline-block', 'width':'5%'}),

])  


@callback(
    Output("tstats", "figure"),
    Input('qid', 'value'),
    Input("ranker-type", "value"))
def tabulate_term_info(qid, ranker_type):

    # Get the query data
    df = pandas.read_csv("traces/query-info.txt", sep="\t")
    # Get the desired subsets
    ranker = util.get_ranker(ranker_type)

    # Subset the data frame
    local_qid = int(qid)
    query_data = df.query("ranker == @ranker and qid == @local_qid")
 
    # Get the desired data
    qlen = query_data.iloc[0,2]
    term_data = query_data.iloc[0,3]
    header = ["Token", "List Length", "Upper Bound"]
    tokens, lens, ubs = util.term_data_to_string(term_data)
    # Get data and convert to lists
    tokens = tokens.strip().split()
    lens = lens.strip().split()
    lens = [util.stringify(x) for x in lens]
    ubs = ubs.strip().split()
    # Build the figure
    fig = go.Figure(data=[go.Table(header=dict(values=header, font_size=15),
                                   cells=dict(values=[tokens, lens, ubs], font_size=14, height=30))])
    fig.update_layout(margin=dict(r=5, l=5, t=5, b=5), height=300, width=350)
    return fig

@callback(
    Output("qstats", "figure"),
    Input('qid', 'value'),
    Input("algo-type", "value"),
    Input("order-type", "value"),
    Input("threshold-type", "value"),
    Input("ranker-type", "value"))
def tabulate_query_info(qid, algo_type, order_type, threshold_type, ranker_type):
    
    # Get the query data
    df = pandas.read_csv("traces/query-info.txt", sep="\t")
    # Get the desired subsets
    ranker = util.get_ranker(ranker_type)

    # Subset the data frame
    local_qid = int(qid)
    query_data = df.query("ranker == @ranker and qid == @local_qid")


    # Get the desired data
    qlen = query_data.iloc[0,2]
    latency, docs_scored, postings_scored, dblock_decodes, fblock_decodes = util.get_performance_info(qid, algo_type, order_type, threshold_type, ranker_type)
    latency = util.stringify(latency)
    docs_scored = util.stringify(docs_scored)
    postings_scored = util.stringify(postings_scored)
    dblock_decodes = util.stringify(dblock_decodes)
    fblock_decodes = util.stringify(fblock_decodes)
    labels = ["QID", "Length (tokens)", "Latency (microsec)", "Documents Touched",
              "Postings Scored", "Document Block Decodes", "Freq. Block Decodes"]
    values = [local_qid, qlen, latency, docs_scored, postings_scored,
              dblock_decodes, fblock_decodes]
    
    # Build the figure
    fig = go.Figure(data=[go.Table(columnwidth = [300,100],header=dict(values=["Type", "Value"], font_size=15), cells=dict(values=[labels, values], font_size=14, height=30))])
    fig.update_layout(margin=dict(r=5, l=5, t=5, b=5), height=300, width=350)
    return fig


'''
This function generates the threshold figure
'''
@callback(
    Output("compare-single", "figure"),
    Input("qid", "value"),
    Input("algo-type", "value"),
    Input("order-type", "value"),
    Input("threshold-type", "value"),
    Input("ranker-type", "value"))
def compare_single(qid, algo_type, order_type, threshold_type, ranker_type): 
    # 1. Load the data
    df = pandas.read_csv("traces/" + str(qid) + ".gz", sep=" ", compression="gzip")
    
    # Get the desired subsets
    algo = util.get_algo(algo_type)
    order = util.get_order(order_type)
    threshold = util.get_threshold(threshold_type)
    ranker = util.get_ranker(ranker_type)

    # Subset the data frame
    trace = df.query("algo == @algo and order == @order and qthresh == @threshold and ranker == @ranker")

    # 2. Prepare the plot
    fig = go.Figure() #make_subplots(rows=3, cols=3)

    fig.add_trace(go.Scattergl(x=trace['frac'], y=trace['score'], mode="markers", name="Scores", marker_color='rgba(220, 100, 120, .3)'))
    fig.add_trace(go.Scatter(x=trace['frac'], y=trace['thresh'], mode="lines", name="Threshold", line_color='rgba(0, 150, 220, 1)'))

    termdata = util.get_query_info(qid, ranker_type)
    terms = termdata[2].strip().split(" ")
    bounds = termdata[4].strip().split(" ")
   
    # Add the bound lines with annotations
    for term, bound in zip(terms, bounds):
      fig.add_hline(y=int(bound), line_dash="dash",
                    annotation_text="Term: " + term,
                    line_color = "orange",
              annotation_position="right")

    fig.update_layout(
        #    autosize=False,
    width=1000,
    height=800,
    margin=dict(l=5,r=5,t=5),
    font_size=15,
    yaxis_title = "Score",
    xaxis_title = "Document"
    )

    return fig


