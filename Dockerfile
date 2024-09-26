FROM python:3.9-slim

RUN pip install --no-cache-dir dask distributed numpy pandas

CMD ["dask-scheduler"]