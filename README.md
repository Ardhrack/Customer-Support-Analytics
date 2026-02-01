# 🎫 Customer Support Analytics Dashboard

An **interactive Streamlit dashboard** for analysing customer support ticket data, tracking KPIs, and uncovering insights on customer satisfaction, resolution time, ticket volume, and support channels.

Built to showcase **end-to-end analytics skills**: data cleaning, KPI computation, interactive visualisation, and dashboard deployment using Python.

---

## 🚀 Features

### 📊 KPI Overview
- Total tickets
- Average customer satisfaction (out of 5)
- Average resolution time (hours)
- Open tickets count

### 🔍 Interactive Filters (Sidebar)
- Date range (Date of Purchase)
- Ticket priority
- Ticket channel
- Ticket status
- Product purchased

### 📈 Analytics & Visualisations
- Satisfaction:
  - By Ticket Type
  - By Priority
  - By Channel
- Resolution Time:
  - Resolution time vs Satisfaction (scatter)
  - Avg resolution time by Priority (bar)
- Volume:
  - Ticket volume by Channel (donut/pie)
  - Ticket volume by Status (bar)

### 📂 Data Explorer
- View the filtered dataset inside the app
- Download filtered data as CSV

### ⚡ Performance + UI
- Streamlit caching for faster reloads
- Responsive layout + custom CSS for better viewing on different screen sizes

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (dashboard UI)
- **Pandas** (data cleaning & analysis)
- **Plotly** (interactive charts)

---

## 📁 Project Structure

```text
customer-support-analytics/
│
├── app.py                       # Main Streamlit dashboard app
├── utils.py                     # Utility functions (load/clean/filter/KPIs)
├── data/
│   └── customer_support_tickets.csv
├── README.md
├── .gitignore
```

---

## 🧠 Data Processing Notes

- Converts key fields to correct data types (dates, numeric ratings).
- **Resolution time fix:** `Time to Resolution` is treated as a timestamp in raw data, so the app computes actual duration in hours:

> Resolution Time (hours) = (Time to Resolution Timestamp) - (First Response Time)

- Invalid/negative resolution times are set to missing to avoid misleading averages.

---

## ▶️ How to Run Locally (Windows 10)

### 1) Clone the repo
```bash
git clone git@github.com:your-username/your-repo-name.git
cd your-repo-name
```

### 2) Create & activate a virtual environment (recommended)
```bash
python -m venv venv
venv\Scripts\activate
```

### 3) Install dependencies
If you don’t have a `requirements.txt` yet, install directly:
```bash
pip install streamlit pandas plotly
```

### 4) Run the Streamlit app
```bash
streamlit run app.py
```

Your browser should open automatically. If not, Streamlit will show a local URL in the terminal.

---

## ✅ Recommended: Add `requirements.txt`

Create a file called `requirements.txt` with:
```text
streamlit
pandas
plotly
```

Then users can install with:
```bash
pip install -r requirements.txt
```

---

## 📊 Example Use Cases

- Support performance monitoring (weekly/monthly)
- Identifying high-friction products or ticket types
- Prioritisation insights: which priority levels take longest to resolve
- Understanding how resolution time impacts satisfaction
- Channel workload insights (e.g., Twitter vs Forum vs Email)

---

## 📌 Skills Demonstrated

- Data cleaning & feature engineering
- KPI design and calculation
- Interactive dashboard building
- Analytics storytelling through charts
- Python project structuring + Git workflow

---

## 🔮 Future Enhancements (Optional)

- SLA breach analysis (e.g., >24h, >48h buckets)
- Trend analysis over time (daily/weekly volume & satisfaction)
- Deployment to Streamlit Community Cloud / Azure
- Add a “Top Issues” NLP section (ticket description clustering)
- Export charts/report snapshots

---

## 👤 Author

**Ardhra C K**  
Master’s in Business Analytics  
Focused on Data, Analytics & Insight roles
