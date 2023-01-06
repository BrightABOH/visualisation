import dash
import base64
from flask import Flask

import pandas as pd
import plotly.io as pio
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
#import dash_core_components as dcc
#import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import load_figure_template

external_stylesheets = ['https://codepen.io/unicorndy/pen/GRJXrvP.css','https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css']

app = dash.Dash(external_stylesheets=[dbc.themes.SOLAR])
server = app.server
load_figure_template("bootstrap")

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app = Flask(__name__)

data  = pd.read_csv("/data/final1.csv")

#####################################################################################################################
#Percentage $ dispaly preprocessing
percent_toilet = ((data["What type of toilet facility are available in this house/structure?"].value_counts()[:1].sort_values(ascending=False)/data["CASE_ID_1"].nunique())*100 ).round(0)
percent_comp = ((data["Level of completion"].value_counts()[:1].sort_values(ascending=False)/data["CASE_ID_1"].nunique())*100).round(0)
percent_res = ((data["Use of structure"].value_counts()[:1].sort_values(ascending=False)/data["CASE_ID_1"].nunique())*100).round(0)
# the style arguments for the sidebar.##################################################################################
SIDEBAR_STYLE = {
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '21%',
    'padding': '18px 10px',
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.4s",
    'background-color': '#00475a' 
}
####################################################################################################################
SIDEBAR_HIDEN = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": 0,
    "height": "100%",
    "z-index": 1,
    "overflow-x": "hidden",
    "transition": "all 0.4s",
    #"padding": "0rem 0rem",
    "background-color": '#00475a',
}

# Header styling #########################################################################################################

header_height = "6rem", 
HEADER_STYLE = {
    "position": "sticky",
    "top": 0,
    "left": 0,
    "right": 0,
    "height": header_height,
    'textAlign': 'center',
    "padding": "1rem 1rem",
    'color': 'white',
    "background-color": '#00475a',
}
# GRAPH_STYLE#########################################################################################################
GRAPH_STYLE ={
    'background-color': '#000000',
    "display":"inline-block" , 
    "float":"left",
    "template" :"plotly_dark"

    
}
    
#################################################################################################################    
BUTTON_STYLE={
    'position': 'fixedrange',
    "top": 15,
    "left": 1200,
    "right": 0,
    'textAlign': 'center',
    'width': "7%"
}

BUTTON_STYLE1={
    'position': 'fixedrange',
    "top": 15,
    "left": 1250,
    "right": 0,
    'textAlign': 'center',
    'width': "7%"
}


# the style arguments for the main content page.
CONTENT_STYLE = {
    "top": 10,
    "transition": "margin-left .4s",
    'margin-left': '22%',
    'margin-right': '1%',
    'padding': '30px 20p',
    'color': "#cbd3da"
    
}

CONTENT_STYLE1 = {
    "transition": "margin-left .4s",
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "color": "#cbd3da",
}



TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#f7fbff',
    
}

CARD_TEXT_STYLE = {
    "position": "sticky",
    'textAlign': 'center',
    'color': '#ffafd7',
    'height':80,
    
    
}
########################################
controls = dbc.Row(
    [
    dbc.Label("Region"),
    dbc.Dropdown(

        id="region-dpdn",
        options=[{'label': s, 'value': s} for s in sorted(data["Region name"].unique())],
        value="OTI",
        clearable=False,

        ),
        

    
    <className="mb-3">,
    dbc.Label("District"),
    dcc.Dropdown(
        id="district-dpdn",
        options=[], multi = True, clearable = False,
        ),

    className="mb-3"

    ],

)



##################################################################################################################
#controls = dbc.Card(
#    [
#        dbc.FormGroup(
#            [
#                dbc.Label("Region"),
#                dcc.Dropdown(
#                    id="region-dpdn",
#                    options=[{'label': s, 'value': s} for s in sorted(data["Region name"].unique())],
#                    value="OTI",
#                    clearable=False,
#                    
#                ),
#            ]
#        ),
#        dbc.FormGroup(
#            [
#                dbc.Label("District"),
#                dcc.Dropdown(
#                    id="district-dpdn",
#                    options=[], multi = True, clearable = False,
                    
