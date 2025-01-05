<link rel="stylesheet" href="style.css">

<div class="hero">

# NEET in Italy

</div>

```js

import * as topojson from "topojson-client";

import { createSelector } from "./selector.js";

const NeetByRegion = await FileAttachment("./final/Neet_1529_regions.csv").csv(); 
const years = ["2018", "2019", "2020", "2021", "2022", "2023"];




/*const selected_year_1 = Inputs.select(years, {value: "2023", label: "Year:", format: (d) => d});
view(selected_year_1);*/


const Neet = {};


years.forEach(year => {
	Neet[`${year}`] = NeetByRegion.filter(row => row["TIME"] === String(year) && row["Territorio"] != "Italia");
});



const italy = await FileAttachment("./final/limits_IT_regions.topo.json").json();
const regions = topojson.feature(italy, italy.objects[Object.keys(italy.objects)[0]])
//const regions = topojson.feature(italy, italy.features);

var min, max;
min = Number(Neet["2018"][0]["Value"]);
max = Number(Neet["2018"][0]["Value"]);

for (let i in years) {
	let year = years[i];
	for(let j in Neet[`${year}`]) {
		//if (j == "columns") continue;

		let value = Number(Neet[`${year}`][j]["Value"]);

		if (value > max) max = value;
		else if (value < min) min = value;
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

	return val + ` × 10${true_exp}`;
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
/*
let zoom_info = [
	{zoomed: false, trans_x: 0, trans_y: 0},
	{zoomed: false, trans_x: 0, trans_y: 0},
	{zoomed: false, trans_x: 0, trans_y: 0},
	{zoomed: false, trans_x: 0, trans_y: 0}
];*/

```
<div class="container">
<div class="plot">

```js

const displayPlot1 = display;

function showPlot1(plot_id, data, column_name, column_label) {

	const NeetValue = new Map(data.map(d => [d["Territorio"], d[column_name]]))
	
	let plot_legend = displayPlot1(
		Plot.legend({
		  color: {
			interpolate: x => colorScale(x*max + min, min, max),
			domain: [min, max],
			label: column_label, 
		  },
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  tickFormat: d => d + "K",
		  label: "Neet amount"
		})
	);

	const mProjection = d3.geoEqualEarth().scale(50)
	
	console.log(NeetValue);

	console.log(min);
	console.log(max);

	let plot = displayPlot1(Plot.plot({
		mProjection,
		width: 640,
		height: 640,
		className: "Za-Warudo",
		marks: [
		Plot.geo(regions, Plot.centroid({
			fill: d => colorScale(Number(NeetValue.get(d.properties.reg_name)), min, max),
		  	//tip: {className: "Za-Warudo-Tip"},
		  	title: d => d.properties.reg_name,

		})),
		Plot.axisX({ticks: []}),
		Plot.axisY({ticks: []}),
	  ]
	}));

	let g = plot.childNodes[1];
	//let tip = plot.childNodes[2];

	g.style.transition = "transform 0.3s ease-in 0s";

	g.style.transform = "";

	//zoom_info[plot_id] = {zoomed: false, trans_x: 0, trans_y: 0};

	g.childNodes.forEach(c => {
    	
		c.addEventListener("mouseover", (e) => {

			let region = e.target.childNodes[0].innerHTML;
			let neet = NeetValue.get(region);
			//let emissions = EmissionByName.get(country);

			neet = numToScientific(neet * 1000);
			//emissions = numToScientific(emissions);

			let tip = document.getElementsByClassName("italy-tooltip")[plot_id];

			console.log(tip);

			tip.style.visibility = "visible";

			tip.innerHTML = `<span><b>Region:</b> ${region}</span><br/>
				<span><b>Neet</b>: ${neet} people</span>`;
			
		})
		c.addEventListener("mouseout", (e) => {

			let tip = document.getElementsByClassName("italy-tooltip")[plot_id];
			tip.style.visibility = "hidden";
		})
	});

	return [plot, plot_legend];

}

let plot1;
let plot1_legend;
let selector = createSelector(years, (value) => {
	
	if (plot1 != undefined) {
    plot1.parentNode.removeChild(plot1);
  }
  if (plot1_legend != undefined) {
    plot1_legend.parentNode.removeChild(plot1_legend);
  }
  
  [plot1, plot1_legend] = showPlot1(0, Neet[2018 + Math.round(value * 5 / 100)], "Value", "Value");

});

view(selector);

[plot1, plot1_legend] = showPlot1(0, Neet[2023], "Value", "Value");



/*
document.getElementsByClassName("unzoom")[0].addEventListener("click", () => {

	let g = plot1.childNodes[1];
	g.style.transform = "";
	zoom_info[0] = {zoomed: false, trans_x: 0, trans_y: 0};

});*/

```
<div class="italy-tooltip">tooltip</div>
</div>
</div>