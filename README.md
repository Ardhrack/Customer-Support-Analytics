# 🎫 Customer Support Analytics Dashboard

An **interactive Streamlit dashboard** for analysing customer support ticket data, tracking KPIs, and uncovering insights related to customer satisfaction, resolution time, ticket volume, and support channels.

This project demonstrates **end-to-end analytics skills**: data cleaning, KPI computation, interactive visualisation, and dashboard deployment using Python.

---

## 🚀 Features

- 📊 **Key Performance Indicators (KPIs)**
  - Total tickets
  - Average customer satisfaction
  - Average resolution time (hours)
  - Open vs closed tickets

- 🔍 **Dynamic Filters**
  - Date range
  - Ticket priority
  - Ticket status
  - Support channel
  - Product purchased

- 📈 **Analytical Visualisations**
  - Satisfaction by ticket type, priority, and channel
  - Resolution time vs customer satisfaction
  - Average resolution time by priority
  - Ticket volume by channel and status

- 📂 **Data Explorer**
  - View filtered ticket-level data
  - Download filtered results as CSV

- ⚡ **Optimised Performance**
  - Streamlit caching for faster data loading
  - Clean, responsive UI design

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** – interactive web dashboard
- **Pandas** – data manipulation & analysis
- **Plotly** – interactive charts and visualisations

---

## 📁 Project Structure

```text
customer-support-analytics/
│
├── app.py                  # Main Streamlit application
├── utils.py                # Data loading, cleaning & analytics functions
├── data/
│   └── customer_support_tickets.csv
├── README.md
├── .gitignore
