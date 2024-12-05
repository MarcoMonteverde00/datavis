<link rel="stylesheet" href="style.css">

<div class="hero">

# CO2 emissions

</div>

```js

let data_year = {
  "2022": await FileAttachment("./data/co2_2022.csv").csv(),
  "2021": await FileAttachment("./data/co2_2021.csv").csv(),
  "2020": await FileAttachment("./data/co2_2020.csv").csv(),
  "2019": await FileAttachment("./data/co2_2019.csv").csv()
};

var minAbs, maxAbs, minCap, maxCap;
minAbs = Number(data_year["2019"][0]["Total CO2"]);
maxAbs = Number(data_year["2019"][0]["Total CO2"]);
minCap = Number(data_year["2019"][0]["Annual CO₂ emissions (per capita)"]);
maxCap = Number(data_year["2019"][0]["Annual CO₂ emissions (per capita)"]);

let _years = ["2019", "2020", "2021", "2022"];

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

  return val + ` × 10${true_exp}`;
}

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

```
<br />

#

# Top 20 polluters (per person) in a year

```js


const years = [2019,2020,2021,2022];

const selected_year = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year);

```

<div class="plot">

```js


let plot1;

let plot1_legend;

function showPlot1() {

  let data1 = data_year[selected_year.value];
  let trimmed1 = data1.slice(0,20)

  plot1_legend = display(
    Plot.legend({
      color: {
        interpolate: x => colorScale(x*(maxCap - minCap) + minCap, minCap, maxCap),
        domain: [minCap, maxCap]
      },
      className: "gradient-legend",
      width: 300,
      ticks: 10,
      label: "Annual CO₂ emissions (per capita, tonnes)"
    })
  )


  plot1 = display(  
    Plot.plot({
      marginBottom: 80,
      title: `Carbone dioxide CO2 emission per capita (tonnes per person) ${selected_year.value}`,
      x: {
        label: "Country",
        tickRotate: -30
      },
      y: {
        label: "CO₂ emissions",
        grid: true,
        percent: false
      },

      marks: [
        Plot.ruleY([0]),
        Plot.barY(trimmed1, {
          x: "Entity", 
          y: "Annual CO₂ emissions (per capita)", 
          sort: {x: "y", reverse: true}, 
          fill: d => colorScale(d["Annual CO₂ emissions (per capita)"],minCap,maxCap),
          tip: {
            format: {
              y: (d) => `${d.toFixed(4)} tonnes/per`   
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
<a href="https://ourworldindata.org/grapher/co-emissions-per-capita" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [CO2 emission per capita - Our World in Data]
</a>
  
The plot aims to investigate which countries were the major contributors to pollution in each year (2019, 2020, 2021, 2022), in terms of CO2 emissions per person. At this purpose, by chosing the year with the selector, the graph displays the CO2 emissions per capita of the 20 most polluting countries of that year and conveys this information through both the size of the bars and their color, the more red and bigger the bar, the more the country is polluting.

<br /><br /><br />

# Top 20 polluters (per person) in a decade
  
<div class="plot">

```js

const data2 = await FileAttachment("./data/co2_2022_mean.csv").csv(); 
const trimmed2 = data2.slice(0,20);

display(
  Plot.legend({
    color: {
      interpolate: x => colorScale(x*(maxCap - minCap) + minCap, minCap, maxCap),
      domain: [minCap, maxCap]
    },
    className: "gradient-legend",
    width: 300,
    ticks: 10,
    label: "Mean CO2 emission (per capita, tonnes)"
  })
)

display(  
  Plot.plot({
    marginBottom: 80,

    title: "Mean Carbone dioxide (CO2) emission per capita (tonnes per person) (2012-2022)",

    x: {
      label: "Country",
      tickRotate: -30
    },
    y: {
      label: "CO₂ emissions",
      grid: true,
      percent: false
    },
    marks: [
      Plot.ruleY([0]),
      Plot.barY(trimmed2, {
        x: "Entity", 
        y: "Annual CO₂ emissions (per capita)", 
        sort: {x: "y", reverse: true}, 
        fill: d => colorScale(d["Annual CO₂ emissions (per capita)"], minCap, maxCap),
        tip: {
          format: {
            y: (d) => `${d.toFixed(4)} tonnes/per`   
          }
        }
      })
    ]
  })
);
```

</div>
<a href="https://ourworldindata.org/grapher/co-emissions-per-capita" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [CO2 emission per capita - Our World in Data]
  </a>

In order to have a more complete analysis the same plot is evaluated in the decade 2012-2022. The CO2 emissions per person value is computed as the mean of the values of the 10 years.

<br /><br /><br />

# Continents Comparison
```js

