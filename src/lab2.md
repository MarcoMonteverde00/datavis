<link rel="stylesheet" href="style.css">

```js

import * as d3 from 'd3';
import { sankey, sankeyLinkHorizontal, sankeyCenter } from 'd3-sankey';

const continentColors = {
  "Europe": "red",
  "Asia": "yellow",
  "Africa": "green",
  "North America": "blue",
  "South America": "purple",
  "Oceania": "cyan",
  "Total": "gray"
};

// Function to generate shades for a base color
function getShades(baseColor, count) {
  const colorScale = d3.scaleLinear()
    .domain([0, count - 1])  // Create a scale based on how many shades you want
    .range([d3.rgb(baseColor).brighter(0.5), d3.rgb(baseColor).darker(0.5)]);  // Adjust brightness for shades

  return d3.range(count).map(i => colorScale(i));  // Return an array of color shades

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

let data_year = {
  "2022": await FileAttachment("./data/co2_2022_stacked.csv").csv(),
  "2021": await FileAttachment("./data/co2_2021_stacked.csv").csv(),
  "2020": await FileAttachment("./data/co2_2020_stacked.csv").csv(),
  "2019": await FileAttachment("./data/co2_2019_stacked.csv").csv()
};


```

<div class="hero">

# Which Countries are the Worst Polluters?

</div>

```js

const years = [2019,2020,2021,2022];

const selected_year = Inputs.select(years, {value: "2022", label: "Year:", format: (d) => d});

view(selected_year);

// Set the diagram dimensions
const width = 1000;
const height = 1700;

// Create an SVG container
let svg = d3.select('#alluvial')
  .attr('width', width)
  .attr('height', height);

```

