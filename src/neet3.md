<link rel="stylesheet" href="style.css">

```js
// Imports
import * as topojson from "topojson-client";
import { createSelector } from "./selector.js";
```

<div class="hero">

# NEET Compared Analysis

</div>

```js

const world = await FileAttachment("./data_EU/countries-50m.json").json();
const country = topojson.feature(world, world.objects.countries);
//const countries = topojson.feature(europe, europe.objects[Object.keys(europe.objects)[0]])

// Define an EventTarget for handling custom events (needed for interaction between dataviz)
const eventBus = new EventTarget();
```

# An European Perspective of NEET Phenomenon
<div class="description">
How are NEET distributed in <b>European countries</b>? If we want to really understand this <b>new societal paradigm</b>, the optimal starting point is to visualize an <b>european counterpart</b> of what we have shown in the maps depitcing the situation in Italy. Before looking at the map ask yourself: what do you think you will find? The data we propose cover <b>main nations</b> of Europe, collected by Eurostat.</br></br>
<i><b>Hint:</b> Clicking on a country in the map let you <b>focus</b> on it, depicting the related information in the graphs underneath. Italy is always pre-selected, so that you can <b>easily confront</b> values between Italy and other european countries.</i>
</div>

```js

let data_year = {
  "2014": await FileAttachment("./data_EU/EU_NEET_PERC_2014_preproc.csv").csv(),
  "2015": await FileAttachment("./data_EU/EU_NEET_PERC_2015_preproc.csv").csv(),
  "2016": await FileAttachment("./data_EU/EU_NEET_PERC_2016_preproc.csv").csv(),
  "2017": await FileAttachment("./data_EU/EU_NEET_PERC_2017_preproc.csv").csv(),
  "2018": await FileAttachment("./data_EU/EU_NEET_PERC_2018_preproc.csv").csv(),
  "2019": await FileAttachment("./data_EU/EU_NEET_PERC_2019_preproc.csv").csv(),
  "2020": await FileAttachment("./data_EU/EU_NEET_PERC_2020_preproc.csv").csv(),
  "2021": await FileAttachment("./data_EU/EU_NEET_PERC_2021_preproc.csv").csv(),
  "2022": await FileAttachment("./data_EU/EU_NEET_PERC_2022_preproc.csv").csv(),
  "2023": await FileAttachment("./data_EU/EU_NEET_PERC_2023_preproc.csv").csv(),
};

var min, max;
min = Number(data_year["2021"][0]["OBS_VALUE"]);
max = Number(data_year["2020"][0]["OBS_VALUE"]);

let _years = ["2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023"];

for (let i in _years) {
	let year = _years[i];
	for(let j in data_year[year]) {
		if (j == "columns") continue;
		let percentage = Number(data_year[year][j]["OBS_VALUE"]);

		if(percentage > max) max = percentage;
		else if (percentage < min) min = percentage;
	}
}

function colorScale(value, min, max) {
  if (!value) // for NaN values
	return `rgb(140, 140, 140)`;
  const ratio = (value - min) / (max - min);
  const r = 0;
  let b,g ;
  if (value<0){
	b=0;
	g = Math.floor(255 * (1 + ratio));
  } else{
	b=255;
	g = Math.floor(255 * (1 - ratio));
	}
  return `rgb(${r}, ${g}, ${b})`;
}

let zoom_info = [
	{zoomed: false, trans_x: 0, trans_y: 0},
	{zoomed: false, trans_x: 0, trans_y: 0},
	{zoomed: false, trans_x: 0, trans_y: 0},
	{zoomed: false, trans_x: 0, trans_y: 0}
];

```

```js
const years = [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023];
const selected_year_1 = Inputs.select(years, {value: "2023", label: "Year:", format: (d) => d});
view(selected_year_1);
```
<div class="plot">
<div class="tooltip">tooltip</div>

```js
const Selected_Country = {
  _value: "not a country",

  set value(newValue) {
    if (newValue !== this._value) {
      const oldValue = this._value;
      this._value = newValue;

      // Dispatch an event when the value changes
      const event = new CustomEvent('valueChanged', {
        detail: { newValue, oldValue }, // Pass data with the event
      });
      eventBus.dispatchEvent(event);
    }
  },

  get value() {
    return this._value;
  },
};

function showPlot1(plot_id, data, projection, column_name, column_label) {

	const TotalNEET = new Map(data.map(d => [d["Geopolitical entity (reporting)"], d[column_name]]));
	const NEETByName = new Map(country.features.map(d => [d.properties.name, TotalNEET.get(d.properties.name)]));
	
	let plot_legend = display(
		Plot.legend({
		  color: {
			interpolate: x => colorScale(x*max + min, min, max),
			domain: [min, max],
			label: column_label,
		  },
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  tickFormat: d => `${d}%`,
		  label: column_label
		})
	);

	let plot = display(Plot.plot({
	  projection: ({width, height}) => d3.geoAzimuthalEqualArea()
    	.rotate([-20.0, -52.0])
    	.translate([width / 2, height / 2])
    	.scale(550)
    	.precision(.1),
	  marks: [
		Plot.geo(country, Plot.centroid({
		  fill: d => colorScale(TotalNEET.get(d.properties.name),min,max),
		  title: d => d.properties.name,
		  className: "Za-Warudo",
		  channels: {
			"NEET (%)": d => TotalNEET.get(d.properties.name),
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
			let country = e.target.childNodes[0].innerHTML;
			Selected_Country.value = country;

			// Object that changes the variable

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
			let NEET = NEETByName.get(country);
			let tip = document.getElementsByClassName("tooltip")[plot_id];

			tip.style.visibility = "visible";

			tip.innerHTML = `<span><b>Country:</b> ${country}</span><br/>
				<span><b>NEET</b>: ${NEET}%</span>`;
				
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

[plot1, plot1_legend] = showPlot1(0, data_year[selected_year_1.value], "mercator", "OBS_VALUE", "NEET (%)");

selected_year_1.addEventListener("change", (e) => {

  if (plot1 != undefined) {
    plot1.parentNode.removeChild(plot1);
  }
  if (plot1_legend != undefined) {
    plot1_legend.parentNode.removeChild(plot1_legend);
  }
  
  [plot1, plot1_legend] = showPlot1(0, data_year[selected_year_1.value], "mercator", "OBS_VALUE", "NEET (%)");

});

document.getElementsByClassName("unzoom")[0].addEventListener("click", () => {
	let g = plot1.childNodes[1];
	g.style.transform = "";
	zoom_info[0] = {zoomed: false, trans_x: 0, trans_y: 0};
});
```
<button class="unzoom"></button>
</div>
<div class="plot">
<a href="https://ec.europa.eu/eurostat/web/products-datasets/-/lfsi_neet_a" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Young people neither in employment nor in education and training (NEET), by sex and age - annual data - <b>Eurostat</b>]
  </a>
