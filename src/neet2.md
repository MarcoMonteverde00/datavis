<link rel="stylesheet" href="style.css">

<div class="hero">

# Who are the NEETs in Italy?

</div>

<br />
The acronym <b>"NEET"</b>, which stands for "Not in Education, Employement or Training", refers to the young people, between <b>15-29 years old</b>, which
are not studying, nor working and are not engaged in any training activity.
In this population there are, however, people with significantly <b>different features</b>, with respect to the sex, the age, the degree,
the citizenship and the role in the family.

These factors are examined in the years 2021,2022 and 2023.
  

<h3> More young <span style="color:DeepPink">women</span> are NEET </h3>
<h2>  </h2>

```js
	const dataSex = await FileAttachment("./data/Neet_sex.csv").csv();

	const years = [2021,2022,2023];
	
	const selected_year = Inputs.select(years, {value: 2023, label: "Year:", format: (d) => d});
	view(selected_year);
	
	years.forEach(year =>{ 
		dataSex[`${year}`] = dataSex.filter(row => row["Year"] == year );
		//dataFR[`${year}`] = dataFR.filter(row => row["Year"] == year );
	});
		
	let plot;

	let plot_legend;

	function showPlot() {
	
		let ds = dataSex[selected_year.value];
	
		plot=display(Plot.plot({
			marginLeft: 90,
			width: 900,
			height: 360,
			title : `Sex comparison in ${selected_year.value}`,
			x: {label: "Sex", percent: false},
			y: {label: "Neet (k)", padding: 0.2, domain:[0,1100],grid: true},
			color: { domain: ["Female", "Male"], range: ["DeepPink", "Blue"], legend: true},
			marks: [
			  Plot.barY(
				ds,
				{   
				  x: "Sex",
				  y: "Value",
				  fill: "Sex",
				  channels: {Incidence : 'Prop'},
				  tip: {
					format: {
					  y: (d) => `${d.toFixed(2)}`, 
					  Incidence: (d) =>`${d} %`,
					  fill: false
					}
				  }
				}
			  ),
			  Plot.ruleY([0]),
			  Plot.text(ds, {x: "Sex",y: "Value",dy: -6, lineAnchor: "bottom", text:(d) => `Neet: ${d.Value} (k)`})				


			]
	  })
	  );
	
	}
	
	
	showPlot();


	selected_year.addEventListener("change", (e) => {

	  if (plot != undefined) {
		plot.parentNode.removeChild(plot);
	  }
	  if (plot_legend != undefined) {
		plot_legend.parentNode.removeChild(plot_legend);
	  }
	  showPlot();
	});
	
	
	

```
</div>
<a href="https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0500LAB,1.0/LAB_OFFER/LAB_OFF_SUPPLDATA/DCCV_NEET1/IT1,172_931_DF_DCCV_NEET1_1,1.0" style="color: #808080; font-size: 12px; text-decoration: none;">
    Data Source: [ISTAT]
</a>

In all the years taken into account the plots show that there are <b>more women</b> NEET than men, even though the difference is not extremely
significant. Moreover, the <b>"Incidence"</b> value, that represents the proportional value of the NEET with respect to the relative population,
confirms this result. 

<h3> How old are NEETs? <span style="color:DeepPink">women</span> older than <span style="color:Blue">men</span> </h3>

