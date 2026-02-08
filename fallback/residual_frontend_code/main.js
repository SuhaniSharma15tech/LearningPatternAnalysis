
// single student score value 
document.getElementById("predictedScore").innerText =
  MODEL_OUTPUT.score_value;

// spider chart comes from here i actually didnt find any way myself
// to make this so chatgippity 
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


// this is academic bar graph;
new Chart(document.getElementById("academicBar"), {
  type: "bar",
  data: {
    labels: MODEL_OUTPUT.charts.academic_distribution.map(d => d.name),
    datasets: [{
      label: "Students",
      data: MODEL_OUTPUT.charts.academic_distribution.map(d => d.value)
    }]
  },
  options: {
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

// here is Persona distribution bar graph;
new Chart(document.getElementById("personaBar"), {
  type: "bar",
  data: {
    labels: MODEL_OUTPUT.charts.overall_persona_distribution.map(d => d.name),
    datasets: [{
      label: "Students",
      data: MODEL_OUTPUT.charts.overall_persona_distribution.map(d => d.value)
    }]
  },
  options: {
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


// pie chart for the academic clusters;
const pieCanvasIds = ["steadyPie", "improvedPie", "decliningPie"];
const clusterEntries = Object.entries(
  MODEL_OUTPUT.charts.persona_per_academic_cluster
);

clusterEntries.forEach(([clusterName, personas], i) => {
  new Chart(document.getElementById(pieCanvasIds[i]), {
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
