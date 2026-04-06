# I-Team Pittsburgh Interview exercise

In 2026 I applied for the I-team Analytics Manager for the city of Pittsburgh. I-teams are funded by the Bloomberg Foundation and staffing is managed by John Hopkins University. I-team stands for "innovation team." The initiative partners with city governments around the world to foster innovation and data-driven initiatives. 

A key part of the interview process is a case study analysis. You are given a handful of census tract level estimates and asked to analyze and your county and provide policy recommentations. In the assignment they mention these columns are used in the Social Vulnerably Index. Figuring the name-drop in the description was not by accident, I replicated the SVI calculation methods on this variable subset. 

Final variables included and caluclated:
 - % of population below the 150% poverty level
 - % of the population is BIPOC
 - % of households without a car
 - % of households with overcrowding
 - Normalized Risk Score


### Distribution of variables across Allegheny County

<p align="left">
  <img src="./img/boxplot_details.png" width="400" height="300" />
  <img src="./img/population_boxplot.png" width="200" height="300"/>
</p>



### Highest Risk Score Tract Values
| Population Size | % Poverty | % BIPOC | % Carless | % Overcrowded | Risk Score |
| ----- | ----- | ----- | ----- | ----- | ----- |
| 1,380 | 73.04% | 99.13% | 76.56% | 2.40% | 100.00% |
| 2,996 | 59.78% | 67.22% | 33.67% | 8.80% | 87.74% |
| 458 | 78.82% | 82.31% | 48.10% | 0.00% | 75.10% |
| 1,574 | 50.44% | 85.71% | 43.12% | 2.90% | 73.15% |
| 2,093 | 44.96% | 98.42% | 31.75% | 3.50% | 72.74% |
| 2,177 | 62.61% | 94.17% | 40.94% | 0.00% | 71.07% |
| 1,951 | 54.43% | 88.36% | 38.27% | 2.10% | 70.80% |
| 4,188 | 44.03% | 59.50% | 30.74% | 6.10% | 68.72% |
| 1,561 | 41.26% | 95.45% | 52.26% | 0.00% | 67.34% |
| 3,505 | 51.36% | 91.18% | 41.44% | 0.00% | 66.92% |


### Mapping of High Risk Census Tracts Within Allegheny Counts

<p align="left">
  <img src="./img/cloropleth2.png" width="400" height="300" />
  <img src="./img/cloropleth5.png" width="400" height="300"/>
</p>

A cursery analysis shows that the high risk score is highly correlated with Poverty, BIPOC, and carless. Which is not surprising, as the three variables are highly correlated to each other. Another factor, given the nature of percentages, is smaller population tracts are swayed to have a bigger impact. 

|  | Correlation with Risk Score |
| :---- | ----- |
| % Poverty | 0.88 |
| % BIPOC | 0.88 |
| % Carless | 0.87 |
| % Overcrowded | 0.45 |

## Nieghborhoods represented in the top 10 high risk tracts
**Hill district**: Bedford Dwellings,Terrace Village, East Hills, Middle Hill <br>
**East End**: Larimer, Homewood South, Wilkinsburg <br>
**Noth Side**: Summer Hill/Northview Heights <br>
**Southside**: Knoxville

While the analysis is for all of Allegheny County, the top 10 tracts were either in or adjacent to the city of Pittsburgh. Four of the tracts are specifically in the Hill district.

## Recommendations
But recommendations? The Urban Redevelopment Authority of Pittsburgh(URA) along with the Hill Community Development Corps is heavily involved in the Hill District. The Greater Hill District Neighborhood Reinvestment Fund (GHDNRF) is already directed by community participation. Within the scope of a two hour exercise, my main thought was maintaining a strong network of social services *now* vs making suggestions for the Hill's future. The recent holes poked in Federal government's safety net leaves people experiencing poverty extremely vulnerable. The one small concrete recommendation I had is for 412 food rescue to put their free community fridges in high risk census tracts. I didn't see one in the Hill District. 

I wanted more data!