<link rel="stylesheet" href="style.css">

<div class="hero">

# Consequences of the global pollution: the climate change

</div>

<div class="plot">

A direct consequence of the global pollution is the climate change. To evaluate the effect of the global pollution
it is therefore interesting to analyze the temperature time series and how much it has changed over the years. 
In order to have a more precise information the minimum, maximum and average temperatures are all taken into account and compared
through the use of different plots, the linechart and radarchart.


Both plots aim to investigate how the monthly minimum, maximum and average temperatures change every five years 
between 1978 and 2023. An immediate result is that all of the three temperatures have drastically increased 
form the beginning of the time interval considered.

```js

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

const dataMax = await FileAttachment("./data/countriesMaxTemperatures.csv").csv();
const dataAvg = await FileAttachment("./data/countriesAvgTemperatures.csv").csv();
const dataMin = await FileAttachment("./data/countriesMinTemperatures.csv").csv();


const years = ["2023", "2018", "2013", "2008", "2003", "1998", "1993", "1988", "1983", "1978"];
const selected_year = Inputs.select(years, {value: "2023", label: "Year:", format: (d) => d});
view(selected_year);

const datasetsMax = {};
const datasetsAvg = {};
const datasetsMin = {};

years.forEach(year => {
    datasetsMax[`${year}`] = dataMax.filter(row => row["State"] === "Alabama" && row["Year"] === String(year));
    datasetsAvg[`${year}`] = dataAvg.filter(row => row["State"] === "Alabama" && row["Year"] === String(year));
    datasetsMin[`${year}`] = dataMin.filter(row => row["State"] === "Alabama" && row["Year"] === String(year));
  });


let plot1;

let plot1_legend;

function showPlot1() {

  let data1Max = datasetsMax[selected_year.value];
  let data1Min = datasetsMin[selected_year.value];
  let data1Avg = datasetsAvg[selected_year.value];


  plot1 = display(  
    Plot.plot({
	  marginBottom: 70,
      title: `Minimum, maximum, average temperature per month in Alabama in ${selected_year.value}`,  
        x: {
            label: "Month",
            tickRotate: -30,
            tickFormat: d => months[Number(d)],
            ticks: 12
        },
        y: {
            label: "Temperature (C°)",
            grid: true,
			domain: [-5,35]		

        },
        marks: [
            Plot.ruleY([0]),
            Plot.lineY(data1Max, {
                x: d => Number(d["Month"]), 
                y: d => Number(d["Value"]),
				stroke: "red",
				tip: {
					format: {
					  y: (d) => `${d}`,
					  x: d => months[Number(d)]
					}
				  }
            }),
            Plot.dot(data1Avg, {
                x: d => Number(d["Month"]), 
                y: d => Number(d["Value"]),
				stroke: "green",
				tip: {
					format: {
					  y: (d) => `${d}`,
					  x: d => months[Number(d)]
					}
				  }
            }),
            Plot.lineY(data1Min, {
                x: d => Number(d["Month"]), 
                y: d => Number(d["Value"]),
				stroke: "blue",
				tip: {
					format: {
					  y: (d) => `${d}`,
					  x: d => months[Number(d)]
					}
				  }
            }),
        ]
    })

  );

}

showPlot1();


selected_year.addEventListener("change", (e) => {

  if (plot1 != undefined) {
    plot1.parentNode.removeChild(plot1);
  }
  if (plot1_legend != undefined) {
    plot1_legend.parentNode.removeChild(plot1_legend);
  }
  showPlot1();
});

```

</div>
<a href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Statewide Time Series - National Centers for Environmental Information]
  </a>

