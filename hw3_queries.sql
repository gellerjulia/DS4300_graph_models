-- Query A: sum of all book prices
-- Output: 253.45
SELECT sum(p.num_value)
FROM
  (SELECT np.num_value
   FROM node_props AS np
   RIGHT JOIN
     (SELECT node_id
      FROM node
      WHERE TYPE='Book') AS n ON np.node_id = n.node_id
    WHERE np.propkey='price') AS p

-- Query B: names of people Spencer knows
-- Output: Emily ; Brendan
SELECT np.string_value
FROM node_props AS np
INNER JOIN
  (SELECT e.out_node
   FROM edge AS e
   INNER JOIN
     (SELECT node_id
      FROM node_props
      WHERE string_value = 'Spencer') AS n ON e.in_node = n.node_id
    WHERE e.type = 'knows') AS k ON np.node_id = k.out_node

-- Query C: title and price of books Spencer bought
-- Output: Cosmos, 17 ; Database Design, 195
SELECT np.string_value,
       MAX(np.num_value)
FROM node_props AS np
INNER JOIN
  (SELECT e.out_node
   FROM edge AS e
   INNER JOIN
     (SELECT node_id
      FROM node_props
      WHERE string_value = 'Spencer') AS n ON e.in_node = n.node_id
    WHERE e.type = 'bought' ) AS b ON np.node_id=b.out_node
GROUP BY np.node_id

-- Query D: pair of names of people who know each other
-- Output: Emily, Spencer ; Spencer, Brendan
SELECT m.knows1,
       np2.string_value AS knows2
FROM node_props AS np2
RIGHT JOIN
  (SELECT np.string_value AS knows1,
          k.knows2
   FROM node_props AS np
   RIGHT JOIN
     (SELECT DISTINCT CASE
                          WHEN e.in_node < e.out_node THEN e.in_node
                          ELSE e.out_node
                      END AS knows1,
                      CASE
                          WHEN e.in_node < e.out_node THEN e.out_node
                          ELSE e.in_node
                      END AS knows2
      FROM edge AS e
      WHERE e.type = 'knows') AS k ON np.node_id = k.knows1) AS m ON np2.node_id = m.knows2

-- Query E: simple recommendation algorithm
-- Output: Database Design ; DNA & You
WITH sk AS
  (SELECT e.out_node
   FROM edge AS e
   INNER JOIN
     (SELECT node_id
      FROM node_props
      WHERE string_value = 'Spencer') AS n ON e.in_node = n.node_id
   WHERE e.type = 'knows')
SELECT np.string_value
FROM node_props AS np
RIGHT JOIN
  (SELECT DISTINCT e.out_node
   FROM edge AS e
   WHERE e.in_node in
       (SELECT *
        FROM sk)) AS b ON np.node_id = b.out_node
WHERE np.propkey='title'