# 🎾 Mini-Project-1  
**Project Title**: *Game Analytics: Unlocking Tennis Data with SportRadar API*

---

## 📂 Domain
- Sports / Data Analytics

## 🧰 Tech Stack
- **Language**: Python  
- **Database**: MySQL  
- **Application**: Streamlit  
- **API Integration**: Sportradar API

---

## 🚀 Project Description

This project aims to develop a solution for **visualizing, managing, and analyzing tennis data** extracted from the Sportradar API.  
Data is retrieved in JSON format and processed using Python to transform **nested JSON** into a **flat relational schema** suitable for storage and querying.

The final product is a user-friendly **Streamlit dashboard** that allows interactive exploration of the data.

---

## 🧠 Approach

### 1. 🔍 Data Extraction
- Fetch tennis match and player data from Sportradar's API.
- Flatten nested JSON into tabular form for analysis.

### 2. 🗃️ Data Storage
- Store structured data into a MySQL database using a custom-designed schema.

### 3. 📊 Data Visualization
- Build an interactive dashboard using **Streamlit** to explore:
  - Gender-based participation
  - Categories & Competitions
  - Summary statistics
  - Competitors by Rank
  - Search & Filter Competitors
  - Country-wise Analysis

---

## 📎 Future Enhancements
- Expand to other sports using different endpoints of the API

---

## 📂 Project Structure

- `db_config.py` — Handles the database connection setup (MySQL).
- `sql_queries.py` — Contains all reusable SQL queries.
- `stream_app.py` — Streamlit application to visualize and analyze the data.

---

## 📁 Data Files

- CSV files used for testing and sample analysis are located in the `data` folder.

---
## 📁 Executed the given queries (Notebooks)

- `competition_data.ipynb` 
- `complexes_data.ipynb`
- `doubles_competitor_rankings_data.ipynb`

These notebooks are responsible for:
- Pulling API data
- Cleaning and flattening nested JSON
- Inserting structured data into MySQL for visualization and analysis
  
---

## 🚀 How to Run
1. Clone the repo
2. Activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run app: `streamlit run stream_app.py`
   
---