```js
	const dataAgeSex = await FileAttachment("./data/Neet_age_sex.csv").csv();
	
	const years = [2021,2022,2023];
	const selected_year = Inputs.select(years, {value: 2023, label: "Year:", format: (d) => d});
	view(selected_year);
	
	years.forEach(year =>{ 
		dataAgeSex[`${year}`] = dataAgeSex.filter(row => row["Year"] == year );
	});
	
	let plot2;

	let plot2_legend;
	
	//const color = d3.scaleOrdinal(d3.schemeBlues[3]);


	function showPlot2() {
		let dAS = dataAgeSex[selected_year.value];

	plot2= display(
	  Plot.plot({
		marginLeft: 90,
		width: 900,
		height: 360,
		title: `Age comparison by sex in ${selected_year.value}`,
		//subtitle: "Carbone dioxide (CO2) emissions proportions of each continent divided into theirs top 5 polluting countries and the sum of all the other ones in 2022.",
		x: {label: "Class age", percent: false,ticks:5},
		y: {label: "NEET (k)", padding: 0.2, domain: [0,600],grid: true},
			color: { domain: ["Female", "Male"], range: ["DeepPink", "Blue"], legend: true},
		marks: [
			Plot.ruleY([0]),
			Plot.lineY(dAS, {x: "Age", y: "Value", stroke: "Sex", marker: true,channels: {Incidence : "Prop"}, 
				tip: {
					format: {
					  y: (d) => `${d.toFixed(2)}`,  
					  Incidence: (d) =>`${d} %`,			  
					  fill: false
					}
				  }})
			//Plot.text(dAS, {x: "Age",y: "Value",fx: "Sex",dy: -6, lineAnchor: "bottom", text:(d) => `Neet: ${d.Value} (k)`})	
		]
	  })
	);
	}

	showPlot2();

	selected_year.addEventListener("change", (e) => {

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
<a href="https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0500LAB,1.0/LAB_OFFER/LAB_OFF_SUPPLDATA/DCCV_NEET1/IT1,172_931_DF_DCCV_NEET1_1,1.0" style="color: #808080; font-size: 12px; text-decoration: none;">
Data Source: [ISTAT]
</a>

To evaluate the differences among the NEET population with respect to the age, the total age range, 15-29 years old, is divided
into three classes, "15-19", "20-24" and "25-29". 

As for the factor "sex", the result is the same over all the three years considered and it shows that: among the <b>women</b> NEETs belong mainly to the class <b>"25-29 y.o."</b>, among the <b>men</b>, instead, <b>"20-24 y.o."</b>.
The difference between the classes "20-24" and "25-29" for the men is not really significant; considering the total population, without sex distinction, then
the result would confirm that the NEETs are mainly people between 25 and 29 years old.   

<h3> Less NEETs with a third level education </h3> 

<div class="plot">

```js
	const dataDegree = await FileAttachment("./data/Neet_degree_mean.csv").csv();

	const values_Heatmap = dataDegree.map(d => d["Value"]);
	const minHeatmap = Math.min(...values_Heatmap);
	const maxHeatmap = Math.max(...values_Heatmap);
	
	const years = [2021,2022,2023];
	const selected_year = Inputs.select(years, {value: 2023, label: "Year:", format: (d) => d});
	view(selected_year);
	
	years.forEach(year =>{ 
		dataDegree[`${year}`] = dataDegree.filter(row => row["Year"] == year );
	});
	
	
	let plot2;

	function showPlot1() {
		let ds = dataDegree[selected_year.value];

		plot2 = display(
			Plot.plot({
			  padding: 0,
			  marginLeft: 150,
			  marginBottom: 80,
			  width: 900,
			  height: 360,
			  title : `Degree title comparison by sex in ${selected_year.value}`,
			  x: {
			  label: "Sex",
			  tickRotate: -30
			  },
			className: "heatmap",
			  color: {
				type: "linear",
				n: 9,
				domain: [minHeatmap-100, maxHeatmap],
				scheme: "blues",
				label: "NEET (k)",
				legend: true
			  },
			  marks: [
				Plot.cell(ds, {
				  x: "Sex",
				  y: "Degree",
				  fill: d => (d["Value"]),
				  inset: 0.5,
				  channels: { Incidence: 'Prop'  },
                    tip: {
                        format: {Incidence: (d) =>`${d} %`}
                    }
				}),
				Plot.text(ds, {x: "Sex",y: "Degree", text:(d) => `NEET: ${d.Value} k`, fill: "black", fill: (d) => (d.Value > 350 ? "white" : "black")})				
			  ]
			})
		)
		}

	showPlot1();


