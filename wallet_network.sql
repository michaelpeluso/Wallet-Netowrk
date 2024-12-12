-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 11, 2024 at 09:35 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `wallet_network`
--

-- --------------------------------------------------------

--
-- Table structure for table `bank_account`
--

CREATE TABLE `bank_account` (
  `BankID` int(11) NOT NULL,
  `BANumber` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `elec_address`
--

CREATE TABLE `elec_address` (
  `Identifier` varchar(100) NOT NULL,
  `Verified` tinyint(1) NOT NULL,
  `Type` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `email_address`
--

CREATE TABLE `email_address` (
  `EmailAdd` varchar(100) NOT NULL,
  `SSN` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `request_transaction`
--

CREATE TABLE `request_transaction` (
  `RTid` int(11) NOT NULL,
  `Amount` decimal(10,2) NOT NULL,
  `Date_Time` datetime NOT NULL,
  `Memo` varchar(255) DEFAULT NULL,
  `SSN` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `send_transaction`
--

CREATE TABLE `send_transaction` (
  `STid` int(11) NOT NULL,
  `Identifier` varchar(100) NOT NULL,
  `I_DTime` datetime NOT NULL,
  `C_DTime` datetime NOT NULL,
  `Memo` varchar(255) DEFAULT NULL,
  `CReason` varchar(255) DEFAULT NULL,
  `CType` varchar(50) NOT NULL,
  `Amount` decimal(10,2) NOT NULL,
  `SSN` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `transaction_source`
--

CREATE TABLE `transaction_source` (
  `RTId` int(11) NOT NULL,
  `Identifier` varchar(100) NOT NULL,
  `Percentage` decimal(5,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `wallet_account`
--

CREATE TABLE `wallet_account` (
  `SSN` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `PhoneNo` varchar(15) NOT NULL,
  `Balance` decimal(10,2) NOT NULL,
  `BankID` int(11) DEFAULT NULL,
  `BANumber` varchar(50) DEFAULT NULL,
  `BAVerified` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bank_account`
--
ALTER TABLE `bank_account`
  ADD PRIMARY KEY (`BankID`,`BANumber`);

--
-- Indexes for table `elec_address`
--
ALTER TABLE `elec_address`
  ADD PRIMARY KEY (`Identifier`);

--
-- Indexes for table `email_address`
--
ALTER TABLE `email_address`
  ADD PRIMARY KEY (`EmailAdd`),
  ADD KEY `SSN` (`SSN`);

--
-- Indexes for table `request_transaction`
--
ALTER TABLE `request_transaction`
  ADD PRIMARY KEY (`RTid`),
  ADD KEY `SSN` (`SSN`);

--
-- Indexes for table `send_transaction`
--
ALTER TABLE `send_transaction`
  ADD PRIMARY KEY (`STid`),
  ADD KEY `Identifier` (`Identifier`),
  ADD KEY `SSN` (`SSN`);

--
-- Indexes for table `transaction_source`
--
ALTER TABLE `transaction_source`
  ADD PRIMARY KEY (`RTId`,`Identifier`),
  ADD KEY `Identifier` (`Identifier`);

--
-- Indexes for table `wallet_account`
--
ALTER TABLE `wallet_account`
  ADD PRIMARY KEY (`SSN`),
  ADD KEY `BankID` (`BankID`,`BANumber`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `email_address`
--
ALTER TABLE `email_address`
  ADD CONSTRAINT `email_address_ibfk_1` FOREIGN KEY (`SSN`) REFERENCES `wallet_account` (`SSN`);

--
-- Constraints for table `request_transaction`
--
ALTER TABLE `request_transaction`
  ADD CONSTRAINT `request_transaction_ibfk_1` FOREIGN KEY (`SSN`) REFERENCES `wallet_account` (`SSN`);

--
-- Constraints for table `send_transaction`
--
ALTER TABLE `send_transaction`
  ADD CONSTRAINT `send_transaction_ibfk_1` FOREIGN KEY (`Identifier`) REFERENCES `elec_address` (`Identifier`),
  ADD CONSTRAINT `send_transaction_ibfk_2` FOREIGN KEY (`SSN`) REFERENCES `wallet_account` (`SSN`);

--
-- Constraints for table `transaction_source`
--
ALTER TABLE `transaction_source`
  ADD CONSTRAINT `transaction_source_ibfk_1` FOREIGN KEY (`RTId`) REFERENCES `request_transaction` (`RTid`),
  ADD CONSTRAINT `transaction_source_ibfk_2` FOREIGN KEY (`Identifier`) REFERENCES `elec_address` (`Identifier`);

--
-- Constraints for table `wallet_account`
--
ALTER TABLE `wallet_account`
  ADD CONSTRAINT `wallet_account_ibfk_1` FOREIGN KEY (`BankID`,`BANumber`) REFERENCES `bank_account` (`BankID`, `BANumber`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