```js



const tooltip = d3.select("#tooltip")
    .append("div")
      .style("position", "fixed")
      .style("visibility", "hidden")
      .style("background-color", "white")
      .style("margin", "0")
      .style("padding","20px")
      .style("border-radius", "5px")
      .text("example");

function showPlot1() {

  let data1 = data_year[selected_year.value].sort((a, b) => {
    if(a.Rank == "Total" && b.Rank != "Total") return 1;
    if(b.Rank == "Total" && a.Rank != "Total") return -1;
    if(a.Continent < b.Continent) return -1;
    if(a.Continent == b.Continent && a.Rank < b.Rank) return -1;
    return 1;
  });

  const links = [];

  data1.forEach((node, index) => {
    if (index < 36) {
      const {Continent} = node;
      let dest = 0;
      switch(Continent) {
        case "Africa":
          dest = 36; break;
        case "Asia":
          dest = 37; break;
        case "Europe":
          dest = 38; break;
        case "North America":
          dest = 39; break;
        case "Oceania":
          dest = 40; break;
        case "South America":
          dest = 41; break;
        default:
          break;
      }

      links.push({source: index, target: dest, value: node["Total CO2"]});
    }

  });


  const nodes = data1.map(d => {
    return {name: d.Entity, continent: d.Continent, rank: d.Rank, per_capita: d["Annual CO₂ emissions (per capita)"]};
  });

  const world = {name: "World Sum", continent: "Total", rank: "Total"};
  nodes.push(world);

  data1.push({Entity: "Total", Continent: "Total", Rank: "Total"});

  for(let i = 36; i < 42; i++) {
    links.push(
      {source: i, target: 42, value: data1[i]["Total CO2"]}
    );
  }

  const data = {
    nodes,
    links
  }

  // Initialize the Sankey generator
  const sankeyGenerator = sankey()
    .nodeWidth(20)
    .nodePadding(10)
    .nodeSort(null)
    .extent([[10, 10], [width - 10, height - 10]])
    .nodeAlign(sankeyCenter); // Optional alignment (e.g., sankeyLeft, sankeyRight)


  // Generate the Sankey layout
  const sankeyData = sankeyGenerator(data);

  // Generate color shades for each continent and its countries
  const continentShadeMap = {};
  data1.forEach(node => {
    const { Continent } = node;
    if (!continentShadeMap[Continent]) {
      // Generate 6 shades for each continent
      continentShadeMap[Continent] = getShades(continentColors[Continent], 6);
    }
  });

  svg.append("g")
    .selectAll('path')
    .data(sankeyData.links)
    .enter()
    .append('path')
    .attr('d', sankeyLinkHorizontal())
    .attr('stroke-width', d => Math.max(1, d.width))
    .attr('fill', 'none')
    .attr('stroke', d => {
      // Links will now have different colors based on both source and target
      const sourceContinent = d.source.continent;
      const targetContinent = d.target.continent;
      
      // Get the correct shade for the source and target
      const sourceShadeIndex = nodes.filter(node => node.name === d.source.name && node.continent === sourceContinent).indexOf(d.source);
      const targetShadeIndex = nodes.filter(node => node.name === d.target.name && node.continent === targetContinent).indexOf(d.target);

      const color = d3.scaleLinear()
        .domain([0, 1])
        .range([continentShadeMap[sourceContinent][sourceShadeIndex], continentShadeMap[targetContinent][targetShadeIndex]])
        (0.75);

      // Color the link based on source and target shades
      return color;
    })
    .attr('opacity', 0.5)
    .on('mouseover', function (event) {
      d3.select(this).transition()
            .duration('50')
            .attr('opacity', '1');

      tooltip.style("visibility", "visible");

    })
    .on("mousemove", function(event){

      const data = event.target.__data__;

      let emissions = data.value

      let emissionsPerCapita = data.source.per_capita;
    
      tooltip
        .html(`
          <b>Country</b>: ${data.source.name}
          <br/>
          <b>Rank</b>: ${data.source.rank}
          <br/>
          <b>Total CO2</b>: ${numToScientific(emissions)} tonnes
          <br/>
          <b>CO2 per capita</b>: ${numToScientific(emissionsPerCapita)} tonnes/person</b>
        `) 
        .style("top", (event.clientY + 30)+"px").style("left",(event.clientX + 30)+"px");

    })
    .on('mouseout', function (event) {
      d3.select(this).transition()
            .duration('50')
            .attr('opacity', '0.5');
      tooltip.style("visibility", "hidden");
    })

      

  // Draw the nodes with shades based on continent and country index

  svg.append('g')
    .selectAll('rect')
    .data(sankeyData.nodes)
    .enter()
    .append('rect')
    .attr('x', d => d.x0)
    .attr('y', d => d.y0)
    .attr('width', d => d.x1 - d.x0)
    .attr('height', d => d.y1 - d.y0)
    .attr('fill', d => {
      // Get the appropriate shade for the country based on its continent
      const continent = d.continent;
      const shadeIndex = nodes.filter(node => node.name === d.name && node.continent === continent).indexOf(d);
      return continentShadeMap[continent][shadeIndex];  // Apply the appropriate shade for this country
    })
    .attr('stroke', '#000');

  // Add node labels
  svg.append('g')
    .selectAll('text')
    .data(sankeyData.nodes)
    .enter()
    .append('text')
    .attr('x', d => d.name.includes(" Sum") ? d.x0 - 10 : d.x1 + 10)
    .attr('y', d => (d.y0 + d.y1) / 2)
    .attr('dy', '0.35em')
    .attr('text-anchor', d => d.name.includes(" Sum") ? 'end' : 'start')
    .text(d => d.name.includes(" Sum") ? d.name.slice(0, d.name.length - 4) : d.name)
    .attr('fill', '#000');

}


showPlot1();

selected_year.addEventListener("change", (e) => {

  let alluvial = document.getElementById("alluvial");
  alluvial.innerHTML = "";
  showPlot1();
});

```

<div id="tooltip"></div>
<svg id="alluvial"></svg>

```js



//const data = await FileAttachment("./data/energy.json").json();

/*
const chart = SankeyChart(
    {links: data},
    {
        nodeGroup: 
        linkSource: d => "Entity",
        linkTarget: d => "Continent"
    }
);*/

//const chart = SankeyChart(data, "source-target", "sankey-left");

```