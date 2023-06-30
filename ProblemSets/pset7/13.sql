SELECT DISTINCT people.name FROM people
JOIN stars AS s1 ON people.id = s1.person_id
JOIN movies AS m1 ON s1.movie_id = m1.id
JOIN stars AS s2 ON m1.id = s2.movie_id
JOIN people AS p2 ON s2.person_id = p2.id
WHERE p2.name = 'Kevin Bacon' AND p2.birth = 1958 AND people.name <> 'Kevin Bacon';
