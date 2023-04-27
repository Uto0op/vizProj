import dash
from dash import html, dcc, Dash, Input, Output, callback
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import util
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import seaborn as sns

dash.register_page(__name__)

pio.templates.default = "seaborn"

df = util.clean_up_stats_df(pd.read_csv('traces/stats.txt', sep = ' '))
#print(df.head(5))

#################################
temp_df = df.drop(columns=['z', 'k'])
tiled_fig = px.scatter_matrix(temp_df)
tiled_fig.update_layout(width = 1400, height = 1400, font_size=10, title='Dataset at a glance')

######################################

# Facotr non-numerical attributes
numerics = ['int16', 'int32', 'int64']
df_cor = df.select_dtypes(include=numerics).corr()
#print(df_cor.head(5))
#cor_fig = go.Figure(data = go.Heatmap(x=df_cor.columns, y=df_cor.columns, zmax = 1, zmin = -1, text = df_cor.values))
cor_fig = px.imshow(df_cor)
cor_fig.update_layout(width = 800, height = 500, font_size=10, title='Heatmap on the settings and metrics')
#cor_fig.add_trace(go.Heatmap(x=cor_fig.columns, y=cor_fig.index, z=np.array(cor_fig), zmax=1, zmin=-1, text=cor_fig.values))

#####################################

#threed_fig = go.Figure(data=[go.Surface(z=df['Latency'].values, x=df['Doc Blocks Decoded'].values, y=df['Freq Blocks Decoded'].values)])
#threed_fig = go.Figure()
#threed_fig.add_trace()
#threed_fig.update_layout(title = 'Latency vs. Docs & Freq blocks decoded', autosize = False, width=500, height=500, margin=dict(l=65, r=50, b=65, t=90))
threeD_fig = px.scatter_3d(df, x='Doc Blocks Decoded', y='Freq Blocks Decoded', z='Latency', color='Algorithm')
threeD_fig.update_layout(width = 800, height = 500, font_size=10, title='3D plot on Doc & Freq Blocks Decoded vs. Latency over Algorithms') 

######################################
#print(df.describe)
trace = df.query('Algorithm == "BMW" and Thresh == "QK" and Ranker == "DeepImpact"')
#detailed_fig = go.Figure()
#detailed_fig.add_trace(go.Histogram(x=trace['Order'], y=trace['Latency'], color=trace['Algorithm']))
#dict_fig = px.histogram(trace, x='Doc Blocks Decoded', y='Latency', color='Algorithm', marginal = 'box', hover_data = trace.columns, color_discrete_sequence=px.colors.qualitative.G10)
#dict_fig.update_layout(font_size=10, title='Distplot on Docs Blocks Decoded vs. Latency')
#dict_fig = ff.create_distplot([trace['Order'], trace['Latency']], group_labels = trace['Algorithm'], colors=['#A56CC1', '#A6ACEC', '#63F5EF'], show_rug=False)

dict_fig = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5], x_title = 'Doc/Freq Blocks Decoded', y_title = 'Latency', subplot_titles=('Doc Blocks Decoded vs. Latency', 'Freq Blocks Decoded vs. Latency'))
dict_fig.add_trace(go.Scatter(x=trace['Doc Blocks Decoded'], y=trace['Latency'], mode = 'lines', name = 'Doc Blocks Decoded vs. Latency'), row=1, col=1)
dict_fig.add_trace(go.Scatter(x=trace['Freq Blocks Decoded'], y=trace['Latency'], mode = 'lines', name = 'Freq Blocks Decoded vs. Latency'), row=1, col=2)
dict_fig.update_layout(font_size=10, title='Scatter plots on Docs & Freq Blocks Decoded vs. Latency')

# dict_fig = go.Figure()
# dict_fig.add_scatter(x=trace['Doc Blocks Decoded'], y=trace['Latency'], name='doc')
# dict_fig.add_scatter(x=trace['Freq Blocks Decoded'], y=trace['Latency'])
# dict_fig.update_layout(font_size=10, title='Distplots on Docs & Freq Blocks Decoded vs. Latency')




