import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import base64

def get_base64_of_bin_file(bin_file_path):
    with open(bin_file_path, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Change path to your image location relative to dashboard.py
bg_image = get_base64_of_bin_file("Pictortelescope.jpg")  # or "assets/Pictortelescope.jpg" if in assets folder

background_style = f"""
<style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
</style>
"""

st.markdown(background_style, unsafe_allow_html=True)
page_bg_css = f"""
<style>
.stApp {{
  background-image: url("data:image/jpg;base64,{bg_image}");
  background-size: cover;
  background-repeat: no-repeat;
  background-attachment: fixed;
  font-family: 'Poppins', sans-serif;
  color: #1f4e79;
}}

html, body, [class*="css"] {{
  font-family: 'Poppins', sans-serif;
  color: #1f4e79;
}}

}}
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

# Session state to persist uploads
if "file_data" not in st.session_state:
    st.session_state.file_data = []
    

# Upload section
st.sidebar.header("📂 Upload CSV")
uploaded_files = st.sidebar.file_uploader("Select CSV files", type="csv", accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        # Check if file already exists to avoid duplication
        if file.name not in [f["Filename"] for f in st.session_state.file_data]:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df = pd.read_csv(file, header=None)
            df.columns = ["Time (s)", "Sensor Output"]

            st.session_state.file_data.append({
                "Filename": file.name,
                "Uploaded At": timestamp,
                "DataFrame": df
            })
        else:
            st.sidebar.warning(f"'{file.name}' already uploaded.")

# Display file manager
if st.session_state.file_data:
    st.subheader("Uploaded Files")
    filenames = [f["Filename"] for f in st.session_state.file_data]
    selected_files = st.multiselect("✅ Select files to view", filenames, default=filenames)

    st.markdown("Remove a file")
    file_to_remove = st.selectbox("Select a file to delete", ["None"] + filenames)
    if file_to_remove != "None":
        if st.button("Delete Selected File"):
            st.session_state.file_data = [f for f in st.session_state.file_data if f["Filename"] != file_to_remove]
            st.success(f"Deleted '{file_to_remove}'")

    # Show file table
    record_df = pd.DataFrame([{"Filename": f["Filename"], "Uploaded At": f["Uploaded At"]} for f in st.session_state.file_data])
    st.dataframe(record_df, use_container_width=True)

    # Plot graphs with min/max values
    for f in st.session_state.file_data:
        if f["Filename"] in selected_files:
            df = f["DataFrame"]
            min_val = df["Sensor Output"].min()
            max_val = df["Sensor Output"].max()

            st.markdown(f"---\n### 📄 {f['Filename']} (Uploaded at {f['Uploaded At']})")
            st.write(f"**🔻 Min Intensity:** {min_val} &nbsp;&nbsp;&nbsp;&nbsp; **🔺 Max Intensity:** {max_val}")

            fig = px.line(df, x="Time (s)", y="Sensor Output",
                          title=f"{f['Filename']} Output vs Time", markers=True)
            st.plotly_chart(fig, use_container_width=True)

            csv = df.to_csv(index=False).encode()
            st.download_button(f"📥 Download {f['Filename']}", csv, f"processed_{f['Filename']}", "text/csv")

else:
    st.info("No files uploaded yet. Use the sidebar to upload CSV files.")


