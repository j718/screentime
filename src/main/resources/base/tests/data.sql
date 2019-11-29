INSERT INTO app (title)
VALUES
    ('Calendar'),
    ('Hyper');

INSERT INTO limit_group (title, time_limit)
VALUES
    ('Productivity', 1),
    ('Code', 0);


INSERT INTO limit_item(app_id, limit_group_id)
VALUES
    (1, 1),
    (2, 1),
    (2, 2);