selected_year.addEventListener("change", (e) => {

  if (plot2 != undefined) {
    plot2.parentNode.removeChild(plot2);
  }
  showPlot1();
});
```

</div>
<a href="https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0500LAB,1.0/LAB_OFFER/LAB_OFF_SUPPLDATA/DCCV_NEET1/IT1,172_931_DF_DCCV_NEET1_2,1.0" style="color: #808080; font-size: 12px; text-decoration: none;">
Data Source: [ISTAT]
</a>

The relationship between NEET and the degree shows that, in all the three years and for both the sexes, the majority of NEETs have an <b>high school diploma</b>
then those who do not have any title, <b>none</b>, and lastly the ones who have a <b>degree or post degree</b>.   



<h3> Are NEETs mainly Italian?</h3>

```js
	const dataCIT = await FileAttachment("./data/Neet_CIT.csv").csv();

	const values_Heatmap = dataCIT.map(d => d["Value"]);
	const minHeatmap = Math.min(...values_Heatmap);
	const maxHeatmap = Math.max(...values_Heatmap);
	
	const years = [2021,2022,2023];
	const selected_year = Inputs.select(years, {value: 2023, label: "Year:", format: (d) => d});
	view(selected_year);
	
	years.forEach(year =>{ 
		dataCIT[`${year}`] = dataCIT.filter(row => row["Year"] == year );
	});
	
	
	let plot2;

	function showPlot1() {
		let ds = dataCIT[selected_year.value];

		plot2 = display(
		  Plot.plot({
			
			title: `Citizenship Comparison by sex in ${selected_year.value}`,
			marginLeft: 90,
			width: 900,
			height: 360,			y: {label: "Citizenship", percent: false,ticks:5},
			x: {label: "NEET (k)", domain:[0,900],padding: 0.2,grid: true},
			color: { domain: ["Female", "Male"], range: ["DeepPink", "MediumBlue"], legend: true},			
			marks: [
			  //Plot.ruleX([0]),
			  Plot.ruleY(ds, Plot.groupY({x1: "min", x2: "max"}, {x: "Value", y: "Citizenship", z: "Citizenship", sort: {y: "x1"}})),
			  Plot.dot(ds, {x: "Value", y: "Citizenship", z: "Citizenship", fill: "Sex",  
				channels: { Neet: 'value',Incidence: 'Prop'  },
                tip: {
                    format: {Neet: d => `${Number(d)}`,Incidence: (d) =>`${d} %`}
                }})//, // color in input order
			  //Plot.text(ds, {x: "Value", y: "Citizenship", textAnchor: "bottom", dy: +6, text:(d) => `NEET: ${d.Value} k`})
			]
			
			
		  })
		);
	}

	showPlot1();

	selected_year.addEventListener("change", (e) => {

	  if (plot2 != undefined) {
		plot2.parentNode.removeChild(plot2);
	  }
	  showPlot1();
	});

```





</div>
<a href="https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0500LAB,1.0/LAB_OFFER/LAB_OFF_SUPPLDATA/DCCV_NEET1/IT1,172_931_DF_DCCV_NEET1_3,1.0" style="color: #808080; font-size: 12px; text-decoration: none;">
Data Source: [ISTAT]
</a>

Evaluating the absolute value of NEET with respect to the citizenship, for both females and males, the result would show
a very significant difference between italians and foreigners, with NEET being mainly made up of <b>italians</b>.

However, this result is not so significant because it is misleading: the important gap is due to the great difference,
 in terms of numbers, between the italians and foreigners. Therefore it is necessary to analyse the <b>incidence</b>, rather then 
the absolute value. 


<h3> NEETs are actually mainly foreigners</h3> 

<div class="plot">

```js
const dataCIT = await FileAttachment("./data/Neet_CIT.csv").csv();


	const years = [2021,2022,2023];
	const selected_year = Inputs.select(years, {value: 2023, label: "Year:", format: (d) => d});
	view(selected_year);
	
	years.forEach(year =>{ 
		dataCIT[`${year}`] = dataCIT.filter(row => row["Year"] == year );
	});
	
	
	let plot2;

	function showPlot1() {
		let ds = dataCIT[selected_year.value];

		plot2 = display(
			Plot.plot({
			  facet: {
				data: ds,
				x: "Sex"//,
				//label: "Proportion of NEET people (color) vs. share of population (gray), by citizenship and year"
			  },
			  x: {
			    label: "Incidence",
				axis: "top",
				domain:[0,100],
				grid: true,
				//ticks: d3.range(0, 51, 10),
				//tickFormat: (d) => (d === 50 ? `${d}%` : `${d}`),
				tickSize: 0
			  },
			  y: {
				label: null,
				domain: ["Foreigner", "Italian"]
			  },
			marginLeft: 90, 
			width: 1000,
			height: 300,
			title: `Proportion of NEET (color) vs. share of population (gray), by citizenship and sex in ${selected_year.value}`,  
			color: { domain: ["Female", "Male"], range: ["DeepPink", "Blue"], legend: true},
			  marks: [
				Plot.barX(ds, {
				  x: "PropPop",
				  y: "Citizenship",
				  fill: "Silver",
				  insetTop: 2,
				  insetBottom: 2
				}),
				Plot.barX(ds, {
				  x: "Prop",
				  y: "Citizenship",
				  fill: "Sex",
				  fx: "Sex",
				  //sort: { fx: "Citizenship", reverse: true },
				  insetTop: 6,
				  insetBottom: 6,
				  channels: { Neet: 'Value', Population: 'PropPop'},
                    tip: {
                        format: {Neet: d => `${Number(d)} k`,x: (d) =>`${d} %`, Population: d => `${Number(d)} %`}
                    }
				}),
				Plot.text(ds, {x: 100,y: "Citizenship",fx: "Sex", textAnchor: "end", text:(d) => `NEET: ${d.Value} k`})				

			  ]
			})
		)
		}

	showPlot1();


