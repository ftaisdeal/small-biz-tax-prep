-- Insert reference data

-- Insert common 1099 payment types
INSERT INTO payment_types_1099 (box_number, description, form_type) VALUES
('1', 'Nonemployee Compensation', '1099-NEC'),
('1', 'Rents', '1099-MISC'),
('2', 'Royalties', '1099-MISC'),
('3', 'Other Income', '1099-MISC'),
('4', 'Federal Income Tax Withheld', '1099-MISC'),
('5', 'Fishing Boat Proceeds', '1099-MISC'),
('6', 'Medical and Health Care Payments', '1099-MISC'),
('7', 'Nonemployee Compensation (prior to 2020)', '1099-MISC'),
('8', 'Substitute Payments in Lieu of Dividends or Interest', '1099-MISC'),
('10', 'Crop Insurance Proceeds', '1099-MISC'),
('14', 'Gross Proceeds Paid to an Attorney', '1099-MISC');
