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