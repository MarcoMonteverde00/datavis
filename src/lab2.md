```js

import * as d3 from 'd3';
import { sankey, sankeyLinkHorizontal, sankeyCenter } from 'd3-sankey';


const continentColors = {
  "Europe": "red",
  "Asia": "yellow",
  "Africa": "green",
  "North America": "blue",
  "South America": "purple",
  "Oceania": "cyan"
};

// Function to generate shades for a base color
function getShades(baseColor, count) {
  const colorScale = d3.scaleLinear()
    .domain([0, count - 1])  // Create a scale based on how many shades you want
    .range([d3.rgb(baseColor).brighter(0.5), d3.rgb(baseColor).darker(0.5)]);  // Adjust brightness for shades

  return d3.range(count).map(i => colorScale(i));  // Return an array of color shades
}

const data0 = await FileAttachment("./data/co2_2022_stacked.csv").csv();

console.log(data0);

const links = [];

data0.forEach((node, index) => {
  if (index < 36) {
    const {Continent} = node;
    let dest = 0;
    switch(Continent) {
      case "Europe":
        dest = 36; break;
      case "Asia":
        dest = 37; break;
      case "Africa":
        dest = 38; break;
      case "North America":
        dest = 39; break;
      case "South America":
        dest = 40; break;
      case "Oceania":
        dest = 41; break;
      default:
        break;
    }

    links.push({source: index, target: dest, value: node["Total CO2"]});
  }

});


const nodes = data0.map(d => {
  return {name: d.Entity, continent: d.Continent};
});

const data = {
  nodes,
  links
}

// Set the diagram dimensions
const width = 900;
const height = 2000;

// Create an SVG container
const svg = d3.select('#alluvial')
  .attr('width', width)
  .attr('height', height);

// Initialize the Sankey generator
const sankeyGenerator = sankey()
  .nodeWidth(20)
  .nodePadding(10)
  .extent([[1, 1], [width - 1, height - 1]])
  .nodeAlign(sankeyCenter); // Optional alignment (e.g., sankeyLeft, sankeyRight)


// Generate the Sankey layout
const sankeyData = sankeyGenerator(data);

console.log(sankeyData.nodes);

 // Generate color shades for each continent and its countries
const continentShadeMap = {};
data0.forEach(node => {
  const { Continent } = node;
  if (!continentShadeMap[Continent]) {
    // Generate 6 shades for each continent
    continentShadeMap[Continent] = getShades(continentColors[Continent], 6);
  }
});

// Draw the links with colors based on the source and target countries' shades
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
    
    // Get the correct shade for the source and target
    const sourceShadeIndex = nodes.filter(node => node.name === d.source.name && node.continent === sourceContinent).indexOf(d.source);
    const targetShadeIndex = nodes.filter(node => node.name === d.target.name && node.continent === targetContinent).indexOf(d.target);

    // Color the link based on source and target shades
    return d3.scaleLinear()
      .domain([0, 1])
      .range([continentShadeMap[sourceContinent][sourceShadeIndex], continentShadeMap[targetContinent][targetShadeIndex]])(0.5);
  })
  .attr('opacity', 0.5);

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