CREATE TABLE `Promotion_Names` (
  `id` int NOT NULL AUTO_INCREMENT,
  `abbreviation` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `promotion_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `startDate` date DEFAULT NULL,
  `endDate` date DEFAULT NULL,
  `mainPicture` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `uploadFolder` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


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
  `id` char(36) NOT NULL,
  `form_submission_id` char(36) NOT NULL,
  `reference_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_created` datetime NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (form_submission_id) REFERENCES Promotions_Form_Submissions (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE Promotion_Winners(
    promotion_winner_id char(36) NOT NULL,
    promotion_id int NOT NULL,
    reference_number varchar(20) NOT NULL,
    date_selected datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (promotion_winner_id),    
    FOREIGN KEY (promotion_id) REFERENCES Promotion_Names (id),
    FOREIGN KEY (reference_number) REFERENCES Promotions_Submission_References (reference_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `Invalid_Promotions_Form_Submissions` (
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

CREATE TABLE `Invalid_Promotions_Submission_References` (
  `id` char(36) NOT NULL,
  `form_submission_id` char(36) NOT NULL,
  `reference_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_created` datetime NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (form_submission_id) REFERENCES Invalid_Promotions_Form_Submissions (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- Query to get Winner Information
SELECT pfs.title, pfs.first_name, pfs.last_name, pfs.email_addr, pfs.phone_num, pw.reference_number, pw.date_selected FROM Promotions_Form_Submissions pfs
INNER JOIN Promotions_Submission_References psr ON pfs.id = psr.form_submission_id
INNER JOIN Promotion_Winners pw ON psr.reference_number = pw.reference_number
ORDER BY pw.date_selected ASC
