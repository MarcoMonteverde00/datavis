<link rel="stylesheet" href="style.css">

<div class="hero">
  <h1>CO2 emission per capita</h1>
</div>

```js

function colorScale(value, min, max) {
  const ratio = (value - min) / (max - min);
  const r = 255; 
  const g = Math.floor(255 * (1-ratio)); 
  const b = 0;
  return `rgb(${r}, ${g}, ${b})`;
}

const data1 = await FileAttachment("./data/co2_2022.csv").csv();
const trimmed1 = data1.slice(0,20)

const values1 = data1.map(d => d["Annual CO₂ emissions (per capita)"]);
const min1 = Math.min(...values1);
const max1 = Math.max(...values1);

```
<br /><br />

#

# Top 20 polluters in a year

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
        fill: d => colorScale(d["Annual CO₂ emissions (per capita)"], min1, max1),
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

# Top 20 polluters in a decade

```js

const data2 = await FileAttachment("./data/co2_2022_mean.csv").csv(); 
const trimmed2 = data2.slice(0,20)

const values2 = data2.map(d => d["Annual CO₂ emissions (per capita)"]);
const min2 = Math.min(...values2);
const max2 = Math.max(...values2);


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
        fill: d => colorScale(d["Annual CO₂ emissions (per capita)"], min2, max2),
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

# Continents Comparison

```js
const data3 = await FileAttachment("./data/co2_2022_stacked.csv").csv();
const data3_without_total = data3.slice(0,36)

display(
  Plot.plot({
    marginLeft: 90,
    width: 900,
    height: 360,
    title: "CO2 emission per capita in each Region (tonnes per person) (2022)",
    //color: { scheme: "Dark2", legend: true},
    x: {label: "Emissions", percent: false},
    y: {label: "Continent", padding: 0.2},
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
      width: 900,
      height: 360,
      title: "CO2 emission per capita in each Region (tonnes per person) (2022)",
      x: {label: "Emissions", domain: [0,250]},
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
            sort: {y: "x", reverse: true },
            //domain: [0, 100],
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

