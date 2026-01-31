

import streamlit as st
import pandas as pd
import joblib
st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #f8fbff 0%, #eef3f8 100%);
}

/* Titles */
h1, h2, h3 {
    color: #1f2937;
    font-weight: 600;
}
 h1 {
    text-align: center;
    font-weight: 800;
    font-size: 2.6rem;
    letter-spacing: -0.6px;
    color: #0f172a;
    margin-bottom: 0.6rem;
    background-color: #ECFDF5;

}

/* Cards */
div[data-testid="stVerticalBlock"] > div {
    background-color: #F0FDF4;
    border-radius: 14px;
    padding: 1.2rem;
    box-shadow: 0px 4px 14px rgba(0, 0, 0, 0.06);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* Buttons */
.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
}
.stButton > button:hover {
    background-color: #1d4ed8;
}

/* Metrics */
div[data-testid="metric-container"] {
    background-color: #f8fafc;
    border-radius: 12px;
    padding: 1rem;
    border-left: 6px solid #2563eb;
}
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Ethanol Yield Predictor", layout="wide",
    initial_sidebar_state="expanded")

@st.cache_resource
def load_model():
    return joblib.load('model3.pkl')

model3 = load_model()

st.title("ETHANOL YIELD PREDICTION")


col1, col2 = st.columns([1.1, 1.1], gap="large")

with col1:
    st.subheader("INPUTS")

    Raw_Material=st.selectbox(
        "Raw_Material",
        ['Sugarcane', 'Corn', 'Bagasse', 'Wheat', 'Cellulose']
    )
    Strain=st.selectbox(
        "Strain",
        ['Z_mobilis', 'K_marxianus', 'S_cerevisiae'])	
    Reactor_Type=st.selectbox(
        "Reactor_Type",
        ['Fluidized_Bed', 'Stirred_Tank', 'Packed_Bed'])	
    Pretreatment=st.selectbox(
        "Pretreatment",
        ['None', 'Physical', 'Chemical', 'Enzymatic'])	
    	
    Lignin_percent=st.number_input(
        "Lignin_percent",
        min_value=0.0,
        max_value=30.0,
        step=0.1
    )
    Moisture_percent=	st.number_input(
        "Moisture_percent",
        min_value=1.0,
        max_value=30.0,
        step=0.1
    )
    Ethanol_Tolerance_percent=st.number_input(
        "Ethanol_Tolerance_percent",
        min_value=4.0,
        step=0.1
    )
    
    Temperature_C=st.number_input(
        "Temperature_C",
        min_value=20.0,
        step=0.1
    )
    pH=st.slider(
        "pH",
        min_value=0.0,
        max_value=14.0,
        step=0.1
    )
    Fermentation_hours=st.number_input(
        "Fermentation_hours",
        min_value=0.0,
        step=0.1
    )
    Agitation_rpm=	st.number_input(
        "Agitation_rpm",
        min_value=10.0,
        step=10.0
    )
    Aeration_vvm=	st.number_input(
        "Aeration_vvm",
        min_value=0.1,
        step=0.1
    )
    Inoculum_percent=st.number_input(
        "Inoculum_percent",
        min_value=1.0,
        step=0.1
    )
    Enzyme_gL=st.number_input(
        "Enzyme_gL",
        min_value=1.0,
        max_value=20.0,
        step=0.1
    )
    Total_Sugar_gL=st.number_input(
        "Total_Sugar_gL",
        min_value=0.0,
        step=0.1
    )
    
    Process_Efficiency=st.number_input(
        "Process_Efficiency",
        min_value=0.5,
        max_value=1.0,
        step=0.1
    )

    input_df = pd.DataFrame({
        "Raw_Material":[Raw_Material],
        "Strain":[Strain],
        "Reactor_Type":[Reactor_Type],
        "Pretreatment": [Pretreatment],
        'Lignin_percent':[Lignin_percent],
        'Moisture_percent':[Moisture_percent],
        'Ethanol_Tolerance_percent':[Ethanol_Tolerance_percent],
        "Temperature_C": [Temperature_C],
        "pH": [pH],
        'Fermentation_hours':[Fermentation_hours],
        'Agitation_rpm':[Agitation_rpm],
            'Aeration_vvm':[Aeration_vvm],
            'Inoculum_percent':[Inoculum_percent],
        "Enzyme_gL": [Enzyme_gL],
        "Total_Sugar_gL":[Total_Sugar_gL],
        "Process_Efficiency":[Process_Efficiency]
    })