layout = html.Div([
   
      #html.Div([html.Br()], style={'display':'inline-block', 'width':'5%'}),
      html.Div(
          [
          html.Br(),
          dcc.Graph(figure = tiled_fig),
          html.Div("The dataset contains 15 attributes each of which describe a feature/configuration of algotithmes. It looks scary but I will drill down step by step as I'm only interesed in some of these attributes.", style={'margin-left':'15px'}),
          ], style={'display': 'inline-block', 'width':'70%', 'vertical-align':'top', 'align-items':'center', 'justify-content':'center'},
          ),

      html.Br(),
      html.Br(),
      html.Br(),

      html.Div([html.Br()], style={'display':'inline-block', 'width':'5%'}),
      html.Div("Firstly I want to narrow down the scope of the 17 attributes to a certain degree for the purpose of my task, which is to find out which factors may have influence on the efficiency of retrieval: ", style={'margin-left':'15px'}),
      html.Div([
        html.H3("Settings", style = {'color':'#002147', 'margin-left':'20px'}),
        html.Br(),
        html.H5("X-Axis Ticks", style = {'color':'#002147', 'margin-left':'20px'}),
        dcc.RadioItems(["Order", "Thresh", "Ranker", "Algorithm"],
                        id = 'x_tick', value = 'Order',
                        style = {'color':'#191970'},
                        labelStyle={'display': 'block', 'margin-left':'20px'}),
     
        html.Br(),
        html.H5("Horizontal Facet", style = {'color':'#002147', 'margin-left':'20px'}),
        dcc.RadioItems(["Order", "Thresh", "Ranker", "Algorithm"],
                        id = 'h_facet', value = 'Thresh',
                        style = {'color':"#191970"},
                        labelStyle={'display': 'block', 'margin-left':'20px'}),
      
        html.Br(),
        html.H5("Vertical Facet", style = {'color':'#002147', 'margin-left':'20px'}),
        dcc.RadioItems(["Order", "Thresh", "Ranker", "Algorithm"],
                        id = 'v_facet', value = 'Ranker',
                        style = {'color':"#191970"},
                        labelStyle={'display': 'block', 'margin-left':'20px'}),
 
        html.Br(),
        html.H5("Group/Colour", style = {'color':'#002147', 'margin-left':'20px'}),
        dcc.RadioItems(["Order", "Thresh", "Ranker", "Algorithm"],
                        id = 'group_col', value = 'Algorithm',
                        style = {'color':'#191970'},
                        labelStyle={'display': 'block', 'margin-left':'20px'}),
 
      ],
      style={'display': 'inline-block', 'width':'15%', 'vertical-align':'top', 'align-items':'center', 'justify-content':'center'}), # end options
        
      html.Div([
        dcc.Graph(id = 'latency_graph'),

        dcc.Graph(id = 'docs_scored_graph'),
 
        dcc.Graph(id = 'postings_scored_graph'),

        dcc.Graph(id = 'docs_decoded_graph'),

        dcc.Graph(id = 'freqs_decoded_graph')
        ], 
        style={'display': 'inline-block', 'width':'70%', 'vertical-align':'top', 'align-items':'center', 'justify-content':'center'}), # end options
      

      #html.Div([html.Br()], style={'display':'inline-block', 'width':'5%'}),
      html.Div(
          [
          html.Br(),
          html.Div("Since in the given context, latency is an important metric for evaluating the performance of the algorithms, I'm interested in finding settings/variables that are strongly correlated with latency:", style={'margin-left':'15px'}),
          dcc.Graph(figure = cor_fig),
          html.Div("From the heatmap, it's fairly easy to observe that postings scored, doc blocks decoded and freq blocks decoded are strongly, positively correlated with latency (r > 0.80), which makes sense, as the more postings to be scored, the more doc/freq blocks to be decoded, the longer the algorithm needs to take to complete the retrieval.", style={'margin-left':'15px'}),
          ], style={'display': 'inline-block', 'width':'70%', 'vertical-align':'top', 'align-items':'center', 'justify-content':'center'},
          ),

      #########################  
      html.Div(
              [
              html.Br(),
              html.Div('Now generate a 3d scatter plot on doc blocks decoded & freq blocks decode vs. latency over three different algorithms to have a more detailed view:',style={'margin-left':'15px'}),
              dcc.Graph(figure = threeD_fig),
              html.Div("The first thing can be seen from the plot is that, again, for all the three algorithms, the more doc/freq blocks to be decoded, the longer the algorithms take to complete retrieval. Additionally, by manipulating the 3d plot, it's quite straightforward that the algorithm BMW produces lowest latency with relatively small number of doc blocks decoded and extremely small number of freq blocks decoded, which means BMW accelerates top-k retrieval by efficiently bypassing many unnecessary doc blocks and seldom or never decoding same doc blocks multiple times.", style={'margin-left':'15px'}),
              ], style={'display': 'inline-block', 'width':'70%', 'vertical-align':'top', 'align-items':'center', 'justify-content':'center'},
              ),

      ##########################
      html.Div(
              [
              html.Br(),
              html.Div("Setting the threshold to be QK, ranker to be DeepImpact as most commonly configired and algorithm to be BMW as noted previously to be most efficient, let's take another closer look at the relationship between latency and doc & freq blocks decoded respectively:", style={'margin-left':'15px'}),
              dcc.Graph(figure = dict_fig),
              html.Div('Note that scales on the x axes are quite different, the plot suggests 10k decoded doc blocks has similar influence on latency as 1k decoded freq blocks, in other word, the influence of the number of decoded doc blocks is 10 times greater than the number of decoded freq blocks. ', style={'margin-left':'15px'}),], style={'display': 'inline-block', 'width':'70%', 'vertical-align':'top', 'align-items':'center', 'justify-content':'center'},
              ),

    
])

