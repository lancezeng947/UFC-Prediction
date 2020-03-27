# UFC-Prediction

Web scraper with Python Requests and BeautifulSoup for http://www.ufcstats.com/statistics/events/completed.

Inspiration from Rajeev Warrier @: https://www.kaggle.com/rajeevw/ufcdata 
 
Project includes:
1. Re-scrape UFC statistics: **Event_Details_Scrape.ipynb, Event_Scrape.ipynb, Fighter Info Scrape.ipynb**
2. Data cleaning & wrangling, feature engineering to generate relevant cumulative statistics: **Data Clean.ipynb**
3. EDA & Modeling: **UFC Exploratory Analysis.ipynb, Model.ipynb**
4. Fight Tracker for incoming predictions: **TBD**

File Dictionary:
a. event_level_data.csv: summary statistics from general event page (ie. http://www.ufcstats.com/event-details/53278852bcd91e11)
b. fight_details_batch{i}.csv {i, 1..6}: detailed match statistics (in batches to lessen load on web server)
c. fighter.csv: physical attributes of individual fighters
d. fights.csv: personal checkpoint (combining a., b., c.)
e. unformatted_final --> model_data.csv (ready-to-model data)
f. to_model.csv: includes additional (optional) feature engineering









