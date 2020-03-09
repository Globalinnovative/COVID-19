# COVID-19
Some useful graph to see how the situation of the novel coronavirus is evolving around the World

# Script
It is based on the database from the [Johns Hopkins University](https://github.com/CSSEGISandData/COVID-19)

# Graph
### Europe
![Italy](/graph/Italy.png)
![France](/graph/France.png)

### China
![China](/graph/China.png)
![Hubei](/graph/Hubei.png)
![Zhejiang](/graph/Zhejiang.png)

### United States
![US](/graph/US.png)

### Canada
![Canada](/graph/Canada.png)
![Toronto](/graph/Toronto.png)

### Australia
![Australia](/graph/Australia.png)

### Other
![Iran](/graph/Iran.png)
![South Korea](/graph/South Korea.png)

## Score
Also i made a *dirty* attempt to create a "score" to measure how well a country is responding to the COVID emergency (the highter the better):
![China Score](/graph/China_score.png)
![Italy Score](/graph/Italy_score.png)
Basically the score is: `(daily recovered / all positives) / ((daily confirmed / (population of the country / 10000)) * (daily deaths / all positives))`
