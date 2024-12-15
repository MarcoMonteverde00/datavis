<link rel="stylesheet" href="style.css">

<div class="hero">

# Temperature time serie

</div>

<div class="plot">

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
				stroke: "red"
            }),
            Plot.dot(data1Avg, {
                x: d => Number(d["Month"]), 
                y: d => Number(d["Value"]),
				stroke: "green"
            }),
            Plot.lineY(data1Min, {
                x: d => Number(d["Month"]), 
                y: d => Number(d["Value"]),
				stroke: "blue"
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
  if (plot1_legend != undefined) {
    plot1_legend.parentNode.removeChild(plot1_legend);
  }
  showPlot1();
});

```


```js

const dataAlabama2023Max = dataMax.filter(row => row["State"] == "Alabama" && row["Year"] == "2023");
const dataAlabama2023Avg = dataAvg.filter(row => row["State"] == "Alabama" && row["Year"] == "2023");
const dataAlabama2023Min = dataMin.filter(row => row["State"] == "Alabama" && row["Year"] == "2023");

/*
const points = dataAlabama2023Max.flatMap(({ State, ...values }) =>
  Object.entries(values).map(([Month, Value]) => ({ name: State, key: Month, value: Value/100.0 }))
)*/

const pointsMax = dataAlabama2023Max.map(({State, Month, Value}) => {
    return {name: "Maximum", key: Month, value: Value * 0.5 / 40, state: State}; // "max" temp = 40
});

//const longitudeMax = d3.scalePoint(new Set(Plot.valueof(pointsMax, "key")), [180, -180]).padding(0.5).align(1);

const pointsMin = dataAlabama2023Min.map(({State, Month, Value}) => {
    return {name: "Minimum", key: Month, value: Value * 0.5 / 40, state: State}; // "max" temp = 40
});

//const longitudeMin = d3.scalePoint(new Set(Plot.valueof(pointsMin, "key")), [180, -180]).padding(0.5).align(1);

const pointsAvg = dataAlabama2023Avg.map(({State, Month, Value}) => {
    return {name: "Average", key: Month, value: Value * 0.5 / 40, state: State}; // "max" temp = 40
});


//const longitudeAvg = d3.scalePoint(new Set(Plot.valueof(pointsAvg, "key")), [180, -180]).padding(0.5).align(1);

const points = pointsMin.concat(pointsMax).concat(pointsAvg);
const longitude = d3.scalePoint(new Set(Plot.valueof(points, "key")), [180, -180]).padding(0.5).align(1);

display(
    Plot.plot({
        width: 450,
        projection: {
            type: "azimuthal-equidistant",
            rotate: [0, -90],
            // Note: 0.625° corresponds to max. length (here, 0.5), plus enough room for the labels
            domain: d3.geoCircle().center([0, 90]).radius(0.625)()
        },
        color: { legend: true },
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

            // axes labels (todo: map index to month)
            Plot.text(longitude.domain(), {
                x: longitude,
                y: 90 - 0.57,
                text: Plot.identity,
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
            
            // Discs labels (to be changed into temperatures up to 40°)
            Plot.text([0.3, 0.4, 0.5], {
                x: 180,
                y: (d) => 90 - d,
                dx: 2,
                textAnchor: "start",
                text: (d) => `????°C`,
                fill: "currentColor",
                stroke: "white",
                fontSize: 8
            }),

            // interactive labels (to be changed into temperatures)
            /*Plot.text(
                points,
                Plot.pointer({
                    x: ({ key }) => longitude(key),
                    y: ({ value }) => 90 - value,
                    text: (d) => `${(100 * d.value).toFixed(0)}%`,
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
```