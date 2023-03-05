SELECT album_name, release_date FROM album_List
WHERE release_date BETWEEN '2018-01-01' AND '2018-12-31';

SELECT track_name, track_time FROM Track_List
ORDER BY track_time DESC;

SELECT track_name FROM Track_List
WHERE track_time >= 03.50;

SELECT collection_name FROM collection_List
WHERE release_date BETWEEN '2018-01-01' AND '2020-12-31';

SELECT name FROM artist_list
WHERE name NOT LIKE '% %';

SELECT track_name FROM Track_List
WHERE track_name LIKE '%my%' OR '%мой%';
