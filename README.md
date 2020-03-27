# UFC-Prediction

Web scraper with Python Requests and BeautifulSoup for http://www.ufcstats.com/statistics/events/completed.

Inspiration from Rajeev Warrier @: https://www.kaggle.com/rajeevw/ufcdata 
 
## Project includes:
1. Re-scrape UFC statistics: **Event_Details_Scrape.ipynb, Event_Scrape.ipynb, Fighter Info Scrape.ipynb
2. Data cleaning & wrangling, feature engineering to generate relevant cumulative statistics: **Data Clean.ipynb
3. EDA & Modeling: **UFC Exploratory Analysis.ipynb, Model.ipynb
4. Fight Tracker for incoming predictions: **TBD


## File Dictionary:
1. event_level_data.csv: summary statistics from general event page (ie. http://www.ufcstats.com/event-details/53278852bcd91e11)
2. fight_details_batch{i}.csv {i, 1..6}: detailed match statistics (in batches to lessen load on web server)
3. fighter.csv: physical attributes of individual fighters
4. fights.csv: personal checkpoint (combining a., b., c.)
5. unformatted_final --> model_data.csv (ready-to-model data)
6. to_model.csv: includes additional (optional) feature engineering

## Data Notes:
1. 'avg' statistics are on total/10 minutes of cumulative match time
2. 'cum' statistics are cumulative, not including the current match (except when it is the first match, otherwise, it is a wasted observation of 0's)
3. Missing heights/weights/reaches imputed using linear regression of physical traits < ~5% data

## Models:
Logistic Regression, Random Forest Classifer, XGBoost
Deep Learning: basic Sequential MLP





