```js

const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

const dataMax = await FileAttachment("./data/countriesMaxTemperatures.csv").csv();
const dataAvg = await FileAttachment("./data/countriesAvgTemperatures.csv").csv();
const dataMin = await FileAttachment("./data/countriesMinTemperatures.csv").csv();

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
                y: d => Number(d["Value"])
            }),
            Plot.dot(dataAlabama2023Avg, {
                x: d => Number(d["Month"]), 
                y: d => Number(d["Value"])
            }),
            Plot.lineY(dataAlabama2023Min, {
                x: d => Number(d["Month"]), 
                y: d => Number(d["Value"])
            })
        ]
    })
);
```