</div>
</br>

<div class="description">
It is immediate to see that young people in Italy have an <b>higher probability to become NEETs</b> than their, let's say, German or French counterpart. A positive notes can be aknowledged about the decreasing of NEET phenomenon from 2014 to 2023 in Italy, a tendency that is <b>more or less diffused</b> in all of southern-european countries, while the phenomenon is more stable in norther nations, like Germany, probably due to a <b>mixture</b> of economic structure and work culture. A note to be remarked is there is a <b>gener gap</b>: girls are more prone to become NEET than boys. 
</div>

<div class="plot">

```js
const rates = await FileAttachment("./data_EU/EU_NEET_PERC_Italy_preproc.csv").csv();
const EU_rates = await FileAttachment("./data_EU/EU_NEET_PERC_preproc.csv").csv();
let confrontation_rates = rates;

const total_rates = rates.filter(row => row.sex === 'T');
let total_conf_rates = "unavailable data"; //confrontation_rates.filter(row => row.sex === 'T');
const EU_mean_value = EU_rates.filter(row => row.sex === 'T' && row.geo === 'EU27_2020');
console.log(EU_mean_value);
const male_rates = rates.filter(row => row.sex === 'M');
const female_rates = rates.filter(row => row.sex === 'F');

// Function to create a custom legend
function createLegend(svg, options) {
	const {
		x,          // X position of the legend
		y,          // Y position of the legend
		label1,     // First label text
		color1,     // Color for the first label
		label2,     // Second label text
		color2,     // Color for the second label
		label3,		// Third label text
		color3,		// Color for the Third label
		label4,     // Fourth label text
		color4,     // Color for the fourth label
		label5,		// Fifth label text
		color5,		// Color for the fifth label
	} = options;

	// Create a group for the legend
	const legendGroup = svg.append("g")
		.attr("class", "custom-legend")
		.attr("transform", `translate(${x}, ${y})`);

	// Add first legend item
	const legendItem1 = legendGroup.append("g").attr("class", "legend-item");
	legendItem1.append("rect")
		.attr("x", 0)
		.attr("y", 4)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color1);
	legendItem1.append("text")
		.attr("x", 30)
		.attr("y", 15)
		.text(label1)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add second legend item
	const legendItem2 = legendGroup.append("g").attr("class", "legend-item");
	legendItem2.append("rect")
		.attr("x", 0)
		.attr("y", 34)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color2);
	legendItem2.append("text")
		.attr("x", 30)
		.attr("y", 45)
		.text(label2)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add third legend item
	const legendItem3 = legendGroup.append("g").attr("class", "legend-item");
	legendItem3.append("rect")
		.attr("x", 0)
		.attr("y", 64)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color3);
	legendItem3.append("text")
		.attr("x", 30)
		.attr("y", 75)
		.text(label3)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");
	
	// Add fourth legend item
	const legendItem4 = legendGroup.append("g").attr("class", "legend-item");
	legendItem4.append("rect")
		.attr("x", 250)
		.attr("y", 4)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color4);
	legendItem4.append("text")
		.attr("x", 280)
		.attr("y", 15)
		.text(label4)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add fifth legend item
	const legendItem5 = legendGroup.append("g").attr("class", "legend-item");
	legendItem5.append("rect")
		.attr("x", 250)
		.attr("y", 34)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color5);
	legendItem5.append("text")
		.attr("x", 280)
		.attr("y", 45)
		.text(label5)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");
}

const svg = d3.select("body").append("svg")
		.attr("width", 390)
		.attr("height", 100);

createLegend(svg, {
		x: 10,
		y: 2,
		label1: "Total (Italy)",
		color1: "#000000",
		label2: "European Union",
		color2: "red",
		label3: "Confrontation Country Total",
		color3: "green",
		label4: "Female (Italy)",
		color4: "lightpink",
		label5: "Male (Italy)",
		color5: "steelblue",

	});

	view(svg.node());

function showPlot2(plot_id, confrontation_country) {
	let plot;
	if (total_conf_rates != "unavailable data") {
		plot = display(
			Plot.plot({
				x: {label: "Year", type: "point", },
				y: {label: "NEET (%)", grid: true, domain: [0,45]},
				geo: {label: "Country", type: "point"},

				marks: [
					Plot.lineY(total_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						marker: "dot",
						channels: {
							total_rates: {
								value: "OBS_VALUE",
								label: "IT NEET",
							},
						},
						tip: {
							anchor: "bottom",
							fill: "lightgrey",
							format: {
								y: false,
								total_rates: d => `${d}%`,
							}
						}
					}),

					Plot.lineY(EU_mean_value, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "red",
						marker: "circle-stroke",
						channels: {
							EU_mean_value: {
								value: "OBS_VALUE",
								label: "EU NEET",
							},
						},
						tip: {
							anchor: "left",
							fill: "#ff5959",
							format: {
								x: false,
								y: false,
								EU_mean_value: d => `${d}%`,
							},
						}
					}),

					Plot.lineY(male_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "steelblue",
						marker: "tick-x",
						opacity: 0.4,
						channels: {
							male_rates: {
								value: "OBS_VALUE",
								label: "NEET",
							},
						},
					}),

					Plot.lineY(female_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "lightpink",
						marker: "tick-y",
						opacity: 0.4,
						channels: {
							female_rates: {
								value: "OBS_VALUE",
								label: "NEET",
							},
						},
					}),

					Plot.lineY(total_conf_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						geo: d => String(d["Geopolitical entity (reporting)"]),
						stroke: "green",
						marker: "circle",
						channels: {
							total_conf_rates: {
								value: "OBS_VALUE",
								label: "NEET",
							},
							country: {
								value: "Geopolitical entity (reporting)",
								label: "Country"
							}
						},
						tip: {
							anchor: "right",
							fill: "lightgreen",
							format: {
								x: false,
								y: false,
								total_conf_rates: d => `${d}%`,
								country: d => `${d}`,
							},
						}
					}),

					Plot.tip([Selected_Country.value], {anchor: "top-right", frameAnchor: "top-right", pointerSize: 0}),
					Plot.axisX(), //{ticks: []}),
					Plot.ruleY([0]),
				]
			})
		);
	}

	else {
		plot = display(
			Plot.plot({
				x: {label: "Year", type: "point", },
				y: {label: "NEET (%)", grid: true, domain: [0,45]},
				geo: {label: "Country", type: "point"},

				marks: [
					Plot.lineY(total_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						marker: "dot",
						channels: {
							total_rates: {
								value: "OBS_VALUE",
								label: "IT NEET",
							},
						},
						tip: {
							anchor: "bottom",
							fill: "lightgrey",
							format: {
								y: false,
								total_rates: d => `${d}%`,
							}
						}
					}),

					Plot.lineY(EU_mean_value, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "red",
						marker: "circle-stroke",
						channels: {
							EU_mean_value: {
								value: "OBS_VALUE",
								label: "EU NEET",
							},
						},
						tip: {
							anchor: "left",
							fill: "#ff5959",
							format: {
								x: false,
								y: false,
								EU_mean_value: d => `${d}%`,
							},
						}
					}),

					Plot.lineY(male_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "steelblue",
						marker: "tick-x",
						opacity: 0.4,
						channels: {
							male_rates: {
								value: "OBS_VALUE",
								label: "NEET",
							},
						},
					}),

					Plot.lineY(female_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "lightpink",
						marker: "tick-y",
						opacity: 0.4,
						channels: {
							female_rates: {
								value: "OBS_VALUE",
								label: "NEET",
							},
						},
					}),

					Plot.axisX(), //{ticks: []}),
					Plot.ruleY([0]),
				]
			})
		);
	}
	return [plot];
}

let plot_viz2;

[plot_viz2] = showPlot2(0, "Italy");

// Unrelated object that listens for changes
const listenerObject = {
    init() {
    // Add an event listener for the 'valueChanged' event
    eventBus.addEventListener('valueChanged', (event) => {
		console.log(
			`Listener of PLOT 2 detected value change from ${event.detail.oldValue} to ${event.detail.newValue}`
		);
		if (event.detail.newValue != event.detail.oldValue) {
			plot_viz2.parentNode.removeChild(plot_viz2);
			(async () => {
				if (event.detail.newValue === "Italy"){
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Italy_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
				}
				else if (event.detail.newValue === "Greece") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Greece_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
				}
				else if (event.detail.newValue === "Spain") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Spain_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "France") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_France_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Germany") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Germany_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Turkey") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Türkiye_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Poland") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Poland_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Romania") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Romania_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Netherlands") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Netherlands_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Belgium") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Belgium_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Czechia") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Czechia_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Portugal") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Portugal_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Sweden") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Sweden_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Hungary") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Hungary_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Austria") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Austria_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Bulgaria") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Bulgaria_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Denmark") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Denmark_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Finland") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Finland_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Slovakia") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Slovakia_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Ireland") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Ireland_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Croatia") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Croatia_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Lithuania") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Lithuania_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Slovenia") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Slovenia_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Latvia") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Latvia_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Estonia") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Estonia_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Cyprus") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Cyprus_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Luxembourg") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Luxembourg_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Malta") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Malta_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Iceland") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Iceland_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Switzerland") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Switzerland_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Montenegro") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Montenegro_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Serbia") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Serbia_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Macedonia") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_North_Macedonia_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Bosnia") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Bosnia_and_Herzegovina_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else if (event.detail.newValue === "Norway") {
					confrontation_rates = await FileAttachment("./data_EU/EU_NEET_PERC_Norway_preproc.csv").csv();
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T');
					}
				else {
					total_conf_rates = "unavailable data";
				}

				[plot_viz2] = showPlot2(0, `${event.detail.newValue}`);
			})();
		}
    	});
  	},
};

// Initialize the listener
listenerObject.init();
```

