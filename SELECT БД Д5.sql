--количество исполнителей в каждом жанре
SELECT Genre_list.Genre_Name, COUNT(artist_id) FROM artist_in_genre
JOIN Genre_list on Genre_list.id = artist_in_genre.genre_id
GROUP BY Genre_list.Genre_Name;

--количество треков, вошедших в альбомы 2019-2020 годов
SELECT COUNT(album_id) FROM Track_List 
JOIN album_List ON Track_List.album_id = album_List.id 
WHERE album_List.release_date BETWEEN 2019 and 2020; 

--средняя продолжительность треков по каждому альбому
SELECT album_List.album_name, AVG(Track_List.track_time) FROM Track_List
LEFT JOIN album_List ON Track_List.album_id = album_List.id
GROUP BY album_List.album_name;

--все исполнители, которые не выпустили альбомы в 2020 году
SELECT DISTINCT a.name FROM artist_list AS a
LEFT JOIN artist_album AS aa ON a.id = aa.id
LEFT JOIN album_List AS am ON aa.id = am.id
WHERE release_date <> 2020;

--названия сборников, в которых присутствует конкретный исполнитель (выберите сами)
SELECT DISTINCT collection_name FROM collection_List AS c
LEFT JOIN artist_list AS a ON c.id = a.id
WHERE a.Name = 'artist_3';

--название альбомов, в которых присутствуют исполнители более 1 жанра
SELECT DISTINCT album_name FROM album_List AS a
LEFT JOIN artist_album AS aa ON a.id = aa.id
LEFT JOIN artist_in_genre AS ag ON aa.id = ag.artist_id
--LEFT JOIN artist_list ON aa.id = Name
GROUP BY album_name
HAVING COUNT(ag.artist_id) > 1;

--наименование треков, которые не входят в сборники
SELECT track_name FROM Track_List AS t
LEFT JOIN collection_track AS cat ON t.id = cat.track_id
WHERE cat.track_id IS NULL;

--исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько
SELECT a.name FROM artist_list AS a
JOIN artist_album AS aa ON a.id = aa.id
JOIN album_List AS am ON aa.album_id = am.id
JOIN Track_List AS t ON am.id = t.album_id
WHERE t.track_time = (SELECT MIN(track_time) FROM Track_List);

--название альбомов, содержащих наименьшее количество треков
SELECT album_name FROM album_List AS a 
JOIN Track_List AS t ON a.id = t.album_id
GROUP BY a.album_name
HAVING COUNT(*) = 
    (SELECT COUNT(*) FROM album_List AS a
    JOIN Track_List AS t ON a.id = t.album_id
    GROUP BY a.album_name
    ORDER BY COUNT(*)
    LIMIT 1);


