# 📈 Sales Analytics Dashboard

> Interactive retail e-commerce dashboard built with Streamlit + Plotly — 3 years of sales data

**Built by:** Ankit Jinkwan  
**Portfolio:** [ankitjhinkwan.github.io/portfolio](https://ankitjhinkwan.github.io/portfolio/)  
**LinkedIn:** [linkedin.com/in/ankit-jinkwan-a16882288](https://www.linkedin.com/in/ankit-jinkwan-a16882288/)

---

## 🎯 Project Overview

An end-to-end sales analytics dashboard analysing 3 years of retail e-commerce data. Built with Streamlit and Plotly for interactive visualisations with a professional dark theme.

### KPIs Tracked
| Metric | Value |
|--------|-------|
| **Total Revenue** | ₹19.5L+ |
| **Total Orders** | 5,000 |
| **Profit Margin** | ~27% |
| **Categories** | 6 |
| **Cities** | 15 |

---

## 📊 Dashboard Features

- **KPI Cards** — Revenue, Profit, Orders, Avg Order Value, Margin
- **Monthly Revenue Trend** — Bar + line combo with orders overlay
- **Category Breakdown** — Revenue, margin, and order share
- **Regional Performance** — Revenue and profit by region
- **Channel Analysis** — Website vs App vs Marketplace vs Direct
- **Top 10 Products** — By revenue with scatter analysis
- **Payment Methods** — Distribution pie chart
- **Return Rate** — By category
- **YoY Comparison** — Year-over-year category performance
- **Day of Week Pattern** — When do customers buy most?
- **Raw Data Explorer** — Search and filter all orders

---

## 📂 Project Structure

```
sales-analytics-dashboard/
│
├── 📓 notebooks/
│   └── sales_analysis.ipynb         ← Full EDA notebook
│
├── 📊 data/
│   ├── generate_data.py             ← Dataset generator
│   └── sales_data.csv               ← 5,000 orders dataset
│
├── 🌐 app/
│   └── app.py                       ← Streamlit dashboard
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/ankitjhinkwan/sales-analytics-dashboard
cd sales-analytics-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate dataset
```bash
cd data
python generate_data.py
cd ..
```

### 4. Launch the dashboard
```bash
streamlit run app/app.py
```

Open `http://localhost:8501` 🎉

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core language |
| **Pandas / NumPy** | Data manipulation |
| **Plotly** | Interactive charts |
| **Streamlit** | Web dashboard |
| **Matplotlib / Seaborn** | Notebook charts |

---

## 🔑 Key Findings

- **Electronics** drives the most revenue (~25% share)
- **Festival season** (Oct–Dec) accounts for ~35% of annual sales
- **UPI** is the most popular payment method (30%+)
- **Mobile App** channel growing fastest year-over-year
- **North & West** regions dominate overall revenue

---

*Made with ❤️ by Ankit Jinkwan*
