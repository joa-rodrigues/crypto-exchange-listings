<div id="top"></div>


<br />
<div align="center">
  <h3 align="center">Crypto Exchange Listings</h3>
</div>



<!-- ABOUT THE PROJECT -->

## About The Project
Receive alerts in a Telegram bot as soon as a new crypto is listed in Coinbase.

The script is working on a raspberry 4 where i installed mongo.

### Built With
* [scrapy](https://scrapy.org/)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->

## Getting Started

Create a Telegram bot. A good starting point link : 

* [telegram bot](https://www.youtube.com/watch?v=67SH6tCuyLQ)

Install a mongo server :

* [mongo](https://www.mongodb.com/developer/how-to/mongodb-on-raspberry-pi/)



### Installation PyCharm

Create a pipenv environment 

![Run in pyCharm](documentation/images/python_interpreter.png)
![Run in pyCharm](documentation/images/add_new_interpreper.png)
![Run in pyCharm](documentation/images/plus_button.png)
![Run in pyCharm](documentation/images/pipenv.png)

Then in a terminal :

`cd crypto-exchange-listings`

`pipenv install -r requirements.txt`


## Usage

### Run with PyCharm

Click on Edit configurations

![Run in pyCharm](documentation/images/edit_configuration.png)


Click the `+` button end then `Add new configuration` and select `python`

![Run in pyCharm](documentation/images/add_new_configuration.png)

 
Then fill run parameters :

![Run in pyCharm](documentation/images/run_config.png)

### Raspberry conf

copy `settings.py.sample` to `settings.py`
Set : `MONGO_SERVER` and `TELEGRAM_BOT` variables.

There is a script `runner.sh` that will trigger the job. 
Just add a cron that will schedulle de job : 

`0,5,10,15,20,25,30,35,40,45,50,55 * * * * /media/usbdrive/dev/crypto-exchange-listings/exchange-scrappers/runner.sh >> /var/log/crypto-exchange-listings.log`