# Map the user request to the data column name
def get_graph_variable(var):
  if var == "Order":
    return 'order'
  elif var == "Thresh":
    return 'qthresh'
  elif var == "Ranker":
    return 'ranker'
  elif var == "Algo":
    return 'algo'
  else: # unreachable
    return 'none'



@callback(
        Output('latency_graph', 'figure'),
        Input('x_tick', 'value'),
        Input('group_col', 'value'),
        Input('h_facet', 'value'),
        Input('v_facet', 'value')
        )
def generate_latency_graph(x_tick, group_col, h_facet, v_facet):
    fig = px.box(df, x=x_tick, y='Latency', color=group_col, facet_col=v_facet, facet_row=h_facet, title='Latency [microseconds/query]', height=900, color_discrete_sequence=px.colors.qualitative.G10)
    fig.update_layout(font_size=15, title=dict(font=dict(size=25))) 
    return fig

@callback(
        Output('docs_scored_graph', 'figure'),
        Input('x_tick', 'value'),
        Input('group_col', 'value'),
        Input('h_facet', 'value'),
        Input('v_facet', 'value')
        )
def generate_docs_scored_graph(x_tick, group_col, h_facet, v_facet):
    fig = px.box(df, x=x_tick, y='Docs Touched', color=group_col, facet_col=v_facet, facet_row=h_facet, title='Documents Touched', height=900, color_discrete_sequence=px.colors.qualitative.G10)
    fig.update_layout(font_size=15, title=dict(font=dict(size=25))) 
    return fig

@callback(
        Output('postings_scored_graph', 'figure'),
        Input('x_tick', 'value'),
        Input('group_col', 'value'),
        Input('h_facet', 'value'),
        Input('v_facet', 'value')
        )
def generate_postings_scored_graph(x_tick, group_col, h_facet, v_facet):
    fig = px.box(df, x=x_tick, y='Postings Scored', color=group_col, facet_col=v_facet, facet_row=h_facet, title='Postings Scored', height=900, color_discrete_sequence=px.colors.qualitative.G10)
    fig.update_layout(font_size=15, title=dict(font=dict(size=25)))
    return fig


@callback(
        Output('docs_decoded_graph', 'figure'),
        Input('x_tick', 'value'),
        Input('group_col', 'value'),
        Input('h_facet', 'value'),
        Input('v_facet', 'value')
        )
def generate_docs_decoded_graph(x_tick, group_col, h_facet, v_facet):
    fig = px.box(df, x=x_tick, y='Doc Blocks Decoded', color=group_col, facet_col=v_facet, facet_row=h_facet, title='Doc Blocks Decoded', height=900, color_discrete_sequence=px.colors.qualitative.G10)
    fig.update_layout(font_size=15, title=dict(font=dict(size=25)))
    return fig

@callback(
        Output('freqs_decoded_graph', 'figure'),
        Input('x_tick', 'value'),
        Input('group_col', 'value'),
        Input('h_facet', 'value'),
        Input('v_facet', 'value')
        )
def generate_freqs__decoded_graph(x_tick, group_col, h_facet, v_facet):
    fig = px.box(df, x=x_tick, y='Freq Blocks Decoded', color=group_col, facet_col=v_facet, facet_row=h_facet, title='Freq Blocks Decoded', height=900, color_discrete_sequence=px.colors.qualitative.G10)
    fig.update_layout(font_size=15, title=dict(font=dict(size=25)))
    return fig
