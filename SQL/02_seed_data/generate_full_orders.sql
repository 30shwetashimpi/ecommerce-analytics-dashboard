USE ecommerce_analytics2;

-- =========================
-- 1. EXTEND DATES (May 1 → July 31, 2023)
-- =========================
-- Keep your existing INSERT IGNORE INTO dates_dim… code here
-- (your previous block for dates_dim is fine)

-- =========================
-- 2. GENERATE RANDOM ORDERS PER CUSTOMER
-- =========================
DELIMITER $$

CREATE PROCEDURE generate_orders2()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE c_id INT;
    DECLARE d_id DATE;
    DECLARE total_amt DECIMAL(10,2);
    DECLARE p_id INT;
    DECLARE qty INT;
    DECLARE new_order_id INT;

    DECLARE cust_cursor CURSOR FOR SELECT customer_id FROM customers_dim;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cust_cursor;

    read_loop: LOOP
        FETCH cust_cursor INTO c_id;
        IF done THEN
            LEAVE read_loop;
        END IF;

        SET @x = 1;
        WHILE @x <= 20 DO  -- 20 orders per customer
            -- random date
            SELECT date_id INTO d_id FROM dates_dim ORDER BY RAND() LIMIT 1;

            -- random total
            SET total_amt = ROUND(200 + RAND()*1500,2);

            -- insert order and capture ID
            INSERT INTO orders_fact (customer_id, order_date, order_status, total_amount)
            VALUES (c_id, d_id, 'Delivered', total_amt);

            SET new_order_id = LAST_INSERT_ID();

            -- insert 1–3 random order items
            SET @y = 1;
            WHILE @y <= FLOOR(1 + RAND()*3) DO
                -- select random product
                SELECT product_id INTO p_id FROM products_dim ORDER BY RAND() LIMIT 1;
                SET qty = FLOOR(1 + RAND()*3);

                INSERT INTO order_items_fact (order_id, product_id, quantity, item_price)
                VALUES (new_order_id, p_id, qty, (SELECT price FROM products_dim WHERE product_id = p_id));

                SET @y = @y + 1;
            END WHILE;

            -- insert payment linked to the order
            INSERT INTO payment_fact (order_id, payment_date, payment_method, payment_amount)
            VALUES (new_order_id, d_id, IF(RAND() > 0.5,'UPI','Credit Card'), total_amt);

            SET @x = @x + 1;
        END WHILE;

    END LOOP;

    CLOSE cust_cursor;
END$$

DELIMITER ;

-- =========================
-- 3. RUN PROCEDURE
-- =========================
CALL generate_orders2();

-- =========================
-- 4. CLEANUP
-- =========================
DROP PROCEDURE generate_orders2;

-- =========================
-- 5. VERIFY DATA
-- =========================
SELECT COUNT(*) AS total_orders FROM orders_fact;
SELECT COUNT(*) AS total_order_items FROM order_items_fact;
SELECT COUNT(*) AS total_payments FROM payment_fact;

SELECT * FROM orders_fact ORDER BY order_id DESC LIMIT 20;
SELECT * FROM order_items_fact ORDER BY order_item_id DESC LIMIT 20;
SELECT * FROM payment_fact ORDER BY payment_id DESC LIMIT 20;
