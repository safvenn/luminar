-- ASSIGNMENT 3-------------------------------------------------------
use practice1;
-- create Tables

CREATE TABLE distribution_companies (
    id INT PRIMARY KEY,
    company_name VARCHAR(100));

create table movies(id int primary key,movie_title varchar(40),imdb_rating float,year_released int,budget double,box_office double,distribution_company_id int,language varchar(30),
		FOREIGN KEY (distribution_company_id)
			REFERENCES distribution_companies(id));
            
INSERT INTO distribution_companies (id, company_name)
VALUES(1, 'Columbia Pictures'),(2, 'Paramount Pictures'),(3, 'Warner Bros. Pictures'),(4, 'United Artists'),
(5, 'Universal Pictures'),(6, 'New Line Cinema'),(7, 'Miramax Films'),
(8, 'Produzioni Europee Associate'),
(9, 'Buena Vista'),
(10, 'StudioCanal');

INSERT INTO movies
(id, movie_title, imdb_rating, year_released, budget, box_office, distribution_company_id, language)
VALUES
(1, 'The Shawshank Redemption', 9.2, 1994, 25.00, 73.30, 1, 'English'),
(2, 'The Godfather', 9.2, 1972, 7.20, 291.00, 2, 'English'),
(3, 'The Dark Knight', 9.0, 2008, 185.00, 1006.00, 3, 'English'),
(4, 'The Godfather Part II', 9.0, 1974, 13.00, 93.00, 2, 'English, Sicilian'),
(5, '12 Angry Men', 9.0, 1957, 0.34, 2.00, 4, 'English'),
(6, 'Schindler''s List', 8.9, 1993, 22.00, 322.20, 5, 'English, German, Yiddish');

select * from movies;


-- 1. Select all data from the table distribution_companies. 

select * from distribution_companies;

-- 2. For each movie, select the movie title, the IMDb rating, and the year the movie was released.

select movie_title,imdb_rating,year_released from movies;


--  3. Select the columns movie_title and box_office from the table movies. 
--  Show only movies with earnings above $300 million.

select movie_title,box_office from movies where box_office >300;
 
--  4. Select the columns movie_title, imdb_rating, and year_released from the table movies. Show movies that have the word ‘Godfather’ in the title. 

select movie_title, imdb_rating,year_released from movies where movie_title like '%Godfather%';

--  5. Select the columns movie_title, imdb_rating, and year_released from the table movies. Show movies that were released before 2001 and had a rating above 9. 

select movie_title, imdb_rating,year_released from movies where year_released <2001 and imdb_rating >9;

--  6. Select the columns movie_title, imdb_rating, and year_released from the table movies. Show movies released after 1991. Sort the output by the year released in ascending order. 

select movie_title, imdb_rating,year_released from movies where year_released >1991 order by year_released;

--  7. Show the count of movies per each language category. 

select language ,count(*) as count from movies group by language; 


--  8. Show the count of movies by year released and language. Sort results by the release date in ascending order. 

select year_released ,language,count(*) from movies group by year_released,language order by year_released; 

--  9. Show the languages spoken and the average movie budget by language category. Show only the languages with an average budget above $50 million

 select language ,avg(budget) as avg from movies group by language having 50<avg;
 
--  10.  Show movie titles from the table movies, each with the name of its distribution company.

select m.movie_title,d.company_name from movies m join distribution_companies d on(m.distribution_company_id = d.id);
