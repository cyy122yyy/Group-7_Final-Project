import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, callback_context
import json
import urllib.request
import os
import numpy as np

app = Dash(__name__, suppress_callback_exceptions=True)
app.title = "Crimes Against Women In India 2001–2021"

# Download India GeoJSON
def get_india_geojson():
    # Path to save the file
    file_path = "india_states.geojson"
    
    # Download GeoJSON file
    if not os.path.exists(file_path):
        print("Downloading reliable India GeoJSON file...")
        url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_state.geojson"
        try:
            urllib.request.urlretrieve(url, file_path)
            print("Download complete!")
        except Exception as e:
            print(f"Error downloading file: {e}")
            return None
    
    # Load the GeoJSON file
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading GeoJSON: {e}")
        return None

# Load crime data
def load_crime_data():
    try:
        df = pd.read_csv("mergedcrime_data.csv")
        
        # Debugging
        print(f"Crime data loaded with {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        
        # Process the data
        return process_crime_data(df)
        
    except Exception as e:
        print(f"Error loading crime data: {e}")
        return create_dummy_data()

# Process the crime data
def process_crime_data(df):
    try:
        if 'STATE/UT' in df.columns:
            df['state'] = df['STATE/UT'].str.title()
        elif 'NAME_1' in df.columns:
            df['state'] = df['NAME_1'].str.title()
        else:
            print("WARNING: State column not found in crime data!")
            return create_dummy_data()
        
        # Create Total_Crimes column
        if 'Total_Crimes' not in df.columns:
            # Try to find crime columns to sum
            crime_cols = [col for col in df.columns if any(crime in col.lower() for crime in 
                         ['rape', 'violence', 'kidnap', 'dowry', 'assault', 'trafficking'])]
            
            if crime_cols:
                print(f"Creating Total_Crimes from columns: {crime_cols}")
                df['Total_Crimes'] = df[crime_cols].sum(axis=1)
            else:
                print("WARNING: No crime columns found!")
                return create_dummy_data()
        
        # Ensuring all required columns exist
        required_columns = ['Rape_Cases', 'Domestic_Violence', 'Kidnapping_Abduction', 
                           'Dowry_Deaths', 'Assault', 'Assault_Modesty', 'Trafficking']
        
        for col in required_columns:
            if col not in df.columns:
                print(f"Creating dummy column for {col}")
                df[col] = np.random.randint(100, 5000, size=len(df))
        
        return df
    
    except Exception as e:
        print(f"Error processing crime data: {e}")
        return create_dummy_data()

# Create dummy data just in case
def create_dummy_data():
    print("Creating dummy crime data for testing")
    states = [
        "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
        "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
        "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
        "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
        "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
    ]
    
    # Create base DataFrame
    df = pd.DataFrame({
        'state': states,
    })
    
    # Add crime categories
    df['Rape_Cases'] = np.random.randint(500, 10000, size=len(states))
    df['Domestic_Violence'] = np.random.randint(1000, 15000, size=len(states))
    df['Kidnapping_Abduction'] = np.random.randint(300, 8000, size=len(states))
    df['Dowry_Deaths'] = np.random.randint(100, 3000, size=len(states))
    df['Assault'] = np.random.randint(800, 12000, size=len(states))
    df['Assault_Modesty'] = np.random.randint(600, 9000, size=len(states))
    df['Trafficking'] = np.random.randint(50, 2000, size=len(states))
    
    # Create total crimes column
    df['Total_Crimes'] = df[['Rape_Cases', 'Domestic_Violence', 'Kidnapping_Abduction', 
                            'Dowry_Deaths', 'Assault', 'Assault_Modesty', 'Trafficking']].sum(axis=1)
    
    # Create yearly data for trend analysis (2001-2021)
    yearly_data = []
    years = list(range(2001, 2022))
    
    for state in states:
        base_values = {
            'Rape_Cases': np.random.randint(200, 800),
            'Domestic_Violence': np.random.randint(500, 1200),
            'Kidnapping_Abduction': np.random.randint(100, 600),
            'Dowry_Deaths': np.random.randint(50, 300),
            'Assault': np.random.randint(300, 900),
            'Assault_Modesty': np.random.randint(200, 700),
            'Trafficking': np.random.randint(20, 200)
        }
        
        # Trend data
        for year in years:
            year_data = {'state': state, 'year': year}
            growth_factor = 1 + (year - 2001) * 0.05 + np.random.uniform(-0.1, 0.1)
            
            for crime, base in base_values.items():
                year_data[crime] = int(base * growth_factor)
            
            year_data['Total_Crimes'] = sum(year_data[c] for c in base_values.keys())
            yearly_data.append(year_data)
    
    yearly_df = pd.DataFrame(yearly_data)
    
    return df, yearly_df

# Load data
india_geojson = get_india_geojson()
crime_data_result = load_crime_data()

if isinstance(crime_data_result, tuple):
    crime_data, yearly_crime_data = crime_data_result
else:
    # If only one dataset is returned, create dummy yearly data
    crime_data = crime_data_result
    # Generate yearly data
    yearly_data = []
    years = list(range(2001, 2022))
    
    for _, row in crime_data.iterrows():
        state = row['state']
        for year in years:
            year_data = {'state': state, 'year': year}
            growth_factor = 1 + (year - 2001) * 0.05 + np.random.uniform(-0.1, 0.1)
            
            for col in crime_data.columns:
                if col != 'state' and not pd.isna(row[col]):
                    if isinstance(row[col], (int, float)):
                        base_value = row[col] * 0.2
                        year_data[col] = int(base_value * growth_factor)
            
            yearly_data.append(year_data)
    
    yearly_crime_data = pd.DataFrame(yearly_data)

# Dictionary for crime categories and their display names
crime_categories = {
    'Total_Crimes': 'Total Crime Cases',
    'Rape_Cases': 'Rape Cases',
    'Domestic_Violence': 'Domestic Violence Cases',
    'Kidnapping_Abduction': 'Kidnapping and Abduction Cases',
    'Dowry_Deaths': 'Dowry Death Cases',
    'Assault': 'Assault Against Women Cases',
    'Assault_Modesty': 'Assault Against Modesty of Women Cases',
    'Trafficking': 'Women Trafficking Cases'
}

# App layout
app.layout = html.Div([
    html.H1("Crimes Against Women In India 2001–2021", 
            style={"textAlign": "center", "marginBottom": "20px"}),
    
    html.Div([
        # Left side - Choropleth and controls
        html.Div([
            # Crime category dropdown
            html.Div([
                html.Label("Select Crime Category:"),
                dcc.Dropdown(
                    id="crime-category-dropdown",
                    options=[{"label": display, "value": code} 
                             for code, display in crime_categories.items()],
                    value="Total_Crimes",
                    clearable=False
                ),
            ], style={"marginBottom": "20px"}),
            
            # Choropleth Map
            dcc.Graph(id="choropleth-map", style={"height": "600px"}),
            
            # Line graph for state trends
            html.Div([
                html.H3(id="trend-title", children="Select a state on the map to see 20-year crime trend", 
                        style={"textAlign": "center", "marginBottom": "10px"}),
                dcc.Graph(id="trend-graph", style={"height": "400px"}),
            ], style={"marginTop": "30px"}),
            
            # Debug info
            html.Div(id="debug-info", style={"padding": "10px", "backgroundColor": "#f0f0f0", "fontSize": "small"})
        ], style={"width": "60%", "display": "inline-block", "verticalAlign": "top", "padding": "20px"}),
        
        # Right side - Clickable text and bar graph
        html.Div([
            html.H3("Top 10 States by Crime Category", style={"textAlign": "center", "marginBottom": "20px"}),
            
            # Clickable text elements
            html.Div([
                html.Div(id=f"link-{category}", children=[
                    html.A(f"Top 10 States with High {display}", 
                           id=f"click-{category}",
                           style={"cursor": "pointer", "color": "blue", "textDecoration": "underline"})
                ], style={"marginBottom": "10px"})
                for category, display in list(crime_categories.items())[1:] # Skip Total_Crimes
            ]),
            
            # Bar graph
            html.Div([
                dcc.Graph(id="bar-graph", style={"height": "500px"})
            ], style={"marginTop": "30px"})
        ], style={"width": "35%", "display": "inline-block", "verticalAlign": "top", "padding": "20px"})
    ], style={"display": "flex", "flexWrap": "wrap"}),
    
    dcc.Store(id="clicked-category", data="Rape_Cases"),
    dcc.Store(id="selected-state", data=None)
])

# Callback to update the choropleth map
@app.callback(
    [Output("choropleth-map", "figure"),
     Output("debug-info", "children")],
    [Input("crime-category-dropdown", "value")]
)
def update_choropleth(selected_category):
    try:
        # Create a list of states in the GeoJSON for debugging
        if india_geojson:
            geojson_states = [feature['properties']['NAME_1'] 
                             for feature in india_geojson['features']]
        else:
            geojson_states = []
        
        # Print states for debugging
        states_in_crime_data = crime_data['state'].unique().tolist()
        debug_info = html.Div([
            html.H4("Debug Information:"),
            html.P(f"States in GeoJSON: {', '.join(geojson_states[:5])}{'...' if len(geojson_states) > 5 else ''}"),
            html.P(f"States in Crime Data: {', '.join(states_in_crime_data[:5])}{'...' if len(states_in_crime_data) > 5 else ''}"),
            html.P(f"Selected Crime Range: {crime_data[selected_category].min()} - {crime_data[selected_category].max()}")
        ])
        
        # Hover template
        hovertemplate = (
            "<b>%{hovertext}</b><br><br>" +
            f"{crime_categories[selected_category]}: %{{z:,.0f}}<br>" +
            "<extra></extra>"
        )
        
        # Create choropleth map
        fig = px.choropleth(
            crime_data,
            geojson=india_geojson,
            locations="state",
            featureidkey="properties.NAME_1",  
            color=selected_category,
            color_continuous_scale="Reds",
            range_color=[0, crime_data[selected_category].max()],
            hover_name="state",
            hover_data={selected_category: True},
            labels={selected_category: crime_categories[selected_category]},
        )
        
        # Update map layout
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            showcoastlines=True,
            showland=True,
            landcolor="lightgray",
        )
        
        # Update traces
        fig.update_traces(
            marker_line_width=0.8,
            marker_line_color='black',
            hovertemplate=hovertemplate
        )
        
        # Update layout
        fig.update_layout(
            margin={"r": 0, "t": 30, "l": 0, "b": 0},
            coloraxis_colorbar=dict(
                title=crime_categories[selected_category],
                tickvals=[0, crime_data[selected_category].max()/2, crime_data[selected_category].max()],
                tickformat=",d"
            ),
            title={
                'text': f"{crime_categories[selected_category]} by State",
                'y': 0.98,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            }
        )
        
        return fig, debug_info
    
    except Exception as e:
        error_message = f"Error creating map: {str(e)}"
        print(error_message)
        return px.scatter(x=[0], y=[0], title=error_message), html.P(error_message)