const data3 = await FileAttachment("./data/co2_2022_stacked.csv").csv();
const data3_without_total = data3.slice(0,36);
const data3_total = data3.slice(36);


display(
  Plot.plot({
    marginLeft: 90,
    width: 900,
    height: 360,
    title: "Total CO2 emission in each Region (tonnes) (2022)",
	subtitle: "Carbone dioxide (CO2) emissions (tonnes) of each continent divided into theirs top 5 polluting countries and the sum of all the other ones in 2022.",
    //color: { scheme: "Spectral", legend: true},
    x: {label: "", percent: false, },
    y: {label: "Continent", padding: 0.2},
    color: {scheme: "Observable10", legend: true},
    marks: [
      Plot.barX(
        data3_without_total,
        {   
          x: "Total CO2",
          fill: "Rank",
          y: "Continent",
          sort: {y: "x", reverse: true },
          channels: {Country: 'Entity'},
          tip: {
            format: {
              x: (d) => {
                let emissions = numToScientific(d);
                return `${emissions} tonnes`;
              },  
              fill: false
            }
          }
        }
      ),

	  //Plot.text(data3_total, {
        //text: d => `${Number(d["Total CO2"]).toFixed(4)} tonnes`,
        //y: "Continent",
        //x: "Total CO2",
        //sort: {y: "x", reverse: true },
        //textAnchor: "start",
        //dx: 30,
        //fill: "rgb(22,22,22)"
      //}),
      //Plot.axisX({ticks: []}),
      Plot.ruleX([0])

    ]
  })
);

```
<a href="https://ourworldindata.org/grapher/co-emissions-per-capita" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [CO2 emission per capita - Our World in Data]
  </a>
  
  
<a href="https://ourworldindata.org/explorers/population-and-demography?tab=table&time=2022&Metric=Population&Sex=Both+sexes&Age+group=Total&Projection+Scenario=None&country=CHN~IND~USA~IDN~PAK~NGA~BRA~JPN" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Global Population - Our World in Data]
  </a>


The plot aims to make a comparison among the continents in terms of CO2 emission. Showing also the contributions of the top 5 polluting countries and the others one all together, for each continent, it is possible to evaluate the continent comparison for each category. This information is conveyed by the ranking of the countries and the dimensions of the bars.

```js

display(
  Plot.plot(
    {
      marginLeft: 90,
      width: 900,
      height: 360,
      title: "Total CO2 emission in each Region (tonnes) (2022)",
	  subtitle: "Carbone dioxide (CO2) emissions (tonnes) of the top 5 polluting countries, the sum of all the other ones and the total for each continent in 2022.",
      x: {label: "Emissions"},
      y: {label: "Continent"},
      color: {scheme: "Observable10",legend: true},
      marks: [
        Plot.barX(
          data3,
          {
            x: "Total CO2",
            fx: "Rank",
            fill: "Rank",
            y: "Continent", 
            sort: {y: "x", reverse: true },
            //domain: [0, 100],
            channels: {Country: 'Entity'},
            tip: {
              format: {
                x: (d) => `${numToScientific(d)} tonnes`,  
                fill: false,
                fx: false
              }
            }
          }
        )
      ]
    }
  )
  
);
```

<a href="https://ourworldindata.org/grapher/co-emissions-per-capita" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [CO2 emission per capita - Our World in Data]
  </a>
  
  
<a href="https://ourworldindata.org/explorers/population-and-demography?tab=table&time=2022&Metric=Population&Sex=Both+sexes&Age+group=Total&Projection+Scenario=None&country=CHN~IND~USA~IDN~PAK~NGA~BRA~JPN" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Global Population - Our World in Data]
  </a>
  
In order to have a better understanding of the comparison between the polluters among the continents, the same data are visualized aligning each contribution with respect to the category.   
The additional 'Total' category allows to compare the CO2 continents emissions more immediately. 

```js
display(
  Plot.plot({
    marginLeft: 90,
    width: 900,
    height: 360,
    title: "Proportions of total CO2 emission in each Region (tonnes) (2022)",
	subtitle: "Carbone dioxide (CO2) emissions proportions of each continent divided into theirs top 5 polluting countries and the sum of all the other ones in 2022.",
    //color: { scheme: "Dark2", legend: true},
    x: {label: "Emissions", percent: false},
    y: {label: "Continent", padding: 0.2},
    color: {scheme: "Observable10", legend: true},
    marks: [
      Plot.barX(
        data3_without_total,
        {   
          x: "Total CO2",
          fill: "Rank",
          y: "Continent",
		  offset:"normalize",
          channels: {Country: 'Entity'},
          tip: {
            format: {
              x: (d) => `${numToScientific(d)} tonnes`,  
              fill: false
            }
          }
        }
      ),
      Plot.ruleX([0])

    ]
  })
);

