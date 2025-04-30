-- create the raw schema for source data only
create schema if not exists raw;

-- load location & weather data from CSV files, merging columns by name and storing as strings
create table if not exists raw.fhv_bases as 
select * from read_csv_auto(
    '../data/fhv_bases.csv',
    union_by_name=True,
    filename=True,
    all_varchar=1,
    header=True
);
create table if not exists raw.central_park_weather as 
select * from read_csv_auto(
    '../data/central_park_weather.csv',
    union_by_name=True,
    filename=True,
    all_varchar=1
);

-- load taxi data from parquet files, merging columns by name
create table if not exists raw.yellow_tripdata as 
select * from read_parquet(
    '../data/taxi/yellow_tripdata_*_sampled.parquet',
    union_by_name=True,
    filename=True
);

create table if not exists raw.green_tripdata as 
select * from read_parquet(
    '../data/taxi/green_tripdata_*_sampled.parquet',
    union_by_name=True,
    filename=True
);

create table if not exists raw.fhvhv_tripdata as 
select * from read_parquet(
    '../data/taxi/fhvhv_tripdata_*_sampled.parquet',
    union_by_name=True,
    filename=True
);

create table if not exists raw.fhv_tripdata as 
select * from read_parquet(
    '../data/taxi/fhv_tripdata_*_sampled.parquet',
    union_by_name=True,
    filename=True
);

-- load bike data from CSV files, merging columns by name and storing as strings
create table if not exists raw.bike_data as 
select * from read_csv_auto(
    '../data/bike/*-citibike-tripdata_sampled.csv',
    union_by_name=True,
    filename=True,
    all_varchar=1
);