#                ),
#            ]
#        ),
        
#    ],
#    body=True,
#)

# Populate the options of district dropdown based on region dropdown
@app.callback(
    Output('district-dpdn', 'options'),
    Input('region-dpdn', 'value')
)
def set_cities_options(chosen_region):
    dff = data[data["Region name"]==chosen_region]
    return [{'label': c, 'value': c} for c in sorted(dff["District name"].unique())]


# populate initial values of district dropdown
@app.callback(
    Output('district-dpdn', 'value'),
    Input('district-dpdn', 'options')
)
def set_cities_value(available_options):
    return [x['value'] for x in available_options]











####################################################################################################################

###sidebar design####
sidebar = html.Div(
    [
        html.H2('Aggregation'),
        html.Hr(),
        controls
    ],
    id = "sidebar",
    style=SIDEBAR_STYLE,
)
###################################################################################################################


####################################################################################################################
content_first_row = dbc.Row([
    
    dbc.Col(
        
        dbc.Card(
            
            
            [
                
                dbc.CardHeader("Number of structures"),
              
                dbc.CardBody(
                    [
                        html.H2(id='card_title_1',children=data["CASE_ID_1"].nunique(), className='className="h-75"', style = CARD_TEXT_STYLE
                        ),
                        html.P(id='card_text_1', children=["Total number of structures listed"],className='className="h-75"'),
                    
                        
                        
                    ]
                )
                
            ]
        ),
        md=3,
    
    
       
    ),

    
    
    
    dbc.Col(
        dbc.Card(
            [
                dbc.CardHeader("Structures without toilet"),
                
                dbc.CardBody(
                    [
                        #html.H2('Structures without toilet', className='card-title', style=CARD_TEXT_STYLE),
                        html.H2(children = data["What type of toilet facility are available in this house/structure?"].value_counts()[:1].sort_values(ascending=False),style=CARD_TEXT_STYLE),
                        html.P(f"{int(percent_toilet):,d}"+ ' % ' +  "of structures have no toilet facility"),
                    ]
                ),
                
            ]

        ),
        md=3
    ),
    
    
    dbc.Col(
        dbc.Card(
            [
                dbc.CardHeader("Residential structures"),
                dbc.CardBody(
                    [
                        #html.H2('Residential structures', className='card-title', style=CARD_TEXT_STYLE),
                        html.H2(children = data["Use of structure"].value_counts()[:1].sort_values(ascending=False), style=CARD_TEXT_STYLE),
                        html.P(f"{int(percent_res):,d}"+ ' % ' +  "of structures listed are residential"),
                    ]
                ),
                
            ]
            
        ),
        md=3
    ),
    
    dbc.Col(
        dbc.Card(
            [
                dbc.CardHeader("Structures listed by region"),
                
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem("Greater Accra:"+" "+ f"{data.groupby('Region name')['CASE_ID_1'].nunique().sort_values(ascending=False)[0]:,d}", color = "danger"),
                        dbc.ListGroupItem("Central region:"+" "+ f"{data.groupby('Region name')['CASE_ID_1'].nunique().sort_values(ascending=False)[1]:,d}",color = "secondary"),
                        dbc.ListGroupItem("Oti region:"+" "+ f"{(data.groupby('Region name')['CASE_ID_1'].nunique().sort_values(ascending=False)[2]):,d}", color = "primary"),
                        dbc.ListGroupItem("Western region:"+" "+ f"{data.groupby('Region name')['CASE_ID_1'].nunique().sort_values(ascending=False)[3]:,d}",color = "success"),
                        
                    ],
                    flush=True,
                ),
                
            ]

        ),
        md=3
    )
    
    
])

content_second_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='use_of_structure_chart',figure = {}), md=6,  
                    className = "card",
        ),
        dbc.Col(
            dcc.Graph(id = "type_of_toilet_chart", figure ={}), md= 6,
            className = "card",
        )
    ]
)