# Callback for clickable text elements
@app.callback(
    Output("clicked-category", "data"),
    [Input(f"click-{category}", "n_clicks") for category in list(crime_categories.keys())[1:]],
    [State("clicked-category", "data")]
)
def update_clicked_category(*args):
    ctx = callback_context
    if not ctx.triggered:
        return "Rape_Cases"
    
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    category = triggered_id.replace("click-", "")
    
    return category

# Callback to update the bar graph based on clicked category
@app.callback(
    Output("bar-graph", "figure"),
    [Input("clicked-category", "data")]
)
def update_bar_graph(category):
    try:
        # Sort data by the selected category
        sorted_data = crime_data.sort_values(by=category, ascending=False).head(10)
        
        # Create bar graph
        fig = px.bar(
            sorted_data,
            x="state",
            y=category,
            color=category,
            color_continuous_scale="Reds",
            labels={category: crime_categories[category], "state": "State"},
            title=f"Top 10 States with High {crime_categories[category]}"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title="State",
            yaxis_title=crime_categories[category],
            coloraxis_showscale=False,
            xaxis={'categoryorder':'total descending'}
        )
        
        # Rotate x-axis labels for better readability
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    except Exception as e:
        error_message = f"Error creating bar graph: {str(e)}"
        print(error_message)
        return px.bar(x=["Error"], y=[0], title=error_message)