```
<a href="https://ourworldindata.org/grapher/co-emissions-per-capita" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [CO2 emission per capita - Our World in Data]
  </a>
  
  
<a href="https://ourworldindata.org/explorers/population-and-demography?tab=table&time=2022&Metric=Population&Sex=Both+sexes&Age+group=Total&Projection+Scenario=None&country=CHN~IND~USA~IDN~PAK~NGA~BRA~JPN" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [Global Population - Our World in Data]
  </a>
 
The same data are also evaluated with respect to the total CO2 emissions of the corresponding continent in order to understand the importance, in terms of CO2 emissions, of the top 5 emittors and the others countries in each continent.
<br /><br /><br />
# Emissions type comparison

<div class="plot">

```js
const data_by_type = await FileAttachment("./data/co2_by_type_Heatmap.csv").csv();

const values_Heatmap = data_by_type.map(d => d["Value"]);
const minHeatmap = Math.min(...values_Heatmap);
const maxHeatmap = Math.max(...values_Heatmap);

function colorScaleWithNegatives(value, min, max) {
  
  let r = 255;
  let g = 255;
  let b = 0;
  let ratio;
  if (min >= 0) {
    ratio = (value - min) / (max - min);
    g = Math.floor(255 * (1 - ratio));
  } else {
    if (value > 0) {
      ratio = value / max;
      g = Math.floor(255 * (1 - ratio));
    } else {
      ratio = value / min;
      r = Math.floor(255 * (1 - ratio));
    }
  }
  return `rgb(${r}, ${g}, ${b})`;
}


display(
  Plot.legend({
    //data: [10,20,30],
    color: {
      interpolate: x => colorScaleWithNegatives(x*(2 * maxHeatmap) - maxHeatmap, -maxHeatmap, maxHeatmap),
      domain: [-maxHeatmap, maxHeatmap]
    },
    className: "heatmap-legend",
    width: 500,
    ticks: 10,
    tickFormat: d => (d / 1000000000) + "B"
  })
)

display(
	Plot.plot({
	  padding: 0,
	  marginLeft: 90,
	  marginBottom: 80,
	  width: 900,
      height: 360,
	  title : "Mean carbone dioxide (CO2) emissions (tonnes) (2012-2022) by type of the top 10 polluting countries in the world",
	  x: {
      label: "Country",
      tickRotate: -30
	  },
    className: "heatmap",
	  color: {legend: true, zero: true},
	  marks: [
		Plot.cell(data_by_type, {
		  x: "Entity",
		  y: "Type",
		  fill: d => colorScaleWithNegatives(d["Value"], -maxHeatmap, maxHeatmap),
		  inset: 0.5,
		  channels: {Co2_Emissions: "Value"},
		tip: {
            format: {Co2_Emissions: d => `${numToScientific(d)} tonnes`}
          }
		})
	  ]
	})
)
```
</div>

<a href="https://ourworldindata.org/grapher/co2-fossil-plus-land-use" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [CO2 emissions by type - Our World in Data]
  </a>

The mean value of the CO2 emissions in the decade 2012-2022 is studied also with respect to their type, fossils and land use.  The colors of the plot show for the top ten global polluters the CO2 emissions quantity divided by type. The value of the emissions increaseas as the color goes from yellow to red while decreases going from yellow to green. 