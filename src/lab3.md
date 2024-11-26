<link rel="stylesheet" href="style.css">

<div class="hero">

# Global Pollution by Country: A Comparison of Map Projections

</div>

<br />

# Global Pollution by Country: A Comparison of Map Projections
<br />

## Carbone dioxide CO2 emissions (tonnes) by country --Equal Earth  projection

```js
//Equal Earth  projection

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

let plot1_zoom = false;
let trans_x = 0;
let trans_y = 0;

function showPlot() {
	let data1 = data_year[selected_year.value];
	
	console.log(country);
	const TotalEmission = new Map(data1.map(d => [d["Numeric Code"], d["Total CO2"]]))
	const EmissionByName = new Map(country.features.map(d => [d.properties.name, TotalEmission.get(d.id)]));

	console.log(TotalEmission)
	console.log(EmissionByName);

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
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  tickFormat: d => (d / 1000000000) + "B",
		  label: "Annual CO₂ emissions (tonnes)"
		})
	);

	plot1 = display(Plot.plot({
	  projection: "equal-earth",
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalEmission.get(d.id),min1,max1),
		  //tip: {className: "Za-Warudo-Tip"},
		  title: d => d.properties.name,
		  className: "Za-Warudo",
		  channels: {
			"CO2 (tonnes)": d => TotalEmission.get(d.id),
			Country: d => d.properties.name,
		  }
		}))
	  ]
	}));

	let g = plot1.childNodes[1];
	let tip = plot1.childNodes[2];

	g.style.transition = "transform 0.3s ease-in 0s";

	g.style.transform = "";
	plot1_zoom = false;
	trans_x = 0;
	trans_y = 0;

	g.childNodes.forEach(c => {
    	c.addEventListener("click", (e) => {
			
			let rect = g.parentNode.getBoundingClientRect()

			let innerRect = e.target.getBoundingClientRect();


			let x = rect.x - innerRect.x;
			let y = rect.y - innerRect.y;


			const zoom_factor = 3;

			if (!plot1_zoom) {
				x *= zoom_factor;
				y *= zoom_factor;
				x -= innerRect.width * zoom_factor / 2;
				y -= innerRect.height * zoom_factor / 2;
			} else {
				
				x -= innerRect.width / 2;
				y -= innerRect.height / 2;
			}

			x += rect.width / 2;
			y += rect.height / 2;

			trans_x += x;
			trans_y += y;

			g.style.transform = "translate(" + trans_x + "px, " + trans_y + "px)" + " scale(" + zoom_factor + ", " + zoom_factor + ")";

			plot1_zoom = true;
		});

		c.addEventListener("mouseover", (e) => {

			let country = e.target.childNodes[0].innerHTML;
			let emissions = EmissionByName.get(country);
			if(emissions == NaN)
				emissions = "No Data";
			else
				emissions = Number(emissions).toFixed(0);

			let tip = document.getElementById("tooltip-1");

			tip.style.visibility = "visible";

			tip.innerHTML = `<span><b>Country:</b> ${country}</span><br/>
				<span><b>CO2 Emissions</b>: ${emissions} tonnes</span>`;
			

				
		})
		c.addEventListener("mouseout", (e) => {

			let tip = document.getElementById("tooltip-1");
			tip.style.visibility = "hidden";
		})
	});

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


document.getElementsByClassName("unzoom")[0].addEventListener("click", () => {

	let g = plot1.childNodes[1];
	g.style.transform = "";
	plot1_zoom = false;
	trans_x = 0;
	trans_y = 0;

});

```
<div class="tooltip" id="tooltip-1">tooltip</div>
</div>
<button class="unzoom">Unzoom</button>
<br/>

<a href="https://ourworldindata.org/grapher/co-emissions-per-capita" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [CO2 emission per capita - Our World in Data]
  </a>
  
  
<a href="https://ourworldindata.org/explorers/population-and-demography?tab=table&time=2022&Metric=Population&Sex=Both+sexes&Age+group=Total&Projection+Scenario=None&country=CHN~IND~USA~IDN~PAK~NGA~BRA~JPN" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Global Population - Our World in Data]
  </a>

<br />

<br />


## Carbone dioxide CO2 emissions (tonnes) by country --Mercator projection

```js
const years2 = [2019,2020,2021,2022];

const selected_year2 = Inputs.select(years2, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year2);
```  