with col2:
    st.subheader("PREDICTION OUTPUT")
    if st.button("Predict Ethanol Yield"):
        if Total_Sugar_gL <5:
            st.warning("⚠️ Low fermentable sugar → ethanol yield will be unrealistic.")
            
        else:    
            prediction = model3.predict(input_df)
            pred_value = float(prediction[0])
            st.success(f"Predicted Ethanol Yield: {pred_value:.2f} g/L")
            type(model3)
            pred = prediction[0]
            max_yield = 150  # adjust to your dataset

            st.metric(
                label="Predicted Ethanol Yield (g/L)",
                value=f"{pred:.2f}",
                delta=f"{(pred/max_yield)*100:.1f}% of max"
            )

            st.progress(min(int((pred/max_yield)*100), 100))

            if pred < 50:
                level = "🔴 Low Yield"
            elif pred < 80:
                level = "🟡 Moderate Yield"
            else:
                level = "🟢 High Yield"

            st.subheader(level)
            import plotly.graph_objects as go

            def yield_gauge(y_pred2):
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=y_pred2,
                    number={
                     "suffix": " g/L",
                    "font": {"size": 36}
                        },
                    title={'text': "Predicted Ethanol Yield (g/L)"},
                    gauge={
                        'axis': {'range': [0, 150]},
                        'bar': {'color': "#2563eb"},
                        'steps': [
                            {'range': [0, 50], 'color': "#fee2e2"},
                            {'range': [50, 90], 'color': "#fef3c7"},
                            {'range': [90, 150], 'color': "#dcfce7"},
                        ],
                    }
                ))
                return fig
            st.plotly_chart(yield_gauge(pred_value), use_container_width=True)
            import plotly.graph_objects as go

            def process_radar(input_df):
                    # Normalize values (0–1 scale) based on realistic industrial ranges
                radar_data = {
                    "Temperature": min(input_df["Temperature_C"].iloc[0] / 40, 1),
                    "pH": min(input_df["pH"].iloc[0] / 5, 1),
                    "Sugar": min(input_df["Total_Sugar_gL"].iloc[0] / 168, 1),
                    "Enzyme": min(input_df["Enzyme_gL"].iloc[0] / 5.65, 1),
                    "Time": min(input_df["Fermentation_hours"].iloc[0] / 40, 1),
                    "Efficiency": min(input_df["Process_Efficiency"].iloc[0] / 1, 1),
                    "Agitation_RPM":min(input_df['Agitation_rpm'].iloc[0]/159,1)
                }

                fig = go.Figure()

                fig.add_trace(go.Scatterpolar(
                    r=list(radar_data.values()),
                    theta=list(radar_data.keys()),
                    fill='toself',
                    name='Process Health'
                    
                ))

                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                    title="Process Health Radar",
                    height=420,
                    showlegend=True,
                )
                fig.add_annotation(
                    text="⬤ Optimal → 1.0<br>⬤ Poor → 0.0",
                    x=1.15,
                    y=0.5,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=12)
                )

                return fig
            
            st.plotly_chart(process_radar(input_df), use_container_width=True)


    import plotly.express as px
    import pandas as pd

    ethanol_frac = 0.70  # typical share
    data = {
                        "Product": ["Ethanol", "CO₂", "Biomass", "Glycerol", "Other losses"],
                        "Fraction (%)": [
                            ethanol_frac * 100,
                            22,
                            5,
                            2,
                            1
                        ]
                    }

    df_pie = pd.DataFrame(data)

    fig = px.pie(
                        df_pie,
                        names="Product",
                        values="Fraction (%)",
                        hole=0.45,
                        title="Estimated Fermentation Product Distribution"
                    )

    fig.update_traces(
                        textinfo="label+percent",
                        pull=[0.05, 0, 0, 0, 0]
                    )

    fig.update_layout(
                        height=420,
                        showlegend=True
                    )

    st.plotly_chart(fig, use_container_width=True)
                
        

kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("Model R² Score", "0.75")

with kpi2:
    st.metric("Algorithm", "GradientBoosting")

with kpi3:
    st.metric("Dataset Size", "7000 rows")
