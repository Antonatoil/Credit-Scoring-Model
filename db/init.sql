create table if not exists prediction_logs (
    id bigserial primary key,
    created_at timestamp not null default current_timestamp,
    probability_default double precision not null,
    predicted_class integer not null,
    threshold double precision not null,
    risk_level varchar(32) not null,
    payload_json text not null
);