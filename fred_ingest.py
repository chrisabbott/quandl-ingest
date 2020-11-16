import click
import influxdb
import logging
import pandas as pd

from datetime import date
from dateutil.relativedelta import relativedelta
from dataset import FREDDataset

DEFAULT_DB_NAME = 'FRED'
DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8086
MAX_DB_RETRIES = 3

LOGGING_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

# https://www.quandl.com/data/FRED-Federal-Reserve-Economic-Data/documentation?anchor=interest-rates
FRED_CODES = [
        "FRED/DFF",
        "FRED/DTB3",
        "FRED/DGS5",
        "FRED/DGS10",
        "FRED/DGS30",
        "FRED/T5YIE",
        "FRED/T10YIE",
        "FRED/T5YIFR",
        "FRED/TEDRATE",
        "FRED/DPRIME"]


@click.group()
@click.option("--verbosity", default="INFO")
@click.pass_context
def cli(ctx, verbosity):
    ctx.obj = {}
    ctx.obj['client'] = influxdb.DataFrameClient(host=DEFAULT_HOST, port=DEFAULT_PORT, database=DEFAULT_DB_NAME)
    logging.basicConfig(
        level=LOGGING_LEVELS[verbosity.upper()],
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


@cli.command("create-database")
@click.pass_context
def create_database(ctx):
    ctx.obj['client'].create_database(DEFAULT_DB_NAME)
    logging.info(f"Successfully created database {DEFAULT_DB_NAME}.")


@cli.command("download-and-insert")
@click.argument("measurement", type=str, required=True)
@click.argument("headers", type=list, default=FRED_CODES)
@click.argument("start-date", type=str, default=f"{date.today()-relativedelta(years=10)}")
@click.argument("end-date", type=str, default=f"{date.today()}")
@click.pass_context
def download_and_insert(ctx, headers, start_date, end_date, measurement):
    dataset = FREDDataset(
        headers=headers,
        start_date=start_date,
        end_date=end_date)

    logging.info(f"Inserting points into {DEFAULT_DB_NAME}/{measurement} ...")

    for i in range(MAX_DB_RETRIES):
        try:
            ctx.obj['client'].write_points(dataset.dataframe, measurement)
            break
        except influxdb.exceptions.InfluxDBServerError:
            continue

    logging.info(f"Inserted {len(dataset.dataframe.index)-1} points to {DEFAULT_DB_NAME}/{measurement}.")


@cli.command("data-summary")
@click.argument("measurement", type=str, required=True)
@click.pass_context
def data_summary(ctx, measurement):
    # Obviously with larger databases we won't use SELECT *, but this is fine for now
    df = ctx.obj['client'].query(f"SELECT * FROM {measurement}")[measurement]
    logging.info(df)


if __name__ == '__main__':
    cli()