</div>
<div class="plot">
<a href="https://ec.europa.eu/eurostat/web/products-datasets/-/lfsi_neet_a" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Young people neither in employment nor in education and training (NEET), by sex and age - annual data - <b>Eurostat</b>]
  </a>
</div>

</br>
<div class="description">
The <b>unsettling fact</b> that we can see both from the map and the graph underneath, is the <b>diffusion</b> of the NEET pheonomenon itself. Comparing Spain with Italy, we can clearly see the problem: in 2023, Italy has still 16.1% of youngs between 15 and 29 years in the NEET situation, while spanish youngs are at 12.3%. Being Spain a country with a <b>lower GDP</b> (30'970€ vs 36'080€ of Italy as 1 December 2023) but similar development, this is an <b>alarming</b> indicator of NEET pheonomenon being <b>highly problematic</b> in Italy.
</div>
</br>

## Understanding NEET Causes: a Focus on Poverty
<div class="description">
We understood that NEETs and Italy have a <b>strong bond</b>. But you are probably already reasoning on our next question: <b>why</b> is it so? We tried to answer by looking at <b>other compared metrics</b>, one of them being the <b>at-risk-of poverty rate</b>, a valid and general indicator of the socio-economical situation of a country. Look at the graph below: also here, you can <b>change focused country</b> by interacting with the initial map.
</div>

<div class="plot">