content_fourth_row = dbc.Row(
    [
        dbc.Col(
            dcc.Graph(id='level_of_completion_chart',figure = {}), md=6, style = {"float":"left"}, className = "card",
        ),
        dbc.Col(
            dcc.Graph(id='Type_of_structure_chart',figure = {}), md=6,style = {"float":"left"}, className = "card",
        )
        
    ]
)




################################################################################################################

                      

#####################################################################################################################
content = html.Div(
   [
       html.H1("2021 Trial Census Dashboard", style=HEADER_STYLE),
                
                
                
                
                
       html.Div(
    [
        dbc.Button(
            "info", id="open-body-scroll",color = "primary", n_clicks=0, style = BUTTON_STYLE,
        ),
        
        dbc.Modal(
            [
                dbc.ModalHeader("Dashboard Info"),
                dbc.ModalBody("This dashboard is developed for Ghana Statistical Service(GSS) through a partnership with\
                Global Partnership for Sustainable Development Data (GPSDD)\
                and the African Institute for Mathematical Sciences (AIMS).\nThe data used in this dashbaord is 2021 trial census data provided by GSS. Use the scroll bar on your right of the dashboard to reach the buttom of the page." "\nUse the sidebar button to show/hide the Aggregation pannel."),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close",
                        id="close-body-scroll",
                        className="ml-auto",
                        n_clicks=0, 
                    )
                ),
            ],
            id="modal-body-scroll",
            size = "lg",
            scrollable=True,
            #fade = True,
            is_open=False,
            
        
        ),

        dbc.Button("Sidebar", color="success", className="mr-1", id="btn_sidebar", style = BUTTON_STYLE1),
    ]
           
),
        #html.Div([
          #  html.Img(
          #          src='data:image/png;base64,{}'.format(encoded_image),
          #          height = '43 px',
          #          width = 'auto')
            
          #  ],
          #  
