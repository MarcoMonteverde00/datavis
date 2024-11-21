<link rel="stylesheet" href="style.css">

<div class="hero">

# Displaying maps

</div>

<br />

#

# Total CO2 emissions

```js


const years = [2019,2020,2021,2022];

const selected_year = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year);

```

```js
import * as topojson from "topojson-client";

const world = await FileAttachment("countries-110m.json").json();

const country = topojson.feature(world, world.objects.countries);

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

//const TotalEmission = data_year.map(d.name => d.Entity, d.value=> d["Total CO2"]);

const TotalEmission = new Map((await FileAttachment("./data/ass3_2022.csv").csv()).map(d => [d["Numeric Code"], +d["Total CO2"]]))
let min1 = Math.min(...TotalEmission);
let max1 = Math.max(...TotalEmission);


let plot1;
let plotprova;
let plot1_legend;

function showPlot() {

plot1_legend = display(
    Plot.legend({
      data: [10,20,30],
      color: {
        interpolate: x => colorScale(x*max1 + min1, min1, max1),
        domain: [min1, max1]
      },
      className: "gradient-legend",
      width: 300,
      ticks: 10,
      label: "Annual CO₂ emissions (per capita, tonnes)"
    })
  )

plot1 = display(Plot.plot({
  projection: "equirectangular",
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
}));

}


showPlot();

```