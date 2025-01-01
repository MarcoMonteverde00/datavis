<link rel="stylesheet" href="style.css">

<div class="hero">

# NEET in Italy

</div>

```js
	const NeetByRegion = await FileAttachment("./final/Neet_1529_regions.csv").csv(); 
	const years = ["2023", "2022", "2021", "2020", "2019", "2018"];
	
	const selected_year = Inputs.select(years, {value: "2023", label: "Year:", format: (d) => d});
	view(selected_year);

	const Neet = {};
	
	years.forEach(year => {
    Neet[`${year}`] = NeetByRegion.filter(row => row["Year"] === String(year));});
	
	import * as topojson from "topojson-client";

	const italy = await FileAttachment("./final/regioni.json").json();
	const regions = topojson.feature(italy, italy.features);

	
	var min, max;
	min = Number(Neet["2018"][0]["Value"]);
	max = Number(Neet["2018"][0]["Value"]);
	
	for (let i in years) {
		let year = years[i];
		for(let j in Neet[`${year}`]) {
			if (j == "columns") continue;
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

	let zoom_info = [
		{zoomed: false, trans_x: 0, trans_y: 0},
		{zoomed: false, trans_x: 0, trans_y: 0},
		{zoomed: false, trans_x: 0, trans_y: 0},
		{zoomed: false, trans_x: 0, trans_y: 0}
	];

```

<div class="plot">

```js

function showPlot1(plot_id, data, projection, column_name, column_label) {

	const NeetValue = new Map(data.map(d => [d["Territorio"], d[column_name]]))
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