```js
/*
const dataAlabama2023Max = dataMax.filter(row => row["State"] == "Alabama" && row["Year"] == "2023");
const dataAlabama2023Avg = dataAvg.filter(row => row["State"] == "Alabama" && row["Year"] == "2023");
const dataAlabama2023Min = dataMin.filter(row => row["State"] == "Alabama" && row["Year"] == "2023");

const pointsMax = dataAlabama2023Max.map(({State, Month, Value}) => {
    return {name: "Maximum", key: Month, value: (Number(Value) + 20.0) * 0.5 / 60.0, state: State}; // "max" temp = 40, "min" temp = -20
});

console.log(pointsMax)

//const longitudeMax = d3.scalePoint(new Set(Plot.valueof(pointsMax, "key")), [180, -180]).padding(0.5).align(1);

const pointsMin = dataAlabama2023Min.map(({State, Month, Value}) => {
    return {name: "Minimum", key: Month, value: (Number(Value) + 20) * 0.5 / 60, state: State}; // "max" temp = 40
});

//const longitudeMin = d3.scalePoint(new Set(Plot.valueof(pointsMin, "key")), [180, -180]).padding(0.5).align(1);

const pointsAvg = dataAlabama2023Avg.map(({State, Month, Value}) => {
    return {name: "Average", key: Month, value: (Number(Value) + 20) * 0.5 / 60, state: State}; // "max" temp = 40
});


//const longitudeAvg = d3.scalePoint(new Set(Plot.valueof(pointsAvg, "key")), [180, -180]).padding(0.5).align(1);

const points = pointsMin.concat(pointsMax).concat(pointsAvg);
const longitude = d3.scalePoint(new Set(Plot.valueof(points, "key")), [180, -180]).padding(0.5).align(1);

display(
    Plot.plot({
        width: 650,
        projection: {
            type: "azimuthal-equidistant",
            rotate: [0, -90],
            // Note: 0.625° corresponds to max. length (here, 0.5), plus enough room for the labels
            domain: d3.geoCircle().center([0, 90]).radius(0.625)()
        },
        color: { legend: true, scheme: "dark2", type: "categorical"},
        marks: [
            // grey discs
            Plot.geo([0.5, 0.4, 0.3, 0.2, 0.1], {
                geometry: (r) => d3.geoCircle().center([0, 90]).radius(r)(),
                stroke: "black",
                fill: "black",
                strokeOpacity: 0.3,
                fillOpacity: 0.03,
                strokeWidth: 0.5
            }),

            // making the zero disk more evident: zero is at 1/3 of the radius (0.5 * 0.333 = 0.167)
            Plot.geo([0.167], {
                geometry: (r) => d3.geoCircle().center([0, 90]).radius(r)(),
                stroke: "steelblue",
                fill: "black",
                strokeOpacity: 0.8,
                fillOpacity: 0.07,
                strokeWidth: 1.5
            }),
            
            // white axes
            Plot.link(longitude.domain(), {
                x1: longitude,
                y1: 90 - 0.57,
                x2: 0,
                y2: 90,
                stroke: "white",
                strokeOpacity: 0.5,
                strokeWidth: 2.5
            }),

            // axes labels
            Plot.text(longitude.domain(), {
                x: longitude,
                y: 90 - 0.57,
                text: d => months[Number(d)],
                lineWidth: 5
            }),

            // lines for max, min, avg            
            Plot.line(
                points, {
                    x: ({ key }) => longitude(key),
                    y: ({ value }) => 90 - value,
                    curve: "cardinal", // Smooth curve that can handle non-monotonic x-axis
                    stroke: "name",
                    strokeWidth: 2
                }
            ),

            // dots
            Plot.dot(
                points, {
                    x: ({ key }) => longitude(key),
                    y: ({ value }) => 90 - value,
                    fill: "name",
                    stroke: "white"
                }
            ),
            
            // Discs labels
            Plot.text([0.167, 0.3, 0.4, 0.5], {
                x: 180,
                y: (d) => 90 - d,
                dx: 2,
                textAnchor: "start",
                text: (d) => `${(d * 60 / 0.5 - 20).toFixed(0)}°C`,
                fill: "currentColor",
                stroke: "white",
                fontSize: 10
            }),

            //interactive labels (to be changed into temperatures)
            Plot.text(
                points,
                Plot.pointer({
                    x: ({ key }) => longitude(key),
                    y: ({ value }) => 90 - value,
                    text: (d) => `${(d["value"] * 60 / 0.5 - 20).toFixed(0)}°C`,
                    textAnchor: "start",
                    dx: 4,
                    fill: "currentColor",
                    stroke: "white",
                    maxRadius: 10
                })
            )
        ]
    
    })
);
*/
```

