import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import spc_core, ai_engine, predictive_engine
from fpdf import FPDF
import io

# PAGE CONFIG 
st.set_page_config(page_title="Smart SPC Dashboard", layout="wide")
st.title(" AI-Powered Production Monitor")

# SIDEBAR & DATA 
st.sidebar.header("AI Settings")
sens = st.sidebar.slider("Detection Sensitivity", 0.01, 0.20, 0.15)

df = pd.read_csv("process_data.csv")
x_bar = df.mean(axis=1, numeric_only=True)

# ANALYTICS 
ucl, lcl, cl = spc_core.get_spc_limits(df)
ai_preds = ai_engine.get_ai_predictions(df, sensitivity=sens)
future_val = predictive_engine.get_next_prediction(df)

# DASHBOARD LAYOUT
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Statistical View")
    fig1, ax1 = plt.subplots()
    ax1.plot(x_bar, marker='o', label='Subgroup Mean')
    
    # Draw the Red Safety Lines
    ax1.axhline(ucl, color='r', linestyle='--', label=f'UCL ({ucl:.2f})')
    ax1.axhline(lcl, color='r', linestyle='--', label=f'LCL ({lcl:.2f})')
    ax1.axhline(cl, color='g', linewidth=2, label=f'Grand Mean ({cl:.2f})')
    ax1.set_title("Traditional X-bar Control Chart")
    ax1.legend()
    st.pyplot(fig1)

with col2:
    st.subheader(" AI & Prediction View")
    fig2, ax2 = plt.subplots()
    ax2.plot(x_bar, color='lightgrey', alpha=0.5, label='Process Flow')
    ax2.axhline(ucl, color='r', linestyle='--', alpha=0.7)
    ax2.axhline(lcl, color='r', linestyle='--', alpha=0.7)
    ax2.axhline(cl, color='g', linewidth=2, alpha=0.7)

    anomalies = x_bar[ai_preds == -1]
    ax2.scatter(anomalies.index, anomalies.values, color='orange', s=100, label='AI Detected')
    ax2.scatter(len(x_bar), future_val, color='purple', marker='X', s=200, label='Next Forecast')
    ax2.legend()
    st.pyplot(fig2)

# ALERTS 
current_val = x_bar.iloc[-1]
if current_val > ucl or current_val < lcl:
    st.error(f"🚨 ALERT: Current Process OUT OF CONTROL! (Value: {current_val:.2f})")
elif future_val > ucl or future_val < lcl:
    st.warning(f"⚠️ WARNING: Future Trend predicts failure! (Predicted: {future_val:.2f})")
else:
    st.success("✅ Process Status: Stable.")

# DOWNLOAD SECTION 
st.divider()
st.subheader("📥 Export Analysis")
down_col1, down_col2 = st.columns(2)

# Function to generate PDF in-memory
def generate_pdf_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "AI-SPC Factory Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Upper Control Limit: {ucl:.2f}", ln=True)
    pdf.cell(200, 10, f"Lower Control Limit: {lcl:.2f}", ln=True)
    pdf.cell(200, 10, f"Grand Mean: {cl:.2f}", ln=True)
    pdf.cell(200, 10, f"Latest Measurement: {current_val:.2f}", ln=True)
    pdf.cell(200, 10, f"AI Sensitivity Setting: {sens}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

with down_col1:
    # Button for PDF
    pdf_data = generate_pdf_report()
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_data,
        file_name="Factory_Quality_Report.pdf",
        mime="application/pdf"
    )

with down_col2:
    # Button for CSV (Analysis Results)
    df_analysis = df.copy()
    df_analysis['Mean'] = x_bar
    df_analysis['AI_Flag'] = ["Anomaly" if p == -1 else "Normal" for p in ai_preds]
    csv = df_analysis.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📊 Download CSV Data",
        data=csv,
        file_name="Processed_Factory_Data.csv",
        mime="text/csv"
    )