function display_AI_Insights(MODEL_OUTPUT){
  insight_card=document.getElementById("insights");
  insight_card.innerHTML=`<p>${MODEL_OUTPUT.ai_insight}</p>`
  insight_card.style.display="block"
}

// Object to store chart instances to prevent overlapping/glitching
let chartInstances = {};

function update_layout(type) {
  const grid = document.getElementById(type)
  if (!grid) return;

  if (type === "single") {
    // Single view: One column, centered, restricted width for the spider chart
    grid.style.display = "flex";
    grid.style.flexDirection = "column";
    grid.style.alignItems = "center";
    grid.style.gap = "20px";
  } else {
      grid.style.display = "flex";
      grid.style.flexDirection = "column";

      const bars = document.getElementById("bars");
      bars.style.display = "flex";
      bars.style.flexWrap = "wrap"; // Crucial for responsiveness
      bars.style.gap = "40px";

      const pies = document.getElementById("pies");
      pies.style.display = "flex";
      pies.style.flexWrap = "wrap"; // Crucial for responsiveness
      pies.style.gap = "20px";




  }
}

function render_charts(MODEL_OUTPUT) {
  // 1. Clear existing charts to fix "weird" overlapping behavior
  Object.values(chartInstances).forEach(chart => chart.destroy());
  chartInstances = {};
  
  // 2.this thing ensures that all the chart-containers disappear everytime you re-run the function
  document.querySelectorAll(".grid").forEach(el => el.style.display='none')

  // 3. Adjust grid organization based on data type
  update_layout(MODEL_OUTPUT.type);

  if (MODEL_OUTPUT.type==="single"){
      // logic for spider charts
      // single student score value 
      document.getElementById("predictedScore").innerText = MODEL_OUTPUT.score_value;
     
  //  spider chart
      new Chart(document.getElementById("spiderChart"), {
          type: "radar",
          data: {
              labels: MODEL_OUTPUT.charts.spider_chart.data.map(d => d.subject),
              datasets: [{
                label: "Student Profile",
                data: MODEL_OUTPUT.charts.spider_chart.data.map(d => d.value),
                fill: true
              }]
            },
          options: {
              scales: {
                r: { min: 0, max: 100 }
              }
            }
          });
              }


   else if (MODEL_OUTPUT.type === "batch") {
    // Render Academic Bar
    chartInstances["academicBar"] = new Chart(document.getElementById("academicBar"), {
      type: "bar",
      data: {
        labels: MODEL_OUTPUT.charts.academic_distribution.map(d => d.name),
        datasets: [{
          label: "Students",
          data: MODEL_OUTPUT.charts.academic_distribution.map(d => d.value),
          backgroundColor: ['#F5F227','#27F579', '#F20A22']
        }]
      },
      options: {indexAxis: 'y' ,
          plugins: {
            tooltip: {
              callbacks: {
                label: ctx =>
                  `${ctx.raw} students (${MODEL_OUTPUT.charts.academic_distribution[ctx.dataIndex].percentage}%)`
              }
            }
          }
        }
      });
  

    // Render Persona Bar (Horizontal)
    chartInstances["personaBar"] = new Chart(document.getElementById("personaBar"), {
      type: "bar",
      data: {
        labels: MODEL_OUTPUT.charts.overall_persona_distribution.map(d => d.name),
        datasets: [{
          label: "Students",
          data: MODEL_OUTPUT.charts.overall_persona_distribution.map(d => d.value),
          backgroundColor: '#00c6ff'
        }]
      },

      options: {indexAxis: 'y',
          plugins: {
            tooltip: {
              callbacks: {
                label: ctx =>
                  `${ctx.raw} students (${MODEL_OUTPUT.charts.overall_persona_distribution[ctx.dataIndex].percentage}%)`
              }
            }
          }
        }
      });


    // Render Cluster Pies
    const pieCanvasIds = ["steadyPie", "improvedPie", "decliningPie"];
    const clusterEntries = Object.entries(MODEL_OUTPUT.charts.persona_per_academic_cluster);

    clusterEntries.forEach(([clusterName, personas], i) => {
      if (i >= pieCanvasIds.length) return;
      const canvasId = pieCanvasIds[i];
      chartInstances[canvasId] = new Chart(document.getElementById(canvasId), {
        type: "pie",
        data: {
          labels: personas.map(p => p.persona),
          datasets: [{
            data: personas.map(p => p.count)
          }]
        },
        options: {
            plugins: {
              tooltip: {
                callbacks: {
                  label: ctx =>
                    `${ctx.label}: ${ctx.raw} (${personas[ctx.dataIndex].percentage}%)`
                }
              }
            }
          }
        });
      });
          }
    
    // insights 
    display_AI_Insights(MODEL_OUTPUT)
}


