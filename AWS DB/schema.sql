CREATE TABLE cryptocurrency (
    type            VARCHAR(256),
    date            DATE,
    closing_price   FLOAT(53),
    opening_price   FLOAT(53),
    highest_price   FLOAT(53),
    lowest_price    FLOAT(53),
    volume          FLOAT(53),
    change          FLOAT(53),
    primary key (type, date),
    check (
        closing_price   >= 0  AND
        opening_price   >= 0  AND
        highest_price   >= 0  AND
        lowest_price    >= 0  AND
        volume          >= 0
    )
);