```js
const rates = await FileAttachment("./data_EU/EU_poverty_risk_total_PERC_preproc.csv").csv();
let confrontation_rates = rates;

const total_rates = rates.filter(row => row.sex === 'T' && row.geo === 'IT');
let total_conf_rates = "unavailable data";
const EU_mean_value = rates.filter(row => row.sex === 'T' && row.geo === 'EU27_2020');

// Function to create a custom legend
function createLegend(svg, options) {
	const {
		x,          // X position of the legend
		y,          // Y position of the legend
		label1,     // First label text
		color1,     // Color for the first label
		label2,     // Second label text
		color2,     // Color for the second label
		label3,		// Third label text
		color3,		// Color for the Third label
	} = options;

	// Create a group for the legend
	const legendGroup = svg.append("g")
		.attr("class", "custom-legend")
		.attr("transform", `translate(${x}, ${y})`);

	// Add first legend item
	const legendItem1 = legendGroup.append("g").attr("class", "legend-item");
	legendItem1.append("rect")
		.attr("x", 0)
		.attr("y", 4)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color1);
	legendItem1.append("text")
		.attr("x", 30)
		.attr("y", 15)
		.text(label1)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add second legend item
	const legendItem2 = legendGroup.append("g").attr("class", "legend-item");
	legendItem2.append("rect")
		.attr("x", 0)
		.attr("y", 34)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color2);
	legendItem2.append("text")
		.attr("x", 30)
		.attr("y", 45)
		.text(label2)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add third legend item
	const legendItem3 = legendGroup.append("g").attr("class", "legend-item");
	legendItem3.append("rect")
		.attr("x", 0)
		.attr("y", 64)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color3);
	legendItem3.append("text")
		.attr("x", 30)
		.attr("y", 75)
		.text(label3)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");
}

const svg = d3.select("body").append("svg")
		.attr("width", 390)
		.attr("height", 100);

createLegend(svg, {
		x: 10,
		y: 2,
		label1: "Total (Italy)",
		color1: "#000000",
		label2: "European Union",
		color2: "red",
		label3: "Confrontation Country Total",
		color3: "green",
	});

	view(svg.node());

function showPlot3(plot_id, confrontation_country) {
	let plot;
	if (total_conf_rates != "unavailable data") {
		plot = display(
			Plot.plot({
				x: {label: "Year", type: "point"},
				y: {label: "Poverty rate", grid: true, domain: [0,28]},
				geo: {label: "Country", type: "point"},

				marks: [
					Plot.lineY(total_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						marker: "dot",
						channels: {
							total_rates: {
								value: "OBS_VALUE",
								label: "IT Pov. Rate",
							},
						},
						tip: {
							anchor: "bottom",
							fill: "lightgrey",
							format: {
								y: false,
								total_rates: d => `${d}%`,
							}
						}
					}),

					Plot.lineY(EU_mean_value, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "red",
						marker: "circle-stroke",
						channels: {
							EU_mean_value: {
								value: "OBS_VALUE",
								label: "EU Pov. Rate",
							},
						},
						tip: {
							anchor: "left",
							fill: "#ff5959",
							format: {
								x: false,
								y: false,
								EU_mean_value: d => `${d}%`,
							},
						}
					}),

					Plot.lineY(total_conf_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						geo: d => String(d["Geopolitical entity (reporting)"]),
						stroke: "green",
						marker: "circle",
						channels: {
							total_conf_rates: {
								value: "OBS_VALUE",
								label: "Pov. Rate",
							},
							country: {
								value: "Geopolitical entity (reporting)",
								label: "Country"
							}
						},
						tip: {
							anchor: "right",
							fill: "lightgreen",
							format: {
								x: false,
								y: false,
								total_conf_rates: d => `${d}%`,
								country: d => `${d}`,
							},
						}
					}),

					Plot.tip([Selected_Country.value], {anchor: "top-right", frameAnchor: "top-right", pointerSize: 0}),
					Plot.axisX(), //{ticks: []}),
					Plot.ruleY([0]),
				]
			})
		);
	}
	else {
		plot = display(
			Plot.plot({
				x: {label: "Year", type: "point"},
				y: {label: "Poverty rate", grid: true, domain: [0,28]},
				geo: {label: "Country", type: "point"},

				marks: [
					Plot.lineY(total_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						marker: "dot",
						channels: {
							total_rates: {
								value: "OBS_VALUE",
								label: "IT Pov. Rate",
							},
						},
						tip: {
							anchor: "bottom",
							fill: "lightgrey",
							format: {
								y: false,
								total_rates: d => `${d}%`,
							}
						}
					}),

					Plot.lineY(EU_mean_value, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "red",
						marker: "circle-stroke",
						channels: {
							EU_mean_value: {
								value: "OBS_VALUE",
								label: "EU Pov. Rate",
							},
						},
						tip: {
							anchor: "left",
							fill: "#ff5959",
							format: {
								x: false,
								y: false,
								EU_mean_value: d => `${d}%`,
							},
						}
					}),
				
					Plot.axisX(), //{ticks: []}),
					Plot.ruleY([0]),
				]
			})
		);
	}

	return [plot];
}

let plot_viz3;

[plot_viz3] = showPlot3(0, "Italy");

// Unrelated object that listens for changes
const listenerObject = {
    init() {
    // Add an event listener for the 'valueChanged' event
    eventBus.addEventListener('valueChanged', (event) => {
		console.log(
			`Listener of PLOT 3 detected value change from ${event.detail.oldValue} to ${event.detail.newValue}`
		);
		if (event.detail.newValue != event.detail.oldValue) {
			plot_viz3.parentNode.removeChild(plot_viz3);
			(async () => {
				if (event.detail.newValue === "Italy"){
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'IT');
				}
				else if (event.detail.newValue === "Greece") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'EL');
				}
				else if (event.detail.newValue === "Spain") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'ES');
					}
				else if (event.detail.newValue === "France") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'FR');
					}
				else if (event.detail.newValue === "Germany") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'DE');
					}
				else if (event.detail.newValue === "Turkey") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'TR');
					}
				else if (event.detail.newValue === "Poland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'PL');
					}
				else if (event.detail.newValue === "Romania") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'RO');
					}
				else if (event.detail.newValue === "Netherlands") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'NL');
					}
				else if (event.detail.newValue === "Belgium") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'BE');
					}
				else if (event.detail.newValue === "Czechia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'CZ');
					}
				else if (event.detail.newValue === "Portugal") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'PT');
					}
				else if (event.detail.newValue === "Sweden") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'SE');
					}
				else if (event.detail.newValue === "Hungary") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'HU');
					}
				else if (event.detail.newValue === "Austria") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'AT');
					}
				else if (event.detail.newValue === "Bulgaria") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'BG');
					}
				else if (event.detail.newValue === "Denmark") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'DK');
					}
				else if (event.detail.newValue === "Finland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'FI');
					}
				else if (event.detail.newValue === "Slovakia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'SK');
					}
				else if (event.detail.newValue === "Ireland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'IE');
					}
				else if (event.detail.newValue === "Croatia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'HR');
					}
				else if (event.detail.newValue === "Lithuania") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'LT');
					}
				else if (event.detail.newValue === "Slovenia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'SI');
					}
				else if (event.detail.newValue === "Latvia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'LV');
					}
				else if (event.detail.newValue === "Estonia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'EE');
					}
				else if (event.detail.newValue === "Cyprus") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'CY');
					}
				else if (event.detail.newValue === "Luxembourg") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'LU');
					}
				else if (event.detail.newValue === "Malta") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'MT');
					}
				else if (event.detail.newValue === "Iceland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'IS');
					}
				else if (event.detail.newValue === "Switzerland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'CH');
					}
				else if (event.detail.newValue === "Montenegro") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'ME');
					}
				else if (event.detail.newValue === "Serbia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'RS');
					}
				else if (event.detail.newValue === "Macedonia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'MK');
					}
				else if (event.detail.newValue === "Norway") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'NO');
					}
				else if (event.detail.newValue === "United Kingdom") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'UK');
					}
				else {
					total_conf_rates = "unavailable data";
				}

				[plot_viz3] = showPlot3(0, `${event.detail.newValue}`);
			})();
		}
    	});
  	},
};

// Initialize the listener
listenerObject.init();
```

