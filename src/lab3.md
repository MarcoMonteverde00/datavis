<link rel="stylesheet" href="style.css">

<div class="hero">

# Rotating Earth

</div>


```js
// THIS VERSION IS STATIC BUT WORKS
/*
Task 1: Equal Earth, Stereographic + ortographic Round Earth rotation
Task 2: Equal Earth, Stereographic + ortographic Round Earth rotation
Task Extra:
*/

/*
import * as d3 from 'd3';
import * as tj from 'topojson-client';

const world = await FileAttachment('./data/land-110m.json').json();
const land = topojson.feature(world, world.objects.land);

const globe = Plot.marks([Plot.graticule(), Plot.geo(land, {fill: "currentColor"}), Plot.sphere()])

const rotate = Inputs.form([
  Inputs.range([-180, 180], {step: 0.1, label: "λ"}),
  Inputs.range([-90, 90], {step: 0.1, label: "φ"}),
  Inputs.range([-180, 180], {step: 0.1, label: "γ"})
])

let rotate_view = view(rotate);

display(globe.plot({height: 640, inset: 1, projection: {type: "orthographic", rotate: rotate_view}}))
*/
```



```js

import * as d3 from 'd3';
import * as tj from 'topojson-client';

const world = await FileAttachment('./data/land-110m.json').json();
const land = topojson.feature(world, world.objects.land);

const globe = Plot.marks([Plot.graticule(), Plot.geo(land, {fill: "currentColor"}), Plot.sphere()]);

// Initial rotation values
let rotation = {
  λ: 0,   // Longitude
  φ: 0,   // Latitude
  γ: 0    // Rotation angle (spin)
};

// Create an input form for rotation control
const rotate = Inputs.form([
  Inputs.range([-180, 180], {step: 0.1, label: "λ", value: rotation.λ}),
  Inputs.range([-90, 90], {step: 0.1, label: "φ", value: rotation.φ}),
  Inputs.range([-180, 180], {step: 0.1, label: "γ", value: rotation.γ})
]);

let rotate_view = view(rotate);

// Function to animate the rotation
function animateRotation() {
  rotation.γ += 0.1; // Rotate around the globe (spin the Earth)

  // Update the input form values
  rotate.setValue({ λ: rotation.λ, φ: rotation.φ, γ: rotation.γ }); // HERE SHOULD BE THE PROBLEM TO BE SOLVED

  // Update the plot with the new rotation
  globe.plot({height: 640, inset: 1, projection: {type: "orthographic", rotate: rotate_view}});
}

// Set an interval to update the rotation every 100 milliseconds
setInterval(animateRotation, 100);

display(globe.plot({height: 640, inset: 1, projection: {type: "orthographic", rotate: rotate_view}}));

```