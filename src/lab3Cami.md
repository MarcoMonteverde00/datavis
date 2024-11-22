<link rel="stylesheet" href="style.css">

<div class="hero">

# Displaying maps

</div>

<br />

# Total CO2 emissions

## Equal Earth  projection
```js

let data_year = {
  "2022": await FileAttachment("./data/ass3_2022.csv").csv(),
  "2021": await FileAttachment("./data/ass3_2021.csv").csv(),
  "2020": await FileAttachment("./data/ass3_2020.csv").csv(),
  "2019": await FileAttachment("./data/ass3_2019.csv").csv()
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

import * as topojson from "topojson-client";

```
<br />

```js

const years = [2019,2020,2021,2022];

const selected_year = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year);
```

<div class="plot">

```js
const world = await FileAttachment("countries-110m.json").json();
const country = topojson.feature(world, world.objects.countries);

let plot1;
let plot1_legend;

function showPlot() {
	let data1 = data_year[selected_year.value];
	
	const TotalEmission = new Map(data1.map(d => [d["Numeric Code"], +d["Total CO2"]]))

	const values1 = data1.map(d => d["Total CO2"]);
	const min1 = Math.min(...values1);
	const max1 = Math.max(...values1);
	
	plot1_legend = display(
		Plot.legend({
		  //data: [10,20,30],
		  color: {
			interpolate: x => colorScale(x*max1 + min1, min1, max1),
			domain: [min1, max1],
			label: "Annual CO₂ emissions (tonnes)",
		  },
		  className: "gradient-legend",
		  width: 300,
		  ticks: 6,
		  label: "Annual CO₂ emissions (tonnes)"
		})
	  )

	plot1 = display(Plot.plot({
	  projection: "equal-earth",
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalEmission.get(d.id),min1,max1),
		  tip: true,
		  channels: {
			"CO2 (tonnes)": d=> TotalEmission.get(d.id),
			Country: d => d.properties.name,
		  }
		})),
	  ]
	}));

}

showPlot();

selected_year.addEventListener("change", (e) => {

  if (plot1 != undefined) {
    plot1.parentNode.removeChild(plot1);
  }
  if (plot1_legend != undefined) {
    plot1_legend.parentNode.removeChild(plot1_legend);
  }
  showPlot();
});

```

<a href="https://ourworldindata.org/grapher/co-emissions-per-capita" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [CO2 emission per capita - Our World in Data]
  </a>
  
  
<a href="https://ourworldindata.org/explorers/population-and-demography?tab=table&time=2022&Metric=Population&Sex=Both+sexes&Age+group=Total&Projection+Scenario=None&country=CHN~IND~USA~IDN~PAK~NGA~BRA~JPN" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Global Population - Our World in Data]
  </a>

<br />

<br />


## Mercator projection

```js

const selected_year2 = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year2);
```  

```js
const world = await FileAttachment("countries-110m.json").json();
const country = topojson.feature(world, world.objects.countries);

let plot2;
let plot2_legend;

function showPlot2() {
	let data1 = data_year[selected_year.value];
	
	const TotalEmission = new Map(data1.map(d => [d["Numeric Code"], +d["Total CO2"]]))

	const values1 = data1.map(d => d["Total CO2"]);
	const min1 = Math.min(...values1);
	const max1 = Math.max(...values1);
	
	plot2_legend = display(
		Plot.legend({
		  //data: [10,20,30],
		  color: {
			interpolate: x => colorScale(x*max1 + min1, min1, max1),
			domain: [min1, max1],
			label: "Annual CO₂ emissions (tonnes)",
		  },
		  className: "gradient-legend",
		  width: 300,
		  ticks: 6,
		  label: "Annual CO₂ emissions (tonnes)"
		})
	  )

	plot2 = display(Plot.plot({
	  projection: "Mercator",
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalEmission.get(d.id),min1,max1),
		  tip: true,
		  channels: {
			"CO2 (tonnes)": d=> TotalEmission.get(d.id),
			Country: d => d.properties.name,
		  }
		})),
	  ]
	}));

}

showPlot2();

selected_year.addEventListener("change", (e) => {

  if (plot2 != undefined) {
    plot2.parentNode.removeChild(plot2);
  }
  if (plot2_legend != undefined) {
    plot2_legend.parentNode.removeChild(plot2_legend);
  }
  showPlot2();
});

/*
display(Plot.plot({
  projection: "equirectangular",
  color: {
    type: "quantize",
    n: 9,
    domain: [min1, max1],
    scheme: "YlOrRd",
    label: "Unemployment rate (%)",
    legend: true
  },
  marks: [
    Plot.geo(country, Plot.centroid({
	fill: d => {
        const emissions = TotalEmission.get(d.id); // Make sure to use the correct property here
        return emissions !== undefined ? emissions : 0; // Default to 0 if no data
      },
      //fill: d => TotalEmission.get(d.Entity),
      tip: true,
      channels: {
        Country: d => d.properties.name,
      }
    })),
  ]
}));*/

```

<a href="https://ourworldindata.org/grapher/co-emissions-per-capita" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [CO2 emission per capita - Our World in Data]
  </a>
  
  
<a href="https://ourworldindata.org/explorers/population-and-demography?tab=table&time=2022&Metric=Population&Sex=Both+sexes&Age+group=Total&Projection+Scenario=None&country=CHN~IND~USA~IDN~PAK~NGA~BRA~JPN" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Global Population - Our World in Data]
  </a>