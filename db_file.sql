-- MySQL dump 10.13  Distrib 5.7.12, for Win32 (AMD64)
--
-- Host: localhost    Database: servicemgmt
-- ------------------------------------------------------
-- Server version	5.7.37-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `brand`
--

DROP TABLE IF EXISTS `brand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `brand` (
  `BrandId` int(11) NOT NULL AUTO_INCREMENT,
  `BrandName` varchar(45) NOT NULL,
  `IsActive` int(11) NOT NULL DEFAULT '1',
  `CreatedUserId` varchar(20) NOT NULL,
  `CreatedDateTime` datetime NOT NULL,
  `UpdatedUserId` varchar(20) NOT NULL,
  `UpdatedDateTime` datetime NOT NULL,
  PRIMARY KEY (`BrandId`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brand`
--

LOCK TABLES `brand` WRITE;
/*!40000 ALTER TABLE `brand` DISABLE KEYS */;
/*!40000 ALTER TABLE `brand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hardwaretype`
--

DROP TABLE IF EXISTS `hardwaretype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hardwaretype` (
  `HardwareId` int(11) NOT NULL AUTO_INCREMENT,
  `HardwareName` varchar(45) NOT NULL,
  `CreatedDateTime` datetime NOT NULL,
  `IsActive` int(1) NOT NULL DEFAULT '1',
  `CreatedUserId` varchar(20) NOT NULL,
  `UpdatedUserId` varchar(20) NOT NULL,
  `UpdatedDateTime` datetime NOT NULL,
  PRIMARY KEY (`HardwareId`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1 COMMENT='Different types of hardware will be enlisted';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hardwaretype`
--

LOCK TABLES `hardwaretype` WRITE;
/*!40000 ALTER TABLE `hardwaretype` DISABLE KEYS */;
/*!40000 ALTER TABLE `hardwaretype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location` (
  `LocationId` int(11) NOT NULL AUTO_INCREMENT,
  `CreatedDateTime` datetime NOT NULL,
  `IsActive` int(1) NOT NULL DEFAULT '1',
  `LocationName` varchar(45) NOT NULL,
  `Floor` varchar(45) NOT NULL,
  `CreatedUserId` varchar(20) NOT NULL,
  `Wing` varchar(20) DEFAULT NULL,
  `UpdatedUserId` varchar(20) NOT NULL,
  `UpdatedDateTime` datetime NOT NULL,
  PRIMARY KEY (`LocationId`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `problemtype`
--

DROP TABLE IF EXISTS `problemtype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `problemtype` (
  `ProblemId` int(11) NOT NULL AUTO_INCREMENT,
  `ProblemDescription` varchar(45) NOT NULL,
  `IsActive` int(11) NOT NULL DEFAULT '1',
  `CreatedUserId` varchar(20) NOT NULL,
  `CreatedDateTime` datetime NOT NULL,
  `UpdatedUserId` varchar(20) NOT NULL,
  `UpdatedDateTime` datetime NOT NULL,
  `HardwareId` int(11) NOT NULL,
  PRIMARY KEY (`ProblemId`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `problemtype`
--

LOCK TABLES `problemtype` WRITE;
/*!40000 ALTER TABLE `problemtype` DISABLE KEYS */;
/*!40000 ALTER TABLE `problemtype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `status`
--

DROP TABLE IF EXISTS `status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `status` (
  `StatusId` int(11) NOT NULL AUTO_INCREMENT,
  `StatusDescription` varchar(45) NOT NULL,
  `IsActive` int(11) NOT NULL DEFAULT '1',
  `CreatedUserId` varchar(20) NOT NULL,
  `CreatedDateTime` datetime NOT NULL,
  `UpdatedUserId` varchar(20) NOT NULL,
  `UpdatedDateTime` datetime NOT NULL,
  PRIMARY KEY (`StatusId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `status`
--

LOCK TABLES `status` WRITE;
/*!40000 ALTER TABLE `status` DISABLE KEYS */;
/*!40000 ALTER TABLE `status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaction`
--

DROP TABLE IF EXISTS `transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaction` (
  `ComplaintId` int(11) NOT NULL AUTO_INCREMENT,
  `TicketId` varchar(45) NOT NULL,
  `ProblemId` int(11) NOT NULL,
  `HardwareId` int(11) NOT NULL,
  `Remark` varchar(500) DEFAULT NULL,
  `CreatedUserId` varchar(20) NOT NULL,
  `CreatedDateTime` datetime NOT NULL,
  `LocationId` int(11) NOT NULL,
  `Name` varchar(45) NOT NULL,
  `SystemName` varchar(20) DEFAULT NULL,
  `IsActive` int(11) DEFAULT '1',
  `AdminId` varchar(20) NOT NULL,
  `SolverId` varchar(20) DEFAULT NULL,
  `Solution` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`ComplaintId`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaction`
--

LOCK TABLES `transaction` WRITE;
/*!40000 ALTER TABLE `transaction` DISABLE KEYS */;
/*!40000 ALTER TABLE `transaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `UserIndex` int(11) NOT NULL AUTO_INCREMENT,
  `UserName` varchar(45) NOT NULL,
  `UserPassword` varchar(60) NOT NULL,
  `UserType` varchar(45) NOT NULL,
  `CreatedDateTime` datetime NOT NULL,
  `IsActive` int(1) NOT NULL DEFAULT '1',
  `EmployeeCode` varchar(20) NOT NULL,
  `UserId` varchar(45) NOT NULL,
  `CreatedUserId` varchar(45) NOT NULL,
  `UpdatedUserId` varchar(45) NOT NULL,
  `UpdatedDateTime` datetime NOT NULL,
  PRIMARY KEY (`UserIndex`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'root','ff9830c42660c1dd1942844f8069b74a','Admin','2022-02-18 10:39:10',1,'101','root','root','root','2022-03-23 10:12:18')
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-24 12:45:32
