# Is The Greenbelt Dry?

The Greenbelt is a park in Austin, TX. One of the more fun things you can do there is climb! This project aims to use weather information form weather stations around Austin to predict if the Greenbelt is dry enough to enjoy climbing.
Check out www.isthegreenbeltdry.com

## Steps to run locally

1. Set environment variable `WEATHER_API_KEY` to the api key for https://www.wunderground.com/
1. Install all the deps listed in `requirements.txt`
1. Run the app using gunicorn

```
$  gunicorn is_the_greenbelt_dry.app:app --log-file -
```
