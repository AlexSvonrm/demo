SELECT genre_id, COUNT(artist_id) FROM artist_in_genre
GROUP BY genre_id;

SELECT COUNT(id) FROM Track_List
WHERE album_id IN(
    SELECT id FROM album_List
	WHERE release_date BETWEEN '2019-01-01' AND '2020-12-31');

SELECT album_id, AVG(track_time) FROM Track_List
GROUP BY album_id;

SELECT DISTINCT a.name FROM artist_list AS a
LEFT JOIN artist_album AS aa ON a.id = aa.id
LEFT JOIN album_List AS am ON aa.id = am.id
WHERE release_date < '2020-01-01';

SELECT DISTINCT c.name FROM collection_List AS c
LEFT JOIN artist_list AS a ON c.id = a.id
WHERE a.id = 4;

SELECT DISTINCT a.name FROM album_List AS a
LEFT JOIN artist_album AS aa ON a.id = aa.id
LEFT JOIN artist_in_genre AS ag ON aa.id = ag.artist_id
GROUP BY a.name
HAVING COUNT(ag.artist_id) > 1;

SELECT t.name FROM Track_List AS t
LEFT JOIN collection_album_track AS cat ON t.id = cat.track_id
WHERE cat.track_id IS NULL;

SELECT a.name FROM artist_list AS a
JOIN artist_album AS aa ON a.id = aa.id
JOIN album_List AS am ON aa.album_id = am.id
JOIN Track_List AS t ON am.id = t.album_id
WHERE t.track_time = (SELECT MIN(track_time) FROM Track_List);

SELECT DISTINCT album_name FROM album_List AS a
INNER JOIN Track_List AS t ON a.id = t.album_id
WHERE album_id IN(
	SELECT COUNT(album_id) FROM Track_List
	GROUP BY album_id
	ORDER BY album_id
	LIMIT 1);
