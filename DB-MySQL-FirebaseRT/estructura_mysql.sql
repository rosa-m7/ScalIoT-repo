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

-- Dump completed on 2025-08-07  7:12:00
