CREATE SCHEMA IF NOT EXISTS `eat_better` DEFAULT CHARACTER SET utf8 ;

USE `eat_better` ;

CREATE TABLE IF NOT EXISTS `eat_better`.`Category` (
  `id` SMALLINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `eat_better`.`Store` (
  `id` SMALLINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `eat_better`.`Brand` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `eat_better`.`Product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  `description` TINYTEXT NULL,
  `url` VARCHAR(255) NOT NULL,
  `nutri_score` VARCHAR(1) NULL,
  `category_0` SMALLINT NOT NULL,
  `category_1` SMALLINT NULL,
  `category_2` SMALLINT NULL,
  `store_0` SMALLINT NOT NULL,
  `store_1` SMALLINT NULL,
  `brand` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_category_1_idx` (`category_0` ASC) VISIBLE,
  INDEX `fk_category_1_idx1` (`category_1` ASC) VISIBLE,
  INDEX `fk_category_2_idx` (`category_2` ASC) VISIBLE,
  INDEX `fk_store_0_idx` (`store_0` ASC) VISIBLE,
  INDEX `fk_store_1_idx` (`store_1` ASC) VISIBLE,
  INDEX `fk_brand_idx` (`brand` ASC) VISIBLE,
  CONSTRAINT `fk_category_0`
    FOREIGN KEY (`category_0`)
    REFERENCES `eat_better`.`Category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_category_1`
    FOREIGN KEY (`category_1`)
    REFERENCES `eat_better`.`Category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_category_2`
    FOREIGN KEY (`category_2`)
    REFERENCES `eat_better`.`Category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_store_0`
    FOREIGN KEY (`store_0`)
    REFERENCES `eat_better`.`Store` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_store_1`
    FOREIGN KEY (`store_1`)
    REFERENCES `eat_better`.`Store` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_brand`
    FOREIGN KEY (`brand`)
    REFERENCES `eat_better`.`Brand` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `eat_better`.`Substitution` (
  `id` SMALLINT NOT NULL,
  `original` INT NULL,
  `substitute` INT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_substitution_idx` (`original` ASC) VISIBLE,
  INDEX `fk_substitute_idx` (`substitute` ASC) VISIBLE,
  CONSTRAINT `fk_original`
    FOREIGN KEY (`original`)
    REFERENCES `eat_better`.`Product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_substitute`
    FOREIGN KEY (`substitute`)
    REFERENCES `eat_better`.`Product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
