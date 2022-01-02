

CREATE TABLE post (
    id              SERIAL      PRIMARY KEY,
    name            VARCHAR     NOT NULL,
    content         TEXT        NOT NULL,
    time            TIMESTAMP   NOT NULL
);


CREATE TABLE comment (
    id              SERIAL      PRIMARY KEY,
    post_id         INT         NOT NULL    REFERENCES post(id),
    name            VARCHAR     NOT NULL,
    message         TEXT        NOT NULL,
    time            TIMESTAMP   NOT NULL
);

