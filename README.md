# CRYPTO PORTFOLIO APP


![appearence of main page][1]



#### Description:

This app this app was created for my Harvard's cs50 final project.

With this application, I wanted to create a website where users can create 
their own cryptocurrency portfolios and trade, 
and get a breakdown of their previous trading transactions. 

***I got help from the videos of algovibes youtube channel while developing this application***


![login][2]  ![register][3]


**crypto.py**: List the best known cryptocurrencies and prices from binance app. It transforms the incoming information into a pandas dataframe using the symbol, interval and lookback selected by the user. I plan to add advanced technical indicators to the charts in later versions of this application.

**app.py**: The main flask app that using flask routes and self created decorators to manage transition between pages and information transfer. Using flask-sqlalchemy to save user information, wallet information and purchase-sale information to the database, to update and select informations from database. While the user is registering and logging in, the password information is encrypted and stored for security purposes.If the user is not logged in, the page information is not displayed to the user so after logging out, the security of the information is ensured.

**style.css**: Css settings the other than bootstrap. And some changes are set in html files using style tags.


![apperance of main page][4]


**chart page**: After logging in it takes the information with the choices of the user, brings up-to-date information about the desired symbols and date range and shows it to the user as a chart. This chart has a dynamic structure(use Chart.js module in between html script tags ), so when the user comes to a date on the chart, information is displayed and the user can add and remove any indicator they want from the chart.


![chart][6]


**quote page**: After logging in it offers the possibility to add or withdraw money to your existing account. It allows him to see his current wallet as a table and buy and sell any symbol he wants.


![apperance of main page][4]


**history page**: After logging in it displays the historical transaction records as a table and allows the user to print them if desired.


![history page][5]

[1]: https://raw.githubusercontent.com/ondersabahat/cs50_Final_Project-Crypto-App/master/static/images/screenshots/homePage.png
[2]: https://raw.githubusercontent.com/ondersabahat/cs50_Final_Project-Crypto-App/master/static/images/screenshots/login.png
[3]: https://raw.githubusercontent.com/ondersabahat/cs50_Final_Project-Crypto-App/master/static/images/screenshots/register.png
[4]: https://raw.githubusercontent.com/ondersabahat/cs50_Final_Project-Crypto-App/master/static/images/screenshots/mainPage2.png
[5]: https://raw.githubusercontent.com/ondersabahat/cs50_Final_Project-Crypto-App/master/static/images/screenshots/history.png
[6]: https://raw.githubusercontent.com/ondersabahat/cs50_Final_Project-Crypto-App/master/static/images/screenshots/chart.png
