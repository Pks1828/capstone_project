# Capstone Project: Stock Market Analysis- A Mathematical and Visual approach

<p> This project can be used for understanding stock data analysis, and gain knowledge about technical indicators by visualizing them.  </p>

Setting up the Project
---

Dependencies:
  1. python (2.x or 3.x): <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>
  2. Django Framework <a href="https://www.djangoproject.com/">https://www.djangoproject.com/</a> 
    * install using `pip install Django`
  3. Numpy <a href="http://www.numpy.org/">http://www.numpy.org/</a>
    * install using `pip install numpy`
  4. MySQL: <a href="https://www.mysql.com/">https://www.mysql.com/</a>
  5. CanvasJS: <a href="http://canvasjs.com/">http://canvasjs.com/</a>
  6. jQuery (1.x): <a href="https://jquery.com/">https://jquery.com/</a>
  7. Bootstrap CSS: <a href="http://getbootstrap.com/">http://getbootstrap.com/</a>
    * Bootstrap Select: <a href="https://silviomoreto.github.io/bootstrap-select/">https://silviomoreto.github.io/bootstrap-select/</a>
    
Setting up Database:
  1. Login to MySQL
    * `mysql -u <username> -p -h <host>`
    * eg. on localhost you can do `mysql -u root -p`
    * eg. on some remote host with ip 172.15.16.1 can be done using `mysql -u root -p -h 172.15.16.1`
  2. Create database `stockdb`
    * `create database stockdb`
  3. Then logout and go to project folder. Source the `schema.sql` file by
    * `mysql -u <user> -p -h <host> < schema.sql`
 
Change DB Settings of Django Project:
  1. Open the file `CapstonProject/settings.py` and change the fields `USER`, `PASSWORD`, `HOST` (`PORT` if applicable) of variable `DATABASES`
    * Note: This step is very important as all other files refers to settings.py for database configuration
  2. run `python manage.py makemigrations`
  3. run `python manage.py migrate`
  
Setting up initial Data:
  1. Run `python download_data.py`
  2. Run `python populate_database_with_indexes.py`
  3. Run `populate_initial_data_sql.py`. It will generate a SQL File `queries_ohlc.sql`.
  4. Import the sql file `queries_ohlc.sql` buy running
    * `mysql -u <user> -p -h <host> < queries_ohlc.sql`
    * Note: This might take a while as the quantity of data is a lot.
 
 Daily Run
  1.  Set up a scheduler (Windows Sceduler in Windows, cron in UNIX based systems) to run `daily_data.py`
    * `python daily_data.py`
    * This updates the database with new data and finds top 10 stocks to BUY/SELL
    
Web Application
---

The Web application has four modules
  1. Report: It lets the user select a particular stock and generates financial charts, report and the **recommendation** for that stock.
  2. Top Picks: It shows the best stocks for BUY/SELL. The information is stored in database by `daily_data.py` which is discussed earlier.
  3. Performance: The recommendation algorithm was tested using 5 stocks and its performance on them was analyzed. This module shows the results of the testing in terms of Charts.
  4. Glossary: All the financial terms and technical indicator information is shown here.
    
<p> Recommendation Algorithm: The algorithm works on statistical analysis of historical prices </p>

<hr/>

##### Stock Selection
![alt tag](https://github.com/Pks1828/capstone_project/blob/master/screenshots/1_stock_select.png)

<hr/>
##### Stock Chart
![alt tag](https://github.com/Pks1828/capstone_project/blob/master/screenshots/2_stock_chart.png)
<hr/>

##### Stock Report
![alt tag](https://github.com/Pks1828/capstone_project/blob/master/screenshots/3_stock_report.png)
<hr/>

##### Top Picks
![alt tag](https://github.com/Pks1828/capstone_project/blob/master/screenshots/4_top_picks.png)
<hr/>

##### Performance
![alt tag](https://github.com/Pks1828/capstone_project/blob/master/screenshots/5_performance.png)
<hr/>

##### Glossary
![alt tag](https://github.com/Pks1828/capstone_project/blob/master/screenshots/6_glossary.png)

<hr/>
 
