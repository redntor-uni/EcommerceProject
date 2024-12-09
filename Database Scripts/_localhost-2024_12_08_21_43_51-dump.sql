-- MySQL dump 10.13  Distrib 8.3.0, for macos14 (arm64)
--
-- Host: 127.0.0.1    Database: Pathfinders
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Carts`
--

DROP TABLE IF EXISTS `Carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Carts` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `ItemID` int NOT NULL,
  `Quantity` int NOT NULL,
  `Total` decimal(10,2) NOT NULL,
  `Status` varchar(20) DEFAULT NULL,
  `OrderID` int DEFAULT NULL,
  `ItemPrice` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Carts`
--

LOCK TABLES `Carts` WRITE;
/*!40000 ALTER TABLE `Carts` DISABLE KEYS */;
INSERT INTO `Carts` VALUES (17,2,2,3,660.00,'Completed',29,220.00),(18,2,4,5,900.00,'Completed',29,180.00),(19,2,5,1,150.00,'Active',NULL,150.00);
/*!40000 ALTER TABLE `Carts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Contact`
--

DROP TABLE IF EXISTS `Contact`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Contact` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Email` varchar(100) DEFAULT NULL,
  `Message` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Contact`
--

LOCK TABLES `Contact` WRITE;
/*!40000 ALTER TABLE `Contact` DISABLE KEYS */;
/*!40000 ALTER TABLE `Contact` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Orders` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `UserID` int NOT NULL,
  `OrderTotal` decimal(10,2) DEFAULT NULL,
  `OrderDate` date DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
INSERT INTO `Orders` VALUES (29,2,1560.00,'2024-12-04');
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Products`
--

DROP TABLE IF EXISTS `Products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Products` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(100) NOT NULL,
  `Description` varchar(250) DEFAULT NULL,
  `Price` decimal(20,2) NOT NULL,
  `Img` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Products`
--

LOCK TABLES `Products` WRITE;
/*!40000 ALTER TABLE `Products` DISABLE KEYS */;
INSERT INTO `Products` VALUES (1,'Nike Air Jordan Retro','The Nike Air Jordan Retro is more than just a sneaker—it\'s an icon. Combining legendary style with modern comfort, these retros pay homage to the original AJ1 design while delivering top-tier performance and durability. Whether you\'re on the court or',310.00,'https://m.media-amazon.com/images/I/51HY1980WNL._AC_SX500_.jpg'),(2,'Nike BB Adapt','The Nike BB Adapt is the future of performance footwear. Equipped with power lacing technology, these sneakers automatically adjust for a customized, secure fit, giving you ultimate comfort and support. Designed for athletes who demand speed and prec',220.00,'https://m.media-amazon.com/images/I/71iTHVTtD+L._AC_SX679_.jpg'),(3,'Nike Air Zoom Pegasus 38','The Nike Air Zoom Pegasus 38 is your go-to running shoe for all-around comfort and performance. Featuring a responsive Zoom Air unit and a breathable mesh upper, it offers a smooth, cushioned ride with every step. Whether you\'re training for a race o',120.00,'https://m.media-amazon.com/images/I/71PWUoL+4qL._AC_SX500_.jpg'),(4,'Nike Nike ZoomX Invincible Run','The Nike ZoomX Invincible Run is built for runners who demand ultimate cushioning and energy return. With a full-length ZoomX foam midsole, it provides a plush, soft ride without sacrificing responsiveness. The lightweight design and breathable upper',180.00,'https://m.media-amazon.com/images/I/71NDLBxr48L._AC_SY500_.jpg'),(5,'Nike Flyknit Trainer','The Nike Flyknit Trainer is the perfect blend of lightweight performance and premium support. Featuring a seamless, breathable Flyknit upper, it wraps your foot like a sock for a snug, adaptive fit. The responsive midsole and durable rubber outsole o',150.00,'https://m.media-amazon.com/images/I/51afR1vPRuL._AC_SY500_.jpg'),(6,'Nike React Infinity Run Flyknit','The Nike React Infinity Run Flyknit is designed to keep you running longer and safer. With a soft, responsive React foam midsole, it provides maximum cushioning and energy return with every stride. The Flyknit upper delivers a snug, breathable fit, w',160.00,'https://m.media-amazon.com/images/I/61PmvuXo66L._AC_SY500_.jpg'),(7,'Nike Blazer Mid \'77','The Nike Blazer Mid \'77 combines retro style with modern comfort. Inspired by classic basketball design, its sleek leather and suede upper offers durability and a timeless look, while the padded collar ensures a supportive fit. With a rubber outsole ',100.00,'https://m.media-amazon.com/images/I/71Zfz8GIcgL._AC_SX500_.jpg'),(8,'Nike Air Max \'97','The Nike Air Max \'97 is a true icon, blending cutting-edge style with comfort and performance. Featuring the signature full-length visible Air cushioning, it delivers a smooth, responsive ride with every step. The sleek, futuristic design and reflect',170.00,'https://m.media-amazon.com/images/I/61BoBHIEznL._AC_SY675_.jpg'),(9,'Nike Free RN 5.0','The Nike Free RN 5.0 is designed for those who crave a natural, flexible feel with every step. With its lightweight, minimalist construction and flexible sole, it allows your foot to move more freely, simulating the feeling of running barefoot. The b',100.00,'https://m.media-amazon.com/images/I/81nadvAWG+L._AC_SX500_.jpg'),(10,'Nike KD13','The Nike KD13 is built for players who want to dominate with speed, agility, and precision. Featuring a responsive Zoom Air unit in the forefoot and heel, it delivers exceptional cushioning and energy return for quick cuts and explosive moves. The br',150.00,'https://m.media-amazon.com/images/I/51a8BvhkYIL._AC_SX500_.jpg');
/*!40000 ALTER TABLE `Products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `User` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Email` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'admin','admin','admin@pathfinders.com'),(2,'Justin','herbert','justin@pathfinders.com');
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-08 21:43:51
