SELECT
CONCAT('i',item_view.record_num, 'a', '          ', title)
--adds i prefix to the item record number and the "a" as a placeholder for the check digit, so the number can be easily copied and pasted into Sierra, also includes the title

FROM sierra_view.bib_view
JOIN sierra_view.bib_record_item_record_link
ON bib_view.id = bib_record_item_record_link.bib_record_id
JOIN sierra_view.item_view 
ON bib_record_item_record_link.item_record_id = item_view.id
JOIN sierra_view.record_metadata
ON record_metadata.id = item_view.id

WHERE
record_last_updated_gmt > TIMESTAMP 'yesterday' AND
bcode3 = 'n' AND
title not like '%linking%' AND
icode2 != 'n'
-- This limits results to any unsuppressed item records updated since midnight of the previous day, that are attached to a suppressed bib

ORDER BY title
--sorts results alphabetically by title