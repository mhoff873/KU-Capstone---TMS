-- MySQL dump 10.13  Distrib 5.7.21, for Linux (x86_64)
--
-- Host: localhost    Database: tmst_db
-- ------------------------------------------------------
-- Server version	5.7.21-0ubuntu0.17.10.1

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
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin` (
  `adminID` int(255) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`adminID`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin`
--

LOCK TABLES `admin` WRITE;
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` VALUES (1,'bosshog','$2a$10$ugB7SLThdWpz1ITi5gHKae7cgbS/v3.dMJ5uUvI7ZW6fy.V3oKa72'),(3,'admin','$2a$10$YVFVai3hgMhDBanY/KuEiukz5FiN6qJoUG9Izr2mbgcIOODSjB1sq');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assigned`
--

DROP TABLE IF EXISTS `assigned`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assigned` (
  `assignedID` int(11) NOT NULL AUTO_INCREMENT,
  `supervisorID` int(11) NOT NULL,
  `taskID` int(11) NOT NULL,
  `formID` int(11) NOT NULL,
  PRIMARY KEY (`assignedID`),
  KEY `supervisorID` (`supervisorID`),
  KEY `taskID` (`taskID`),
  KEY `formID` (`formID`),
  CONSTRAINT `assigned_ibfk_1` FOREIGN KEY (`supervisorID`) REFERENCES `supervisors` (`supervisorID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `assigned_ibfk_2` FOREIGN KEY (`taskID`) REFERENCES `task` (`taskID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `assigned_ibfk_3` FOREIGN KEY (`formID`) REFERENCES `surveyForm` (`formID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=198 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assigned`
--

LOCK TABLES `assigned` WRITE;
/*!40000 ALTER TABLE `assigned` DISABLE KEYS */;
INSERT INTO `assigned` VALUES (197,10,654706,96);
/*!40000 ALTER TABLE `assigned` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `completedSteps`
--

DROP TABLE IF EXISTS `completedSteps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `completedSteps` (
  `completedstepID` int(11) NOT NULL AUTO_INCREMENT,
  `completedTaskID` int(255) DEFAULT NULL,
  `mainStepID` int(11) NOT NULL,
  `detailedStepsUsed` int(11) DEFAULT '0',
  `timeSpent` int(11) DEFAULT '0',
  `dateTimeCompleted` datetime DEFAULT NULL,
  PRIMARY KEY (`completedstepID`),
  KEY `mainStepID` (`mainStepID`),
  KEY `userID` (`completedTaskID`),
  KEY `completedTaskID` (`completedTaskID`),
  KEY `mainStepID_2` (`mainStepID`),
  CONSTRAINT `completedSteps_ibfk_2` FOREIGN KEY (`mainStepID`) REFERENCES `mainSteps` (`mainStepID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `completedSteps_ibfk_3` FOREIGN KEY (`completedTaskID`) REFERENCES `completedTasks` (`completedTaskID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=303 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `completedSteps`
--

LOCK TABLES `completedSteps` WRITE;
/*!40000 ALTER TABLE `completedSteps` DISABLE KEYS */;
INSERT INTO `completedSteps` VALUES (293,63,65,1,5673,'2018-04-19 21:38:04'),(294,63,66,1,980,'2018-04-19 21:38:05'),(295,63,67,1,886,'2018-04-19 21:38:05'),(296,63,68,1,1068,'2018-04-19 21:38:07'),(297,63,69,1,816,'2018-04-19 21:38:07'),(298,63,70,1,651,'2018-04-19 21:38:08'),(299,63,71,1,777,'2018-04-19 21:38:09'),(300,63,72,1,892,'2018-04-19 21:38:10'),(301,63,73,1,1104,'2018-04-19 21:38:11'),(302,63,74,1,689,'2018-04-19 21:38:12');
/*!40000 ALTER TABLE `completedSteps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `completedTasks`
--

DROP TABLE IF EXISTS `completedTasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `completedTasks` (
  `completedTaskID` int(255) NOT NULL AUTO_INCREMENT,
  `taskID` int(255) DEFAULT NULL,
  `userID` int(255) DEFAULT NULL,
  `totalTime` int(255) NOT NULL DEFAULT '0',
  `dateStarted` datetime NOT NULL,
  `dateTimeCompleted` datetime DEFAULT NULL,
  `detailedStepsUsed` int(255) NOT NULL DEFAULT '0',
  `ipAddr` char(16) NOT NULL,
  PRIMARY KEY (`completedTaskID`),
  KEY `taskID` (`taskID`),
  KEY `userID` (`userID`),
  CONSTRAINT `completedTasks_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `completedTasks_ibfk_2` FOREIGN KEY (`taskID`) REFERENCES `task` (`taskID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `completedTasks`
--

LOCK TABLES `completedTasks` WRITE;
/*!40000 ALTER TABLE `completedTasks` DISABLE KEYS */;
INSERT INTO `completedTasks` VALUES (63,654706,4,13536,'2018-04-19 21:38:04','2018-04-19 21:38:12',1,'156.12.4.3');
/*!40000 ALTER TABLE `completedTasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detailedSteps`
--

DROP TABLE IF EXISTS `detailedSteps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `detailedSteps` (
  `detailedStepID` int(11) NOT NULL AUTO_INCREMENT,
  `mainStepID` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `stepText` varchar(255) DEFAULT NULL,
  `listOrder` int(11) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`detailedStepID`),
  UNIQUE KEY `title` (`title`),
  KEY `mainStepID` (`mainStepID`),
  CONSTRAINT `detailedSteps_ibfk_1` FOREIGN KEY (`mainStepID`) REFERENCES `mainSteps` (`mainStepID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detailedSteps`
--

LOCK TABLES `detailedSteps` WRITE;
/*!40000 ALTER TABLE `detailedSteps` DISABLE KEYS */;
INSERT INTO `detailedSteps` VALUES (32,65,'Grab toothbrush','Once you find your toothbrush. Get ready to find your toothpaste',1,''),(33,66,'Apply toothpaste','Once you have your toothpaste get ready to open it. ',2,'');
/*!40000 ALTER TABLE `detailedSteps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groupOf`
--

DROP TABLE IF EXISTS `groupOf`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groupOf` (
  `groupID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(11) NOT NULL,
  `supervisorID` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`groupID`),
  UNIQUE KEY `name` (`name`),
  KEY `userID` (`userID`),
  KEY `supervisorID` (`supervisorID`),
  CONSTRAINT `groupOf_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `groupOf_ibfk_3` FOREIGN KEY (`supervisorID`) REFERENCES `supervisors` (`supervisorID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groupOf`
--

LOCK TABLES `groupOf` WRITE;
/*!40000 ALTER TABLE `groupOf` DISABLE KEYS */;
/*!40000 ALTER TABLE `groupOf` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keywords`
--

DROP TABLE IF EXISTS `keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `keywords` (
  `keywordID` int(11) NOT NULL AUTO_INCREMENT,
  `taskID` int(11) NOT NULL,
  `word` varchar(255) NOT NULL,
  PRIMARY KEY (`keywordID`),
  KEY `taskID` (`taskID`),
  CONSTRAINT `keywords_ibfk_1` FOREIGN KEY (`taskID`) REFERENCES `task` (`taskID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4291 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keywords`
--

LOCK TABLES `keywords` WRITE;
/*!40000 ALTER TABLE `keywords` DISABLE KEYS */;
INSERT INTO `keywords` VALUES (5,654706,'Toothbrush'),(6,654706,'Toothpaste\r\n'),(4289,654706,' Toothpaste\r\n'),(4290,654706,' ');
/*!40000 ALTER TABLE `keywords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mainSteps`
--

DROP TABLE IF EXISTS `mainSteps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mainSteps` (
  `mainStepID` int(11) NOT NULL AUTO_INCREMENT,
  `taskID` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `requiredInfo` varchar(255) DEFAULT NULL,
  `listOrder` int(255) DEFAULT NULL,
  `requiredItem` varchar(255) DEFAULT NULL,
  `stepText` varchar(255) DEFAULT NULL,
  `audio` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `video` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`mainStepID`),
  UNIQUE KEY `title` (`title`),
  KEY `taskID` (`taskID`),
  CONSTRAINT `mainSteps_ibfk_1` FOREIGN KEY (`taskID`) REFERENCES `task` (`taskID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=75 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mainSteps`
--

LOCK TABLES `mainSteps` WRITE;
/*!40000 ALTER TABLE `mainSteps` DISABLE KEYS */;
INSERT INTO `mainSteps` VALUES (65,654706,'Find your Toothbrush','Toothbrush',1,NULL,'Grab your own tooth brush. That is one of the two things you will need for this Tas',NULL,'',NULL),(66,654706,'Grab your toothpaste','Toothpaste',2,NULL,'Get ready to apply your toothpaste to your toothbrush',NULL,'',NULL),(67,654706,'Wet your toothbrush','Water, Toothbrush, Toothpaste',3,NULL,'Turn on your sink and run your toothbrush under water.',NULL,'',NULL),(68,654706,'Open the Cap','Toothpaste',4,NULL,'Now that you got your toothpaste make sure to flip the cap off. ',NULL,'',NULL),(69,654706,'Apply toothpaste to brush','Toothpaste, toothbrush',5,NULL,'Apply your toothpaste onto your toothbrush, in order to do this line up your toothpaste to the end of your toothbrush known as the bristles. You may use as much as you want to as little as a penny size. (A little goes a long way!).',NULL,'',NULL),(70,654706,'(Optional Step) Wet toothbrush after toothpaste has been applied.','Toothbrush, toothpaste, water',6,NULL,'This is another optional step, some people prefer to apply cold water after they apply toothpaste to their toothbrush. This will wet your toothpaste and make it easier to brush.\r\n',NULL,'',NULL),(71,654706,'Now brush your teeth','Toothbrush, toothpaste, teeth',7,NULL,' Apply your prepared toothbrush to your mouth and brush back and forth in a scrubbing motion. Left and right left and right. Keep doing that for a good while do not rush to be done.',NULL,'',NULL),(72,654706,'Put your toothbrush away','Toothbrush',8,NULL,'Place your dry toothbrush away and put it back where you found it.',NULL,'',NULL),(73,654706,'Put your toothpaste away','toothpaste',9,NULL,'Place your toothpaste away where you found it.',NULL,'',NULL),(74,654706,'Clean up any water droplets','Rag, Paper Towl',10,NULL,'Get a rag or a paper towel and clean up any water droplets or toothpaste that may have fallen out of your mouth. ',NULL,'',NULL);
/*!40000 ALTER TABLE `mainSteps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `request`
--

DROP TABLE IF EXISTS `request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `request` (
  `requestID` int(255) NOT NULL AUTO_INCREMENT,
  `userID` int(255) NOT NULL,
  `supervisorID` int(255) NOT NULL,
  `taskID` int(255) NOT NULL,
  `requestDescription` varchar(255) DEFAULT NULL,
  `isApproved` tinyint(1) DEFAULT '0',
  `dateRequested` date DEFAULT NULL,
  PRIMARY KEY (`requestID`),
  KEY `userID` (`userID`),
  KEY `supervisorID` (`supervisorID`),
  KEY `taskID` (`taskID`),
  CONSTRAINT `request_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `request_ibfk_2` FOREIGN KEY (`taskID`) REFERENCES `task` (`taskID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `request_ibfk_3` FOREIGN KEY (`supervisorID`) REFERENCES `supervisors` (`supervisorID`)
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `request`
--

LOCK TABLES `request` WRITE;
/*!40000 ALTER TABLE `request` DISABLE KEYS */;
INSERT INTO `request` VALUES (136,4,10,654706,NULL,1,'2018-04-20');
/*!40000 ALTER TABLE `request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supervisors`
--

DROP TABLE IF EXISTS `supervisors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supervisors` (
  `supervisorID` int(255) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fname` varchar(255) DEFAULT NULL,
  `mname` varchar(255) DEFAULT NULL,
  `lname` varchar(255) DEFAULT NULL,
  `isLoggedIn` tinyint(1) DEFAULT NULL,
  `dateCreated` date DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `active` tinyint(1) DEFAULT '1',
  `birthday` date DEFAULT NULL,
  `ethnicity` varchar(255) DEFAULT NULL,
  `picture` varchar(255) DEFAULT NULL,
  `affiliation` varchar(255) DEFAULT NULL,
  `phone` bigint(255) DEFAULT NULL,
  PRIMARY KEY (`supervisorID`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supervisors`
--

LOCK TABLES `supervisors` WRITE;
/*!40000 ALTER TABLE `supervisors` DISABLE KEYS */;
INSERT INTO `supervisors` VALUES (5,'Bettycooper@gmail.com','$2b$12$LufSdoTDau58P/txOJ7wkOz2GOag2Hx3eEw1zIecpCd8W7T.cvBXO','Betty','','Cooper',1,'2018-02-14','female',1,'1996-11-13','White',NULL,NULL,1231231234),(10,'test@test.com','$2b$12$LufSdoTDau58P/txOJ7wkOz2GOag2Hx3eEw1zIecpCd8W7T.cvBXO','Mason',NULL,'Hoffman',1,'2018-02-14','male',1,'1992-09-23','Right Triangle',NULL,'Cult of Pythagoras',1234567890),(53,'best@test.com','$2a$10$luvdo1it.QANhLzBujBnA.UM2bs6RoN7EYAd4TiNWOgUCU9U..7q6','Tyler',NULL,'Lance',1,'2008-02-01','other',1,'1992-09-23','Isosceles Triangle',NULL,'Freemason',1234567890);
/*!40000 ALTER TABLE `supervisors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surveyForm`
--

DROP TABLE IF EXISTS `surveyForm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `surveyForm` (
  `formID` int(11) NOT NULL AUTO_INCREMENT,
  `supervisorID` int(11) NOT NULL,
  `formTitle` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `dateCreated` date DEFAULT NULL,
  `dateModified` date DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`formID`),
  UNIQUE KEY `formTitle` (`formTitle`),
  KEY `supervisorID` (`supervisorID`),
  CONSTRAINT `surveyForm_ibfk_1` FOREIGN KEY (`supervisorID`) REFERENCES `supervisors` (`supervisorID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surveyForm`
--

LOCK TABLES `surveyForm` WRITE;
/*!40000 ALTER TABLE `surveyForm` DISABLE KEYS */;
INSERT INTO `surveyForm` VALUES (96,10,'Questionaire','regarding the brush your teeth survey','2018-04-19','2018-04-19',1);
/*!40000 ALTER TABLE `surveyForm` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surveyMultQuest`
--

DROP TABLE IF EXISTS `surveyMultQuest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `surveyMultQuest` (
  `multiQuestID` int(255) NOT NULL AUTO_INCREMENT,
  `questID` int(255) DEFAULT NULL,
  `questText` varchar(255) DEFAULT NULL,
  `questOrder` int(255) DEFAULT NULL,
  PRIMARY KEY (`multiQuestID`),
  KEY `questID` (`questID`),
  CONSTRAINT `surveyMultQuest_ibfk_1` FOREIGN KEY (`questID`) REFERENCES `surveyQuest` (`questID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surveyMultQuest`
--

LOCK TABLES `surveyMultQuest` WRITE;
/*!40000 ALTER TABLE `surveyMultQuest` DISABLE KEYS */;
INSERT INTO `surveyMultQuest` VALUES (35,117,'Excellent',1),(36,117,'Alright',2),(37,117,'Poor',3);
/*!40000 ALTER TABLE `surveyMultQuest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surveyQuest`
--

DROP TABLE IF EXISTS `surveyQuest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `surveyQuest` (
  `questID` int(11) NOT NULL AUTO_INCREMENT,
  `formID` int(11) NOT NULL,
  `questType` varchar(255) DEFAULT NULL,
  `questText` varchar(255) DEFAULT NULL,
  `isActive` tinyint(1) DEFAULT NULL,
  `questOrder` int(255) DEFAULT NULL,
  PRIMARY KEY (`questID`),
  KEY `formID` (`formID`),
  CONSTRAINT `surveyQuest_ibfk_1` FOREIGN KEY (`formID`) REFERENCES `surveyForm` (`formID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=119 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surveyQuest`
--

LOCK TABLES `surveyQuest` WRITE;
/*!40000 ALTER TABLE `surveyQuest` DISABLE KEYS */;
INSERT INTO `surveyQuest` VALUES (117,96,'multiple choice','How well was the task laid out?',1,1),(118,96,'open ended','Comments?',1,2);
/*!40000 ALTER TABLE `surveyQuest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surveyQuestResults`
--

DROP TABLE IF EXISTS `surveyQuestResults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `surveyQuestResults` (
  `questResultID` int(255) NOT NULL AUTO_INCREMENT,
  `resultID` int(255) DEFAULT NULL,
  `questID` int(255) DEFAULT NULL,
  `response` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`questResultID`),
  KEY `resultID` (`resultID`),
  KEY `questID` (`questID`),
  CONSTRAINT `surveyQuestResults_ibfk_1` FOREIGN KEY (`questID`) REFERENCES `surveyQuest` (`questID`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `surveyQuestResults_ibfk_2` FOREIGN KEY (`resultID`) REFERENCES `surveyResults` (`resultID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surveyQuestResults`
--

LOCK TABLES `surveyQuestResults` WRITE;
/*!40000 ALTER TABLE `surveyQuestResults` DISABLE KEYS */;
INSERT INTO `surveyQuestResults` VALUES (143,65,117,'Excellent'),(144,65,118,'I really like how detailed this got. Thank you.');
/*!40000 ALTER TABLE `surveyQuestResults` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surveyResults`
--

DROP TABLE IF EXISTS `surveyResults`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `surveyResults` (
  `resultID` int(11) NOT NULL AUTO_INCREMENT,
  `userID` int(11) NOT NULL,
  `formID` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `timeSpent` int(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `ipAddr` varchar(16) DEFAULT NULL,
  `ageGroup` int(255) DEFAULT NULL,
  `results` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `comments` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`resultID`),
  KEY `userID` (`userID`),
  KEY `formID` (`formID`),
  CONSTRAINT `surveyResults_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `surveyResults_ibfk_2` FOREIGN KEY (`formID`) REFERENCES `surveyForm` (`formID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surveyResults`
--

LOCK TABLES `surveyResults` WRITE;
/*!40000 ALTER TABLE `surveyResults` DISABLE KEYS */;
INSERT INTO `surveyResults` VALUES (65,4,96,'mark smith',0,'test.com','156.12.4.3',0,'','2018-04-19 21:38:30','');
/*!40000 ALTER TABLE `surveyResults` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `task` (
  `taskID` int(11) NOT NULL AUTO_INCREMENT,
  `supervisorID` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `activated` tinyint(1) DEFAULT NULL,
  `dateCreated` date DEFAULT NULL,
  `dateModified` date DEFAULT NULL,
  `lastUsed` datetime DEFAULT NULL,
  `published` tinyint(1) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`taskID`),
  UNIQUE KEY `title` (`title`),
  KEY `supervisorID` (`supervisorID`),
  CONSTRAINT `task_ibfk_1` FOREIGN KEY (`supervisorID`) REFERENCES `supervisors` (`supervisorID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=654793 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task`
--

LOCK TABLES `task` WRITE;
/*!40000 ALTER TABLE `task` DISABLE KEYS */;
INSERT INTO `task` VALUES (654706,10,'Brush your teeth','Properly Brush your teeth',0,'2018-02-23','2018-02-23','2018-02-23 00:00:00',0,''),(654707,10,'Make a sandwhich','How to properly make a sandwhich',1,'2018-02-23','2018-02-23','2018-02-23 00:00:00',1,NULL),(654792,10,'Attract a m8','',0,'2018-04-20','2018-04-20','2018-04-20 01:31:20',0,'T=None');
/*!40000 ALTER TABLE `task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `userID` int(255) NOT NULL AUTO_INCREMENT,
  `supervisorID` int(255) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` bigint(11) DEFAULT NULL,
  `fname` varchar(255) DEFAULT NULL,
  `mname` varchar(255) DEFAULT NULL,
  `lname` varchar(255) DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `affiliation` varchar(255) DEFAULT NULL,
  `ethnicity` varchar(255) DEFAULT NULL,
  `active` tinyint(1) DEFAULT '1',
  `isLoggedIn` tinyint(1) DEFAULT '0',
  `dateCreated` date DEFAULT NULL,
  `lastActive` datetime DEFAULT NULL,
  `picture` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`userID`),
  UNIQUE KEY `email` (`email`),
  KEY `supervisorID` (`supervisorID`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`supervisorID`) REFERENCES `supervisors` (`supervisorID`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=123457052 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,5,'test','$2a$10$pi2lCpa.xn853mTaFoXobOJBNZmAyen1Fz5GD95bK/KwetVGKZBye',16109449595,'Tyler','Harry','Lance','female','2017-03-14','Kutztown','White',1,1,'2018-01-22','2018-03-08 15:33:55','2'),(4,10,'test.com','$2a$10$6WFbSunIrYPmvCrmtSBKc.Ek.23aqS0yaIz79EVj6O/TG0v1LQzoC',19999999999,'mark','russell','smith','male','0000-00-00','kutztown','white',0,1,'2018-03-10','2018-04-19 21:32:18','image.jpg'),(5,10,'test@test.com','$2a$10$PjvPAgq51mSNX/pddmTk1.6qLweF7vzGhtXYZyFHhle.Zapjvdv1K',6109441111,'Tom','Brady',NULL,'other','2017-12-31','Patriots','White',1,0,'2018-02-01','2018-02-01 00:00:00',NULL),(14,NULL,'Wonderwoman@dc.com','$2a$10$lyBR2qFPTxsEPYJ.wONj2.PKqYivXO6tplCSxMMl4eXlzDUKex48a',NULL,'Diana',NULL,'Prince','female','2018-02-05',NULL,'white',1,0,'2018-02-25','2018-02-01 00:00:00',NULL),(15,10,'GreenArrow@dc.com','$2a$10$RpPndKv8vhqhT1M4SArpC.GYiJuliGzK8qrSBkGgGOLLLTwh1hQWe',NULL,'Oliver',NULL,'Queen\r\n','male','2018-02-05',NULL,'white',1,1,'2018-02-01','2018-03-27 11:42:57',NULL),(16,5,'Superman@dc.com','$2a$10$59imyzs9vH8h5AMToStrpOZLzSmlHBuRyRsAzVm3FSuwRuQ.u6gLu',NULL,'Clark',NULL,'Kent','female','2018-02-05',NULL,'white',1,0,'2018-02-01','2018-02-01 00:00:00',NULL),(17,NULL,'Zatanna@dc.com','$2a$10$yen/keqcpsoU1h/Fimm1UOV/t/fCM3SAz/6iWwJ8jWIv4XT3D8WKO',NULL,'Zatanna',NULL,'Zatara','female','2018-02-05',NULL,'white',1,0,'2018-02-01','2018-02-01 00:00:00',NULL),(18,5,'HulkHogan@wwe.com','$2a$10$NJvQ4rdKeG65OHYf5FC43eYc5Zchuh1UqY9YE.2Kzi72BhDhpvuli',NULL,'Hulk',NULL,'Hogan','female','2018-02-05',NULL,'white',1,0,'2018-02-01','2018-02-01 00:00:00',NULL),(69,10,'nyost448@kutztown.edu','$2a$10$LCHDf6MdoP3gftzZiJIj6ubUwXGsYQ4uBo4MsBO3SqmDJ3ka91nm2',4843007777,'Nathan','Bruce','Yost','male','0000-00-00','Kutztown','white',1,0,'2018-03-10','2018-03-27 11:40:46','NULL'),(123457051,NULL,'me@reee.com','$2b$12$0tysir3old5n9VPDIU8ytOqDruokTgxJKLXG/4KYsusiCD1i0x/iO',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2018-04-20','2018-04-20 01:27:01',NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-04-19 21:41:13
