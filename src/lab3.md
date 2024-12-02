<link rel="stylesheet" href="style.css">

<div class="hero">

# Global Pollution by Country: A Comparison of Map Projections

</div>

<br />

# Global Pollution by Country: A Comparison of Map Projections
<br />

## Carbone dioxide CO2 emissions (tonnes) by country --Equal Earth  projection

```js

let data_year = {
  "2022": await FileAttachment("./data/ass3_2022.csv").csv(),
  "2021": await FileAttachment("./data/ass3_2021.csv").csv(),
  "2020": await FileAttachment("./data/ass3_2020.csv").csv(),
  "2019": await FileAttachment("./data/ass3_2019.csv").csv()
};

var minAbs, maxAbs, minCap, maxCap;
minAbs = Number(data_year["2019"][0]["Total CO2"]);
maxAbs = Number(data_year["2019"][0]["Total CO2"]);
minCap = Number(data_year["2019"][0]["Annual CO₂ emissions (per capita)"]);
maxCap = Number(data_year["2019"][0]["Annual CO₂ emissions (per capita)"]);

let _years = ["2019", "2020", "2021", "2022"];

console.log(maxAbs);
console.log(minAbs);

for (let i in _years) {
	let year = _years[i];
	for(let j in data_year[year]) {
		if (j == "columns") continue;
		let abs = Number(data_year[year][j]["Total CO2"]);
		let cap = Number(data_year[year][j]["Annual CO₂ emissions (per capita)"]);

		if (abs > maxAbs) maxAbs = abs;
		else if (abs < minAbs) minAbs = abs;

		if(cap > maxCap) maxCap = cap;
		else if (cap < minCap) minCap = cap;
	}
}


function numToScientific(number) {
  let digits = ["⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹", "⁻"];

  let num = Number(number).toExponential(2);

  let [val, exp] = num.split("e");

  let true_exp = "";
  if (exp[0] == "-") true_exp = digits[10];

  for(let i in exp.slice(1)) {
    true_exp += digits[Number(exp[Number(i)+1])];
  }

  return val + ` x 10${true_exp}`;
}

function colorScale(value, min, max) {
  if (!value) // for NaN values
	return `rgb(140, 140, 140)`;
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

const world = await FileAttachment("countries-110m.json").json();
const country = topojson.feature(world, world.objects.countries);

let zoom_info = [
	{zoomed: false, trans_x: 0, trans_y: 0},
	{zoomed: false, trans_x: 0, trans_y: 0},
	{zoomed: false, trans_x: 0, trans_y: 0},
	{zoomed: false, trans_x: 0, trans_y: 0}
];

```
<br />

```js

const years = [2019,2020,2021,2022];

const selected_year_1 = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year_1);

```

<div class="plot">

