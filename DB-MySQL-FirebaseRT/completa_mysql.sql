CREATE DATABASE  IF NOT EXISTS `Proyecto_Escalera_Pared` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `Proyecto_Escalera_Pared`;
-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 35.223.160.190    Database: Proyecto_Escalera_Pared
-- ------------------------------------------------------
-- Server version	8.0.41-google

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '526fc6a7-52a9-11f0-8e46-42010a400002:1-857';

--
-- Table structure for table `acceso`
--

DROP TABLE IF EXISTS `acceso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `acceso` (
  `id_acceso` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `fecha_acceso` datetime DEFAULT CURRENT_TIMESTAMP,
  `tipo_acceso` enum('login','logout','fallido') DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text,
  PRIMARY KEY (`id_acceso`),
  KEY `idx_acceso_usuario_fecha` (`id_usuario`,`fecha_acceso`),
  CONSTRAINT `acceso_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `acceso`
--

LOCK TABLES `acceso` WRITE;
/*!40000 ALTER TABLE `acceso` DISABLE KEYS */;
INSERT INTO `acceso` VALUES (1,1,'2025-07-08 00:43:29','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(2,1,'2025-07-08 00:43:39','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(3,1,'2025-07-08 01:28:16','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(4,1,'2025-07-08 01:28:30','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(5,1,'2025-07-08 02:58:44','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(6,1,'2025-07-08 16:27:01','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(7,1,'2025-07-08 16:40:55','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(8,2,'2025-07-08 16:41:47','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(9,2,'2025-07-08 16:42:47','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(10,1,'2025-07-08 16:46:05','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(11,1,'2025-07-09 01:57:51','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(12,2,'2025-07-09 01:58:07','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(13,2,'2025-07-09 02:00:04','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(14,1,'2025-07-09 02:01:50','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(15,1,'2025-07-09 19:22:03','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(16,1,'2025-07-10 11:29:04','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(17,1,'2025-07-12 02:30:19','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(18,1,'2025-07-12 15:59:24','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'),(19,1,'2025-07-12 15:59:28','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'),(20,1,'2025-07-12 15:59:46','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'),(21,1,'2025-07-12 11:08:52','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'),(22,1,'2025-07-12 14:22:01','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(23,1,'2025-07-12 14:53:37','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(24,1,'2025-07-12 15:27:56','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(25,1,'2025-07-12 15:28:21','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(26,2,'2025-07-12 15:28:43','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(27,2,'2025-07-12 15:29:38','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(28,1,'2025-07-12 15:29:48','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(29,1,'2025-07-14 23:42:50','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(30,1,'2025-07-15 02:38:07','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(31,1,'2025-07-15 02:47:18','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(32,1,'2025-07-15 02:51:49','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(33,1,'2025-07-15 03:08:38','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(34,1,'2025-07-15 03:15:35','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(35,1,'2025-07-15 03:26:24','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(36,1,'2025-07-15 03:26:36','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(37,1,'2025-07-15 04:02:33','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(38,2,'2025-07-15 04:03:09','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(39,2,'2025-07-15 04:06:51','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(40,1,'2025-07-15 04:07:02','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(41,1,'2025-07-15 05:15:53','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(42,1,'2025-07-15 12:12:57','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(43,1,'2025-07-15 12:12:57','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(44,1,'2025-07-15 16:22:28','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(45,1,'2025-07-15 16:53:16','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(46,1,'2025-07-15 16:59:09','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(47,1,'2025-07-15 17:06:04','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(48,1,'2025-07-15 17:06:21','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(49,1,'2025-07-15 17:25:16','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(50,1,'2025-07-15 17:25:26','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(51,1,'2025-07-15 17:35:10','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(52,1,'2025-07-15 19:17:11','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(53,1,'2025-07-15 19:17:21','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(54,1,'2025-07-16 07:22:03','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(55,1,'2025-07-16 16:47:31','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(56,1,'2025-07-16 16:47:41','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(57,1,'2025-07-16 22:37:03','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(58,1,'2025-07-17 09:45:51','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(59,1,'2025-07-17 16:14:59','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(60,1,'2025-07-17 18:44:46','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(61,1,'2025-07-17 19:55:32','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(62,1,'2025-07-17 19:55:56','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0'),(63,1,'2025-07-18 01:06:03','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0'),(64,1,'2025-07-18 01:39:46','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(65,1,'2025-07-18 01:41:34','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(66,1,'2025-07-18 01:43:19','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0'),(67,1,'2025-07-18 01:43:50','logout','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(68,1,'2025-07-18 01:49:38','logout','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0'),(69,2,'2025-07-18 01:50:11','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0'),(70,2,'2025-07-18 01:52:27','logout','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0'),(71,1,'2025-07-18 01:58:24','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(72,1,'2025-07-18 02:36:57','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(73,1,'2025-07-17 22:29:05','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(74,1,'2025-07-17 22:29:20','login','127.0.0.1','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(75,1,'2025-07-17 22:52:13','logout','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(76,1,'2025-07-17 22:52:24','login','127.0.0.1','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(77,1,'2025-07-18 05:39:59','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(78,1,'2025-07-18 06:11:54','login','169.254.169.126','Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(79,1,'2025-07-18 06:12:20','logout','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(80,1,'2025-07-18 01:21:13','logout','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0'),(81,1,'2025-07-18 01:21:32','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(82,1,'2025-07-18 08:37:40','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0'),(83,1,'2025-07-18 08:48:49','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(84,1,'2025-07-18 09:10:51','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(85,1,'2025-07-18 09:48:11','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(86,1,'2025-07-18 09:55:25','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(87,1,'2025-07-18 10:02:12','logout','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(88,1,'2025-07-18 12:03:49','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(89,1,'2025-07-18 12:08:57','logout','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(90,4,'2025-07-18 12:09:45','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(91,4,'2025-07-18 12:10:41','logout','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(92,1,'2025-07-18 14:27:56','logout','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0'),(93,4,'2025-07-18 14:43:10','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 OPR/119.0.0.0'),(94,1,'2025-07-31 21:31:11','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0'),(95,1,'2025-08-01 09:56:38','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0'),(96,4,'2025-08-01 10:36:56','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36'),(97,1,'2025-08-01 11:24:03','logout','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0'),(98,4,'2025-08-01 11:28:36','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0'),(99,1,'2025-08-06 16:13:46','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(100,1,'2025-08-06 16:43:06','logout','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'),(101,1,'2025-08-06 18:16:30','login','169.254.169.126','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'),(102,1,'2025-08-06 20:18:06','login','169.254.169.126','Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36');
/*!40000 ALTER TABLE `acceso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `condicion`
--

DROP TABLE IF EXISTS `condicion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `condicion` (
  `id_condicion` int NOT NULL AUTO_INCREMENT,
  `nombre_condicion` varchar(100) DEFAULT NULL,
  `categoria` enum('neurológica','física','psicológica','genética','cognitiva') DEFAULT NULL,
  `descripcion` text,
  PRIMARY KEY (`id_condicion`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `condicion`
--

LOCK TABLES `condicion` WRITE;
/*!40000 ALTER TABLE `condicion` DISABLE KEYS */;
INSERT INTO `condicion` VALUES (1,'TDAH','neurológica','Trastorno por Déficit de Atención e Hiperactividad'),(2,'TEA','neurológica','Trastorno del Espectro Autista'),(3,'Dislexia','neurológica','Dificultad en el aprendizaje de la lectura'),(4,'Parálisis Cerebral','física','Trastorno del movimiento y postura'),(5,'Síndrome de Down','genética','Alteración genética del cromosoma 21'),(6,'Discapacidad Intelectual','cognitiva','Limitaciones en el funcionamiento intelectual');
/*!40000 ALTER TABLE `condicion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genero`
--

DROP TABLE IF EXISTS `genero`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genero` (
  `id_genero` int NOT NULL AUTO_INCREMENT,
  `nombre_genero` varchar(20) NOT NULL,
  PRIMARY KEY (`id_genero`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genero`
--

LOCK TABLES `genero` WRITE;
/*!40000 ALTER TABLE `genero` DISABLE KEYS */;
INSERT INTO `genero` VALUES (1,'Masculino'),(2,'Femenino'),(3,'No especificado');
/*!40000 ALTER TABLE `genero` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nino`
--

DROP TABLE IF EXISTS `nino`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nino` (
  `id_nino` int NOT NULL AUTO_INCREMENT,
  `codigo_nino` varchar(50) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL,
  `id_genero` int DEFAULT NULL,
  `peso` decimal(5,2) DEFAULT NULL,
  `altura` decimal(5,2) DEFAULT NULL,
  `tutor_responsable` varchar(100) DEFAULT NULL,
  `telefono_contacto` varchar(20) DEFAULT NULL,
  `email_contacto` varchar(100) DEFAULT NULL,
  `observaciones` text,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_nino`),
  UNIQUE KEY `codigo_nino` (`codigo_nino`),
  KEY `id_genero` (`id_genero`),
  KEY `idx_nino_codigo` (`codigo_nino`),
  CONSTRAINT `nino_ibfk_1` FOREIGN KEY (`id_genero`) REFERENCES `genero` (`id_genero`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nino`
--

LOCK TABLES `nino` WRITE;
/*!40000 ALTER TABLE `nino` DISABLE KEYS */;
INSERT INTO `nino` VALUES (1,'NINO-20250708004809','Defecto','Defecto','2010-02-01',1,50.00,100.00,'Rosa Maldonado','0989874391','edwin.arroyo@ucuenca.edu.ec','no hay fock',1,'2025-07-08 00:48:10'),(2,'NINO-20250708033045','Juana','Velez','2012-12-01',2,60.00,110.00,'Rosa Maldonado','0989874391','johmayra.velez@ucuenca.edu.ec','Ninguna',1,'2025-07-08 03:30:46'),(3,'NINO-20250708033229','Victoria','Aguilar','2013-11-11',2,60.00,100.00,'juan jaramillo ','0989674391','johmiya.velez@ucuenca.edu.ec','Ninguna',1,'2025-07-08 03:32:30'),(4,'NINO-20250718144429','Joaquin','Contreras','2015-11-19',1,40.00,129.00,'Rosa Maldonado','','','',1,'2025-07-18 14:44:29'),(5,'NINO-20250801113012','Jhomayra','Velez','2015-02-15',2,115.00,115.00,'Stalin','','','',1,'2025-08-01 11:30:13');
/*!40000 ALTER TABLE `nino` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nino_condicion`
--

DROP TABLE IF EXISTS `nino_condicion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nino_condicion` (
  `id_nino_condicion` int NOT NULL AUTO_INCREMENT,
  `id_nino` int DEFAULT NULL,
  `id_condicion` int DEFAULT NULL,
  `severidad` enum('leve','moderada','severa') DEFAULT NULL,
  `fecha_diagnostico` date DEFAULT NULL,
  `observaciones` text,
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_nino_condicion`),
  UNIQUE KEY `id_nino` (`id_nino`,`id_condicion`),
  KEY `id_condicion` (`id_condicion`),
  CONSTRAINT `nino_condicion_ibfk_1` FOREIGN KEY (`id_nino`) REFERENCES `nino` (`id_nino`) ON DELETE CASCADE,
  CONSTRAINT `nino_condicion_ibfk_2` FOREIGN KEY (`id_condicion`) REFERENCES `condicion` (`id_condicion`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nino_condicion`
--

LOCK TABLES `nino_condicion` WRITE;
/*!40000 ALTER TABLE `nino_condicion` DISABLE KEYS */;
INSERT INTO `nino_condicion` VALUES (1,1,6,'severa','2025-11-10','N/A',1);
/*!40000 ALTER TABLE `nino_condicion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rol`
--

DROP TABLE IF EXISTS `rol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `nombre_rol` varchar(50) NOT NULL,
  `descripcion` text,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol`
--

LOCK TABLES `rol` WRITE;
/*!40000 ALTER TABLE `rol` DISABLE KEYS */;
INSERT INTO `rol` VALUES (1,'admin','Administrador del sistema con acceso completo'),(2,'evaluador','Evaluador que puede realizar sesiones de evaluación'),(3,'supervisor','Supervisor que puede ver reportes y gestionar evaluadores');
/*!40000 ALTER TABLE `rol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sesion`
--

DROP TABLE IF EXISTS `sesion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sesion` (
  `id_sesion` int NOT NULL AUTO_INCREMENT,
  `id_nino` int DEFAULT NULL,
  `id_usuario` int DEFAULT NULL,
  `session_id_firebase` varchar(100) DEFAULT NULL,
  `fecha_sesion` datetime DEFAULT NULL,
  `tipo_evaluacion` enum('diagnóstica','seguimiento') DEFAULT NULL,
  `estado` enum('programada','en_curso','completada','cancelada') DEFAULT 'programada',
  `observaciones_inicio` text,
  `observaciones_final` text,
  `sincronizado_firebase` tinyint(1) DEFAULT '0',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_sesion`),
  UNIQUE KEY `session_id_firebase` (`session_id_firebase`),
  KEY `id_nino` (`id_nino`),
  KEY `id_usuario` (`id_usuario`),
  KEY `idx_sesion_firebase` (`session_id_firebase`),
  KEY `idx_sesion_fecha` (`fecha_sesion`),
  CONSTRAINT `sesion_ibfk_1` FOREIGN KEY (`id_nino`) REFERENCES `nino` (`id_nino`),
  CONSTRAINT `sesion_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sesion`
--

LOCK TABLES `sesion` WRITE;
/*!40000 ALTER TABLE `sesion` DISABLE KEYS */;
INSERT INTO `sesion` VALUES (1,1,1,'2025-07-08_16-52-58','2025-07-08 21:53:00','diagnóstica','completada',NULL,NULL,1,'2025-07-08 21:53:00'),(2,1,1,'2025-07-09_01-52-10','2025-07-09 06:52:11','diagnóstica','en_curso',NULL,NULL,1,'2025-07-09 06:52:11'),(3,3,1,'2025-07-09_01-56-35','2025-07-09 06:56:35','diagnóstica','completada',NULL,NULL,1,'2025-07-09 06:56:35'),(4,2,2,'2025-07-09_01-58-19','2025-07-09 06:58:20','diagnóstica','completada',NULL,NULL,1,'2025-07-09 06:58:20'),(5,1,1,'2025-07-10_12-14-19','2025-07-10 17:14:05','diagnóstica','en_curso',NULL,NULL,1,'2025-07-10 17:14:05'),(6,1,1,'2025-07-10_12-14-22','2025-07-10 17:14:08','diagnóstica','en_curso',NULL,NULL,1,'2025-07-10 17:14:08'),(7,1,1,'2025-07-10_12-14-24','2025-07-10 17:14:11','diagnóstica','completada',NULL,NULL,1,'2025-07-10 17:14:11'),(8,1,1,'2025-07-15_18-43-28','2025-07-15 23:43:15','diagnóstica','completada',NULL,NULL,1,'2025-07-15 23:43:15'),(9,2,1,'2025-07-15_18-44-49','2025-07-15 23:44:35','diagnóstica','completada',NULL,NULL,1,'2025-07-15 23:44:35'),(10,1,1,'2025-07-15_18-53-59','2025-07-15 23:53:58','diagnóstica','en_curso',NULL,NULL,1,'2025-07-15 23:53:58'),(11,1,1,'2025-07-15_18-55-08','2025-07-15 23:55:07','diagnóstica','en_curso',NULL,NULL,1,'2025-07-15 23:55:07'),(12,1,1,'2025-07-16_17-14-32','2025-07-16 22:14:32','diagnóstica','completada',NULL,NULL,1,'2025-07-16 22:14:32'),(13,1,1,'2025-07-16_19-05-37','2025-07-17 00:05:36','diagnóstica','completada',NULL,NULL,1,'2025-07-17 00:05:36'),(14,1,1,'2025-07-16_19-13-02','2025-07-17 00:13:02','diagnóstica','completada',NULL,NULL,1,'2025-07-17 00:13:02'),(15,3,1,'2025-07-16_19-16-55','2025-07-17 00:16:55','diagnóstica','en_curso',NULL,NULL,1,'2025-07-17 00:16:55'),(16,1,1,'2025-07-18_01-07-35','2025-07-18 01:07:35','diagnóstica','completada',NULL,NULL,1,'2025-07-18 01:07:35'),(17,2,1,'2025-07-18_01-08-22','2025-07-18 01:08:22','diagnóstica','en_curso',NULL,NULL,1,'2025-07-18 01:08:22'),(18,1,1,'2025-07-18_05-24-32','2025-07-18 05:24:32','diagnóstica','completada',NULL,NULL,1,'2025-07-18 05:24:32'),(19,1,1,'2025-07-18_09-48-30','2025-07-18 14:48:31','diagnóstica','completada',NULL,NULL,1,'2025-07-18 14:48:31'),(20,1,1,'2025-07-18_09-49-46','2025-07-18 14:49:46','diagnóstica','completada',NULL,NULL,1,'2025-07-18 14:49:46'),(21,1,1,'2025-07-18_09-51-42','2025-07-18 14:51:42','diagnóstica','en_curso',NULL,NULL,1,'2025-07-18 14:51:42'),(22,1,1,'2025-07-18_09-55-44','2025-07-18 14:55:44','diagnóstica','completada',NULL,NULL,1,'2025-07-18 14:55:44'),(23,1,1,'2025-07-18_14-14-41','2025-07-18 19:14:41','diagnóstica','completada',NULL,NULL,1,'2025-07-18 19:14:41'),(24,1,1,'2025-07-18_14-16-09','2025-07-18 19:16:09','diagnóstica','en_curso',NULL,NULL,1,'2025-07-18 19:16:09'),(25,1,4,'2025-07-18_14-44-56','2025-07-18 19:44:57','diagnóstica','en_curso',NULL,NULL,1,'2025-07-18 19:44:57'),(26,4,4,'2025-07-18_15-06-15','2025-07-18 20:06:15','diagnóstica','en_curso',NULL,NULL,1,'2025-07-18 20:06:15'),(27,1,4,'2025-08-01_10-37-36','2025-08-01 15:37:37','diagnóstica','completada',NULL,NULL,1,'2025-08-01 15:37:37'),(28,1,4,'2025-08-01_10-40-52','2025-08-01 15:40:52','diagnóstica','completada',NULL,NULL,1,'2025-08-01 15:40:52'),(29,1,1,'2025-08-01_11-20-05','2025-08-01 16:20:05','diagnóstica','completada',NULL,NULL,1,'2025-08-01 16:20:05'),(30,5,4,'2025-08-01_11-30-30','2025-08-01 16:30:30','diagnóstica','en_curso',NULL,NULL,1,'2025-08-01 16:30:30'),(31,1,1,'2025-08-01_11-33','2025-08-01 16:33:00','diagnóstica','completada',NULL,NULL,1,'2025-08-01 16:33:00');
/*!40000 ALTER TABLE `sesion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `cedula` varchar(20) DEFAULT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `apellido` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `password` text NOT NULL,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `activo` tinyint(1) DEFAULT '1',
  `id_rol` int DEFAULT NULL,
  `especialidad` text,
  `anos_experiencia` int DEFAULT NULL,
  `certificaciones` text,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `cedula` (`cedula`),
  UNIQUE KEY `email` (`email`),
  KEY `id_rol` (`id_rol`),
  KEY `idx_usuario_email` (`email`),
  KEY `idx_usuario_cedula` (`cedula`),
  CONSTRAINT `usuario_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `rol` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'0123456789','Admin','Sistema','admin@sistema.com','None','scrypt:32768:8:1$JuyLhyzU3tLXCCri$be8e30662ea0e008079232867de5049f4f5f6dadfd9afe767a27a676b3e91ffcf763fc6bf55518de56994683a30cf56ec8cf2d01cb4eaeaaeaee367ea4e91e05','2025-07-08 05:16:41',1,1,NULL,NULL,NULL),(2,'3333333333','stalin','Espinoza','stalin.espinoza@ucuenca.edu.ec','0989874391','pbkdf2:sha256:600000$0unA5dPhoepXSZKQ$485f9b340244ac0e4f6fe7022bbfe8205c7baf2302285bb5eeb80b4038938583','2025-07-08 05:44:22',1,2,'Psicologia Infantil',1,'tdaa'),(3,'4444444444','Pedro','Lopez','stalin2020espinoza@gmail.com','0989874392','pbkdf2:sha256:600000$vgoUN0FQbJVJUrsj$d92749286a4583fb06367debb2eab8a16c197049c0544b05843de6b499d7fca8','2025-07-09 06:43:02',0,3,NULL,NULL,NULL),(4,'0151075082','Rosa','Maldonado ','rosa.maldonado@ucuenca.edu.ec','0991031115','pbkdf2:sha256:600000$MKo2q0qzDHog4Bv5$f21aea5fafe3d52032f2f81f9a81691ee3e3574b2672b512aee3b1f79f06d31d','2025-07-18 17:08:05',1,2,'Psicología Infantil ',1,'TEA');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vista_evaluadores`
--

DROP TABLE IF EXISTS `vista_evaluadores`;
/*!50001 DROP VIEW IF EXISTS `vista_evaluadores`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_evaluadores` AS SELECT 
 1 AS `id_usuario`,
 1 AS `cedula`,
 1 AS `nombre_completo`,
 1 AS `email`,
 1 AS `telefono`,
 1 AS `especialidad`,
 1 AS `anos_experiencia`,
 1 AS `certificaciones`,
 1 AS `activo`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_ninos_completa`
--

DROP TABLE IF EXISTS `vista_ninos_completa`;
/*!50001 DROP VIEW IF EXISTS `vista_ninos_completa`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_ninos_completa` AS SELECT 
 1 AS `id_nino`,
 1 AS `codigo_nino`,
 1 AS `nombre`,
 1 AS `apellido`,
 1 AS `fecha_nacimiento`,
 1 AS `edad`,
 1 AS `nombre_genero`,
 1 AS `peso`,
 1 AS `altura`,
 1 AS `tutor_responsable`,
 1 AS `telefono_contacto`,
 1 AS `activo`,
 1 AS `condiciones`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_sesiones_completa`
--

DROP TABLE IF EXISTS `vista_sesiones_completa`;
/*!50001 DROP VIEW IF EXISTS `vista_sesiones_completa`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_sesiones_completa` AS SELECT 
 1 AS `id_sesion`,
 1 AS `session_id_firebase`,
 1 AS `codigo_nino`,
 1 AS `nombre_nino`,
 1 AS `nombre_evaluador`,
 1 AS `fecha_sesion`,
 1 AS `tipo_evaluacion`,
 1 AS `estado`,
 1 AS `sincronizado_firebase`*/;
SET character_set_client = @saved_cs_client;

--
-- Dumping events for database 'Proyecto_Escalera_Pared'
--

--
-- Dumping routines for database 'Proyecto_Escalera_Pared'
--

--
-- Final view structure for view `vista_evaluadores`
--

/*!50001 DROP VIEW IF EXISTS `vista_evaluadores`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Rosa`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_evaluadores` AS select `u`.`id_usuario` AS `id_usuario`,`u`.`cedula` AS `cedula`,concat(`u`.`nombre`,' ',`u`.`apellido`) AS `nombre_completo`,`u`.`email` AS `email`,`u`.`telefono` AS `telefono`,`u`.`especialidad` AS `especialidad`,`u`.`anos_experiencia` AS `anos_experiencia`,`u`.`certificaciones` AS `certificaciones`,`u`.`activo` AS `activo` from `usuario` `u` where ((`u`.`id_rol` = 2) and (`u`.`activo` = true)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_ninos_completa`
--

/*!50001 DROP VIEW IF EXISTS `vista_ninos_completa`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Rosa`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_ninos_completa` AS select `n`.`id_nino` AS `id_nino`,`n`.`codigo_nino` AS `codigo_nino`,`n`.`nombre` AS `nombre`,`n`.`apellido` AS `apellido`,`n`.`fecha_nacimiento` AS `fecha_nacimiento`,timestampdiff(YEAR,`n`.`fecha_nacimiento`,curdate()) AS `edad`,`g`.`nombre_genero` AS `nombre_genero`,`n`.`peso` AS `peso`,`n`.`altura` AS `altura`,`n`.`tutor_responsable` AS `tutor_responsable`,`n`.`telefono_contacto` AS `telefono_contacto`,`n`.`activo` AS `activo`,group_concat((case when (`nc`.`activo` = true) then `c`.`nombre_condicion` end) separator ', ') AS `condiciones` from (((`nino` `n` left join `genero` `g` on((`n`.`id_genero` = `g`.`id_genero`))) left join `nino_condicion` `nc` on((`n`.`id_nino` = `nc`.`id_nino`))) left join `condicion` `c` on((`nc`.`id_condicion` = `c`.`id_condicion`))) where (`n`.`activo` = true) group by `n`.`id_nino`,`n`.`codigo_nino`,`n`.`nombre`,`n`.`apellido`,`n`.`fecha_nacimiento`,`g`.`nombre_genero`,`n`.`peso`,`n`.`altura`,`n`.`tutor_responsable`,`n`.`telefono_contacto`,`n`.`activo` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_sesiones_completa`
--

/*!50001 DROP VIEW IF EXISTS `vista_sesiones_completa`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`Rosa`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_sesiones_completa` AS select `s`.`id_sesion` AS `id_sesion`,`s`.`session_id_firebase` AS `session_id_firebase`,`n`.`codigo_nino` AS `codigo_nino`,concat(`n`.`nombre`,' ',`n`.`apellido`) AS `nombre_nino`,concat(`u`.`nombre`,' ',`u`.`apellido`) AS `nombre_evaluador`,`s`.`fecha_sesion` AS `fecha_sesion`,`s`.`tipo_evaluacion` AS `tipo_evaluacion`,`s`.`estado` AS `estado`,`s`.`sincronizado_firebase` AS `sincronizado_firebase` from ((`sesion` `s` join `nino` `n` on((`s`.`id_nino` = `n`.`id_nino`))) join `usuario` `u` on((`s`.`id_usuario` = `u`.`id_usuario`))) order by `s`.`fecha_sesion` desc */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-07  7:10:19
