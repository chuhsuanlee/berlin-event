# Document

This project includes two parts:
1. **berlin-event**:​​ Updating event information from three websites: ​[Deutsche Oper Berlin​](https://www.deutscheoperberlin.de/en_EN/calendar), [GORKI](https://gorki.de/en/programme)​ and [Berghain Berlin](http://berghain.de/events/)​. This part is programmed with python and docker.
2. **berlin-event-app**:​​ Web application built on Ruby on Rails for visitors to filter events based on three criteria: web source, date and event title.

Following are the process of deployment:
1. Change the directory to **berlin-event-app**, run `rails db:migrate​​`, this will initialize the database, create a new schema called ​**myapp_development**​​ in the localhost server and a table called ​**events​**.
2. Run the following SQL Script to make sure the default behavior of the column **created_at​​** and​ **updated_at**​​ remains the same in the update process.
  ```sql
  ALTER TABLE `myapp_development`.`events`
  CHANGE COLUMN `created_at` `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ,
  CHANGE COLUMN `updated_at` `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP ;
  ```
3. Since the first part of this project is dockerized, ​[Docker](https://docs.docker.com/install/)​ needs to be installed to run this
project.
4. Change the directory to ​**berlin-event​​**, run ​`make exec​​`. After it enters the bash terminal of this docker container, run ​`python main.py`​​. This will update event information from three websites sequentially.  
  
   This implementation uses some useful libraries:
   * [Beautiful Soup​](https://pypi.org/project/beautifulsoup4/) and ​[Selenium​](https://github.com/SeleniumHQ/docker-selenium/tree/master/StandaloneChrome) are used for scraping and parsing the html information from different websites.
   * [PyMySQL](https://pypi.org/project/PyMySQL/)​ and ​[SQLAlchemy​](https://pypi.org/project/SQLAlchemy/) are used for communicating with database, adding and updating event information.
5. Last but not least, change the directory to ​**berlin-event-app** again, run ​`rails server​​`. Navigate the browser to ​http://localhost:3000/​, you will see message like this

   **Hello, Berliners!**  
   Here are some ​[Berlin events](http://localhost:3000/events) you might be interested!  

   Click on ​​[Berlin events](http://localhost:3000/events)​ and start to search the events.
