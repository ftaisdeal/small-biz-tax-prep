-- Sample queries for 1099 calculations and reporting

-- 1. Find all vendors who need 1099s for a specific year
-- SELECT * FROM v_1099_nec_report WHERE tax_year = 2024;

-- 2. Get total payments to a specific vendor for a tax year
-- SELECT vendor_name, SUM(ABS(amount)) as total_paid
-- FROM transactions t
-- JOIN vendors v ON t.vendor_id = v.id
-- WHERE v.vendor_name LIKE '%contractor_name%' 
--   AND t.tax_year = 2024 
--   AND t.is_1099_reportable = TRUE
--   AND t.amount < 0;

-- 3. Find vendors approaching the $600 threshold
-- SELECT v.vendor_name, SUM(ABS(t.amount)) as total_paid
-- FROM vendors v
-- JOIN transactions t ON v.id = t.vendor_id
-- WHERE t.is_1099_reportable = TRUE 
--   AND t.tax_year = 2024
--   AND t.amount < 0
-- GROUP BY v.id
-- HAVING total_paid >= 500 AND total_paid < 600;

-- 4. Monthly payment summary for a vendor
-- SELECT 
--     strftime('%Y-%m', t.transaction_date) as month,
--     SUM(ABS(t.amount)) as monthly_total
-- FROM transactions t
-- JOIN vendors v ON t.vendor_id = v.id
-- WHERE v.vendor_name = 'Contractor Name'
--   AND t.tax_year = 2024
--   AND t.is_1099_reportable = TRUE
--   AND t.amount < 0
-- GROUP BY month
-- ORDER BY month;

-- 5. Insert sample account (correct SQLite syntax)
-- INSERT INTO accounts (account_type, account_name) VALUES ('checking', 'B of A checking');

-- 6. Get all transactions for an account
-- SELECT t.*, v.vendor_name, c.name as category_name
-- FROM transactions t
-- LEFT JOIN vendors v ON t.vendor_id = v.id
-- LEFT JOIN transaction_categories tc ON t.id = tc.transaction_id
-- LEFT JOIN categories c ON tc.category_id = c.id
-- WHERE t.account_id = 1
-- ORDER BY t.transaction_date DESC;