```js
const years = ["2023", "2018", "2013", "2008", "2003", "1998", "1993", "1988", "1983", "1978"];
const selected_year2 = Inputs.select(years, {value: "2023", label: "Year:", format: (d) => d});
view(selected_year2);

const dMax = {};
const dAvg = {};
const dMin = {};

years.forEach(year => {
    dMax[`${year}`] = dataMax.filter(row => row["State"] === "Alabama" && row["Year"] === String(year));
    dAvg[`${year}`] = dataAvg.filter(row => row["State"] === "Alabama" && row["Year"] === String(year));
    dMin[`${year}`] = dataMin.filter(row => row["State"] === "Alabama" && row["Year"] === String(year));
	});

let plot2;

let plot2_legend;

function showPlot2() {

  let Max = dMax[selected_year2.value];
  let Min = dMin[selected_year2.value];
  let Avg = dAvg[selected_year2.value];

  const pointsMax = Max.map(({State, Month, Value}) => {
    return {name: "Maximum", key: Month, value: (Number(Value) + 20.0) * 0.5 / 60.0, state: State}; // "max" temp = 40, "min" temp = -20
	});
  const pointsMin = Min.map(({State, Month, Value}) => {
    return {name: "Minimum", key: Month, value: (Number(Value) + 20) * 0.5 / 60, state: State}; // "max" temp = 40
	});
  const	pointsAvg = Avg.map(({State, Month, Value}) => {
    return {name: "Average", key: Month, value: (Number(Value) + 20) * 0.5 / 60, state: State}; // "max" temp = 40
	});
  const	points = pointsMin.concat(pointsMax).concat(pointsAvg);
  const	longitude = d3.scalePoint(new Set(Plot.valueof(points, "key")), [180, -180]).padding(0.5).align(1);


  plot2 =display(
    Plot.plot({
        width: 650,
		title: `Minimum, maximum, average temperature per month in Alabama in ${selected_year2.value}`,
        projection: {
            type: "azimuthal-equidistant",
            rotate: [0, -90],
            // Note: 0.625° corresponds to max. length (here, 0.5), plus enough room for the labels
            domain: d3.geoCircle().center([0, 90]).radius(0.625)()
        },
        color: { domain: ["Minimum", "Maximum", "Average"], range: ["blue", "red", "green"], legend: true}, //scheme: "dark2", type: "categorical"
        marks: [
            // grey discs
            Plot.geo([0.5, 0.4, 0.3, 0.2, 0.1], {
                geometry: (r) => d3.geoCircle().center([0, 90]).radius(r)(),
                stroke: "black",
                fill: "black",
                strokeOpacity: 0.3,
                fillOpacity: 0.03,
                strokeWidth: 0.5
            }),

            // making the zero disk more evident: zero is at 1/3 of the radius (0.5 * 0.333 = 0.167)
            Plot.geo([0.167], {
                geometry: (r) => d3.geoCircle().center([0, 90]).radius(r)(),
                stroke: "steelblue",
                fill: "black",
                strokeOpacity: 0.8,
                fillOpacity: 0.07,
                strokeWidth: 1.5
            }),
            
            // white axes
            Plot.link(longitude.domain(), {
                x1: longitude,
                y1: 90 - 0.57,
                x2: 0,
                y2: 90,
                stroke: "white",
                strokeOpacity: 0.5,
                strokeWidth: 2.5
            }),

            // axes labels
            Plot.text(longitude.domain(), {
                x: longitude,
                y: 90 - 0.57,
                text: d => months[Number(d)],
                lineWidth: 5
            }),

            // lines for max, min, avg            
            Plot.line(
                points, {
                    x: ({ key }) => longitude(key),
                    y: ({ value }) => 90 - value,
                    curve: "cardinal", // Smooth curve that can handle non-monotonic x-axis
                    stroke: "name",
                    strokeWidth: 2
                }
            ),

            // dots
            Plot.dot(
                points, {
                    x: ({ key }) => longitude(key),
                    y: ({ value }) => 90 - value,
                    fill: "name",
                    stroke: "white"
                }
            ),
            
            // Discs labels
            Plot.text([0.167, 0.3, 0.4, 0.5], {
                x: 180,
                y: (d) => 90 - d,
                dx: 2,
                textAnchor: "start",
                text: (d) => `${(d * 60 / 0.5 - 20).toFixed(0)}°C`,
                fill: "currentColor",
                stroke: "white",
                fontSize: 10
            }),

            //interactive labels (to be changed into temperatures)
            Plot.text(
                points,
                Plot.pointer({
                    x: ({ key }) => longitude(key),
                    y: ({ value }) => 90 - value,
                    text: (d) => `${(d["value"] * 60 / 0.5 - 20).toFixed(0)}°C`,
                    textAnchor: "start",
                    dx: 4,
                    fill: "currentColor",
                    stroke: "white",
                    maxRadius: 10
                })
            )
        ]
    
    })
); 
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

```
</div>
<a href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Statewide Time Series - National Centers for Environmental Information]
  </a>
  