selected_year.addEventListener("change", (e) => {

  if (plot2 != undefined) {
    plot2.parentNode.removeChild(plot2);
  }
  showPlot1();
});
```
</div>
<a href="https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0500LAB,1.0/LAB_OFFER/LAB_OFF_SUPPLDATA/DCCV_NEET1/IT1,172_931_DF_DCCV_NEET1_3,1.0" style="color: #808080; font-size: 12px; text-decoration: none;">
Data Source: [ISTAT]
</a>

Considering the incidence, which represents as percentage the number of NEET over the cardinality of the corresponding 
population, we get another outcome: almost the <b>same percentage</b> of italians and foreigners <b>men</b> are NEETs while the NEET foreigners
<b>women</b> are <b>about twice as much</b> the italian ones.


<h3> Does not having family responsabilities influence being NEETs? </h3> 

<div class="plot">

```js

	const dataFR = await FileAttachment("./data/Neet_FR.csv").csv();
	const dataFR_TEXT = await FileAttachment("./data/Neet_FR_TEXT_Sex.csv").csv();

	const years = [2023, 2022, 2021];
	const selected_year = Inputs.select(years, {value: 2023, label: "Year:", format: (d) => d});
	view(selected_year);
	
	years.forEach(year => {dataFR[`${year}`] = dataFR.filter(row => row["Year"] == year );});
	
	//const Factors = ["Sex", "Citizenship"];
	//const selected_factor = Inputs.select(Factors, {value: "Total", label: "Factor:", format: (d) => d});
	//view(selected_factor);
	
	//Factors.forEach(factor => {dataFR_TEXT[`${factor}`] = dataFR_TEXT.filter(row => row["Index"] == factor );});

	years.forEach(year => {dataFR_TEXT[`${year}`] = dataFR_TEXT.filter(row => row["Year"] == year );});

	let plot3;

	let plot3_legend;

	function showPlot3() {
		let dFR = dataFR[selected_year.value];
		let dFR_TEXT = dataFR_TEXT[selected_year.value];
		


		plot3= display(
		
			Plot.plot({
				marginLeft: 90,
				width: 900,
				height: 360,
				title: `Family role comparison by sex in ${selected_year.value}`,
				x: {label: "Sex", percent: false,ticks:5},
				y: {label: "NEET (k)", padding: 0.2, domain: [0,1000],grid: true},
		        //color: { domain: ["Parent", "Single/Partner without children/Other", "Son/Daughter"], range: ["Lavender", "SkyBlue", "Pink"], legend: true},
				color: { domain: ["Female", "Male"], range: ["DeepPink", "Blue"], legend: true},				
				marks: [
				
				  Plot.barY(
						dFR,
						{   
						  x: "Sex",
						  y: "Value",
						  fx: "Family Role",
						  fill: "Sex",
						  channels: { Citizenship: "Citizenship", Incidence: "Prop"},
						  tip: {
							format: {
							  y: (d) => `${d.toFixed(2)}`, 
							  Incidence: (d) =>`${d} %`,
							  fill: false
							}
						  }
						}
					  ),
					Plot.ruleY([0]), 
					Plot.text(dFR_TEXT, {x: "Sex" ,y: "Sum1",fx: "Family Role",dy: -6, lineAnchor: "bottom", text:(d) => `Neet: ${d.Sum1} (k)`})
				]
			  })
			  );
		
		
		
		
	}

	showPlot3();
	
	selected_year.addEventListener("change", (e) => {

	  if (plot3 != undefined) {
		plot3.parentNode.removeChild(plot3);
	  }
	  if (plot3_legend != undefined) {
		plot3_legend.parentNode.removeChild(plot3_legend);
	  }
	  showPlot3();
	});
