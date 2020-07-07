COPY private_school_dma FROM 'MYPATH\Google_Trends_Scrubber\Data\googletrends_private school_dma.csv'
DELIMITER ',' CSV HEADER;

COPY private_school_state FROM 'MYPATH\Google_Trends_Scrubber\Data\googletrends_private school_state.csv'
DELIMITER ',' CSV HEADER;

COPY home_school_dma FROM 'MYPATH\Google_Trends_Scrubber\Data\googletrends_home school_dma.csv'
DELIMITER ',' CSV HEADER;

COPY home_school_state FROM 'MYPATH\Google_Trends_Scrubber\Data\googletrends_home school_state.csv'
DELIMITER ',' CSV HEADER;
