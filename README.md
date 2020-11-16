# quandl-ingest
*A small pipeline for ingesting FRED interest rate data from Quandl into InfluxDB*  

**Requirements:**
- Python 3.7.9
- [Docker](https://docs.docker.com/get-docker/)
- [InfluxDB](https://docs.influxdata.com/influxdb/v1.8/introduction/install/) (only required if you want to interact with the database directly)
- [Pyenv](https://github.com/pyenv/pyenv-installer) (recommended)

**Setup your environment:**
```bash
pyenv install 3.7.9 && pyenv virtualenv 3.7.9 quandl && pyenv activate quandl
pip install -r requirements.txt
```

**Export your API key:**
```bash
export QUANDL_API_KEY=<your API key>
```

**To start development influxdb and ingest FRED interest rate data from Quandl:**  
```bash
./devDatabase.sh start
python fred_ingest.py create-database
python fred_ingest.py download-and-insert interest_rates_raw
```

**To query the database:**
```
influx -database FRED
> SELECT * FROM interest_rates_raw ORDER BY DESC
```

**To tear down:**  
```bash
./devDatabase.sh stop
./devDatabase.sh cleanup
```
