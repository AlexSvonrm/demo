--количество исполнителей в каждом жанре
SELECT genre_id, COUNT(artist_id) FROM artist_in_genre
GROUP BY genre_id;

--количество треков, вошедших в альбомы 2019-2020 годов
SELECT COUNT(id) FROM Track_List
WHERE album_id IN(
    SELECT id FROM album_List
	WHERE release_date BETWEEN '2019-01-01' AND '2020-12-31');

--средняя продолжительность треков по каждому альбому
SELECT album_id, AVG(track_time) FROM Track_List
GROUP BY album_id;

--все исполнители, которые не выпустили альбомы в 2020 году
SELECT DISTINCT a.name FROM artist_list AS a
LEFT JOIN artist_album AS aa ON a.id = aa.id
LEFT JOIN album_List AS am ON aa.id = am.id
WHERE release_date < '2020-01-01';

--названия сборников, в которых присутствует конкретный исполнитель (выберите сами)
SELECT DISTINCT c.name FROM collection_List AS c
LEFT JOIN artist_list AS a ON c.id = a.id
WHERE a.id = 4;

--название альбомов, в которых присутствуют исполнители более 1 жанра
SELECT DISTINCT a.name FROM album_List AS a
LEFT JOIN artist_album AS aa ON a.id = aa.id
LEFT JOIN artist_in_genre AS ag ON aa.id = ag.artist_id
GROUP BY a.name
HAVING COUNT(ag.artist_id) > 1;

--наименование треков, которые не входят в сборники
SELECT t.name FROM Track_List AS t
LEFT JOIN collection_album_track AS cat ON t.id = cat.track_id
WHERE cat.track_id IS NULL;

--исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько
SELECT a.name FROM artist_list AS a
JOIN artist_album AS aa ON a.id = aa.id
JOIN album_List AS am ON aa.album_id = am.id
JOIN Track_List AS t ON am.id = t.album_id
WHERE t.track_time = (SELECT MIN(track_time) FROM Track_List);

--название альбомов, содержащих наименьшее количество треков
SELECT DISTINCT album_name FROM album_List AS a
INNER JOIN Track_List AS t ON a.id = t.album_id
WHERE album_id IN(
	SELECT COUNT(album_id) FROM Track_List
	GROUP BY album_id
	ORDER BY album_id
	LIMIT 1);
