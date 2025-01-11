<link rel="stylesheet" href="style.css">

<div class="hero">

# NEET in Italy

</div>

# What NEETs are, and why they are a problem

<br/>
"NEET" is a term that is recently getting more and more used, but what does it mean and what does it represent?<br/>
NEET is an acronym for "Not in Education, Employment, or Training"; a NEET is a person who is unemployed and is not receiving education or formal training of any kind, a kind of individual that in the last decade, especially during the COVID outbreak, became more and more common. The last few years saw a steep betterment of the situation, but we'll show that here in Italy we cannot rest easy yet and we still need to tackle this problem.
<br/>
<br/>
<div class="container">
<div class="plot">


## Employment Rate vs NEET Rate

```js

const rates = await FileAttachment("./final/italy_employment_vs_neet_rate.csv").csv();

console.log(rates);

const y2 = d3.scaleLinear(d3.extent(rates, d => Number(d["Neet_Rate"])), [52, 68]);

display(
	Plot.plot({
		x: {label: "year", type: "point"},
		y: {axis: "left", label: "employment rate", domain: [50,70]},
		
		marks: [
			Plot.axisY(y2.ticks(), {
				color: "steelblue", 
				anchor: "right", 
				label: "neet rate", 
				y: y2, 
				tickFormat: y2.tickFormat()
			}),
			Plot.lineY(rates, {
				x: "Year",
				y: d => Number(d["Employment_Rate"]),
				tip: {
					format: {
						y: d => `${d}%`
					}
				},
			}),
			Plot.lineY(rates, 
				Plot.mapY((D) => D.map(y2), {
					x: "Year", 
					y: d => Number(d["Neet_Rate"]), 
					stroke: "steelblue", 
					channels: {
						neet_rate: {
							value: "Neet_Rate",
							label: "neet rate"
						}
					},
					tip: {
						format: {
							y: false,
							neet_rate: d => `${d}%`
						}
							
					}
				})
			),
			Plot.ruleY([50])
		]
	})
);

```

</div>
</div>

<br />

<p class="description">
	The trends show that in the last 2 years we've been experiencing an improvement in terms of increase of 
	the employment rate and reduction of the neet rate. However, do not be fooled: you may notice that neither 
	axis on the previous chart starts at y = 0. While the neet rate seems to have followed, with inverted 
	proportionality, the employment trend we must be aware that we barely moved from 1 young person unwilling 
	to work every 4, to 1 every 6 in 2023; while this is indeed a respectable achievement that amount is still 
	way to high to consider the problem close to be solved. The worst part? The economy recover after the covid 
	lockdown enabled some generational replacement in the workforce, but this trend is not guaranteed to continue 
	in the following years.
</p>

<br/>

<div class="container">
<div class="plot">


## Inactive Citizens in Italy 

```js

const actual_data = await FileAttachment("./final/inattivi.csv").csv();
const predicted_data = await FileAttachment("./final/inattivi_pred.csv").csv();

const predictionPlot = Plot.plot({
	x: {label: "Year", domain: [2004, 2027], tickFormat: d3.format(",.1c")},
	y: {label: "Neet Amount", domain: [50, 80], tickFormat: d => `${d}K`},
	marks: [
		Plot.lineY(
			actual_data, {
				x: "Time",
				y: d => Number(d["Total"]),
				tip: {
					format: {
						x: d3.format(",.1c"),
						y: d => `${d}K`
					}
				}
				// tip: {
				// 	format: {
				// 		y: d => `${d}%`
				// 	}
				// },
			}
		),
		Plot.areaY(
			predicted_data, {
				x: "Time",
				y1: d => Number(d["Low"]),
				y2: d => Number(d["High"]),
				fill: "steelblue",
			}
		),
		Plot.lineY(
			predicted_data, {
				x: "Time",
				y: d => Number(d["Predicted"]),
				strokeDasharray: "8 4",
				channels: {
						predicted_amount: {
							value: "Predicted",
							label: "Predicted Amount"
						},
						upper_bound: {
							value: "High",
							label: "Upper Bound"
						},
						lower_bound: {
							value: "Low",
							label: "Lower Bound"
						}
					},
				tip: {
					format: {
						x: d3.format(",.1c"),
						predicted_amount: d => `${Number(d).toFixed(2)}K`,
						upper_bound: d => `${Number(d).toFixed(2)}K`,
						lower_bound: d => `${Number(d).toFixed(2)}K`,
						y: false
					}
				}
			}
		),
		Plot.ruleY([50])
	]
}
);

display(predictionPlot);

```


