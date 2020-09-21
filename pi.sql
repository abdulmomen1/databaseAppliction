-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 08, 2020 at 11:28 PM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.4.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pi`
--

-- --------------------------------------------------------

--
-- Table structure for table `fields`
--

CREATE TABLE `fields` (
  `field_id` int(11) DEFAULT NULL,
  `field_name` varchar(99) DEFAULT NULL,
  `plant_type` varchar(99) DEFAULT NULL,
  `Width_F` int(11) NOT NULL,
  `Height_F` int(11) NOT NULL,
  `water_mm` float DEFAULT NULL,
  `Day_of_plant` int(11) DEFAULT NULL,
  `soil` int(11) DEFAULT NULL,
  `water_l` int(11) DEFAULT NULL,
  `temp` int(11) DEFAULT NULL,
  `humidity` int(11) DEFAULT NULL,
  `Date_s` date DEFAULT NULL,
  `Date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `fields`
--

INSERT INTO `fields` (`field_id`, `field_name`, `plant_type`, `Width_F`, `Height_F`, `water_mm`, `Day_of_plant`, `soil`, `water_l`, `temp`, `humidity`, `Date_s`, `Date`) VALUES
(1, 'potatoField', 'potato', 54, 70, 0.75, 32, 50, 50, 30, 32, NULL, '2020-08-07'),
(2, 'potatoField', 'tomato', 54, 70, 0.45, 0, NULL, NULL, NULL, NULL, NULL, '2020-09-08'),
(3, 'dd', 'potato', 23, 22, 0, 0, NULL, NULL, NULL, NULL, NULL, '2020-09-08');

-- --------------------------------------------------------

--
-- Table structure for table `irregationtable`
--

CREATE TABLE `irregationtable` (
  `plTypeID` int(11) NOT NULL,
  `stageID` int(11) NOT NULL,
  `amount` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `irregationtable`
--

INSERT INTO `irregationtable` (`plTypeID`, `stageID`, `amount`) VALUES
(1, 1, 0.45),
(1, 2, 0.75),
(1, 3, 1.15),
(1, 4, 0.85),
(2, 1, 0.45),
(2, 2, 0.75),
(2, 3, 1.15),
(2, 4, 0.8);

-- --------------------------------------------------------

--
-- Stand-in structure for view `plantstageduration`
-- (See below for the actual view)
--
CREATE TABLE `plantstageduration` (
`amount` float
,`pTypeName` varchar(99)
,`StName` varchar(99)
,`StDuration` int(11)
,`ptId` int(11)
);

-- --------------------------------------------------------

--
-- Table structure for table `planttype`
--

CREATE TABLE `planttype` (
  `pTypeID` int(11) NOT NULL,
  `pTypeName` varchar(99) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `planttype`
--

INSERT INTO `planttype` (`pTypeID`, `pTypeName`) VALUES
(1, 'potato'),
(2, 'tomato');

-- --------------------------------------------------------

--
-- Table structure for table `stagetable`
--

CREATE TABLE `stagetable` (
  `StID` int(11) NOT NULL,
  `StName` varchar(99) NOT NULL,
  `duration` int(11) NOT NULL,
  `plantId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `stagetable`
--

INSERT INTO `stagetable` (`StID`, `StName`, `duration`, `plantId`) VALUES
(1, 'stage1', 30, 1),
(1, 'stage1', 35, 2),
(2, 'stage2', 35, 1),
(2, 'stage2', 45, 2),
(3, 'stage3', 50, 1),
(3, 'stage3', 70, 2),
(4, 'stage4', 30, 1),
(4, 'stage4', 30, 2);

-- --------------------------------------------------------

--
-- Structure for view `plantstageduration`
--
DROP TABLE IF EXISTS `plantstageduration`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `plantstageduration`  AS  select `arr`.`amount` AS `amount`,`plty`.`pTypeName` AS `pTypeName`,`stg`.`StName` AS `StName`,`stg`.`duration` AS `StDuration`,`plty`.`pTypeID` AS `ptId` from ((`irregationtable` `arr` join `stagetable` `stg` on(`stg`.`StID` = `arr`.`stageID` and `stg`.`plantId` = `arr`.`plTypeID`)) join `planttype` `plty` on(`plty`.`pTypeID` = `stg`.`plantId`)) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `irregationtable`
--
ALTER TABLE `irregationtable`
  ADD KEY `plTypeID` (`plTypeID`,`stageID`),
  ADD KEY `amount` (`amount`),
  ADD KEY `amount_2` (`amount`);

--
-- Indexes for table `planttype`
--
ALTER TABLE `planttype`
  ADD PRIMARY KEY (`pTypeID`);

--
-- Indexes for table `stagetable`
--
ALTER TABLE `stagetable`
  ADD PRIMARY KEY (`StID`,`plantId`),
  ADD KEY `plantId` (`plantId`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `irregationtable`
--
ALTER TABLE `irregationtable`
  ADD CONSTRAINT `irregForien` FOREIGN KEY (`plTypeID`,`stageID`) REFERENCES `stagetable` (`plantId`, `StID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `stagetable`
--
ALTER TABLE `stagetable`
  ADD CONSTRAINT `stagetable_ibfk_1` FOREIGN KEY (`plantId`) REFERENCES `planttype` (`pTypeID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
