# Executive Summary
---

- My goal for this project was to use machine learning in order to predict who the most valuable players would be in the upcoming 2020 fantasy football season
- Idea was to use a player's statistics in year $n$ as features for a predictive model that projects points scored in year $n + 1$
- Using a neural network, I was able to make projections that were on average about 50-60 points off from a player's true total for the following year
- After feeding the model 2019 data, I got projections for the 2020 season

# Background
---

After a series of glorious years in which I dominated my family fantasy football league (finishing 1st, 1st, and 2nd in consecutive years), I placed 8th (out of 10) during our most recent season.

Wishing to never relive this shame, I decided to make use of the 3 months I spent learning data science.

# Data Acquisition & Cleaning
---

The website [PFR](https://www.pro-football-reference.com) has individual player statistics for every NFL season dating back to 1970 ([2019](https://www.pro-football-reference.com/years/2019/fantasy.htm), [2018](https://www.pro-football-reference.com/years/2018/fantasy.htm), ...). I wrote a [Python script](./code/webscraping.py) to scrape for this data. Data cleaning involved:
- Handling over 100,000 missing entries
- Removing superfluous columns

# EDA
---

Since my primary focus was prediction rather than inference, I didn't spend much time doing EDA. I did, however, look at correlation heatmaps to view which features were most correlated with points scored by position. In addition, I looked at a boxplot to view the distribution of points scored by position, which confirmed the conventional wisdom of "always draft a RB in the 1st round."


# Modeling
---

I fitted both a LASSO model and a neural network to the data. The LASSO model got an $R^2$ score of around 0.5, confirming the feasibility of predicting a player's future output from his statistics in the most recent season. After that, I fit a sequential neural network that got an RMSE of about 50-60 fantasy points.

# Findings
---

- Although the RMSE of the neural network was reasonably good, the actual projections for 2020 look suspect
- In particular, the model seems to predict players to do exactly as good or as bad (relative to others at their position) as they did in 2019. This means that if you were the 4th ranked player at your position in 2019, the model has you ranked as roughly the 4th ranked player at your position for 2020
- This is not often the case in fantasy football, the model needs to account for overachievers and underperformers
- Model doesn't yet appear to be production ready