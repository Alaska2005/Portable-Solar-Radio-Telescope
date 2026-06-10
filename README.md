#  Portable Solar Radio Telescope Dashboard

A **Streamlit-based dashboard** for visualizing, analyzing, and monitoring solar radio telescope sensor data. Upload your CSV observation files, detect solar events automatically, and explore signal intensity trends — all in one place.

Built for educational, research, and amateur radio astronomy applications.


##  Features

###  Data Management
- Upload multiple CSV files simultaneously
- Persistent file management using Streamlit Session State
- View uploaded file records with timestamps
- Delete previously uploaded files
- Download processed CSV files

### 📊 Data Visualization
- Interactive Plotly graphs
- Time vs Sensor Output visualization
- Automatic minimum and maximum intensity detection
- Multi-file comparison support

### Solar Activity Analysis

The dashboard automatically classifies each observation into one of the following categories:

| Status | Detection Condition |
|--------|-------------------|
| **Sun Entering Feed** | Signal intensity increases significantly (`Change > 0.05`) |
| **Sun Leaving Feed** | Signal intensity decreases significantly (`Change < -0.05`) |
| **Gain Saturated – Sun Out of Feed** | Three consecutive readings within ±0.01 of each other |
| **Unusual Solar Activity – Possible Solar Flare** | Sudden large change in intensity (`abs(Change) > 2.5`) |
| **Stable** | No significant variation detected |

---

## Project Structure

```
portable-solar-radio-telescope/
│
├── dashboard.py          # Streamlit UI, plotting, file management
├── solar_analysis.py     # Solar event detection and classification logic
├── requirements.txt      # Python dependencies
├── README.md
├── test_data.csv         # Sample dataset for testing
└── Pictortelescope.jpg   # Dashboard background image
```

---

## CSV File Format

The dashboard expects **headerless CSV files** with two columns:

| Column | Description |
|--------|-------------|
| Column 1 | Time (seconds) |
| Column 2 | Sensor Output |

**Example:**
```
0,0.12
1,0.15
2,0.18
3,0.19
4,0.21
```

> Columns are automatically assigned as `["Time (s)", "Sensor Output"]` on upload.

---

## Solar Analysis Logic

Signal change is calculated as:

```python
df["Change"] = df["Sensor Output"].diff()
```

Classification rules applied in order:

```python
# Gain Saturation
Three consecutive readings within ±0.01 of each other

# Solar Flare
abs(Change) > 2.5

# Sun Entering Feed
Change > 0.05

# Sun Leaving Feed
Change < -0.05

# Stable
No significant variation detected
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/portable-solar-radio-telescope.git
cd portable-solar-radio-telescope
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Dashboard

```bash
streamlit run dashboard.py
```

The app will open automatically in your browser.

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repository to GitHub
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click **New app** and configure:
   - **Repository:** `portable-solar-radio-telescope`
   - **Branch:** `main`
   - **Main file:** `dashboard.py`
4. Click **Deploy**

---

##  Dependencies

```
streamlit
pandas
numpy
plotly
```

---

##  Planned Features

- Solar transit prediction
- Automatic peak detection
- Noise filtering
- Real-time serial data acquisition
- Telescope pointing assistance
- Observation logging
- Data export in scientific formats (FITS, HDF5)
- Machine Learning based event classification
- Historical observation database

---

## 👩‍💻 Author

**Lavanya Saindane**  
Electronics & Telecommunication Engineering  
Portable Solar Radio Telescope Project — [IUCAA Pune](https://www.iucaa.in)
