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

let plot = display(
    Plot.plot({
        marginBottom: 70,
        x: {
            label: "Month",
            tickRotate: -30,
            tickFormat: d => months[Number(d)],
            ticks: 12
        },
        y: {
            label: "Temperature (C°)",
            grid: true
			},
        marks: [
            Plot.ruleY([0]),
            Plot.lineY(dataAlabama2023Max, {
                x: d => Number(d["Month"]), 
                y: d => Number(d["Value"]),
				stroke: "red"
            }),
            Plot.dot(dataAlabama2023Avg, {
                x: d => Number(d["Month"]), 
                y: d => Number(d["Value"]),
				stroke: "green"
            }),
            Plot.lineY(dataAlabama2023Min, {
                x: d => Number(d["Month"]), 
                y: d => Number(d["Value"]),
				stroke: "blue"
            })
        ]
    })
);
```