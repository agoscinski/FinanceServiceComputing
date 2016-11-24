-- This is an example SQL File

SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;

CREATE TABLE IF NOT EXISTS `TestFSCDatabase`.`Stock` (
  `Ticker` VARCHAR(6) NOT NULL,
  `CompanyName` VARCHAR(45) NULL,
  `LotSize` INT NULL,
  `TickSize` DECIMAL(20,2) NULL,
  `TotalVolume` INT NULL,
  PRIMARY KEY (`Ticker`))
ENGINE = InnoDB;

-- Some comment in between
INSERT INTO Stock(Ticker, CompanyName, LotSize, TickSize, TotalVolume) VALUES('MS','Morgan Stanley','100','0.01','10000000');

-- TODO update and delete FROM
