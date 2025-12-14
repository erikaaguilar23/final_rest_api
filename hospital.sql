-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: hospital
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `diagnosis`
--

DROP TABLE IF EXISTS `diagnosis`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diagnosis` (
  `idDiagnosis` int NOT NULL AUTO_INCREMENT,
  `diagnosis_name` varchar(45) NOT NULL,
  `category` varchar(45) NOT NULL,
  PRIMARY KEY (`idDiagnosis`)
) ENGINE=InnoDB AUTO_INCREMENT=445 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diagnosis`
--

LOCK TABLES `diagnosis` WRITE;
/*!40000 ALTER TABLE `diagnosis` DISABLE KEYS */;
INSERT INTO `diagnosis` VALUES (1,'hypertension','cardiovascular'),(2,'asthma','respiratory'),(3,'migraine','neurological'),(4,'diabetes','endocrine'),(5,'chickenpox','infection');
/*!40000 ALTER TABLE `diagnosis` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `iddoctors` int NOT NULL AUTO_INCREMENT,
  `doctor_name` varchar(45) NOT NULL,
  `specialization` varchar(45) NOT NULL,
  PRIMARY KEY (`iddoctors`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (1,'marc rebbit','cardiology'),(2,'raymart diaz','pediatrics'),(3,'axel flores','neurology'),(4,'eden rose','pulmonology');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors_has_patient`
--

DROP TABLE IF EXISTS `doctors_has_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors_has_patient` (
  `doctors_iddoctors` int NOT NULL,
  `Patient_idPatient` int NOT NULL,
  `Patient_Diagnosis_idDiagnosis` int NOT NULL,
  PRIMARY KEY (`doctors_iddoctors`,`Patient_idPatient`,`Patient_Diagnosis_idDiagnosis`),
  KEY `fk_doctors_has_Patient_Patient1_idx` (`Patient_idPatient`,`Patient_Diagnosis_idDiagnosis`),
  KEY `fk_doctors_has_Patient_doctors1_idx` (`doctors_iddoctors`),
  CONSTRAINT `fk_doctors_has_Patient_doctors1` FOREIGN KEY (`doctors_iddoctors`) REFERENCES `doctors` (`iddoctors`),
  CONSTRAINT `fk_doctors_has_Patient_Patient1` FOREIGN KEY (`Patient_idPatient`, `Patient_Diagnosis_idDiagnosis`) REFERENCES `patient` (`idPatient`, `Diagnosis_idDiagnosis`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors_has_patient`
--

LOCK TABLES `doctors_has_patient` WRITE;
/*!40000 ALTER TABLE `doctors_has_patient` DISABLE KEYS */;
INSERT INTO `doctors_has_patient` VALUES (1,1,1),(4,4,4);
/*!40000 ALTER TABLE `doctors_has_patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `idPatient` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `age` varchar(45) NOT NULL,
  `Diagnosis_idDiagnosis` int NOT NULL,
  PRIMARY KEY (`idPatient`,`Diagnosis_idDiagnosis`),
  KEY `fk_Patient_Diagnosis_idx` (`Diagnosis_idDiagnosis`),
  CONSTRAINT `fk_Patient_Diagnosis` FOREIGN KEY (`Diagnosis_idDiagnosis`) REFERENCES `diagnosis` (`idDiagnosis`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (1,'erika aguilar','23',1),(1,'erika aguilar','23',2),(4,'rabang','30',4),(5,'John Doe','30',2);
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-14  9:15:53
