
INSERT INTO artist_list(id, Name, Alias)
VALUES	(1, 'artist_1', 'alias_1'),
	    (2, 'artist_2', 'alias_2'),
	    (3, 'artist_3', 'alias_3'),
	    (4, 'artist_4', 'alias_4'),
	    (5, 'artist_5', 'alias_5'),
	    (6, 'artist_6', 'alias_6'),
	    (7, 'artist_7', 'alias_7'),
	    (8, 'artist_8', 'alias_8');

INSERT INTO Genre_list(id, Genre_Name)
VALUES	(1, 'genre_1'),
        (2, 'genre_2'),
        (3, 'genre_3'),
        (4, 'genre_4'),
        (5, 'genre_5');

INSERT INTO artist_in_genre(id, artist_id, genre_id)
VALUES	(1, 1, 1),
        (2, 2, 2),
        (3, 3, 3),
        (4, 4, 4),
        (5, 5, 5),
        (6, 6, 3),
        (7, 7, 4),
        (8, 8, 5);
       
INSERT INTO album_List(id, album_name, release_date)
VALUES	(1, 'album_name_1', 2016),
	    (2, 'album_name_2', 2015),
	    (3, 'album_name_3', 2017),
	    (4, 'album_name_4', 2018),
	    (5, 'album_name_5', 2018),
	    (6, 'album_name_6', 2018),
	    (7, 'album_name_7', 2020),
	    (8, 'album_name_8', 2020);

INSERT INTO artist_album (id, artist_id, album_id)
VALUES	(1, 1, 1),
        (2, 2, 2),
        (3, 3, 3),
        (4, 4, 4),
        (5, 5, 5),
        (6, 6, 3),
        (7, 7, 6),
        (8, 8, 8);

INSERT INTO Track_List(id, album_id, track_name, track_time)
VALUES	(1, 1, 'track_1', '00:03:00'),
	    (2, 1,'my_2', '00:03:10'),
	    (3, 2,'track_3', '00:03:20'),
	    (4, 2,'track_4', '00:03:30'),
	    (5, 3,'track_5', '00:03:40'),
	    (6, 3,'track_my', '00:03:50'),
	    (7, 4,'track_7', '00:04:00'),
	    (8, 4,'track_8', '00:04:10'),
	    (9, 5,'мой', '00:04:20'),
	    (10, 5,'track_10', '00:04:30'),
	    (11, 6,'track_11', '00:04:40'),
	    (12, 6,'track_12', '00:04:50'),
	    (13, 7,'track_13', '00:05:00'),
	    (14, 7,'track_14', '00:05:10'),
	    (15, 8,'track_15', '00:05:20');

INSERT INTO collection_List(id, collection_name, release_date)
VALUES	(1, 'collection_1', 2017),
	    (2, 'collection_2', 2016),
	    (3, 'collection_3', 2017),
	    (4, 'collection_4', 2018),
	    (5, 'collection_5', 2018),
	    (6, 'collection_6', 2019),
	    (7, 'collection_7', 2020),
	    (8, 'collection_8', 2021);

INSERT INTO collection_track(id, collection_id, track_id)
VALUES	(1, 1, 2),
	    (2, 2, 3),
	    (3, 3, 4),
	    (4, 4, 8),
	    (5, 5, 9),
	    (6, 6, 11),
	    (7, 7, 13),
	    (8, 8, 15);