</div>
<div class="plot">
<a href="https://ec.europa.eu/eurostat/web/products-datasets/-/tessi120" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [At-risk-of poverty rate by detailed age group - EU-SILC survey - <b>Eurostat</b>]
  </a>
</div>
</br>

<div class="description">
We can clearly see that people in Italy have a <b>much higher risk of being in poverty</b> than in many other countries. This can seem obvious at first when comparing Italy to other advanced countries with a <b>more stable economy</b> like France, or with <b>nordic countries</b> like Sweeden due to their more developed <b>social welfare</b>, but the situation is <b>far worse in Italy</b> than that: from the start of 2020s, the countries with closer situation in risk of poverty are Greece (Greece and Italy both have a poverty rate of <b>18.9%</b> in 2023), Croatia, Serbia and Montenegro. In this metric, Spain is in a bad scenario, with 20.2% being a worrying value. Interestingly, Estonia and Latvia score a <b>tremendous record</b>, with 22.5%.
</div>
</br>

## Death on Work: a Deterrent Phenomenon?
<div class="description">
May the risk of <b>death on work</b> be related to some sort of <b>"fear of working"</b> in younger generations? We thought it could be interesting to look at this phenomenon to see if the countries with lower rate of NEET also are the ones in which working is safer.
</div>

<div class="plot">

