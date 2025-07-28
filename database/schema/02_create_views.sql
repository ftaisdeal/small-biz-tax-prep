-- Create views for reporting and analysis

-- 1099 Summary View for easy reporting
CREATE VIEW v_1099_summary AS
SELECT 
    v.id as vendor_id,
    v.vendor_name,
    v.business_name,
    v.tax_id,
    t.tax_year,
    pt.box_number,
    pt.description as payment_type_description,
    pt.form_type,
    SUM(ABS(t.amount)) as total_amount,
    COUNT(t.id) as transaction_count
FROM vendors v
JOIN transactions t ON v.id = t.vendor_id
JOIN payment_types_1099 pt ON t.payment_type_1099_id = pt.id
WHERE t.is_1099_reportable = TRUE
  AND t.amount < 0  -- Only outgoing payments
GROUP BY v.id, t.tax_year, pt.id
HAVING total_amount >= 600; -- IRS threshold for 1099-NEC

-- Query to get 1099-NEC reportable amounts for a specific tax year
CREATE VIEW v_1099_nec_report AS
SELECT 
    v.vendor_name,
    v.business_name,
    v.tax_id,
    v.address_line1,
    v.address_line2,
    v.city,
    v.state,
    v.zip_code,
    t.tax_year,
    SUM(ABS(t.amount)) as box_1_amount -- Nonemployee compensation
FROM vendors v
JOIN transactions t ON v.id = t.vendor_id
JOIN payment_types_1099 pt ON t.payment_type_1099_id = pt.id
WHERE t.is_1099_reportable = TRUE
  AND pt.form_type = '1099-NEC'
  AND pt.box_number = '1'
  AND t.amount < 0
GROUP BY v.id, t.tax_year
HAVING box_1_amount >= 600
ORDER BY v.vendor_name, t.tax_year;