</div>
</div>
<br/>

<p class="description">
Indeed we can see that the amount of NEETs in Italy has since long surpassed the 70K people, and even the most optimistic forecasts predict that we are unlikely to see levels like 20 years ago for a while.
</p>

<br/>

<h1 class="smaller-header"> What are the consequences of this phenomenon? </h1>

<br/>

<div class="container">
<div class="plot">

## Percentages of working population in Italy, divided by age group

```js

let occupied = await FileAttachment("./final/occupati.csv").csv();
occupied = occupied.filter(d => d["Territorio"] == "Italia" && d["Sesso"] == "totale" && years.includes(String(d["TIME"])));

const ageGroups = ["Y15-24", "Y25-34", "Y35-44", "Y45-54", "Y55-64"];

occupied = occupied.filter(d => ageGroups.includes(d["ETA1"]));

const occupiedByYear = {}

for (let j in years) {
	occupiedByYear[years[j]] = occupied.filter(d => String(d["TIME"]) == years[j])
}

function showPieChart(year) {

	let data = occupiedByYear[year]

	let total = data.reduce((acc, d) => acc += Number(d["Value"]), 0);
	console.log(total);

	const width = 928;
	const height = Math.min(width, 500);

	const tooltip = d3.select("#pie-tooltip")
		.append("div")
		.style("position", "fixed")
		.style("visibility", "hidden")
		.style("background-color", "white")
		.style("margin", "0")
		.style("padding","14px")
		.style("border-radius", "3px")
		.style("border","1px solid black")
		.text("example");

	// Create the color scale.
	const color = d3.scaleOrdinal()
		.domain(data.map(d => d["ETA1"]))
		.range(d3.quantize(t => d3.interpolateSpectral(t * 0.8 + 0.1), data.length).reverse())

	// Create the pie layout and arc generator.
	const pie = d3.pie()
		.sort(null)
		.value(d => d["Value"]);

	const arc = d3.arc()
		.innerRadius(0)
		.outerRadius(Math.min(width, height) / 2 - 1);

	const labelRadius = arc.outerRadius()() * 0.8;

	// A separate arc generator for labels.
	const arcLabel = d3.arc()
		.innerRadius(labelRadius)
		.outerRadius(labelRadius);

	const arcs = pie(data);

	// Create the SVG container.
	const svg = d3.create("svg")
		.attr("width", width)
		.attr("height", height)
		.attr("viewBox", [-width / 2, -height / 2, width, height])
		.attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");

	// Add a sector path for each value.
	svg.append("g")
		.attr("stroke", "white")
	.selectAll()
	.data(arcs)
	.join("path")
		.attr("fill", d => color(d.data["ETA1"]))
		.attr("d", arc)
		.attr('opacity', 0.85)
		.on('mouseover', function (event) {

			d3.select(this.parentNode).selectAll("path")
				.transition()
				.duration('50')
				.attr('opacity', '0.5')

			d3.select(this).transition()
				.duration('50')
				.attr('opacity', '1');

			tooltip.style("visibility", "visible");

		})
		.on("mousemove", function(event){

		const data = event.target.__data__;
		
		tooltip
			.html(`
				<b>Age group</b>: ${data.data["ETA1"]}<br/>
				<b>Amount</b>: ${Number(data.data["Value"]).toFixed(0)}K
			`) 
			.style("top", (event.clientY + 20)+"px").style("left",(event.clientX + 20)+"px");

		})
		.on('mouseout', function (event) {
		
			console.log(this.parentNode);
			d3.select(this.parentNode).selectAll("path").transition()
				.duration('50')
				.attr('opacity', '0.85')

			tooltip.style("visibility", "hidden");
		})
		.append("title")
			.text(d => `${d.data["ETA1"]}: ${Number(d.data["Value"]).toFixed(0)}K`);

	// Create a new arc generator to place a label close to the edge.
	// The label shows the value if there is enough room.
	svg.append("g")
		.attr("text-anchor", "middle")
	.selectAll()
	.data(arcs)
	.join("text")
		.attr("transform", d => `translate(${arcLabel.centroid(d)})`)
		.call(text => text.append("tspan")
			.attr("y", "-0.4em")
			.attr("font-weight", "bold")
			.attr("font-size","small")
			.text(d => d.data["ETA1"]))
		.call(text => text.filter(d => (d.endAngle - d.startAngle) > 0.25).append("tspan")
			.attr("x", 0)
			.attr("y", "0.7em")
			.attr("fill-opacity", 0.7)
			.attr("font-size","small")
			.text(d => `${(Number(d.data["Value"]) / total * 100).toFixed(2)}%`));

	return svg.node();
}

let pieChart;

let selectorPie = createSelector(years, (value) => {
	
	if (pieChart != undefined) {
    	pieChart.parentNode.removeChild(pieChart);
  	}

  pieChart = showPieChart(2018 + Math.round(value * 5 / 100));

  view(pieChart);

});

pieChart = showPieChart(2023);

view(pieChart);
```
<div id="pie-tooltip"></div>
</div>

