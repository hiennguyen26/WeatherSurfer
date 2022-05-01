# WeatherSurfer
Gamified Weather Prediction with AI

This project's objective was to help people understand the rising global temperatures and future harsh weather occurences by playing a game.
The game includes various enemy obstacles that are representative of various weather types.   
For example:
- Rainy days spawn rain mobs, which displaces the user slightly randomly to the left or right.
- Snowy days spawn snow mobs, which slows the user down significantly.
- Hot days spawn fire mobs, which damages the user health. 
- Windy days spawn wind mobs, which displaces the user by a lot in the opposite direction.  
- Sky clear days spawn carrots, which the user can eat to regain health. 

Mobs are spawned in the order of days foward in the future calendar. Initally, 7 years of Boston weather data was preprocessed, cleaned and weather descriptions were numericalized into 5 categories. Neural Prophet was used to predict 7 years of future weather data for each weather data point, such as: wind degree, temperature, dew point, feels like, minimum and maximum temperature, humidity, wind gust, etc. These data points are then used to train via Logistic Regression models, SVM and KNN classifiers to predict the numerical weather descriptions. The predicted numerical weather descriptions are then used in the game to bring gamified experience.

