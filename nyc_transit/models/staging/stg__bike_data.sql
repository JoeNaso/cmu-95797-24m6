with source as (

    select * from {{ source('raw', 'bike_data') }}

),

renamed as (

    select
        tripduration,
        starttime,
        stoptime,
        "start station id" as start_station_id,
        "start station name" as start_station_name,
        "start station latitude" as start_lat,
        "start station longitude" as start_lng,
        "end station id" as end_station_id,
        "end station name" as end_station_name,
        "end station latitude" as end_lat,
        "end station longitude" as end_lng,
        bikeid as bike_id,
        usertype as user_type,
        "birth year" as birth_year,
        "gender" as gender,
        filename

    from source

)

select
	starttime::timestamp as started_at_ts,
	stoptime::timestamp as ended_at_ts,
	coalesce(tripduration::int,datediff('second', started_at_ts, ended_at_ts)) as tripduration,
	start_station_id,  
	start_station_name,
	start_lat::double as start_lat,
	start_lng::double as start_lng, 
	end_station_id,  
	end_station_name,
	end_lat::double as end_lat,
	end_lng::double as end_lng,
    bike_id,
    user_type,
    birth_year,
    gender,
	filename
from renamed