```js
view(selectorPie);
```

</div>
<br/>

<p class="description">
	We can see how very young people are incredibly under-represented in the job market, so much that it is noticeable even in a pie chart: this is mostly caused by them 
	continuing their studies to improve their opportunities, which is not a problem. Nontheless, we're facing the issue that the majority
	of the current workforce is composed by people that are relatively close to retirement (almost 53% of all the workers are people over 45) 
	and, for this reason, the continuation of a phenomenom where young individuals CHOOSE not to work at all is expected to be
	pretty catastrophic in the foreseeable future.

</p>

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

<br/>

<h1 class="smaller-header"> Where are the Neet? </h1>
<br/>
<div class="container">
<div class="plot">

## NEET amount per region in Italy 

```js

const displayPlotItaly = display;

function showPlotItaly(plot_id, data, column_name, column_label) {

	const NeetValue = new Map(data.map(d => [d["Territorio"], d[column_name]]))
	
	let plot_legend = displayPlotItaly(
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

	const mProjection = d3.geoEqualEarth().scale(50);
	
	let plot = displayPlotItaly(Plot.plot({
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

let plotItaly;
let plotItalyLegend;
let selector = createSelector(years, (value) => {
	
	if (plotItaly != undefined) {
    plotItaly.parentNode.removeChild(plotItaly);
  }
  if (plotItalyLegend != undefined) {
    plotItalyLegend.parentNode.removeChild(plotItalyLegend);
  }
  
  [plotItaly, plotItalyLegend] = showPlotItaly(0, Neet[2018 + Math.round(value * 5 / 100)], "Value", "Value");

});

[plotItaly, plotItalyLegend] = showPlotItaly(0, Neet[2023], "Value", "Value");

/*
document.getElementsByClassName("unzoom")[0].addEventListener("click", () => {

	let g = plot1.childNodes[1];
	g.style.transform = "";
	zoom_info[0] = {zoomed: false, trans_x: 0, trans_y: 0};

});*/

```
<div class="italy-tooltip">tooltip</div>
</div>

```js
view(selector);
```

</div>