#),


       
       html.Hr(),
       content_first_row,
       content_second_row,
       #content_third_row,
       content_fourth_row,
        
        
    ],
    
    id = "page-content",
    style=CONTENT_STYLE
    
)
#Modal call back..Info button#############################
@app.callback(
    Output("modal-body-scroll", "is_open"),
    [
        Input("open-body-scroll", "n_clicks"),
        Input("close-body-scroll", "n_clicks"),
    ],
    [State("modal-body-scroll", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

### Sidebar button . To maximise graph view session by hiding/showing the sidebars

@app.callback(
    [
        Output("sidebar", "style"),
        Output("page-content", "style"),
        Output("side_click", "data"),
    ],

    [Input("btn_sidebar", "n_clicks")],
    [
        State("side_click", "data"),
    ]
)
def toggle_sidebar(n, nclick):
    if n:
        if nclick == "SHOW":
            sidebar_style = SIDEBAR_HIDEN
            content_style = CONTENT_STYLE1
            cur_nclick = "HIDDEN"
        else:
            sidebar_style = SIDEBAR_STYLE
            content_style = CONTENT_STYLE
            cur_nclick = "SHOW"
    else:
        sidebar_style = SIDEBAR_STYLE
        content_style = CONTENT_STYLE
        cur_nclick = 'SHOW'

    return sidebar_style, content_style, cur_nclick

################################################################################################################
        




app.layout = html.Div([sidebar, content, dcc.Store(id='side_click'),])
#####################################################################################################################


#################################################################################################################

 


####################################################################################################################

@app.callback(
    Output('use_of_structure_chart', 'figure'),
    Input('district-dpdn', 'value'),
    Input('region-dpdn', 'value')
)


def update_grpah(selected_counties, selected_state):
    if len(selected_counties)==0:
        return dash.no_update
        emp_list = list(set(data['District name'].to_list()))
        return [{'label': i, 'value': i} for i in emp_list] 
    
    
    else:
        dff = data[(data["Region name"]==selected_state) & (data["District name"].isin(selected_counties))]
        use_of_structure_chart_figure = {
        "data": [
            {
                "y": dff["Use of structure"].unique(),
                "x": dff["Use of structure"].value_counts()[:10],
                "type": "bar",
                "orientation":"h",

                "hovertemplate": "%{x:0f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "DISTRIBUTION OF STUCTURES BY USE",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True,"title":"COUNT"},
            "yaxis": {"fixedrange": True, "title":"USE"},
           
            "colorway": ["#fdfab1"],
            'paper_bgcolor': colors['background'],
            'plot_bgcolor': colors['background'],
            'font':{'color': colors['text']},
            
        },
    }

    return use_of_structure_chart_figure


        
        
@app.callback(
    Output('type_of_toilet_chart', 'figure'),
    Input('district-dpdn', 'value'),
    Input('region-dpdn', 'value')
)


def update_grpah(selected_counties, selected_state):
    if len(selected_counties)==0:
        return dash.no_update
        emp_list = list(set(data['District name'].to_list()))
        return [{'label': i, 'value': i} for i in emp_list] 
    
    else:
        dff = data[(data["Region name"]==selected_state) & (data["District name"].isin(selected_counties))]
        type_of_toilet_chart_figure = {
        "data": [
            {
                "y": dff["What type of toilet facility are available in this house/structure?"].unique(),
                "x": dff["What type of toilet facility are available in this house/structure?"].value_counts(),
                "type": "funnel","opacity": 0.85,"size":100,"textinfo":"value+percent total", "textposition":"outside",

                "hovertemplate": "%{x:0f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "TYPE OF TOILET AVAILABLE",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True,"title":"COUNT"},
            "yaxis": {"fixedrange": True, "title":"TYPE"},
            
            "colorway": ["#bb6190"],
            'paper_bgcolor': colors['background'],
            'plot_bgcolor': colors['background'],
            'font':{'color': colors['text']},
        },
    }
    
    return type_of_toilet_chart_figure





@app.callback(
    Output("level_of_completion_chart", 'figure'),
    [Input('district-dpdn', 'value'),
    Input('region-dpdn', 'value')],
)


def update_grpah(selected_counties, selected_state):
    if len(selected_counties)==0:
        return dash.no_update
        emp_list = list(set(data['District name'].to_list()))
        return [{'label': i, 'value': i} for i in emp_list] 
    #return dash.no_update
 #   
    else:
        dff = data[(data["Region name"]==selected_state) & (data["District name"].isin(selected_counties))]
        level_of_completion_chart_figure = {
        "data": [
            {
                "x": dff["Level of completion"].unique(),
                "y": dff["Level of completion"].value_counts(),
                "type": "bar","textinfo":"value+percent total",
               

                "hovertemplate": "%{y:0f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "DISTRIBUTION OF STUCTURES BY LEVEL OF COMPLETION",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": False,"title":"LEVEL"},
            "yaxis": {"fixedrange": True,"title":"COUNT"},
            
            "colorway": ["#d8fdb1"],
            'paper_bgcolor': colors['background'],
            'plot_bgcolor': colors['background'],
            'font':{'color': colors['text']},
        },
    }
    
    return level_of_completion_chart_figure


        

    
    
    
@app.callback(
    Output("Type_of_structure_chart", 'figure'),
    [Input('district-dpdn', 'value'),
    Input('region-dpdn', 'value')],
)


def update_grpah(selected_counties, selected_state):
    if len(selected_counties)==0:
        return dash.no_update
        emp_list = list(set(data['District name'].to_list()))
        return [{'label': i, 'value': i} for i in emp_list] 
    #return dash.no_update
 #   
    else:
        dff = data[(data["Region name"]==selected_state) & (data["District name"].isin(selected_counties))]

    Type_of_structure_chart_figure = {
        "data": [
            {    
                "y": dff["Type of structure"].unique(),
                "x": dff["Type of structure"].value_counts(),
                "type": "funnel","textinfo":"value+percent total","textposition":"outside",

                "hovertemplate": "%{x:0f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "DISTRIBUTION OF STUCTURES BY TYPE",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            
            "colorway": ["#f88824"],
            'paper_bgcolor': colors['background'],
            'plot_bgcolor': colors['background'],
            'font':{'color': colors['text']},
           
        },
    }
    
    return Type_of_structure_chart_figure


if __name__ == '__main__':
    app.run_server(debug=True)