```js

function showPlot1(plot_id, data, projection, column_name, column_label) {

	const TotalEmission = new Map(data.map(d => [d["Numeric Code"], d[column_name]]))
	const EmissionByName = new Map(country.features.map(d => [d.properties.name, TotalEmission.get(d.id)]));
	
	let plot_legend = display(
		Plot.legend({
		  //data: [10,20,30],
		  color: {
			interpolate: x => colorScale(x*maxAbs + minAbs, minAbs, maxAbs),
			domain: [minAbs, maxAbs],
			label: column_label,
		  },
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  tickFormat: d => (d / 1000000000) + "B",
		  label: column_label
		})
	);

	let plot = display(Plot.plot({
	  projection,
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalEmission.get(d.id),minAbs,maxAbs),
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

	let g = plot.childNodes[1];
	let tip = plot.childNodes[2];

	g.style.transition = "transform 0.3s ease-in 0s";

	g.style.transform = "";

	zoom_info[plot_id] = {zoomed: false, trans_x: 0, trans_y: 0};

	g.childNodes.forEach(c => {
    	c.addEventListener("click", (e) => {

			let {zoomed, trans_x, trans_y} = zoom_info[plot_id];
			
			let rect = g.parentNode.getBoundingClientRect()

			let innerRect = e.target.getBoundingClientRect();


			let x = rect.x - innerRect.x;
			let y = rect.y - innerRect.y;


			const zoom_factor = 3;

			if (!zoomed) {
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

			zoomed = true;

			zoom_info[plot_id] = {zoomed, trans_x, trans_y};
		});

		c.addEventListener("mouseover", (e) => {

			let country = e.target.childNodes[0].innerHTML;
			let emissions = EmissionByName.get(country);


			emissions = numToScientific(emissions);

			let tip = document.getElementsByClassName("tooltip")[plot_id];

			tip.style.visibility = "visible";

			tip.innerHTML = `<span><b>Country:</b> ${country}</span><br/>
				<span><b>CO2 Emissions</b>: ${emissions} tonnes</span>`;
			

				
		})
		c.addEventListener("mouseout", (e) => {

			let tip = document.getElementsByClassName("tooltip")[plot_id];
			tip.style.visibility = "hidden";
		})
	});

	return [plot, plot_legend]

}

let plot1;
let plot1_legend;

[plot1, plot1_legend] = showPlot1(0, data_year[selected_year_1.value], "equal-earth", "Total CO2", "Annual CO₂ emissions (tonnes)");

selected_year_1.addEventListener("change", (e) => {

  if (plot1 != undefined) {
    plot1.parentNode.removeChild(plot1);
  }
  if (plot1_legend != undefined) {
    plot1_legend.parentNode.removeChild(plot1_legend);
  }
  
  [plot1, plot1_legend] = showPlot1(0, data_year[selected_year_1.value], "equal-earth", "Total CO2", "Annual CO₂ emissions (tonnes)");

});


document.getElementsByClassName("unzoom")[0].addEventListener("click", () => {

	let g = plot1.childNodes[1];
	g.style.transform = "";
	zoom_info[0] = {zoomed: false, trans_x: 0, trans_y: 0};

});

```
<div class="tooltip">tooltip</div>
<button class="unzoom"></button>
</div>
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

const selected_year_2 = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year_2);

```

<div class="plot">

```js