<p class="description">
	We can see that NEETs are present all across Italy, with somewhat a higher concentration in the more southern 
	regions. This visualization, however, favours a bit too much smaller regions, since it shows absolute values 
	instead of per capita one (thus, of course Molise and Valle d'Aosta are completely yellow). So we propose another
	one with values shown in percentage with respect to the population of each region.
</p>

<br/>

<div class="container">
<div class="plot">

## NEET percentage of the population per region, in Italy 

```js

const population = await FileAttachment("./final/popolazione_regioni.csv").csv();

const populationMap = {};
for(let i = 2018; i < 2024; ++i) {
	populationMap[i] = {};
}

population.map((d) => {
	populationMap[Number(d["TIME"]) - 1][d["Territory"]] = d["Value"];
})

var min2, max2;
min2 = Number(Neet["2018"][0]["Value"])*1000 / Number(populationMap["2018"][Neet["2018"][0]["Territorio"]]);
max2 = min2;

for (let i in years) {
	let year = years[i];
	for(let j in Neet[`${year}`]) {
		//if (j == "columns") continue;

		let region = Neet[`${year}`][j];
		let value = Number(region["Value"]) * 1000 / Number(populationMap[`${year}`][region["Territorio"]]);
		if (value > max2) max2 = value;
		else if (value < min2) min2 = value;
	}
}



const displayPlotItaly2 = display;

function showPlotItaly2(year) {

	const data = Neet[year];

	const NeetValue = new Map(data.map(d => [d["Territorio"], d["Value"] * 1000 / populationMap[`${year}`][d["Territorio"]]]))
	
	let plot_legend = displayPlotItaly2(
		Plot.legend({
		  color: {
			interpolate: x => colorScale(x*max2 + min2, min2, max2),
			domain: [min2, max2],
			label: "Value", 
		  },
		  className: "world-gradient-legend",
		  width: 300,
		  ticks: 6,
		  tickFormat: d => d * 100 + "%",
		  label: "Neet percentage"
		})
	);

	const mProjection = d3.geoEqualEarth().scale(50)
	
	let plot = displayPlotItaly2(Plot.plot({
		mProjection,
		width: 640,
		height: 640,
		className: "Za-Warudo",
		marks: [
		Plot.geo(regions, Plot.centroid({
			fill: d => colorScale(Number(NeetValue.get(d.properties.reg_name)), min2, max2),
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

			neet = `${(neet * 100).toFixed(2)}%`;
			//emissions = numToScientific(emissions);

			let tip = document.getElementsByClassName("italy-tooltip")[1];

			console.log(tip);

			tip.style.visibility = "visible";

			tip.innerHTML = `<span><b>Region:</b> ${region}</span><br/>
				<span><b>Neet per capita</b>: ${neet} of population</span>`;
			
		})
		c.addEventListener("mouseout", (e) => {

			let tip = document.getElementsByClassName("italy-tooltip")[1];
			tip.style.visibility = "hidden";
		})
	});

	return [plot, plot_legend];

}

let plotItaly2;
let plotItalyLegend2;
let selector2 = createSelector(years, (value) => {
	
	if (plotItaly2 != undefined) {
    plotItaly2.parentNode.removeChild(plotItaly2);
  }
  if (plotItalyLegend2 != undefined) {
    plotItalyLegend2.parentNode.removeChild(plotItalyLegend2);
  }
  
  [plotItaly2, plotItalyLegend2] = showPlotItaly2(2018 + Math.round(value * 5 / 100));

});

[plotItaly2, plotItalyLegend2] = showPlotItaly2(2023);



```

<div class="italy-tooltip">tooltip</div>
</div>

```js
view(selector2);
```

</div>

<p class="description">This chart shows that the problem is clearly more severe in the southern regions of Italy (even though in the last couple of years, it definitely got better). But why is that? There is a lot of possible reasons for why southern Italy has a higher chance of producing people unwilling to work or pursue higher studies, starting from the fact that the average salary in those region is notoriusly lower. As we don't have the resources, nor the authority, to denounce a list of exact reasons why southern Italy struggles more with the presence of NEETs (and why Italy struggles as a whole), we'll continue to present other aspects that characterize this phenomenon in our country and let the reader deduce their own theories.</p>


