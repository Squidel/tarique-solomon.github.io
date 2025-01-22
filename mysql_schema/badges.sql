USE promoti5_promotions;

DROP TABLE IF EXISTS `badges`;

CREATE TABLE `promoti5_promotions`.`badges` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `badge_name` VARCHAR(80) NOT NULL,
    `badge_description` VARCHAR(255) NULL,
    `winner_id` CHAR(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
    PRIMARY KEY (`id`),
    INDEX `promotion_winner_id_idx` (`winner_id` ASC) VISIBLE,
    CONSTRAINT `winner_badge_fk` FOREIGN KEY (`winner_id`) REFERENCES `promoti5_promotions`.`promotion_winners` (`promotion_winner_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE = InnoDB DEFAULT CHARSET = latin1 COLLATE = latin1_swedish_ci;