```js
/*
const alabamaPoints = {};
const longitudes = {}

let years = [2023, 2018, 2013, 2008, 2003, 1998, 1993, 1988, 1983, 1978];

years.forEach( year => {

    let data = dataAvg
        .filter(row => row["State"] === "Alabama" && Number(row["Year"]) == year )
        .sort( (a, b) => (a["Month"] - b["Month"]) );

    alabamaPoints[year] = data.map(({State, Month, Value, Year}) => {
        return {name: "Average", key: Month, value: (Number(Value) + 10) * 0.5 / 40, state: State, order: ((Number(Year)-2018) * 12 + 0 * Number(Month)) / 71.0}; // "max" temp = 30, "min" temp = -10
    });

    longitudes[year] = d3.scalePoint(new Set(Plot.valueof(alabamaPoints[year], "key")), [180, -180]).padding(0.5).align(1);

});
*/

const dataAlabama = dataAvg
    .filter(row => row["State"] === "Alabama" && (Number(row["Year"]) - 1978) % 5 == 0 && Number(row["Year"] >= 1978) && Number(row["Year"] <= 2023))
    .sort( (a, b) => (a["Year"] == b["Year"]) ? a["Month"] - b["Month"] : a["Year"] - b["Year"]);


const points2 = dataAlabama.map(({State, Month, Value, Year}) => {
    return {name: "Average", key: Month, value: (Number(Value) + 10) * 0.5 / 40, state: State, Year: Year}; // "max" temp = 30, "min" temp = -10
});


const longitude2 = d3.scalePoint(new Set(Plot.valueof(points2, "key")), [180, -180]).padding(0.5).align(1);


display(
    Plot.plot({
        width: 650,
		title: `Average temperature per month in Alabama`,
        projection: {
            type: "azimuthal-equidistant",
            rotate: [0, -90],
            // Note: 0.625° corresponds to max. length (here, 0.5), plus enough room for the labels
            domain: d3.geoCircle().center([0, 90]).radius(0.625)()
        },
        color: { 
            legend: true, 
            width: 300,
            scheme: "turbo", 
            type: "categorical",
            ticks: 10,
            label: "Year",
            //range: [0,1],
            //domain: [0,1],
            //tickFormat: d => Number(d * 5 + 1978).toFixed(0),
            tip: false
        },
        className: "radar-chart",
        marks: [
            // grey discs
            Plot.geo([0.5, 0.4, 0.3, 0.2, 0.1], {
                geometry: (r) => d3.geoCircle().center([0, 90]).radius(r)(),
                stroke: "black",
                fill: "black",
                strokeOpacity: 0.3,
                fillOpacity: 0.03,
                strokeWidth: 0.5
            }),

            // making the zero disk more evident: zero is at 1/4 of the radius (0.5 * 0.25 = 0.125)
            Plot.geo([0.125], {
                geometry: (r) => d3.geoCircle().center([0, 90]).radius(r)(),
                stroke: "steelblue",
                fill: "black",
                strokeOpacity: 0.8,
                fillOpacity: 0.07,
                strokeWidth: 1.5
            }),
            
            // white axes
            Plot.link(longitude2.domain(), {
                x1: longitude2,
                y1: 90 - 0.57,
                x2: 0,
                y2: 90,
                stroke: "white",
                strokeOpacity: 0.5,
                strokeWidth: 2.5
            }),

            // axes labels
            Plot.text(longitude2.domain(), {
                x: longitude2,
                y: 90 - 0.57,
                text: d => months[Number(d)],
                lineWidth: 5
            }),

            // lines for max, min, avg            
            Plot.line(
                points2, {
                    x: ({ key }) => longitude2(key),
                    y: ({ value }) => 90 - value,
                    curve: "cardinal", // Smooth curve that can handle non-monotonic x-axis
                    stroke: "Year",
                    strokeWidth: 2,
                    channels: { Temperature: 'value' },
                    tip: {
                        format: {
                            Temperature: d => `${Number(d * 40 / 0.5 - 10).toFixed(0)} °C`,
                            x: null,
                            y: null,
                   
                        }
                    }
                }
            ),

            // dots
            Plot.dot(
                points2, {
                    x: ({ key }) => longitude2(key),
                    y: ({ value }) => 90 - value,
                    fill: "Year",
                    stroke: "white"
                }
            ),
/*
            // lines for max, min, avg      
            years.map( year => {

                Plot.line(
                alabamaPoints[year], {
                    x: ({ key }) => longitudes[year](key),
                    y: ({ value }) => 90 - value,
                    z: null,
                    stroke: "order",
                    curve: "cardinal", // Smooth curve that can handle non-monotonic x-axis
                    strokeWidth: 2,  
                    channels: { Temperature: 'value', Year: 'order' }, 
               
                    tip: {
                        format: {
                            Year: d => Number(d * 6 + 2018 + 0.1).toFixed(0),
                            Temperature: d => `${Number(d * 40 / 0.5 - 10).toFixed(0)} °C`,
                            x: null,
                            y: null
                        }
                    }
                }),

                // dots
                Plot.dot(
                    alabamaPoints[year], {
                        x: ({ key }) => longitudes[year](key),
                        y: ({ value }) => 90 - value,
                        fill: "order",
                        stroke: "white"
                    }
                )
            }),  
          */  
            // Discs labels
            Plot.text([0.125, 0.3, 0.4, 0.5], {
                x: 180,
                y: (d) => 90 - d,
                dx: 2,
                textAnchor: "start",
                text: (d) => `${(d * 40 / 0.5 - 10).toFixed(0)}°C`,
                fill: "currentColor",
                stroke: "white",
                fontSize: 10
            })

            //interactive labels (to be changed into temperatures)
            /*Plot.text(
                points2,
                Plot.pointer({
                    x: ({ key }) => longitude(key),
                    y: ({ value }) => 90 - value,
                    text: (d) => `${(d["value"] * 40 / 0.5 - 10).toFixed(0)}°C`,
                    textAnchor: "start",
                    dx: 4,
                    fill: "currentColor",
                    stroke: "white",
                    maxRadius: 10
                })
            )*/
        ]
    
    })
);

let charts = document.getElementsByClassName("radar-chart");

for (let i = 0; i < charts.length; i++) {
    let lines = charts.item(i).querySelector('[aria-label="line"]').childNodes;
    let dots = charts.item(i).querySelector('[aria-label="dot"]').childNodes;

    lines.forEach( line => {
		line.addEventListener("mouseout", () => {
            lines.forEach(l => l.setAttribute('class', "focus")); 
        });
        line.addEventListener("mouseover", (e) => {
            for (let j = 0; j < lines.length; j++) {
                lines[j].setAttribute('class', "out-of-focus");
            }

            line.setAttribute('class', "");
        });
    });

    for(let j = 0; j < dots.length; j++) {
        let dot = dots[j];
        dot.addEventListener("mouseout", () => {
            lines.forEach(l => l.setAttribute('class', "focus")); 
        });
        dot.addEventListener("mouseover", () => {
            
            for (let k = 0; k < lines.length; k++) {
                lines[k].setAttribute('class', "out-of-focus");
            }
            let selected = Math.floor(j / 12);
            lines[selected].setAttribute('class', "");
        });
    }
}


/*.forEach( chart => {
    
    let lines = chart.querySelector('[aria-label="line"]').childNodes;

    console.log(lines);

});*/

```
</div>
<a href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Statewide Time Series - National Centers for Environmental Information]
  </a>