```

</div>
<a href="https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0500LAB,1.0/LAB_OFFER/LAB_OFF_SUPPLDATA/DCCV_NEET1/IT1,172_931_DF_DCCV_NEET1_5,1.0" style="color: #808080; font-size: 12px; text-decoration: none;">
Data Source: [ISTAT]
</a>

The last factor analysed is about the role in the family of the NEETs. At this purpose three roles have been identified:
<b>Son/Daugther</b>, <b>Single/Partner without children/Other</b>, <b>Parent</b>.

It is immediately evident that, with respect to the role of <b>Parent</b>, there is an important difference among the sexes, the number of women that are
mothers and NEETs is about <b>10 times</b> the one of men.
  
However for both females and males, the highest values of NEETs are in correspondence of <b>Son and Daugther</b>.
And viceversa only few of the people who have a family responsability, <b>Single/Partner without children/Other</b>
and <b>Parent</b>, are NEET.

This result could misleads the readers into thinking that NEETs are mainly son or daughters, and hence people without an important
responsability towards theirs families. 

Analyzing the <b>incidence</b> value in fact, this conclusion results completely wrong for the females, showing two opposite pictures
for men and women.



<div class="plot">
<h3> Parenthood has a different influence on <span style="color:DeepPink">women</span> and <span style="color:Blue">men</span> </h3> 

```js
const dataFRprop = await FileAttachment("./data/Neet_FR_POP.csv").csv();


	const years = [2021,2022,2023];
	const selected_year = Inputs.select(years, {value: 2023, label: "Year:", format: (d) => d});
	view(selected_year);
	
	years.forEach(year =>{ 
		dataFRprop[`${year}`] = dataFRprop.filter(row => row["Year"] == year );
	});
	
	
	let plot2;

	function showPlot1() {
		let ds = dataFRprop[selected_year.value];

		plot2 = display(
			Plot.plot({
			  facet: {
				data: ds,
				x: "Sex"//,
				//label: "Proportion of NEET people (color) vs. share of population (gray), by family role and year"
			  },
			  x: {
			    label: "Incidence",
				axis: "top",
				domain:[0,100],
				grid: true,
				//ticks: d3.range(0, 51, 10),
				//tickFormat: (d) => (d === 50 ? `${d}%` : `${d}`),
				tickSize: 0
			  },
			  y: {
				label: "Family Role",
				domain: ["Parent", "Single/Partner without children/Other", "Son/Daughter"],
				tickRotate: -30
			  },
			marginLeft: 200, 
			width: 1000,
			height: 300,
			title: `Proportion of NEET (color) vs. share of population (gray), by family role and sex in ${selected_year.value}`,  
			color: { domain: ["Female", "Male"], range: ["DeepPink", "Blue"], legend: true},
			  marks: [
				Plot.barX(ds, {
				  x: "PropPop",
				  y: "Family Role",
				  fill: "Silver",
				  insetTop: 2,
				  insetBottom: 2
				}),
				Plot.barX(ds, {
				  x: "Prop",
				  y: "Family Role",
				  fill: "Sex",
				  fx: "Sex",
				  //sort: { fx: "Citizenship", reverse: true },
				  insetTop: 6,
				  insetBottom: 6,
				  channels: { Neet: 'Sum1', Population: 'PropPop'},
                    tip: {
                        format: {Neet: d => `${Number(d)} k`,x: (d) =>`${d} %`, Population: d => `${Number(d)} %`}
                    }
				}),
				Plot.text(ds, {x: 100,y: "Family Role",fx: "Sex", textAnchor: "end", text:(d) => `NEET: ${d.Sum1} k`})				

			  ]
			})
		)
		}

	showPlot1();


selected_year.addEventListener("change", (e) => {

  if (plot2 != undefined) {
    plot2.parentNode.removeChild(plot2);
  }
  showPlot1();
});
```
</div>
<a href="https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0500LAB,1.0/LAB_OFFER/LAB_OFF_SUPPLDATA/DCCV_NEET1/IT1,172_931_DF_DCCV_NEET1_5,1.0" style="color: #808080; font-size: 12px; text-decoration: none;">
Data Source: [ISTAT]
</a>

What is immediately evident by looking at the representation above is that the trends of the colured bars, which represent
the NEET incidence, are completly the opposite between males and females. NEETs women are mainly those with an active family role
and in particular those that are mothers. Viceversa, even if the changes is almost null, NEETs are mainly men that do not have an active family role.

Another worrying result is that more than the <b>60%</b> of young women that has children belongs to the NEETs.

*To summarise:*

NEETS are mainly <b>women</b>, whose age is in <b>25-29</b> and which have an <b>high school diploma</b>,
and they are particularly influenced by the <b>citizenship</b> and the <b>family role</b>. 