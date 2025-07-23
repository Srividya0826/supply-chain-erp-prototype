from datetime import datetime, timedelta
from modules.predictive_analytics import PredictiveAnalytics

pa = PredictiveAnalytics()

# Add past orders (simulate last 30 days)
today = datetime.now()
for i in range(1, 31):
    pa.add_order(today - timedelta(days=i), "I001", i)  # increasing quantity daily

# Add delivery records
pa.add_delivery("S001", "PO1001", today - timedelta(days=10), today - timedelta(days=5))
pa.add_delivery("S001", "PO1002", today - timedelta(days=20), today - timedelta(days=15))
pa.add_delivery("S002", "PO1003", today - timedelta(days=25), today - timedelta(days=23))

# Test forecasting demand for item I001 for next 30 days
forecast = pa.forecast_demand("I001")
print(f"Forecast demand for I001 next 30 days: {forecast:.2f}")

# Test predicting lead time for supplier S001
lead_time = pa.predict_lead_time("S001")
print(f"Predicted lead time for S001: {lead_time} days")

# Test lead time for supplier with no data
lead_time_none = pa.predict_lead_time("S999")
print(f"Predicted lead time for unknown supplier: {lead_time_none}")
