-- Create tables for expense tracking and 1099 reporting

-- Accounts table
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_type VARCHAR(20) NOT NULL,
    account_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Categories table for expense categorization
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    parent_category_id INTEGER,
    FOREIGN KEY (parent_category_id) REFERENCES categories(id)
);

-- Vendors/Contractors table for 1099 tracking
CREATE TABLE vendors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vendor_name VARCHAR(255) NOT NULL,
    business_name VARCHAR(255),
    tax_id VARCHAR(20), -- SSN or EIN
    address_line1 VARCHAR(255),
    address_line2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip_code VARCHAR(20),
    email VARCHAR(255),
    phone VARCHAR(20),
    requires_1099 BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 1099 Payment Types table
CREATE TABLE payment_types_1099 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    box_number VARCHAR(10) NOT NULL, -- e.g., '1', '2', '3', '7'
    description VARCHAR(255) NOT NULL, -- e.g., 'Nonemployee Compensation', 'Rent'
    form_type VARCHAR(20) DEFAULT '1099-NEC' -- 1099-NEC, 1099-MISC, etc.
);

-- Transactions table with all fields including 1099 tracking
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER NOT NULL,
    transaction_date DATE NOT NULL,
    reference_number VARCHAR(50),
    payee_description TEXT,
    address_info VARCHAR(255),
    amount DECIMAL(10, 2) NOT NULL,
    vendor_id INTEGER,
    payment_type_1099_id INTEGER,
    is_1099_reportable BOOLEAN DEFAULT FALSE,
    tax_year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(id),
    FOREIGN KEY (vendor_id) REFERENCES vendors(id),
    FOREIGN KEY (payment_type_1099_id) REFERENCES payment_types_1099(id)
);

-- Transaction categories junction table
CREATE TABLE transaction_categories (
    transaction_id INTEGER,
    category_id INTEGER,
    PRIMARY KEY (transaction_id, category_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
