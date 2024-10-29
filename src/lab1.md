# CO2 emission per capita

```js
const data = await FileAttachment("./data/co2_2022.csv").csv();
const trimmed = data.slice(0,20)

```
```js
//display(data);
```
```js
display(  
  Plot.plot({
    marginBottom: 80,
    title: "2022 CO2 emission per capita",
    x: {
      label: "Country",
      tickRotate: -30
    },
    y: {
      label: "CO₂ emissions (tonnes per person)",
      grid: true,
      percent: false
    },
    marks: [
      Plot.ruleY([0]),
      Plot.barY(trimmed, {x: "Entity", y: "Annual CO₂ emissions (per capita)", sort: {x: "y", reverse: true}})
    ]
  })
);
```