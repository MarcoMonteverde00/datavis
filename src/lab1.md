# CO2 emission per capita

```js
const data = FileAttachment("./co2_2022.csv").csv();
```
```js
display(data);
```
```js
display(  
  Plot.plot({
  title: "2022 CO2 emission per capita",
  y: {
    grid: true,
    percent: true
  },
  marks: [
    Plot.ruleY([0]),
    Plot.barY(data, {x: "country", y: "co2_per_capita", sort: {x: "y", reverse: true}})
  ]
})
);
```