<script>
  import { onMount } from 'svelte';
  import { Line } from 'svelte-chartjs';
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale,
  } from 'chart.js';
  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    PointElement,
    CategoryScale
  );
  let chartData = {
    labels: [],
    datasets: [
      {
        label: 'Sensor Data',
        data: [],
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };
let chartOptions = {
    responsive: true,
    animation: {
      duration: 0
    },
    scales: {
      x: {
        ticks: {
          maxRotation: 0,
          autoSkip: true,
          maxTicksLimit: 10,
          color: 'white',
          font: {
            size: 12
          }
        }
      },
      y: {
        beginAtZero: true,
        ticks: { 
          color: 'white',
          font: {
            size: 12
          }
        }
      }
    }
  };
  function fetchData() {
    fetch('/api/')
      .then(response => response.json())
      .then(data => {
        chartData.labels = data.map(item => new Date(item.timestamp).toLocaleTimeString());
        chartData.datasets[0].data = data.map(item => item.value);
        chartData = {...chartData}; // Trigger Svelte reactivity
      })
      .catch(error => console.error('Error fetching data:', error));
  }
  onMount(() => {
    fetchData(); // Fetch initial data
    const interval = setInterval(fetchData, 5000); // Fetch data every 5 seconds
    return () => clearInterval(interval);
  });
</script>
<main>
  <h1>Sensor Data Graph</h1>
  <div style="width: 800px; height: 400px;">
    <Line data={chartData} options={chartOptions} />
  </div>
</main>