```js
const rates = await FileAttachment("./data_EU/EU_fatal_accidents_total_IR_preproc.csv").csv();
let confrontation_rates = rates;

const total_rates = rates.filter(row => row.sex === 'T' && row.geo === 'IT');
let total_conf_rates = "unavailable data";
const EU_mean_value = rates.filter(row => row.sex === 'T' && row.geo === 'EU27_2020');
const male_rates = rates.filter(row => row.sex === 'M' && row.geo === 'IT');
const female_rates = rates.filter(row => row.sex === 'F' && row.geo === 'IT');

// Function to create a custom legend
function createLegend(svg, options) {
	const {
		x,          // X position of the legend
		y,          // Y position of the legend
		label1,     // First label text
		color1,     // Color for the first label
		label2,     // Second label text
		color2,     // Color for the second label
		label3,		// Third label text
		color3,		// Color for the Third label
		label4,     // Fourth label text
		color4,     // Color for the fourth label
		label5,		// Fifth label text
		color5,		// Color for the fifth label
	} = options;

	// Create a group for the legend
	const legendGroup = svg.append("g")
		.attr("class", "custom-legend")
		.attr("transform", `translate(${x}, ${y})`);

	// Add first legend item
	const legendItem1 = legendGroup.append("g").attr("class", "legend-item");
	legendItem1.append("rect")
		.attr("x", 0)
		.attr("y", 4)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color1);
	legendItem1.append("text")
		.attr("x", 30)
		.attr("y", 15)
		.text(label1)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add second legend item
	const legendItem2 = legendGroup.append("g").attr("class", "legend-item");
	legendItem2.append("rect")
		.attr("x", 0)
		.attr("y", 34)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color2);
	legendItem2.append("text")
		.attr("x", 30)
		.attr("y", 45)
		.text(label2)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add third legend item
	const legendItem3 = legendGroup.append("g").attr("class", "legend-item");
	legendItem3.append("rect")
		.attr("x", 0)
		.attr("y", 64)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color3);
	legendItem3.append("text")
		.attr("x", 30)
		.attr("y", 75)
		.text(label3)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");
	
	// Add fourth legend item
	const legendItem4 = legendGroup.append("g").attr("class", "legend-item");
	legendItem4.append("rect")
		.attr("x", 250)
		.attr("y", 4)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color4);
	legendItem4.append("text")
		.attr("x", 280)
		.attr("y", 15)
		.text(label4)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add fifth legend item
	const legendItem5 = legendGroup.append("g").attr("class", "legend-item");
	legendItem5.append("rect")
		.attr("x", 250)
		.attr("y", 34)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color5);
	legendItem5.append("text")
		.attr("x", 280)
		.attr("y", 45)
		.text(label5)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");
}

const svg = d3.select("body").append("svg")
		.attr("width", 390)
		.attr("height", 100);

createLegend(svg, {
		x: 10,
		y: 2,
		label1: "Total (Italy)",
		color1: "#000000",
		label2: "European Union",
		color2: "red",
		label3: "Confrontation Country Total",
		color3: "green",
		label4: "Female (Italy)",
		color4: "lightpink",
		label5: "Male (Italy)",
		color5: "steelblue",

	});

	view(svg.node());

function showPlot3(plot_id, confrontation_country) {
	let plot;
	if (total_conf_rates != "unavailable data") {
		plot = display(
			Plot.plot({
				x: {label: "Year", type: "point"},
				y: {label: "Incidence rate", grid: true, domain: [0,15]},
				geo: {label: "Country", type: "point"},

				marks: [
					Plot.lineY(total_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						marker: "dot",
						channels: {
							total_rates: {
								value: "OBS_VALUE",
								label: "IT Inc. Rate",
							},
						},
						tip: {
							anchor: "bottom",
							fill: "lightgrey",
							format: {
								y: false,
								total_rates: d => `${d}%`,
							}
						}
					}),

					Plot.lineY(EU_mean_value, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "red",
						marker: "circle-stroke",
						channels: {
							EU_mean_value: {
								value: "OBS_VALUE",
								label: "EU Inc. Rate",
							},
						},
						tip: {
							anchor: "left",
							fill: "#ff5959",
							format: {
								x: false,
								y: false,
								EU_mean_value: d => `${d}%`,
							},
						}
					}),

					Plot.lineY(male_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "steelblue",
						marker: "tick-x",
						opacity: 0.4,
						channels: {
							male_rates: {
								value: "OBS_VALUE",
								label: "Inc. Rate",
							},
						},
					}),

					Plot.lineY(female_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "lightpink",
						marker: "tick-y",
						opacity: 0.4,
						channels: {
							female_rates: {
								value: "OBS_VALUE",
								label: "Inc. Rate",
							},
						},
					}),

					Plot.lineY(total_conf_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						geo: d => String(d["Geopolitical entity (reporting)"]),
						stroke: "green",
						marker: "circle",
						channels: {
							total_conf_rates: {
								value: "OBS_VALUE",
								label: "Inc. Rate",
							},
							country: {
								value: "Geopolitical entity (reporting)",
								label: "Country"
							}
						},
						tip: {
							anchor: "right",
							fill: "lightgreen",
							format: {
								x: false,
								y: false,
								total_conf_rates: d => `${d}%`,
								country: d => `${d}`,
							},
						}
					}),

					Plot.tip([Selected_Country.value], {anchor: "top-right", frameAnchor: "top-right", pointerSize: 0}),
					Plot.axisX(), //{ticks: []}),
					Plot.ruleY([0]),
				]
			})
		);
	}
	else {
		plot = display(
			Plot.plot({
				x: {label: "Year", type: "point"},
				y: {label: "Inc. rate", grid: true, domain: [0,15]},
				geo: {label: "Country", type: "point"},

				marks: [
					Plot.lineY(total_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						marker: "dot",
						channels: {
							total_rates: {
								value: "OBS_VALUE",
								label: "IT Inc. Rate",
							},
						},
						tip: {
							anchor: "bottom",
							fill: "lightgrey",
							format: {
								y: false,
								total_rates: d => `${d}%`,
							}
						}
					}),

					Plot.lineY(EU_mean_value, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "red",
						marker: "circle-stroke",
						channels: {
							EU_mean_value: {
								value: "OBS_VALUE",
								label: "EU Inc. Rate",
							},
						},
						tip: {
							anchor: "left",
							fill: "#ff5959",
							format: {
								x: false,
								y: false,
								EU_mean_value: d => `${d}%`,
							},
						}
					}),

					Plot.lineY(male_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "steelblue",
						marker: "tick-x",
						opacity: 0.4,
						channels: {
							male_rates: {
								value: "OBS_VALUE",
								label: "Inc. Rate",
							},
						},
					}),

					Plot.lineY(female_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "lightpink",
						marker: "tick-y",
						opacity: 0.4,
						channels: {
							female_rates: {
								value: "OBS_VALUE",
								label: "Inc. Rate",
							},
						},
					}),
				
					Plot.axisX(), //{ticks: []}),
					Plot.ruleY([0]),
				]
			})
		);
	}

	return [plot];
}

let plot_viz3;

[plot_viz3] = showPlot3(0, "Italy");

// Unrelated object that listens for changes
const listenerObject = {
    init() {
    // Add an event listener for the 'valueChanged' event
    eventBus.addEventListener('valueChanged', (event) => {
		console.log(
			`Listener of PLOT 3 detected value change from ${event.detail.oldValue} to ${event.detail.newValue}`
		);
		if (event.detail.newValue != event.detail.oldValue) {
			plot_viz3.parentNode.removeChild(plot_viz3);
			(async () => {
				if (event.detail.newValue === "Italy"){
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'IT');
				}
				else if (event.detail.newValue === "Greece") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'EL');
				}
				else if (event.detail.newValue === "Spain") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'ES');
					}
				else if (event.detail.newValue === "France") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'FR');
					}
				else if (event.detail.newValue === "Germany") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'DE');
					}
				else if (event.detail.newValue === "Turkey") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'TR');
					}
				else if (event.detail.newValue === "Poland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'PL');
					}
				else if (event.detail.newValue === "Romania") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'RO');
					}
				else if (event.detail.newValue === "Netherlands") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'NL');
					}
				else if (event.detail.newValue === "Belgium") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'BE');
					}
				else if (event.detail.newValue === "Czechia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'CZ');
					}
				else if (event.detail.newValue === "Portugal") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'PT');
					}
				else if (event.detail.newValue === "Sweden") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'SE');
					}
				else if (event.detail.newValue === "Hungary") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'HU');
					}
				else if (event.detail.newValue === "Austria") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'AT');
					}
				else if (event.detail.newValue === "Bulgaria") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'BG');
					}
				else if (event.detail.newValue === "Denmark") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'DK');
					}
				else if (event.detail.newValue === "Finland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'FI');
					}
				else if (event.detail.newValue === "Slovakia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'SK');
					}
				else if (event.detail.newValue === "Ireland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'IE');
					}
				else if (event.detail.newValue === "Croatia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'HR');
					}
				else if (event.detail.newValue === "Lithuania") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'LT');
					}
				else if (event.detail.newValue === "Slovenia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'SI');
					}
				else if (event.detail.newValue === "Latvia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'LV');
					}
				else if (event.detail.newValue === "Estonia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'EE');
					}
				else if (event.detail.newValue === "Cyprus") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'CY');
					}
				else if (event.detail.newValue === "Luxembourg") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'LU');
					}
				else if (event.detail.newValue === "Malta") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'MT');
					}
				else if (event.detail.newValue === "Iceland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'IS');
					}
				else if (event.detail.newValue === "Switzerland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'CH');
					}
				else if (event.detail.newValue === "Montenegro") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'ME');
					}
				else if (event.detail.newValue === "Serbia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'RS');
					}
				else if (event.detail.newValue === "Macedonia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'MK');
					}
				else if (event.detail.newValue === "Norway") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'NO');
					}
				else if (event.detail.newValue === "United Kingdom") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'UK');
					}
				else {
					total_conf_rates = "unavailable data";
				}

				[plot_viz3] = showPlot3(0, `${event.detail.newValue}`);
			})();
		}
    	});
  	},
};

// Initialize the listener
listenerObject.init();
```

