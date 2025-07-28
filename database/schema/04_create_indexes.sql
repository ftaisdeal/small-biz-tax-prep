-- Create indexes for performance optimization

CREATE INDEX idx_vendors_tax_id ON vendors(tax_id);
CREATE INDEX idx_vendors_requires_1099 ON vendors(requires_1099);
CREATE INDEX idx_transactions_vendor_id ON transactions(vendor_id);
CREATE INDEX idx_transactions_1099_reportable ON transactions(is_1099_reportable);
CREATE INDEX idx_transactions_tax_year ON transactions(tax_year);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_account_id ON transactions(account_id);
CREATE INDEX idx_transaction_categories_transaction_id ON transaction_categories(transaction_id);
CREATE INDEX idx_transaction_categories_category_id ON transaction_categories(category_id);