In order to have an easier comparison among the years considered the radarchart plot is also used to display
each of the monthly average temperatures.
```js
	//ridgeline
	const data = await FileAttachment("./data/dataRidgeLine.csv").csv();
	console.log("data", data)
	
	display(Plot.plot({
	  title: "Temperature density estimation",
	  height: 300,
	  marginLeft: 60,
	  y: { axis: null },
	  x: { label: "Temperature (°C)", nice: true },
	  fy: { domain: ["2023", "2018", "2013", "2008", "2003", "1998", "1993", "1988", "1983", "1978"] }, // excludes N/A
	  color: {domain: ["Min", "Max"], range: ["blue", "red"], legend: true },
	  facet: { data: data, y: "Year" },
	  marks: [
		Plot.areaY(
		  data,
		  Plot.binX(
			{ y2: "proportion" }, // using y2 to avoid areaY’s implicit stacking
			{
			  x: "Value",
			  fill: "Index",
			  fillOpacity: 0.1,
			  //thresholds: 10,
			  curve: "natural"
			}
		  )
		),
		Plot.ruleY([0]),
		Plot.lineY(
		  data,
		  Plot.binX(
			{ y: "proportion" },
			{
			  x: "Value",
			  stroke: "Index",
			  //thresholds: 10,
			  curve: "natural",
			  tip: {
					format: {
					  "Index": false,
					  Year: false,
					  y: (d) => `${d}`,
					  x: d => `${d}`,
                      fill: false,
					  stroke: false
					}
				  }
			}
		  )
		)
	  ]
	})
	)

```
</div>
<a href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Statewide Time Series - National Centers for Environmental Information]
  </a>
  
A possible alternative to convey informations about the minimum and maximum temperatures of each year is represented by
the ridgeline plot, which shows the probability distibution of the temperature.