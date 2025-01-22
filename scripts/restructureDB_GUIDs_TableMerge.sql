CREATE TABLE `Promotions_Form_Submissions` (
  `id` char(36) NOT NULL,
  `promotion_id` int NOT NULL,
  `title` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email_addr` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_num` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  	PRIMARY KEY (id),
    FOREIGN KEY (promotion_id) REFERENCES Promotion_Names (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `Promotions_Submission_References` (
  `id` char(36) NULL,
  `form_submission_id` char(36) NOT NULL,
  `reference_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_created` datetime NOT NULL,
    FOREIGN KEY (form_submission_id) REFERENCES Promotions_Form_Submissions (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add GUID column to table pairs

ALTER TABLE PureScholars_Forms
ADD COLUMN guid CHAR(36);

ALTER TABLE PureScholars_Submissions
ADD COLUMN guid CHAR(36);

ALTER TABLE PureMoneyChristmas_Forms
ADD COLUMN guid CHAR(36);

ALTER TABLE PureMoneyChristmas_Submissions
ADD COLUMN guid CHAR(36);

-- Run Python Script restructureFunctions.py, uncomment updateExistingTables_withGUID

-- Run these INSERT INTO SELECTS for each table pair

INSERT INTO Promotions_Form_Submissions (id, promotion_id, title, first_name, last_name, email_addr, phone_num, image)
SELECT guid, 2, title, first_name, last_name, email_addr, phone_num, image
FROM PureMoneyChristmas_Forms
ORDER BY id;

INSERT INTO Promotions_Submission_References (form_submission_id, reference_number, date_created)
SELECT guid, reference_number, date_created
FROM PureMoneyChristmas_Submissions
ORDER BY id;

-- Run Python Script restructureFunctions.py, uncomment addGUIDto_ExistingTable 

ALTER TABLE  `Promotions_Submission_References`
MODIFY COLUMN id CHAR(36) PRIMARY KEY NOT NULL;
