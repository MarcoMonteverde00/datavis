<link rel="stylesheet" href="style.css">

# CO2 emission per capita

```js
const data1 = await FileAttachment("./data/co2_2022.csv").csv();
const trimmed1 = data1.slice(0,20)

const data2 = await FileAttachment("./data/co2_2022_mean.csv").csv(); 
const trimmed2 = data2.slice(0,20)
```
<br /><br />

## Top 20 polluters in a single year

```js
display(  
  Plot.plot({
    marginBottom: 80,
    title: "CO2 emission per capita (tonnes per person) (2022)",
    x: {
      label: "Country",
      tickRotate: -30
    },
    y: {
      label: "CO₂ emissions",
      grid: true,
      percent: false
    },
    marks: [
      Plot.ruleY([0]),
      Plot.barY(trimmed1, {
        x: "Entity", 
        y: "Annual CO₂ emissions (per capita)", 
        sort: {x: "y", reverse: true}, 
        tip: {
          format: {
            y: (d) => `${d.toFixed(4)} tonnes/per`   
          }
        }
      })
    ]
  })
);
```
<br /><br /><br />

## Top 20 polluters in a decade

```js
display(  
  Plot.plot({
    marginBottom: 80,
    title: "Mean CO2 emission per capita (tonnes per person) (2012-2022)",
    x: {
      label: "Country",
      tickRotate: -30
    },
    y: {
      label: "CO₂ emissions",
      grid: true,
      percent: false
    },
    marks: [
      Plot.ruleY([0]),
      Plot.barY(trimmed2, {
        x: "Entity", 
        y: "Annual CO₂ emissions (per capita)", 
        sort: {x: "y", reverse: true}, 
        tip: {
          format: {
            y: (d) => `${d.toFixed(4)} tonnes/per`   
          }
        }
      })
    ]
  })
);
```

<br /><br /><br />

#  Country Comparison

## Simple Visualization

```js
const data3 = await FileAttachment("./data/co2_2022_stacked.csv").csv();
const data3_without_total = data3.slice(0,36)

display(
  Plot.plot({
    marginLeft: 90,
    //color: { scheme: "Dark2", legend: true},
    x: {label: "Emissions", percent: false},
    y: {label: "Continent"},
    color: {legend: true},
    marks: [
      Plot.barX(
        data3_without_total,
        {   
          x: "Annual CO₂ emissions (per capita)",
          fill: "Rank",
          y: "Continent",
          channels: {Country: 'Entity'},
          tip: {
            format: {
              x: (d) => `${d.toFixed(4)} tonnes/per`,  
              fill: false
            }
          }
        }
      ),
      Plot.ruleX([0])
    ]
  })
);

```
```js

display(
  Plot.plot(
    {
      marginLeft: 90,
      x: {label: "Emissions"},
      y: {label: "Continent"},
      color: {legend: true},
      marks: [
        Plot.barX(
          data3,
          {
            x: "Annual CO₂ emissions (per capita)",
            fx: "Rank",
            fill: "Rank",
            y: "Continent",
            channels: {Country: 'Entity'},
            tip: {
              format: {
                x: (d) => `${d.toFixed(4)} tonnes/per`,  
                fill: false,
                fx: false
              }
            }
          }
        )
      ]
    }
  )
  
);
```

