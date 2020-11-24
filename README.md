# A simple web scraper

This simple Python script shows how webscraping works.  
A counter starts counting up from 1 and for each number calls
a single webpage from city-data.com containing the location of
Starbucks cafes in Los Angeles. There are several pages so the 
scraper goes through the pages until there are no more and it receives
no response or an error.

The scraped data is then processed to extract the portion that contains
the actual locations. They are cleaned and transfered to a Pandas dataframe
that is then written to a csv-file.