```js
const world = await FileAttachment("countries-110m.json").json();
const country = topojson.feature(world, world.objects.countries);

let plot2;
let plot2_legend;

function showPlot2() {
	let data2 = data_year[selected_year2.value];
	
	const TotalEmission2 = new Map(data2.map(d => [d["Numeric Code"], +d["Total CO2"]]))

	const values2 = data2.map(d => d["Total CO2"]);
	const min2 = Math.min(...values2);
	const max2 = Math.max(...values2);
	
	plot2_legend = display(
		Plot.legend({
		  //data: [10,20,30],
		  color: {
			interpolate: x => colorScale(x*max2 + min2, min2, max2),
			domain: [min2, max2],
			label: "Annual CO₂ emissions (tonnes)",
		  },
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  label: "Annual CO₂ emissions (tonnes)",
		  tickFormat: d => (d / 1000000000) + "B"
		})
	  )

	plot2 = display(Plot.plot({
	  projection: "Mercator",
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalEmission2.get(d.id),min2,max2),
		  tip: true,
		  channels: {
			"CO2 (tonnes)": d=> TotalEmission2.get(d.id),
			Country: d => d.properties.name,
		  }
		})),
	  ]
	}));

}

showPlot2();

selected_year2.addEventListener("change", (e) => {

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
  
Both projections aim to convey, through the use of colors, how much each country contributes to global pollution. 

The main difference between them lies in the fact that the Mercator projection distorts areas, while the Equal Earth projection preserves 
them. In particular, the Mercator projection causes countries closer to the poles to appear disproportionately large, which can 
create a misleading impression of pollution levels. For instance, Russia might appear less significant as a polluter  with respect to the apparent size.
Moreover changing only the size of countries in the northern or southern extremes a comparison of the CO2 emissions among all the countries is not accurate.
On the other hand, while the Equal Earth projection distorts shapes, it preserves the relative size of countries, making the representation of pollution data more accurate.

## Carbone dioxide CO2 emissions per capita (tonnes per person) by country --Equal earth projection

```js

const selected_year3 = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year3);
``` 

```js
const world = await FileAttachment("countries-110m.json").json();
const country = topojson.feature(world, world.objects.countries);

let plot3;
let plot3_legend;

function showPlot3() {
	let data1 = data_year[selected_year3.value];
	
	const TotalEmission = new Map(data1.map(d => [d["Numeric Code"], +d["Annual CO₂ emissions (per capita)"]]))

	const values1 = data1.map(d => d["Annual CO₂ emissions (per capita)"]);
	const min1 = Math.min(...values1);
	const max1 = Math.max(...values1);
	
	plot3_legend = display(
		Plot.legend({
		  //data: [10,20,30],
		  color: {
			interpolate: x => colorScale(x*max1 + min1, min1, max1),
			domain: [min1, max1],
			label: "Annual CO₂ emissions per capita (tonnes/person)",
		  },
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  label: "Annual CO₂ emissions per capita (tonnes/person)"
		})
	  )

	plot3 = display(Plot.plot({
	  projection: "equal-earth",
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalEmission.get(d.id),min1,max1),
		  tip: true,
		  channels: {
			"CO2 (tonnes/person)": d=> TotalEmission.get(d.id),
			Country: d => d.properties.name,
		  }
		})),
	  ]
	}));

}

showPlot3();

selected_year3.addEventListener("change", (e) => {

  if (plot3 != undefined) {
    plot3.parentNode.removeChild(plot3);
  }
  if (plot3_legend != undefined) {
    plot3_legend.parentNode.removeChild(plot3_legend);
  }
  showPlot3();
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

## Carbone dioxide CO2 emissions per capita (tonnes per person) by country --Mercator projection

```js

const selected_year4 = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year4);
``` 

```js
const world = await FileAttachment("countries-110m.json").json();
const country = topojson.feature(world, world.objects.countries);

let plot4;
let plot4_legend;

function showPlot4() {
	let data1 = data_year[selected_year4.value];
	
	const TotalEmission = new Map(data1.map(d => [d["Numeric Code"], +d["Annual CO₂ emissions (per capita)"]]))

	const values1 = data1.map(d => d["Annual CO₂ emissions (per capita)"]);
	const min1 = Math.min(...values1);
	const max1 = Math.max(...values1);
	
	plot4_legend = display(
		Plot.legend({
		  //data: [10,20,30],
		  color: {
			interpolate: x => colorScale(x*max1 + min1, min1, max1),
			domain: [min1, max1],
			label: "Annual CO₂ emissions per capita (tonnes/person)",
		  },
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  label: "Annual CO₂ emissions per capita (tonnes/person)"
		})
	  )

	plot4 = display(Plot.plot({
	  projection: "Mercator",
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalEmission.get(d.id),min1,max1),
		  tip: true,
		  channels: {
			"CO2 (tonnes/person)": d=> TotalEmission.get(d.id),
			Country: d => d.properties.name,
		  }
		})),
	  ]
	}));

}

showPlot4();

selected_year4.addEventListener("change", (e) => {

  if (plot4 != undefined) {
    plot4.parentNode.removeChild(plot4);
  }
  if (plot4_legend != undefined) {
    plot4_legend.parentNode.removeChild(plot4_legend);
  }
  showPlot4();
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