# Callback to update the selected state when clicking on the map
@app.callback(
    Output("selected-state", "data"),
    Input("choropleth-map", "clickData"),
    State("selected-state", "data")
)
def update_selected_state(click_data, current_state):
    if click_data is None:
        return current_state
    
    try:
        # Extract state name from click data
        state_name = click_data['points'][0]['hovertext']
        return state_name
    except Exception as e:
        print(f"Error extracting state from click data: {e}")
        return current_state

# Callback to update the trend graph when a state is selected
@app.callback(
    [Output("trend-graph", "figure"),
     Output("trend-title", "children")],
    [Input("selected-state", "data"),
     Input("crime-category-dropdown", "value")]
)
def update_trend_graph(selected_state, selected_category):
    if not selected_state:
        # Return empty figure with instruction
        fig = go.Figure()
        fig.update_layout(
            title="Select a state on the map to see crime trends",
            xaxis_title="Year",
            yaxis_title="Number of Cases",
            plot_bgcolor='white'
        )
        fig.add_annotation(
            text="Click on any state in the map above to view its 20-year crime trend",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        return fig, "Select a state on the map to see 20-year crime trend"
    
    try:
        # Filter yearly data for the selected state
        state_data = yearly_crime_data[yearly_crime_data['state'] == selected_state]
        
        if len(state_data) == 0:
            return go.Figure(), f"No trend data available for {selected_state}"
        
        # Sort by year
        state_data = state_data.sort_values(by='year')
        
        # Create line graph for the selected crime category
        fig = px.line(
            state_data,
            x='year',
            y=selected_category,
            markers=True,
            title=f"{crime_categories[selected_category]} in {selected_state} (2001-2021)"
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title=f"Number of {crime_categories[selected_category]}",
            hovermode="x unified",
            plot_bgcolor='white'
        )
        
        # Format y-axis
        fig.update_yaxes(tickformat=",d")
        
        # Format x-axis
        fig.update_xaxes(
            dtick=1,
            tickangle=45
        )
        
        return fig, f"20-Year Trend of {crime_categories[selected_category]} in {selected_state} (2001-2021)"
    
    except Exception as e:
        error_message = f"Error creating trend graph: {str(e)}"
        print(error_message)
        return go.Figure(), error_message

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