function showPlot2(plot_id, data, projection, column_name, column_label) {

	const TotalEmission = new Map(data.map(d => [d["Numeric Code"], d[column_name]]))
	const EmissionByName = new Map(country.features.map(d => [d.properties.name, TotalEmission.get(d.id)]));
	
	let plot_legend = display(
		Plot.legend({
		  //data: [10,20,30],
		  color: {
			interpolate: x => colorScale(x*maxAbs + minAbs, minAbs, maxAbs),
			domain: [minAbs, maxAbs],
			label: column_label,
		  },
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  tickFormat: d => (d / 1000000000) + "B",
		  label: column_label
		})
	);

	let plot = display(Plot.plot({
	  projection,
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalEmission.get(d.id),minAbs,maxAbs),
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

	let g = plot.childNodes[1];
	let tip = plot.childNodes[2];

	g.style.transition = "transform 0.3s ease-in 0s";

	g.style.transform = "";

	zoom_info[plot_id] = {zoomed: false, trans_x: 0, trans_y: 0};

	g.childNodes.forEach(c => {
    	c.addEventListener("click", (e) => {

			let {zoomed, trans_x, trans_y} = zoom_info[plot_id];
			
			let rect = g.parentNode.getBoundingClientRect()

			let innerRect = e.target.getBoundingClientRect();


			let x = rect.x - innerRect.x;
			let y = rect.y - innerRect.y;


			const zoom_factor = 3;

			if (!zoomed) {
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

			zoomed = true;

			zoom_info[plot_id] = {zoomed, trans_x, trans_y};
		});

		c.addEventListener("mouseover", (e) => {

			let country = e.target.childNodes[0].innerHTML;
			let emissions = EmissionByName.get(country);
			
			emissions = numToScientific(emissions);

			let tip = document.getElementsByClassName("tooltip")[plot_id];

			tip.style.visibility = "visible";

			tip.innerHTML = `<span><b>Country:</b> ${country}</span><br/>
				<span><b>CO2 Emissions</b>: ${emissions} tonnes</span>`;
			

				
		})
		c.addEventListener("mouseout", (e) => {

			let tip = document.getElementsByClassName("tooltip")[plot_id];
			tip.style.visibility = "hidden";
		})
	});

	return [plot, plot_legend]

}

let plot2;
let plot2_legend;

[plot2, plot2_legend] = showPlot2(1, data_year[selected_year_2.value], "Mercator", "Total CO2", "Annual CO₂ emissions (tonnes)");

selected_year_2.addEventListener("change", (e) => {

  if (plot2 != undefined) {
    plot2.parentNode.removeChild(plot2);
  }
  if (plot2_legend != undefined) {
    plot2_legend.parentNode.removeChild(plot2_legend);
  }
  
  [plot2, plot2_legend] = showPlot2(1, data_year[selected_year_2.value], "Mercator", "Total CO2", "Annual CO₂ emissions (tonnes)");

});


document.getElementsByClassName("unzoom")[1].addEventListener("click", () => {

	let g = plot2.childNodes[1];
	g.style.transform = "";
	zoom_info[1] = {zoomed: false, trans_x: 0, trans_y: 0};

});

```
<div class="tooltip">tooltip</div>
<button class="unzoom"></button>
</div>
<br/>

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

const selected_year_3 = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year_3);
``` 

<div class="plot">

```js

function showPlot3(plot_id, data, projection, column_name, column_label) {

	const TotalEmission = new Map(data.map(d => [d["Numeric Code"], d[column_name]]))
	const EmissionByName = new Map(country.features.map(d => [d.properties.name, TotalEmission.get(d.id)]));

	let plot_legend = display(
		Plot.legend({
		  //data: [10,20,30],
		  color: {
			interpolate: x => colorScale(x*maxCap + minCap, minCap, maxCap),
			domain: [minCap, maxCap],
			label: column_label,
		  },
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  //tickFormat: d => (d / 1000000000) + "B",
		  label: column_label
		})
	);

	let plot = display(Plot.plot({
	  projection,
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalEmission.get(d.id),minCap,maxCap),
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

	let g = plot.childNodes[1];
	let tip = plot.childNodes[2];

	g.style.transition = "transform 0.3s ease-in 0s";

	g.style.transform = "";

	zoom_info[plot_id] = {zoomed: false, trans_x: 0, trans_y: 0};

	g.childNodes.forEach(c => {
    	c.addEventListener("click", (e) => {

			let {zoomed, trans_x, trans_y} = zoom_info[plot_id];
			
			let rect = g.parentNode.getBoundingClientRect()

			let innerRect = e.target.getBoundingClientRect();


			let x = rect.x - innerRect.x;
			let y = rect.y - innerRect.y;


			const zoom_factor = 3;

			if (!zoomed) {
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

			zoomed = true;

			zoom_info[plot_id] = {zoomed, trans_x, trans_y};
		});

		c.addEventListener("mouseover", (e) => {

			let country = e.target.childNodes[0].innerHTML;
			let emissions = EmissionByName.get(country);
			emissions = numToScientific(emissions);

			let tip = document.getElementsByClassName("tooltip")[plot_id];

			tip.style.visibility = "visible";

			tip.innerHTML = `<span><b>Country:</b> ${country}</span><br/>
				<span><b>CO2 Emissions</b>: ${emissions} tonnes</span>`;
			

				
		})
		c.addEventListener("mouseout", (e) => {

			let tip = document.getElementsByClassName("tooltip")[plot_id];
			tip.style.visibility = "hidden";
		})
	});

	return [plot, plot_legend]

}

let plot3;
let plot3_legend;

[plot3, plot3_legend] = showPlot3(2, data_year[selected_year_3.value], "equal-earth", "Annual CO₂ emissions (per capita)", "Annual CO₂ emissions per capita (tonnes/person)");

selected_year_3.addEventListener("change", (e) => {

  if (plot3 != undefined) {
    plot3.parentNode.removeChild(plot3);
  }
  if (plot3_legend != undefined) {
    plot3_legend.parentNode.removeChild(plot3_legend);
  }
  
  [plot3, plot3_legend] = showPlot3(2, data_year[selected_year_3.value], "equal-earth", "Annual CO₂ emissions (per capita)", "Annual CO₂ emissions per capita (tonnes/person)");

});


document.getElementsByClassName("unzoom")[2].addEventListener("click", () => {

	let g = plot3.childNodes[1];
	g.style.transform = "";
	zoom_info[2] = {zoomed: false, trans_x: 0, trans_y: 0};

});

```
<div class="tooltip">tooltip</div>
<button class="unzoom"></button>
</div>
<br/>

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

const selected_year_4 = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year_4);
``` 

<div class="plot">

```js

function showPlot4(plot_id, data, projection, column_name, column_label) {

	const TotalEmission = new Map(data.map(d => [d["Numeric Code"], d[column_name]]))
	const EmissionByName = new Map(country.features.map(d => [d.properties.name, TotalEmission.get(d.id)]));

	let plot_legend = display(
		Plot.legend({
		  //data: [10,20,30],
		  color: {
			interpolate: x => colorScale(x*maxCap + minCap, minCap, maxCap),
			domain: [minCap, maxCap],
			label: column_label,
		  },
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  //tickFormat: d => (d / 1000000000) + "B",
		  label: column_label
		})
	);

	let plot = display(Plot.plot({
	  projection,
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalEmission.get(d.id),minCap,maxCap),
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

	let g = plot.childNodes[1];
	let tip = plot.childNodes[2];

	g.style.transition = "transform 0.3s ease-in 0s";

	g.style.transform = "";

	zoom_info[plot_id] = {zoomed: false, trans_x: 0, trans_y: 0};

	g.childNodes.forEach(c => {
    	c.addEventListener("click", (e) => {

			let {zoomed, trans_x, trans_y} = zoom_info[plot_id];
			
			let rect = g.parentNode.getBoundingClientRect()

			let innerRect = e.target.getBoundingClientRect();


			let x = rect.x - innerRect.x;
			let y = rect.y - innerRect.y;


			const zoom_factor = 3;

			if (!zoomed) {
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

			zoomed = true;

			zoom_info[plot_id] = {zoomed, trans_x, trans_y};
		});

		c.addEventListener("mouseover", (e) => {

			let country = e.target.childNodes[0].innerHTML;
			let emissions = EmissionByName.get(country);
			emissions = numToScientific(emissions);

			let tip = document.getElementsByClassName("tooltip")[plot_id];

			tip.style.visibility = "visible";

			tip.innerHTML = `<span><b>Country:</b> ${country}</span><br/>
				<span><b>CO2 Emissions</b>: ${emissions} tonnes</span>`;
			

				
		})
		c.addEventListener("mouseout", (e) => {

			let tip = document.getElementsByClassName("tooltip")[plot_id];
			tip.style.visibility = "hidden";
		})
	});

	return [plot, plot_legend]

}

let plot4;
let plot4_legend;

[plot4, plot4_legend] = showPlot4(3, data_year[selected_year_4.value], "Mercator", "Annual CO₂ emissions (per capita)", "Annual CO₂ emissions per capita (tonnes/person)");

selected_year_4.addEventListener("change", (e) => {

  if (plot4 != undefined) {
    plot4.parentNode.removeChild(plot4);
  }
  if (plot4_legend != undefined) {
    plot4_legend.parentNode.removeChild(plot4_legend);
  }
  
  [plot4, plot4_legend] = showPlot4(3, data_year[selected_year_4.value], "Mercator", "Annual CO₂ emissions (per capita)", "Annual CO₂ emissions per capita (tonnes/person)");

});


document.getElementsByClassName("unzoom")[3].addEventListener("click", () => {

	let g = plot4.childNodes[1];
	g.style.transform = "";
	zoom_info[3] = {zoomed: false, trans_x: 0, trans_y: 0};

});

```
<div class="tooltip">tooltip</div>
<button class="unzoom"></button>
</div>
<br/>

<a href="https://ourworldindata.org/grapher/co-emissions-per-capita" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [CO2 emission per capita - Our World in Data]
  </a>
  
  
<a href="https://ourworldindata.org/explorers/population-and-demography?tab=table&time=2022&Metric=Population&Sex=Both+sexes&Age+group=Total&Projection+Scenario=None&country=CHN~IND~USA~IDN~PAK~NGA~BRA~JPN" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Global Population - Our World in Data]
  </a>

<br />

<br />