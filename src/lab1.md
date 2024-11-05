<link rel="stylesheet" href="style.css">

<div class="hero">
  <h1>CO2 emission per capita</h1>
</div>

```js

let data_year = {
  "2022": await FileAttachment("./data/co2_2022.csv").csv(),
  "2021": await FileAttachment("./data/co2_2021.csv").csv(),
  "2020": await FileAttachment("./data/co2_2020.csv").csv(),
  "2019": await FileAttachment("./data/co2_2019.csv").csv()
};

function colorScale(value, min, max) {
  const ratio = (value - min) / (max - min);
  const b = 0;
  let r,g ;
  if (value<0){
	r=0;
	g = Math.floor(255 * (1 + ratio));
  } else{
	r=255;
	g = Math.floor(255 * (1 - ratio));
	}
  return `rgb(${r}, ${g}, ${b})`;
}

```
<br /><br />

# Top 20 polluters in a year

```js


const years = [2019,2020,2021,2022];

const selected_year = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year);

let plot1;

function showPlot1() {

  let data1 = data_year[selected_year.value];
  let trimmed1 = data1.slice(0,20)

  let values1 = data1.map(d => d["Annual CO₂ emissions (per capita)"]);
  let min1 = Math.min(...values1);
  let max1 = Math.max(...values1);

  plot1 = display(  
    Plot.plot({
      marginBottom: 80,
      title: `CO2 emission per capita (tonnes per person) ${selected_year.value}`,
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
}

showPlot1();


selected_year.addEventListener("change", (e) => {

  if (plot1 != undefined) {
    plot1.parentNode.removeChild(plot1);
  }
  showPlot1();
});

```
<br /><br /><br />

# Top 20 polluters in a decade

```js

const data2 = await FileAttachment("./data/co2_2022_mean.csv").csv(); 
const trimmed2 = data2.slice(0,20);

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
const data3_without_total = data3.slice(0,36);
const data3_total = data3.slice(36);

console.log(data3_total);

display(
  Plot.plot({
    marginLeft: 90,
    width: 900,
    height: 360,
    title: "CO2 emission per capita in each Region (tonnes per person) (2022)",
    //color: { scheme: "Dark2", legend: true},
    x: {label: "", percent: false, },
    y: {label: "Continent", padding: 0.2},
    color: {legend: true},
    marks: [
      Plot.barX(
        data3_without_total,
        {   
          x: "Annual CO₂ emissions (per capita)",
          fill: "Rank",
          y: "Continent",
          sort: {y: "x", reverse: true },
          channels: {Country: 'Entity'},
          tip: {
            format: {
              x: (d) => `${d.toFixed(4)} tonnes/per`,  
              fill: false
            }
          }
        }
      ),
      Plot.text(data3_total, {
        text: d => `${Number(d["Annual CO₂ emissions (per capita)"]).toFixed(4)}`,
        y: "Continent",
        x: "Annual CO₂ emissions (per capita)",
        //sort: {y: "x", reverse: true },
        textAnchor: "end",
        dx: -30,
        fill: "rgb(22,22,22)"
      }),

      Plot.axisX({ticks: []}),
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

```js
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
		  offset:"normalize",
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

<br /><br /><br />
# Emission type comparison top 10 polluters

```js
const data_by_type = await FileAttachment("./data/co2_by_type_Heatmap.csv").csv();

const values_Heatmap = data_by_type.map(d => d["Value"]);
const minHeatmap = Math.min(...values_Heatmap);
const maxHeatmap = Math.max(...values_Heatmap);

display(
	Plot.plot({
	  padding: 0,
	  marginLeft: 90,
	  marginBottom: 80,
	  width: 900,
      height: 360,
      title: "Mean total CO2 emission for each country divided by type (tonnes) (2012-2022)",
	  x: {
      label: "Country",
      tickRotate: -30
	  },
	  color: {legend: true, zero: true},
	  marks: [
		Plot.cell(data_by_type, {
		  x: "Entity",
		  y: "Type",
		  fill: d => colorScale(d["Value"], minHeatmap, maxHeatmap),
		  inset: 0.5,
		  channels: {Co2_Emissions: "Value"},
		tip: {
            format: {value: true}
          }
		})
	  ]
	})
)

```

