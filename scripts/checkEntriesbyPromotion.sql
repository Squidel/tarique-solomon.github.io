SELECT * FROM `Promotions_Submission_References` psr 
INNER JOIN `Promotions_Form_Submissions` pfs 
ON psr.form_submission_id = pfs.id 
WHERE pfs.promotion_id = 5 
ORDER BY reference_number DESC;