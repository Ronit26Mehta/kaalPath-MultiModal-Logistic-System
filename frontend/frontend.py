import streamlit as st
import requests
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta
import random

# Set page configuration
st.set_page_config(
    page_title="Kaal Path - Multi-Modal Route Selector",
    layout="wide",
    page_icon="🚚",
    initial_sidebar_state="expanded"
)

# Load custom CSS for consistent styling
def load_css():
    css = """
    <style>
    body {
        font-family: 'Roboto', sans-serif;
        background-color: #f5f6f5;
        color: #333;
    }
    .stButton>button {
        background-color: #1e88e5;
        color: white;
        border: none;
        padding: 12px 24px;
        font-size: 16px;
        border-radius: 6px;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1565c0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #0277bd, #b3e5fc);
        color: white;
        padding: 20px;
    }
    h1, h2, h3 {
        color: #0277bd;
        font-weight: 500;
    }
    .stTextInput>label, .stNumberInput>label, .stSelectbox>label, .stDateInput>label {
        font-weight: bold;
        color: #424242;
    }
    .metric-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Apply CSS
load_css()

# Title and branding
st.title("🚚 Kaal Path - Multi-Modal Logistics Optimization")
st.markdown("Optimize cross-border shipments with advanced routing solutions.")

# Sidebar navigation
st.sidebar.image("https://via.placeholder.com/150x50.png?text=Kaal+Path", use_container_width=True)
st.sidebar.title("Navigation")
pages = [
    "Shipment & Simulation",
    "Quantum Annealing Optimization",
    "Fuzzy Logic Ranking",
    "Deep Route Prediction",
    "Dashboard"
]
page = st.sidebar.radio("Go to", pages)

# Function to simulate shipment data
def get_shipment_data():
    data = {
        "Shipment ID": [f"S{i:03d}" for i in range(1, 11)],
        "Origin": ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"],
        "Destination": ["London", "Paris", "Berlin", "Tokyo", "Beijing", "Sydney", "Dubai", "Singapore", "Hong Kong", "Mumbai"],
        "Weight (kg)": [random.uniform(50, 500) for _ in range(10)],
        "Volume (m³)": [random.uniform(10, 100) for _ in range(10)],
        "Cargo Type": random.choices(["Fragile", "Non-Fragile", "Hazardous"], k=10),
        "Transport Modes": random.choices(["Air", "Sea", "Land", "Air-Land", "Sea-Land"], k=10),
        "Shipping Date": [date.today() - timedelta(days=random.randint(0, 30)) for _ in range(10)],
        "Distance (km)": [random.uniform(500, 10000) for _ in range(10)],
        "Cost ($)": [random.uniform(1000, 10000) for _ in range(10)],
        "Time (hrs)": [random.uniform(10, 100) for _ in range(10)],
        "Efficiency": [random.uniform(50, 100) for _ in range(10)]
    }
    return pd.DataFrame(data)

# Function to simulate Quantum Annealing Optimization data
def get_quantum_optimization_data():
    data = {
        "Route ID": [f"R{i:03d}" for i in range(1, 11)],
        "Optimization Score": [random.uniform(60, 100) for _ in range(10)],
        "Transport Mode": random.choices(["Air", "Sea", "Land", "Air-Land", "Sea-Land"], k=10)
    }
    return pd.DataFrame(data)

# Function to simulate Fuzzy Logic Ranking data
def get_fuzzy_ranking_data():
    data = {
        "Route ID": [f"R{i:03d}" for i in range(1, 11)],
        "Ranking Score": [random.uniform(0, 1) for _ in range(10)],
        "Ranking Date": [date.today() - timedelta(days=random.randint(0, 30)) for _ in range(10)]
    }
    return pd.DataFrame(data)

# Function to simulate Deep Route Prediction data
def get_route_prediction_data():
    data = {
        "Route ID": [f"R{i:03d}" for i in range(1, 11)],
        "Predicted Time (hrs)": [random.uniform(10, 100) for _ in range(10)],
        "Actual Time (hrs)": [random.uniform(10, 100) for _ in range(10)],
        "Prediction Accuracy (%)": [random.uniform(80, 100) for _ in range(10)]
    }
    return pd.DataFrame(data)

# Page 1: Shipment & Simulation
def shipment_simulation_page():
    st.header("Shipment Input & Route Simulation")
    st.markdown("Enter shipment details and simulate multi-modal routes.")
    
    with st.form("shipment_form"):
        col1, col2 = st.columns(2)
        with col1:
            shipment_id = st.number_input("Shipment ID", min_value=1, step=1, value=1)
            origin = st.text_input("Origin", "New York")
            destination = st.text_input("Destination", "London")
            weight = st.number_input("Weight (kg)", min_value=1.0, value=100.0)
        with col2:
            volume = st.number_input("Volume (m³)", min_value=1.0, value=50.0)
            cargo_type = st.selectbox("Cargo Type", ["Fragile", "Non-Fragile", "Hazardous"])
            transport_modes = st.multiselect("Preferred Transport Modes", ["Air", "Sea", "Land"], default=["Air", "Land"])
            shipping_date = st.date_input("Shipping Date", date.today())
        
        submitted = st.form_submit_button("Submit Shipment")
        if submitted:
            with st.spinner("Submitting shipment..."):
                data = {
                    "shipment_id": shipment_id,
                    "origin": origin,
                    "destination": destination,
                    "weight": weight,
                    "volume": volume,
                    "cargo_type": cargo_type,
                    "transport_modes": transport_modes,
                    "shipping_date": shipping_date.strftime("%Y-%m-%d")
                }
                try:
                    res = requests.post("http://localhost:5000/shipment", json=data)
                    if res.status_code == 200:
                        st.success("Shipment submitted successfully!")
                        st.json(res.json())
                    else:
                        st.error(f"Error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Failed to submit shipment: {str(e)}")
    st.subheader("Simulate Multi-Modal Routes")
    with st.expander("Route Simulation", expanded=False):
        sim_origin = st.text_input("Simulation Origin", origin)
        sim_destination = st.text_input("Simulation Destination", destination)
        if st.button("Simulate Routes"):
            with st.spinner("Simulating routes..."):
                try:
                    res = requests.post("http://localhost:5000/simulate", json={"origin": sim_origin, "destination": sim_destination})
                    if res.status_code == 200:
                        routes = res.json().get("routes", [])
                        st.info("Simulated Multi-Modal Routes")
                        st.json(routes)
                    else:
                        st.error(f"Simulation failed: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Error during simulation: {str(e)}")

# Page 2: Quantum Annealing Optimization
def quantum_annealing_page():
    st.header("Quantum Annealing Optimization")
    st.markdown("Optimize routes using quantum annealing.")
    
    with st.form("quantum_form"):
        col1, col2 = st.columns(2)
        with col1:
            q_shipment_id = st.number_input("Shipment ID", min_value=1, step=1, value=2)
            q_origin = st.text_input("Origin", "New York")
            q_destination = st.text_input("Destination", "London")
            q_weight = st.number_input("Weight (kg)", min_value=1.0, value=150.0)
        with col2:
            q_volume = st.number_input("Volume (m³)", min_value=1.0, value=60.0)
            q_cargo_type = st.selectbox("Cargo Type", ["Fragile", "Non-Fragile", "Hazardous"])
            q_transport_modes = st.multiselect("Preferred Transport Modes", ["Air", "Sea", "Land"], default=["Air", "Land"])
            q_shipping_date = st.date_input("Shipping Date", date.today())
        
        q_submitted = st.form_submit_button("Run Quantum Optimization")
        if q_submitted:
            with st.spinner("Running quantum optimization..."):
                data = {
                    "shipment_id": q_shipment_id,
                    "origin": q_origin,
                    "destination": q_destination,
                    "weight": q_weight,
                    "volume": q_volume,
                    "cargo_type": q_cargo_type,
                    "transport_modes": q_transport_modes,
                    "shipping_date": q_shipping_date.strftime("%Y-%m-%d")
                }
                try:
                    res = requests.post("http://localhost:5000/quantum_analysis", json=data)
                    if res.status_code == 200:
                        st.success("Quantum Optimization Report")
                        st.json(res.json())
                    else:
                        st.error(f"Error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Failed to run quantum optimization: {str(e)}")

# Page 3: Fuzzy Logic Ranking
def fuzzy_logic_page():
    st.header("Fuzzy Logic Route Ranking")
    st.markdown("Rank routes based on fuzzy logic.")
    
    with st.form("fuzzy_form"):
        f_origin = st.text_input("Origin", "New York")
        f_destination = st.text_input("Destination", "London")
        f_submitted = st.form_submit_button("Run Fuzzy Logic Ranking")
        if f_submitted:
            with st.spinner("Ranking routes..."):
                try:
                    res = requests.post("http://localhost:5000/fuzzy_logic_ranking", json={"origin": f_origin, "destination": f_destination})
                    if res.status_code == 200:
                        st.success("Fuzzy Logic Ranked Routes")
                        st.json(res.json())
                    else:
                        st.error(f"Error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Failed to rank routes: {str(e)}")

# Page 4: Deep Route Prediction
def deep_route_prediction_page():
    st.header("Deep Route Prediction")
    st.markdown("Predict route quality with deep learning.")
    
    with st.form("ml_form"):
        st.write("Enter route features:")
        feature1 = st.number_input("Distance (km)", min_value=0.0, value=1200.0)
        feature2 = st.number_input("Cost ($)", min_value=0.0, value=800.0)
        feature3 = st.number_input("Time (hours)", min_value=0.0, value=30.0)
        feature4 = st.number_input("Efficiency Score", min_value=0.0, value=85.0)
        ml_submitted = st.form_submit_button("Predict Route Quality")
        if ml_submitted:
            features = [feature1, feature2, feature3, feature4]
            with st.spinner("Predicting route quality..."):
                try:
                    res = requests.post("http://localhost:5000/ml_predict", json={"features": features})
                    if res.status_code == 200:
                        ml_pred = res.json().get("ml_prediction", 0.0)
                        st.success(f"Predicted Route Quality Score: {ml_pred:.2f}")
                    else:
                        st.error(f"Error: {res.status_code} - {res.text}")
                except Exception as e:
                    st.error(f"Failed to predict route quality: {str(e)}")

# Page 5: Enhanced Dashboard
def dashboard_page():
    st.header("Logistics Dashboard")
    st.markdown("Monitor and analyze your cross-border shipment performance.")

    # Get simulated data from all pages
    df_shipment = get_shipment_data()
    df_quantum = get_quantum_optimization_data()
    df_fuzzy = get_fuzzy_ranking_data()
    df_prediction = get_route_prediction_data()

    # Tabs for organizing visualizations
    tab1, tab2, tab3, tab4 = st.tabs([
        "Shipment & Simulation",
        "Quantum Annealing Optimization",
        "Fuzzy Logic Ranking",
        "Deep Route Prediction"
    ])

    # Tab 1: Shipment & Simulation
    with tab1:
        st.subheader("Shipment & Simulation Metrics")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Shipments", len(df_shipment))
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Cost", f"${df_shipment['Cost ($)'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Time", f"{df_shipment['Time (hrs)'].mean():.2f} hrs")
            st.markdown('</div>', unsafe_allow_html=True)
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Efficiency", f"{df_shipment['Efficiency'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col5:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Total Volume", f"{df_shipment['Volume (m³)'].sum():.2f} m³")
            st.markdown('</div>', unsafe_allow_html=True)

        # Interactive Data Table
        st.subheader("Shipment Data")
        st.dataframe(df_shipment)

        # Pie Chart: Cargo Type Distribution
        st.subheader("Cargo Type Distribution")
        cargo_counts = df_shipment['Cargo Type'].value_counts()
        fig_pie = px.pie(cargo_counts, names=cargo_counts.index, values=cargo_counts.values, title="Cargo Type Distribution")
        st.plotly_chart(fig_pie, use_container_width=True)

        # Line Chart: Shipment Costs Over Time
        st.subheader("Shipment Costs Over Time")
        df_shipment['Shipping Date'] = pd.to_datetime(df_shipment['Shipping Date'])
        df_sorted = df_shipment.sort_values('Shipping Date')
        fig_line = px.line(df_sorted, x='Shipping Date', y='Cost ($)', title="Shipment Costs Over Time", markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

        # Scatter Plot: Distance vs Time
        st.subheader("Distance vs Time by Transport Mode")
        fig_scatter = px.scatter(df_shipment, x='Distance (km)', y='Time (hrs)', color='Transport Modes', size='Weight (kg)', hover_data=['Shipment ID'], title="Distance vs Time by Transport Mode")
        st.plotly_chart(fig_scatter, use_container_width=True)

        # Heatmap: Correlations
        st.subheader("Correlation Heatmap")
        corr_matrix = df_shipment[['Distance (km)', 'Time (hrs)', 'Cost ($)', 'Efficiency']].corr()
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='Viridis'
        ))
        fig_heatmap.update_layout(title="Correlation Heatmap")
        st.plotly_chart(fig_heatmap, use_container_width=True)

        # Box Plot: Cost Distribution by Transport Mode
        st.subheader("Cost Distribution by Transport Mode")
        fig_box = px.box(df_shipment, x='Transport Modes', y='Cost ($)', title="Cost Distribution by Transport Mode")
        st.plotly_chart(fig_box, use_container_width=True)

    # Tab 2: Quantum Annealing Optimization
    with tab2:
        st.subheader("Quantum Annealing Optimization Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Optimization Score", f"{df_quantum['Optimization Score'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Best Route", df_quantum.loc[df_quantum['Optimization Score'].idxmax(), 'Route ID'])
            st.markdown('</div>', unsafe_allow_html=True)

        # Bar Chart: Optimization Scores by Route
        st.subheader("Optimization Scores by Route")
        fig_bar_quantum = px.bar(df_quantum, x='Route ID', y='Optimization Score', color='Transport Mode', title="Optimization Scores by Route")
        st.plotly_chart(fig_bar_quantum, use_container_width=True)

    # Tab 3: Fuzzy Logic Ranking
    with tab3:
        st.subheader("Fuzzy Logic Ranking Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Ranking Score", f"{df_fuzzy['Ranking Score'].mean():.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Top Ranked Route", df_fuzzy.loc[df_fuzzy['Ranking Score'].idxmax(), 'Route ID'])
            st.markdown('</div>', unsafe_allow_html=True)

        # Line Chart: Ranking Trends Over Time
        st.subheader("Ranking Trends Over Time")
        df_fuzzy['Ranking Date'] = pd.to_datetime(df_fuzzy['Ranking Date'])
        df_fuzzy_sorted = df_fuzzy.sort_values('Ranking Date')
        fig_line_fuzzy = px.line(df_fuzzy_sorted, x='Ranking Date', y='Ranking Score', color='Route ID', title="Ranking Trends Over Time", markers=True)
        st.plotly_chart(fig_line_fuzzy, use_container_width=True)

    # Tab 4: Deep Route Prediction
    with tab4:
        st.subheader("Deep Route Prediction Metrics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Avg Prediction Accuracy", f"{df_prediction['Prediction Accuracy (%)'].mean():.2f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Most Accurate Route", df_prediction.loc[df_prediction['Prediction Accuracy (%)'].idxmax(), 'Route ID'])
            st.markdown('</div>', unsafe_allow_html=True)

        # Scatter Plot: Predicted vs Actual Time
        st.subheader("Predicted vs Actual Time")
        fig_scatter_pred = px.scatter(df_prediction, x='Predicted Time (hrs)', y='Actual Time (hrs)', color='Route ID', size='Prediction Accuracy (%)', hover_data=['Route ID'], title="Predicted vs Actual Time")
        st.plotly_chart(fig_scatter_pred, use_container_width=True)

# Page routing
if page == "Shipment & Simulation":
    shipment_simulation_page()
elif page == "Quantum Annealing Optimization":
    quantum_annealing_page()
elif page == "Fuzzy Logic Ranking":
    fuzzy_logic_page()
elif page == "Deep Route Prediction":
    deep_route_prediction_page()
elif page == "Dashboard":
    dashboard_page()

# Footer
st.markdown("---")
st.markdown("© 2025 Kaal Path | Powered by IIT Bombay LogiTHON")