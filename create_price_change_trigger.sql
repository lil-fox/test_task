CREATE TABLE IF NOT EXISTS product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    price NUMERIC
);

CREATE OR REPLACE FUNCTION product_price_change_listener()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the 'price' field has changed
    IF TG_OP = 'INSERT' OR NEW.price <> OLD.price THEN
        -- Send a notification with the changed data
        PERFORM pg_notify('product_price_change', row_to_json(NEW)::text);
    END IF;
    RETURN NEW;
END;
$$
 LANGUAGE plpgsql;


CREATE TRIGGER product_add_trigger
AFTER INSERT ON product
FOR EACH ROW
EXECUTE FUNCTION product_price_change_listener();


CREATE TRIGGER product_price_change_trigger
BEFORE UPDATE OF price ON product
FOR EACH ROW
EXECUTE FUNCTION product_price_change_listener();