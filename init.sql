CREATE EXTENSION postgis;

CREATE TABLE public.trips (
	id serial4 NOT NULL,
	region varchar NULL,
	origin_coord public.geometry(point) NULL,
	destination_coord public.geometry(point) NULL,
	datetime timestamp NULL,
	datasource varchar NULL,
	trip_group varchar NULL,
	CONSTRAINT trips_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_trips_destination_coord ON public.trips USING gist (destination_coord);
CREATE INDEX idx_trips_origin_coord ON public.trips USING gist (origin_coord);
create or replace FUNCTION public.udf_get_trips_grouped(minimum_count   int)
  returns TABLE (id int, region varchar, origin_coord varchar, destination_coord varchar, datetime varchar, datasource varchar, trip_group varchar)
LANGUAGE plpgsql AS
$func$
begin
	return QUERY
	with t_trip_groups as (
		select z.trip_group, count(*) as tot from trips z group by z.trip_group having count(*) >= minimum_count
	)
    select 
    	a.id, 
    	a.region, 
    	ST_AsText(a.origin_coord)::varchar as origin_coord, 
    	ST_AsText(a.destination_coord)::varchar as destination_coord, 
    	to_char(a.datetime, 'YYYY-MM-DD HH:MI:SS')::varchar(30) as datetime, 
    	a.datasource, 
    	a.trip_group 
    from trips a 
    inner join t_trip_groups b on a.trip_group  = b.trip_group 
    order by trip_group;   
END
$func$;

create or replace FUNCTION public.udf_get_weekly_average_trips_by_region(pregion varchar)
  returns TABLE (week_year varchar, num_trips int)
LANGUAGE plpgsql AS
$func$
begin
	return QUERY
	SELECT 
		Concat('Week ', extract('week' from datetime), ' - Year ', extract('isoyear' from datetime))::varchar AS week_year, 
		count(*)::int AS num_trips 
	FROM trips 
	WHERE region =  pregion
	GROUP BY region, week_year 
	ORDER BY week_year;
end;
$func$;

create or replace FUNCTION public.udf_get_weekly_average_trips_by_bbox(minlon float, minlat float, maxlon float, maxlat float)
  returns TABLE (week_year varchar, num_trips int)
LANGUAGE plpgsql AS
$func$
begin
	return QUERY
	select 
        Concat('Week ', extract('week' from datetime), ' - Year ', extract('isoyear' from datetime))::varchar as week_year
        , count(*)::int AS num_trips 
    from trips 
    where ST_MakeLine(origin_coord, destination_coord) &&
        ST_MakeEnvelope(minlon, minlat, maxlon, maxlat)
    GROUP BY week_year 
   ORDER BY week_year;
end;
$func$
;
create or replace procedure public.udp_update_trip_group(degree float)
LANGUAGE plpgsql
as $$ 
begin
	update trips 
	set trip_group = concat(
		ST_AsText(ST_SnapToGrid(ST_SetSRID(origin_coord, 4326), degree))
		,'_'
		,ST_AsText(ST_SnapToGrid(ST_SetSRID(destination_coord, 4326), degree))
		,'_'
		,extract(hour from datetime));   
end; 
$$;
