CREATE TABLE private_school_dma(
   term VARCHAR(75),
   dma VARCHAR(75),
   search_date DATE,
   interest decimal(4,1) CHECK(interest BETWEEN 0 AND 100),
   CONSTRAINT private_school_dma_con PRIMARY KEY (term, dma, search_date)
);

CREATE TABLE private_school_state(
   term VARCHAR(75),
   state_var VARCHAR(75),
   search_date DATE,
   interest decimal(4,1) CHECK(interest BETWEEN 0 AND 100),
   CONSTRAINT private_school_state_con PRIMARY KEY (term, state_var, search_date)
);

CREATE TABLE home_school_dma(
   term VARCHAR(75),
   dma VARCHAR(75),
   search_date DATE,
   interest decimal(4,1) CHECK(interest BETWEEN 0 AND 100),
   CONSTRAINT home_school_dma_con PRIMARY KEY (term, dma, search_date)
);

CREATE TABLE home_school_state(
   term VARCHAR(75),
   state_var VARCHAR(75),
   search_date DATE,
   interest decimal(4,1) CHECK(interest BETWEEN 0 AND 100),
   CONSTRAINT home_school_state_con PRIMARY KEY (term, state_var, search_date)
)