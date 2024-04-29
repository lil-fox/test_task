CREATE OR REPLACE FUNCTION notify_price_change()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if the cost was actually changed
    IF OLD.price <> NEW.price THEN
        perform pg_notify('notify_price_change', '' || NEW.title || '-' || NEW.price);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Now, create the trigger on the products table
CREATE TRIGGER product_price_changed_trigger
AFTER UPDATE OF price ON product
FOR EACH ROW EXECUTE FUNCTION notify_price_change();