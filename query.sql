-- кількість коміксів, яку написав кожен автор

SELECT
  w.writer_name,
  COUNT(DISTINCT wr.comic_id) AS total_comics_written
FROM
  Writer w
  JOIN Written wr ON w.writer_id = wr.writer_id
GROUP BY
  w.writer_id;

-- -- кількість коміксів за різні роки

SELECT
  EXTRACT(YEAR FROM date) AS comic_year,
  COUNT(DISTINCT comic_id) AS total_comics
FROM
  Written
GROUP BY
  comic_year
ORDER BY
  comic_year;

-- кількість коміксів кожного формату

SELECT
  comic_format,
  COUNT(comic_id) AS total_comics
FROM
  Comic
GROUP BY
  comic_format;

  

