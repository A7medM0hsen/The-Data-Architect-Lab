# 📊 Power BI Dashboards & Reporting Layer

The interactive reporting layer of this project connects directly to the curated data warehouse models to deliver actionable insights for aviation executives and operational managers[cite: 2]. The dashboard consists of two specialized pages designed to track key performance indicators (KPIs), analyze flight operational health, and diagnose the root causes of disruptions[cite: 2].

---

## 📈 Core KPIs Tracked
The reporting layer evaluates operational efficiency through the following high-level metrics[cite: 2]:
* **Total Flights:** 16 Million domestic flights analyzed[cite: 2].
* **On-Time Arrival Rate:** 78.9% of flights arrived within scheduled limits[cite: 2].
* **On-Time Departure Rate:** 79.0% of flights departed on schedule.
* **Average Departure Delay:** 13.1 minutes[cite: 2].
* **Average Arrival Delay:** 7.58 minutes[cite: 2].
* **Average Flight Distance:** 840 Miles[cite: 2].
* **Cancellation Rate:** 1.56% of total scheduled flights[cite: 2].

---

## 📋 Dashboard Pages Breakdown

### 🗺️ Page 1: Flight Operations & Cancellations Overview
*Focuses on macro-level operational metrics, monthly trends, holiday seasonality, and detailed cancellation root-cause analysis[cite: 2].*

#### 📊 Visualizations Included:
1. **Total Flights by AIRLINE_NAME (Bar Chart):** Ranks airlines by volume, highlighting **Southwest Airlines** as the market share leader (exceeding 3M flights), followed by **Delta Air Lines** and **American Airlines**.
2. **Cancellation Reasons Breakdown (Donut Chart):** Segregates the drivers behind flight cancellations:
    * **Weather:** The dominant factor, causing **62.68%** of total cancellations.
    * **Carrier:** Operational or maintenance issues contribute to **23.78%**.
    * **National Air System (NAS):** Infrastructure or traffic constraints cause **13.49%**.
    * **Security:** Minimal impact at **0.05%**.
3. **Total Flights by MONTH (Line Chart):** Illustrates operational seasonality throughout the year, identifying a peak volume in month 3 (March) reaching **1.80M flights** and a sharp drop-off in month 4 (April) down to **1.21M flights**.
4. **Cancellation Rate in Holiday (Column Chart):** Tracks the direct correlation between holiday periods and operational failures, pinning **Martin Luther King Day (MLK)** as the period with the highest severe spike in flight cancellations.

---

### 🔍 Page 2: Delays Deep-Dive & Airline Performance
*Focuses on granular delay analysis, geographic bottleneck identification, and evaluating the operational efficiency of individual carriers[cite: 2].*

#### 📊 Visualizations Included:
1. **Geographic Operational Ledger (Table):** Provides state-level performance breakdown including `Total Flights`, `Avg Arrival Delay Minutes`, and `On-Time Departure Rate %`, showing high flight concentration in states like **Texas** (1.68M flights) and **California** (1.66M flights).
2. **Impact of Airline Rating on Delays (Scatter Plot):** Correlates user/industry ratings against average arrival delays to analyze if higher-rated carriers deliver better on-time reliability.
3. **Avg Arrival Delay Minutes by AIRPORT_TYPE (Pie Chart):** Identifies capacity constraints based on infrastructure size:
    * **Large Airports:** Responsible for the largest share of delays at **48.02%**.
    * **Medium Airports:** Account for **28.19%** of delay minutes.
    * **Small Airports:** Account for **23.79%** of delay minutes.
4. **Highest Flight Delays by State (Funnel Chart):** Isolates states with the worst flight lag, highlighting **West Virginia** with the highest average arrival delay (**22.94 minutes**), followed by **Wyoming** (**12.63 minutes**).
5. **Flight Delay Breakdown by Airline (Stacked Bar Chart):** Provides a detailed breakdown of delay types (Air System, Weather, Late Aircraft, Carrier, Security) for each airline, allowing executives to contrast carrier-controlled delays versus environmental factors[cite: 2].

---

## 💡 Key Analytical Insights Extracted
* **Infrastructure Strain:** Nearly half of all arrival delays (**48.02%**) are concentrated in **Large Airports**, signaling a critical need for slot optimization and ground operational changes at major hubs.
* **Environmental Vulnerability:** Weather is not only the leading cause of cancellation (**62.68%**) but also correlates strongly with massive operational dips during winter holiday periods (e.g., MLK Day).
* **Regional Bottlenecks:** While high-volume states like California maintain low average delays (4.34 minutes), low-volume regional points like West Virginia suffer from outsized average delays (22.94 minutes), pointing to potential local routing inefficiencies.
