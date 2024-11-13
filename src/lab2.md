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

const data0 = await FileAttachment("./data/co2_2022_stacked.csv").csv();

const data1 = data0.sort((a, b) => {
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

// Set the diagram dimensions
const width = 1000;
const height = 1700;

// Create an SVG container
const svg = d3.select('#alluvial')
  .attr('width', width)
  .attr('height', height);

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
  if (Continent == "Total") console.log("test1");
  if (!continentShadeMap[Continent]) {
    // Generate 6 shades for each continent
    continentShadeMap[Continent] = getShades(continentColors[Continent], 6);
  }
});

// Draw the links with colors based on the source and target countries' shades

/*var tooltipsvg = d3.select("#tooltip")
  .append("svg")
    .attr("width", 400)
    .attr("height", 400);*/

var tooltip = d3.select("#tooltip")
  .append("div")
    .style("position", "fixed")
    .style("visibility", "hidden")
    .style("background-color", "white")
    .style("margin", "0")
    .style("padding","20px")
    .style("border-radius", "5px")
    .text("example");

const link = svg.append("g")
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

    console.log("");
    console.log(sourceContinent);
    console.log(targetContinent);
    
    // Get the correct shade for the source and target
    const sourceShadeIndex = nodes.filter(node => node.name === d.source.name && node.continent === sourceContinent).indexOf(d.source);
    const targetShadeIndex = nodes.filter(node => node.name === d.target.name && node.continent === targetContinent).indexOf(d.target);

    console.log("the problem is after");

    const color = d3.scaleLinear()
      .domain([0, 1])
      .range([continentShadeMap[sourceContinent][sourceShadeIndex], continentShadeMap[targetContinent][targetShadeIndex]])(0.5);

    console.log("ciao");
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
  
    tooltip
      .html(`
        <b>Country</b>: ${data.source.name}
        <br/>
        <b>Rank</b>: ${data.source.rank}
        <br/>
        <b>Total CO2</b>: ${Number(data.value).toFixed(2)} tonnes
        <br/>
        <b>CO2 per capita</b>: ${Number(data.source.per_capita).toFixed(4)} tonnes/person</b>
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

```

# Prova

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