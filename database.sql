CREATE SCHEMA IF NOT EXISTS `eat_better` DEFAULT CHARACTER SET utf8mb4;

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
  `id` SMALLINT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `eat_better`.`Product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(150) NOT NULL,
  `description` TINYTEXT NULL,
  `url` VARCHAR(255) NOT NULL,
  `nutri_score` VARCHAR(1) NULL,
  `category` SMALLINT NOT NULL,
  `sub_category` SMALLINT NULL,
  `store_0` SMALLINT NOT NULL,
  `store_1` SMALLINT NULL,
  `brand` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE,
  INDEX `fk_category_idx` (`category` ASC) VISIBLE,
  INDEX `fk_sub_category_idx1` (`sub_category` ASC) VISIBLE,
  INDEX `fk_store_0_idx` (`store_0` ASC) VISIBLE,
  INDEX `fk_store_1_idx` (`store_1` ASC) VISIBLE,
  INDEX `fk_brand_idx` (`brand` ASC) VISIBLE,
  CONSTRAINT `fk_category`
    FOREIGN KEY (`category`)
    REFERENCES `eat_better`.`Category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_sub_category`
    FOREIGN KEY (`sub_category`)
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
  `id` SMALLINT NOT NULL AUTO_INCREMENT,
  `original` INT NOT NULL,
  `substitute` INT NOT NULL,
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