</div>
<div class="plot">
<a href="https://ec.europa.eu/eurostat/web/products-datasets/-/sdg_08_60" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Fatal accidents at work per 100 000 workers, by sex - <b>Eurostat</b>]
  </a>
</div>
</br>

<div class="description">
We discovered that there is <b>no relation</b> between these two metrics, but, unsurprisingly, Germany, Finland and nordic countries are <b>way safer</b> than the western europe ones, these last being not so different from the balcans or slavic countries in term of safety at work. Italy is <b>better than many countries</b> in this regard, with a general lower rate than France in the last measurement. 
</div>
</br>

## Am I a NEET or an Unrecognized Caretaker?
<div class="description">
In an european society that is becoming mainly populated by elders, the <b>caretaker</b> is emerging as a fundamental social and family role. Many young people are caretakers and this sometimes can force them to reconsider their life choices, favouring the caring responsibilities over career or scolarship. It is natural to think that NEETs and caretakers could in some way be related.
</div>

<div class="plot">

```js
const rates = await FileAttachment("./data_EU/EU_outside_labour_4_caring_total_PERC_preproc.csv").csv();
let confrontation_rates = rates;

const total_rates = rates.filter(row => row.sex === 'T' && row.geo === 'IT');
let total_conf_rates = "unavailable data";
const EU_mean_value = rates.filter(row => row.sex === 'T' && row.geo === 'EU27_2020');
const male_rates = rates.filter(row => row.sex === 'M' && row.geo === 'IT');
const female_rates = rates.filter(row => row.sex === 'F' && row.geo === 'IT');

// Function to create a custom legend
function createLegend(svg, options) {
	const {
		x,          // X position of the legend
		y,          // Y position of the legend
		label1,     // First label text
		color1,     // Color for the first label
		label2,     // Second label text
		color2,     // Color for the second label
		label3,		// Third label text
		color3,		// Color for the Third label
		label4,     // Fourth label text
		color4,     // Color for the fourth label
		label5,		// Fifth label text
		color5,		// Color for the fifth label
	} = options;

	// Create a group for the legend
	const legendGroup = svg.append("g")
		.attr("class", "custom-legend")
		.attr("transform", `translate(${x}, ${y})`);

	// Add first legend item
	const legendItem1 = legendGroup.append("g").attr("class", "legend-item");
	legendItem1.append("rect")
		.attr("x", 0)
		.attr("y", 4)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color1);
	legendItem1.append("text")
		.attr("x", 30)
		.attr("y", 15)
		.text(label1)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add second legend item
	const legendItem2 = legendGroup.append("g").attr("class", "legend-item");
	legendItem2.append("rect")
		.attr("x", 0)
		.attr("y", 34)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color2);
	legendItem2.append("text")
		.attr("x", 30)
		.attr("y", 45)
		.text(label2)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add third legend item
	const legendItem3 = legendGroup.append("g").attr("class", "legend-item");
	legendItem3.append("rect")
		.attr("x", 0)
		.attr("y", 64)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color3);
	legendItem3.append("text")
		.attr("x", 30)
		.attr("y", 75)
		.text(label3)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");
	
	// Add fourth legend item
	const legendItem4 = legendGroup.append("g").attr("class", "legend-item");
	legendItem4.append("rect")
		.attr("x", 250)
		.attr("y", 4)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color4);
	legendItem4.append("text")
		.attr("x", 280)
		.attr("y", 15)
		.text(label4)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");

	// Add fifth legend item
	const legendItem5 = legendGroup.append("g").attr("class", "legend-item");
	legendItem5.append("rect")
		.attr("x", 250)
		.attr("y", 34)
		.attr("width", 20)
		.attr("height", 20)
		.attr("fill", color5);
	legendItem5.append("text")
		.attr("x", 280)
		.attr("y", 45)
		.text(label5)
		.style("font-size", "14px")
		.attr("alignment-baseline", "middle");
}

const svg = d3.select("body").append("svg")
		.attr("width", 390)
		.attr("height", 100);

createLegend(svg, {
		x: 10,
		y: 2,
		label1: "Total (Italy)",
		color1: "#000000",
		label2: "European Union",
		color2: "red",
		label3: "Confrontation Country Total",
		color3: "green",
		label4: "Female (Italy)",
		color4: "lightpink",
		label5: "Male (Italy)",
		color5: "steelblue",

	});

	view(svg.node());

function showPlot3(plot_id, confrontation_country) {
	let plot;
	if (total_conf_rates != "unavailable data") {
		plot = display(
			Plot.plot({
				x: {label: "Year", type: "point"},
				y: {label: "Outside Labour (%)", grid: true, domain: [0,4]},
				geo: {label: "Country", type: "point"},

				marks: [
					Plot.lineY(total_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						marker: "dot",
						channels: {
							total_rates: {
								value: "OBS_VALUE",
								label: "IT Outside",
							},
						},
						tip: {
							anchor: "bottom",
							fill: "lightgrey",
							format: {
								y: false,
								total_rates: d => `${d}%`,
							}
						}
					}),

					Plot.lineY(EU_mean_value, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "red",
						marker: "circle-stroke",
						channels: {
							EU_mean_value: {
								value: "OBS_VALUE",
								label: "EU Outside",
							},
						},
						tip: {
							anchor: "left",
							fill: "#ff5959",
							format: {
								x: false,
								y: false,
								EU_mean_value: d => `${d}%`,
							},
						}
					}),

					Plot.lineY(male_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "steelblue",
						marker: "tick-x",
						opacity: 0.4,
						channels: {
							male_rates: {
								value: "OBS_VALUE",
								label: "Outside",
							},
						},
					}),

					Plot.lineY(female_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "lightpink",
						marker: "tick-y",
						opacity: 0.4,
						channels: {
							female_rates: {
								value: "OBS_VALUE",
								label: "Outside",
							},
						},
					}),

					Plot.lineY(total_conf_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						geo: d => String(d["Geopolitical entity (reporting)"]),
						stroke: "green",
						marker: "circle",
						channels: {
							total_conf_rates: {
								value: "OBS_VALUE",
								label: "Outside",
							},
							country: {
								value: "Geopolitical entity (reporting)",
								label: "Country"
							}
						},
						tip: {
							anchor: "right",
							fill: "lightgreen",
							format: {
								x: false,
								y: false,
								total_conf_rates: d => `${d}%`,
								country: d => `${d}`,
							},
						}
					}),

					Plot.tip([Selected_Country.value], {anchor: "top-right", frameAnchor: "top-right", pointerSize: 0}),
					Plot.axisX(), //{ticks: []}),
					Plot.ruleY([0]),
				]
			})
		);
	}
	else {
		plot = display(
			Plot.plot({
				x: {label: "Year", type: "point"},
				y: {label: "Outside Labour (%)", grid: true, domain: [0,4]},
				geo: {label: "Country", type: "point"},

				marks: [
					Plot.lineY(total_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						marker: "dot",
						channels: {
							total_rates: {
								value: "OBS_VALUE",
								label: "IT Outside",
							},
						},
						tip: {
							anchor: "bottom",
							fill: "lightgrey",
							format: {
								y: false,
								total_rates: d => `${d}%`,
							}
						}
					}),

					Plot.lineY(EU_mean_value, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "red",
						marker: "circle-stroke",
						channels: {
							EU_mean_value: {
								value: "OBS_VALUE",
								label: "EU Outside",
							},
						},
						tip: {
							anchor: "left",
							fill: "#ff5959",
							format: {
								x: false,
								y: false,
								EU_mean_value: d => `${d}%`,
							},
						}
					}),

					Plot.lineY(male_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "steelblue",
						marker: "tick-x",
						opacity: 0.4,
						channels: {
							male_rates: {
								value: "OBS_VALUE",
								label: "Outside",
							},
						},
					}),

					Plot.lineY(female_rates, {
						x: d => String(d["TIME_PERIOD"]),
						y: d => Number(d["OBS_VALUE"]),
						stroke: "lightpink",
						marker: "tick-y",
						opacity: 0.4,
						channels: {
							female_rates: {
								value: "OBS_VALUE",
								label: "Outside",
							},
						},
					}),
				
					Plot.axisX(), //{ticks: []}),
					Plot.ruleY([0]),
				]
			})
		);
	}

	return [plot];
}

let plot_viz3;

[plot_viz3] = showPlot3(0, "Italy");

// Unrelated object that listens for changes
const listenerObject = {
    init() {
    // Add an event listener for the 'valueChanged' event
    eventBus.addEventListener('valueChanged', (event) => {
		console.log(
			`Listener of PLOT 3 detected value change from ${event.detail.oldValue} to ${event.detail.newValue}`
		);
		if (event.detail.newValue != event.detail.oldValue) {
			plot_viz3.parentNode.removeChild(plot_viz3);
			(async () => {
				if (event.detail.newValue === "Italy"){
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'IT');
				}
				else if (event.detail.newValue === "Greece") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'EL');
				}
				else if (event.detail.newValue === "Spain") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'ES');
					}
				else if (event.detail.newValue === "France") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'FR');
					}
				else if (event.detail.newValue === "Germany") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'DE');
					}
				else if (event.detail.newValue === "Turkey") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'TR');
					}
				else if (event.detail.newValue === "Poland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'PL');
					}
				else if (event.detail.newValue === "Romania") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'RO');
					}
				else if (event.detail.newValue === "Netherlands") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'NL');
					}
				else if (event.detail.newValue === "Belgium") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'BE');
					}
				else if (event.detail.newValue === "Czechia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'CZ');
					}
				else if (event.detail.newValue === "Portugal") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'PT');
					}
				else if (event.detail.newValue === "Sweden") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'SE');
					}
				else if (event.detail.newValue === "Hungary") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'HU');
					}
				else if (event.detail.newValue === "Austria") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'AT');
					}
				else if (event.detail.newValue === "Bulgaria") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'BG');
					}
				else if (event.detail.newValue === "Denmark") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'DK');
					}
				else if (event.detail.newValue === "Finland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'FI');
					}
				else if (event.detail.newValue === "Slovakia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'SK');
					}
				else if (event.detail.newValue === "Ireland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'IE');
					}
				else if (event.detail.newValue === "Croatia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'HR');
					}
				else if (event.detail.newValue === "Lithuania") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'LT');
					}
				else if (event.detail.newValue === "Slovenia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'SI');
					}
				else if (event.detail.newValue === "Latvia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'LV');
					}
				else if (event.detail.newValue === "Estonia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'EE');
					}
				else if (event.detail.newValue === "Cyprus") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'CY');
					}
				else if (event.detail.newValue === "Luxembourg") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'LU');
					}
				else if (event.detail.newValue === "Malta") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'MT');
					}
				else if (event.detail.newValue === "Iceland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'IS');
					}
				else if (event.detail.newValue === "Switzerland") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'CH');
					}
				else if (event.detail.newValue === "Montenegro") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'ME');
					}
				else if (event.detail.newValue === "Serbia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'RS');
					}
				else if (event.detail.newValue === "Macedonia") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'MK');
					}
				else if (event.detail.newValue === "Norway") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'NO');
					}
				else if (event.detail.newValue === "United Kingdom") {
					total_conf_rates = confrontation_rates.filter(row => row.sex === 'T' && row.geo === 'UK');
					}
				else {
					total_conf_rates = "unavailable data";
				}

				[plot_viz3] = showPlot3(0, `${event.detail.newValue}`);
			})();
		}
    	});
  	},
};

// Initialize the listener
listenerObject.init();
```

</div>
<div class="plot">
<a href="https://ec.europa.eu/eurostat/web/products-datasets/-/sdg_05_40" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Persons outside the labour force due to caring responsibilities by sex - <b>Eurostat</b>]
  </a>
</div>
</br>

<div class="description">
Surprisingly, they are <b>not strongly related</b>. If we take Romania, we can see that the people outside of labour force due to caring responsibility are way lower than their italian counterpart, but the NEET phenomenon is much higher. Germany, in 2020s is close to Italy in this metric, but NEETs are lower. This seems to indicate that in the last years, italian caretakers are <b>more and more expert</b> in managing their <b>balance</b> between caretaking and employment, resulting in a <b>reduction of the phenomenon</b> that is now more or less in line with other advanced countries. This may also be due the fact that <b>many initiatives</b> to reitroduce caretakers in the academia have been performed: an example is universities creating <b>favourable payment regimes</b> for this category.   
</div>

  