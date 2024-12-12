-- Create the BANK_ACCOUNT table
CREATE TABLE BANK_ACCOUNT (
    BankID INT NOT NULL,
    BANumber VARCHAR(20) NOT NULL,
    Verified BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (BankID, BANumber) -- Composite Primary Key
);

-- Create the ELEC_ADDRESS table
CREATE TABLE ELEC_ADDRESS (
    Identifier VARCHAR(100) PRIMARY KEY, -- Central electronic address (email/phone)
    Verified BOOLEAN DEFAULT FALSE,
    Type ENUM('Email', 'Phone') NOT NULL
);

-- Create the WALLET_ACCOUNT table
CREATE TABLE WALLET_ACCOUNT (
    SSN VARCHAR(11) PRIMARY KEY, -- Unique identifier for wallet account
    Name VARCHAR(50) NOT NULL,
    PhoneNo VARCHAR(15) UNIQUE NOT NULL,
    Balance DECIMAL(10, 2) DEFAULT 0,
    BankID INT, -- Foreign key part of composite key
    BANumber VARCHAR(20), -- Foreign key part of composite key
    BAVerified BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (BankID, BANumber) REFERENCES BANK_ACCOUNT(BankID, BANumber),
    FOREIGN KEY (PhoneNo) REFERENCES ELEC_ADDRESS(Identifier)
);

-- Create the EMAIL_ADDRESS table
CREATE TABLE EMAIL_ADDRESS (
    EmailAdd VARCHAR(100) PRIMARY KEY, -- Email is the primary key
    SSN VARCHAR(11) NOT NULL, -- Foreign key to WALLET_ACCOUNT.SSN
    Verified BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (SSN) REFERENCES WALLET_ACCOUNT(SSN),
    FOREIGN KEY (EmailAdd) REFERENCES ELEC_ADDRESS(Identifier)
);

-- Create the SEND_TRANSACTION table
CREATE TABLE SEND_TRANSACTION (
    TId INT AUTO_INCREMENT PRIMARY KEY, -- Unique transaction ID
    Identifier VARCHAR(100) NOT NULL, -- Recipient's electronic address
    L_DTime DATETIME NOT NULL, -- Initiated timestamp
    C_DTime DATETIME, -- Completed timestamp
    Memo TEXT,
    CReason TEXT, -- Cancellation reason
    CType ENUM('Pending', 'Completed', 'Cancelled') NOT NULL, -- Transaction status
    Amount DECIMAL(10, 2) NOT NULL,
    SSN VARCHAR(11) NOT NULL, -- Sender's SSN
    FOREIGN KEY (Identifier) REFERENCES ELEC_ADDRESS(Identifier), -- Recipient reference
    FOREIGN KEY (SSN) REFERENCES WALLET_ACCOUNT(SSN) -- Sender reference
);

-- Create the REQUEST_TRANSACTION table
CREATE TABLE REQUEST_TRANSACTION (
    RId INT AUTO_INCREMENT PRIMARY KEY, -- Unique request ID
    Amount DECIMAL(10, 2) NOT NULL,
    DateTime DATETIME NOT NULL,
    Memo TEXT,
    SSN VARCHAR(11) NOT NULL, -- Requester's SSN
    FOREIGN KEY (SSN) REFERENCES WALLET_ACCOUNT(SSN)
);

-- Create the REQUEST_FROM table
CREATE TABLE REQUEST_FROM (
    RId INT NOT NULL, -- Request ID
    Identifier VARCHAR(100) NOT NULL, -- Recipient's electronic address
    PRIMARY KEY (RId, Identifier),
    FOREIGN KEY (RId) REFERENCES REQUEST_TRANSACTION(RId), -- Request reference
    FOREIGN KEY (Identifier) REFERENCES ELEC_ADDRESS(Identifier) -- Recipient reference
);


-- Queries

-- Insert sample data into BANK_ACCOUNT
INSERT INTO BANK_ACCOUNT (BankID, BANumber, Verified)
VALUES 
(1, '1234567890', TRUE),
(2, '9876543210', FALSE);

-- Insert sample data into ELEC_ADDRESS
INSERT INTO ELEC_ADDRESS (Identifier, Verified, Type)
VALUES 
('leonardo.dicaprio@example.com', TRUE, 'Email'),
('meryl.streep@example.com', TRUE, 'Email'),
('5551234567', TRUE, 'Phone'),
('5559876543', FALSE, 'Phone');

-- Insert sample data into WALLET_ACCOUNT
INSERT INTO WALLET_ACCOUNT (SSN, Name, PhoneNo, Balance, BankID, BANumber, BAVerified)
VALUES 
('123-45-6789', 'Leonardo DiCaprio', '5551234567', 1000.00, 1, '1234567890', TRUE),
('987-65-4321', 'Meryl Streep', '5559876543', 500.00, 2, '9876543210', FALSE);

-- Insert sample data into EMAIL_ADDRESS
INSERT INTO EMAIL_ADDRESS (EmailAdd, SSN, Verified)
VALUES 
('leonardo.dicaprio@example.com', '123-45-6789', TRUE),
('meryl.streep@example.com', '987-65-4321', TRUE);

-- Insert sample data into SEND_TRANSACTION
INSERT INTO SEND_TRANSACTION (Identifier, L_DTime, C_DTime, Memo, CReason, CType, Amount, SSN)
VALUES 
('meryl.streep@example.com', NOW(), NOW(), 'Payment for groceries', NULL, 'Completed', 100.00, '123-45-6789'),
('5559876543', NOW(), NULL, 'Lunch split', NULL, 'Pending', 50.00, '123-45-6789');

-- Insert sample data into REQUEST_TRANSACTION
INSERT INTO REQUEST_TRANSACTION (Amount, DateTime, Memo, SSN)
VALUES 
(200.00, NOW(), 'Utilities', '123-45-6789'),
(150.00, NOW(), 'Dinner', '987-65-4321');

-- Insert sample data into REQUEST_FROM
INSERT INTO REQUEST_FROM (RId, Identifier, Percentage)
VALUES 
(1, 'leonardo.dicaprio@example.com', 50.00),
(1, 'meryl.streep@example.com', 50.00),
(2, 'leonardo.dicaprio@example.com', 60.00),
(2, '5551234567', 40.00);
