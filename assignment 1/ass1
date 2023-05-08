-- COMP3311 22T3 assignment 1
--
-- Fill in the gaps ("...") below with your code
-- You can add any auxiliary views/function that you like
-- The code in this file *MUST* load into an empty database in one pass
-- It will be tested as follows:
-- createdb test; psql test -f ass1.dump; psql test -f ass1.sql
-- Make sure it can load without error under these conditions


-- Q1: new breweries in Sydney in 2020

create or replace view Q1(brewery,suburb)
as
select B.name as brewery, L.town as suburb
from Breweries B
join Locations L on B.located_in = L.id
where L.metro = 'Sydney' and B.founded = 2020
;

-- Q2: beers whose name is same as their style

create or replace view Q2(beer,brewery)
as
select B.name as beer, breweries.name as brewery 
from Breweries join brewed_by on breweries.id = brewed_by.brewery
join Beers B on B.id = brewed_by.beer 
join Styles on styles.id = B.style
where B.name = styles.name
;

-- Q3: original Californian craft brewery
// METHOD 1
create view calibe as
select b.name, b.founded
from breweries b
join locations l on b.located_in = l.id
where l.region = 'California'
;

select name, founded as year
from calibe
where founded = (select min(founded) from calibe)
;

// METHOD 2
create or replace view Q3(brewery,founded)
as
select breweries.name as brewery, breweries.founded as founded
from Breweries 
join Locations on breweries.located_in = locations.id
where locations.region='California' 
and breweries.founded = (select min(founded) 
												 from (select * from breweries 
												 join locations on breweries.located_in = locations.id 
												 where locations.region='California') as X)
;

-- Q4: all IPA variations, and how many times each occurs

create or replace view Q4(style,count)
as
select s.name as style, count(b.name) 
from Beers b 
join Styles s on b.style = s.id 
where s.name like '%IPA%' group by s.name order by s.name
;

-- Q5: all Californian breweries, showing precise location

create or replace view Q5(brewery,location)
as
select b.name as brewery, 
       case when l.town is null then l.metro 
            else l.town end as location
from Breweries b
join Locations l ON b.located_in = l.id
where l.region = 'California' order by b.name
;

-- Q6: strongest barrel-aged beer

create or replace view Q6(beer,brewery,abv)
as
select beers."name" as beer,breweries."name" as brewery, beers.abv 
from Beers
join brewed_by on
beers.id = brewed_by.beer 
join Breweries on
brewed_by.brewery = breweries.id
where beers.abv = (select MAX(beers.abv) from beers where lower(beers.notes) LIKE '%barrel%' and lower(beers.notes) LIKE '%aged%' )
;

-- Q7: most popular hop

create or replace view Q7(hop)
as
select a."name" as hop 
from Ingredients a
join (select query1.* 
	from (select ingredient, Count(*) as order_count 
	from contains group by contains.ingredient) query1,
   	 (select max(query2.order_count) as highest_count  
			from (select ingredient, Count(*) as order_count 
			from contains group by contains.ingredient) query2) query3
			where query1.order_count = query3.highest_count) b on
			b.ingredient = a.id
;

-- Q8: breweries that don't make IPA or Lager or Stout (any variation thereof)
// METHOD 1
create or replace view Q8(brewery)
as
select "name" as brewery 
from Breweries
except
select breweries."name" 
from styles
join Beers ON beers.style = styles.id
join brewed_by on beers.id = brewed_by.beer 
join Breweries on brewed_by.brewery = breweries.id
where styles."name" LIKE '%IPA%' 
or styles."name" LIKE '%Lager%' 
or styles."name" LIKE '%Stout%'
group by breweries."name"
order by brewery
;

// METHOD 2
select
    Breweries.name
from
    Breweries
where
    not exists (
        select
            *
        from
            brewed_by
            join beers on brewed_by.beer = beers.id
            join Styles on Beers.style = Styles.id
        where
            brewed_by.brewery = Breweries.id
            and (
                Styles.name like ('%IPA%')
                or Styles.name like ('%Lager%')
                or Styles.name like ('%Stout%')
            )
    );
    
    
-- Q9: most commonly used grain in Hazy IPas

create or replace view Q9(grain)
as
select query1."name" as grain 
from (select ingredients."name",count(*) as order_count 
from styles
join Beers on Beers.style = styles.id
and styles."name" like 'Hazy IPA'
join contains on
Beers.id = contains.beer
join ingredients on 
contains.ingredient = ingredients.id
and ingredients.itype = 'grain'
group by ingredients."name") query1,
(select max(query2.order_count) as highest_count 
from (select ingredients."name",count(*) as order_count 
from styles
join Beers on Beers.style = styles.id
and styles."name" LIKE 'Hazy IPA'
join contains on
Beers.id = contains.beer
join ingredients on contains.ingredient = ingredients.id
and ingredients.itype = 'grain'
group by ingredients."name") query2 ) query3
where query1.order_count = query3.highest_count
;

-- Q10: ingredients not used in any beer

create or replace view Q10(unused)
as
select "name" as unused from ingredients
except
select ingredients."name"
from Beers
join contains on Beers.id = contains.beer
join ingredients on contains.ingredient = ingredients.id
group by ingredients."name"
;

-- Q11: min/max abv for a given country

drop type if exists ABVrange cascade;
create type ABVrange as (minABV float, maxABV float);
create or replace function q11(_country text)
returns abvrange as $$
	DECLARE
	    abv abvrange;
	begin
		select 
		case when MIN(beers.abv) is null then 0 else MIN(beers.abv)::numeric(4,1) END,
		case when MAX(beers.abv) IS null then 0 else MAX(beers.abv)::numeric(4,1) END
		into abv.minabv,abv.maxabv FROM
		beers
		join brewed_by on
		brewed_by.beer = beers.id
		join breweries on 
		breweries.id = brewed_by.brewery
		join locations on
		locations.id = breweries.located_in
		and locations.country LIKE _country;
		return abv;
end;

$$ LANGUAGE plpgsql;



-- Q12: details of beers

drop type if exists BeerData cascade;
create type BeerData as (beer text, brewer text, info text);

create or replace function
    allBreweriesFunc(s1 text, s2 text) returns text
as $$
begin
    if s1 = '' then
        return s2;
    end if;
    return s1 || ' + ' || s2; 
end;
$$ language plpgsql;

create or replace aggregate allBreweries(text) (
    stype    = text,    -- the accumulator type
    initcond = '',      -- initial accumulator value
    sfunc    = allBreweriesFunc -- increment function
);


create or replace function
    Q12(partial_name text) returns setof BeerData
as $$
declare
    i RECORD;
    r BeerData;
begin
    for i in
    select Beers.name as beerName, allBreweries(Breweries.name) as brewery
    from Beers 
    join Brewed_by on Beers.id = Brewed_by.beer
    join Breweries on Brewed_by.brewery = Breweries.id
    where lower(Beers.name) like '%' || lower(partial_name) || '%'
    group by Beers.name
    loop
        r.beer := i.beerName;
        r.brewer := i.brewery;
        r.info := '12312';
        return next r;
    end loop;
end
$$
language plpgsql;



