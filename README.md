# quandl-ingest

**Requirements:**
- Python 3.7.9
- Docker
- InfluxDB (only required if you want to interact with the database directly)

**To start development influxdb and ingest FRED interest rate data from Quandl:**  
```
pip install -r requirements.txt
./devDatabase start
python fred_ingest.py create-database
python fred_ingest.py download-and-insert --api-key <QUANDL-API-KEY> interest_rates_raw
```

**To tear down:**  
```
./devDatabase stop
./devDatabase cleanup
```
