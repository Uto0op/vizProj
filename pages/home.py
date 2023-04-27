import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div([
    html.Div([html.Br()], style={'display':'inline-block', 'width':'5%'}),
    
    # Introductory message
    html.Div(children='''
             Welcome to the Dyno, the dynamic pruning profiling visualization system. 
             Please use the navigation bar to check out the different dashboards and
             analysis regimes.
             ''',
             style={'margin-left':'15px','fontsize':16}),
    
    html.Br(),
    
    # Page info
    html.Div("Here's an overview of the three pages on the navigation bar:", style={'margin-left':'15px','fontsize':16}),
    html.Br(),
    html.H5(children='\u25C8 Global Comparison'),
    html.Div(children='''This page facilitates comparisons of all systems (that is, all unique 
            algorithms and configurations) as box-and-whisker plots based on data derived from 
            all queries in the query log. A plot is presented for each of the metrics of interest. 
            These metrics together provide a detailed view of algorithm performance, and can 
            further "drill down" to the data for query-level tracing. Users are expected to configure 
            the plots by adjusting the settings on the left hand side to have different views on the data.
            ''',
            style={'margin-left':'15px','fontsize':14}),
            
    html.Br(),
    
    html.H5(children='\u25C8 Query Tracing'),
    html.Div(['''This page allows a specific system to have its performance interrogated for 
            a query of choice. With adjustable settings, it tabulates a number of meaningful statistics
            which elaborate on the algorithm performances, accompanied by a figure tracing the documents
            scored during the index traversal. This visualization is inspired by the static figures shown by 
            ''', 
            html.A('Petri et al. [38]', href='https://culpepper.io/publications/pcm13-adcs.pdf')],
            style={'margin-left':'15px','fontsize':14}),

    html.Br(),
    
    html.H5(children='\u25C8 Per-query Stats'),
    html.Div(children='''This page displays a large table containing all systems and performance metrics for
            a single query, which can be filtered and sorted to allow users to rapidly pinpoint any anomalies 
            in performace in comparison to other configurations.
            ''',
            style={'margin-left':'15px','fontsize':14})

])
            

