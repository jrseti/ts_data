# ts_data
A Python package for accessing Tradestation data

## Ramblings before I start creating this code...

This package is an attempt to create a simple method to provide Tradestation data to any strategy code. The goal is to be able to eventually write trading strategy functions in Python without having to worry about where the data is coming from or how it is coming into the system. 

This package allows us to specify the stock tickers we are interested in, and the one-minute bars are received and automatically pushed to a redis stream. Also, other Tradestation info will also be available with simple calls to functions to retrieve account info, stock ticker info, positions, etc.

This is a work in progress. The goal is to make this available via pip install. I created the ts_auth0 package to facilitate easy Tradestation authentication and it turned out to be really useful to have that part of the Tradestation process be available via a simple "pip install ts_auth0". I never have to think about the details of authentication again.


