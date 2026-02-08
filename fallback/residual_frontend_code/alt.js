//   if (MODEL_OUTPUT.type === "single") {
//     // Update Score
//     const scoreEl = document.getElementById("predictedScore");
//     if (scoreEl) scoreEl.innerText = MODEL_OUTPUT.score_value;

//     // Render Spider Chart
//     const ctx = document.getElementById("spiderChart");
//     chartInstances["spiderChart"] = new Chart(ctx, {
//       type: "radar",
//       data: {
//         labels: MODEL_OUTPUT.charts.spider_chart.data.map(d => d.subject),
//         datasets: [{
//           label: "Performance Profile",
//           data: MODEL_OUTPUT.charts.spider_chart.data.map(d => d.value),
//           backgroundColor: 'rgba(0, 198, 255, 0.2)',
//           borderColor: '#00c6ff',
//           borderWidth: 2
//         }]
//       },
//       options: {
//         responsive: true,
//         scales: { r: { min: 0, max: 100 } }
//       }
//     });
