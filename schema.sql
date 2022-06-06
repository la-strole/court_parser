CREATE TABLE courts
(
court_name TEXT NOT NULL,
id INTEGER NOT NULL UNIQUE,
full_name TEXT NOT NULL,
article TEXT NOT NULL,
judge_full_name TEXT,
date_adoption TEXT,
decision_date TEXT,
effective_date TEXT,
judicial_act TEXT,
date_update TEXT NOT NULL
);