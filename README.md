# COVID-19
Some useful graph to see and understand how the novel Coronavirus is evolving around the World.
If you wish to add a Country open an [Issue](https://github.com/aster94/COVID-19/issues/new).

# Script
It is based on the database from the [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19). 

NOTE: The maintainers of the database are facing some problems so some data are not correctly updated for some countries, we all hope that it would be fixed.

# Graph
Updated at 2020-03-19 12:42:14.

## Asia
![](/graph/China.png)

![](/graph/Hubei.png)

![](/graph/Zhejiang.png)

![](/graph/South%20Korea.png)

![](/graph/Thailand.png)

![](/graph/Japan.png)

![](/graph/Taiwan.png)

![](/graph/Macau.png)

![](/graph/Singapore.png)

![](/graph/Vietnam.png)

![](/graph/Nepal.png)

![](/graph/India.png)

![](/graph/Bangladesh.png)

![](/graph/Hong%20Kong.png)

![](/graph/Iran.png)

![](/graph/Iraq.png)

![](/graph/Saudi%20Arabia.png)

![](/graph/Russia.png)

## Europe
![](/graph/Italy.png)

![](/graph/France.png)

![](/graph/Spain.png)

![](/graph/Iceland.png)

![](/graph/Germany.png)

![](/graph/UK.png)

![](/graph/Finland.png)

![](/graph/Sweden.png)

![](/graph/Belgium.png)

## Americas
![](/graph/US.png)

![](/graph/Washington.png)

![](/graph/Canada.png)

![](/graph/Argentina.png)

![](/graph/Cambodia.png)

![](/graph/Peru.png)

## Australia
![](/graph/Australia.png)

## Africa
![](/graph/Egypt.png)

# Score
Also I made a *dirty* attempt to create a "score" to measure how well a country is responding to the COVID emergency (the highter the better):

![](/graph/China_score.png)

![](/graph/Italy_score.png)

Basically the score is: `(daily recovered / all positives) / ((daily confirmed / (population of the country / 10000)) * (daily deaths / all positives))`
