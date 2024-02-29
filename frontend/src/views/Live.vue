<template>
  <v-container class="container" align="center">
    <v-row class="row">
      <v-col cols="9">
        <figure class="highcharts-figure">
          <div id="container"></div>
        </figure>
      </v-col>
      <v-col cols="3">
        <v-card
          class="mb-5"
          style="max-width: 500px"
          color="primaryContainer"
          subtitle="Temperature"
        >
          <v-card-item>
            <span class="text-onPrimaryContainer text-h3">
              {{ temperature }}
            </span>
          </v-card-item>
        </v-card>
        <v-card
          class="mb-5"
          style="max-width: 500px"
          color="tertiaryContainer"
          subtitle="Heat Index (Feels Like)"
        >
          <v-card-item>
            <span class="text-onTertiaryContainer text-h3">
              {{ heatindex }}
            </span>
          </v-card-item>
        </v-card>
        <v-card
          class="mb-5"
          style="max-width: 500px"
          color="secondaryContainer"
          subtitle="Humidity"
        >
          <v-card-item>
            <span class="text-onSecondaryContainer text-h3">
              {{ humidity }}
            </span>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
    <v-row class="row" justify="start">
      <v-col class="col-9">
        <figure class="highcharts-figure">
          <div id="container1"></div>
        </figure>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
/** JAVASCRIPT HERE */

// IMPORTS

import { useMqttStore } from "@/store/mqttStore"; // Import Mqtt Store
import { storeToRefs } from "pinia";

// Highcharts, Load the exporting module and Initialize exporting module.
import Highcharts from "highcharts";
import more from "highcharts/highcharts-more";
import Exporting from "highcharts/modules/exporting";
Exporting(Highcharts);
more(Highcharts);

import {
  ref,
  reactive,
  watch,
  onMounted,
  onBeforeUnmount,
  computed,
} from "vue";

import { useRoute, useRouter } from "vue-router";

// VARIABLES
const router = useRouter();
const route = useRoute();

const Mqtt = useMqttStore();
const { payload, payloadTopic } = storeToRefs(Mqtt);

const tempHiChart = ref(null); // Chart object
const humChart = ref(null); // Chart object

const points = ref(600); // Specify the quantity of points to be shown on the live graph simultaneously.
const shift = ref(false); // Delete a point from the left side and append a new point to the right side of the graph.

// FUNCTIONS

onMounted(() => {
  // THIS FUNCTION IS CALLED AFTER THIS COMPONENT HAS BEEN MOUNTED
  CreateCharts();
  CreateCharts_2();

  Mqtt.connect(); // Connect to Broker located on the backend
  setTimeout(() => {
    // Subscribe to each topic
    Mqtt.subscribe("620152511");
    Mqtt.subscribe("620152511_sub");
  }, 3000);
});

onBeforeUnmount(() => {
  // THIS FUNCTION IS CALLED RIGHT BEFORE THIS COMPONENT IS UNMOUNTED
  // unsubscribe from all topics
  Mqtt.unsubcribeAll();
});

const CreateCharts = async () => {
  // TEMPERATURE CHART
  tempHiChart.value = Highcharts.chart("container", {
    chart: { zoomType: "x" },
    title: { text: "Air Temperature and Heat Index Analysis", align: "left" },
    yAxis: {
      title: {
        text: "°C",
        style: { color: "#000000" },
      },
      labels: { format: "{value} °C" },
    },
    xAxis: {
      type: "datetime",
      title: { text: "Time", style: { color: "#000000" } },
    },
    tooltip: { shared: true },
    series: [
      {
        name: "Temperature",
        type: "spline",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[0],
      },
      {
        name: "Heat Index",
        type: "spline",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[1],
      },
    ],
  });
};

const CreateCharts_2 = async () => {
  // Humidity CHART
  humChart.value = Highcharts.chart("container1", {
    chart: { zoomType: "x" },
    title: { text: "Humidity Analysis(Live)", align: "left" },
    yAxis: {
      title: {
        text: "%",
        style: { color: "#000000" },
      },
      labels: { format: "{value} %" },
    },
    xAxis: {
      type: "datetime",
      title: { text: "Time", style: { color: "#000000" } },
    },
    tooltip: { shared: true },
    series: [
      {
        name: "Humidity",
        type: "spline",
        data: [],
        turboThreshold: 0,
        color: Highcharts.getOptions().colors[0],
      },
    ],
  });
};

// COMPUTED PROPERTIES
const temperature = computed(() => {
  if (!!payload.value) {
    return `${payload.value.temperature.toFixed(2)} °C`;
  }
});
const heatindex = computed(() => {
  if (!!payload.value) {
    return `${payload.value.heatindex.toFixed(2)} °C`;
  }
});
const humidity = computed(() => {
  if (!!payload.value) {
    return `${payload.value.humidity.toFixed(2)} %`;
  }
});

// WATCHERS
watch(payload, (data) => {
  if (points.value > 0) {
    points.value--;
  } else {
    shift.value = true;
  }
  tempHiChart.value.series[0].addPoint(
    { y: parseFloat(data.temperature.toFixed(2)), x: data.timestamp * 1000 },
    true,
    shift.value
  );
  tempHiChart.value.series[1].addPoint(
    { y: parseFloat(data.heatindex.toFixed(2)), x: data.timestamp * 1000 },
    true,
    shift.value
  );
  humChart.value.series[0].addPoint(
    { y: parseFloat(data.humidity.toFixed(2)), x: data.timestamp * 1000 },
    true,
    shift.value
  );
});
</script>

<style scoped>
.row {
  max-width: 1200px;
}

.container {
  background-color: #f5f5f5;
  width: 1200px;
  height: 900px;
}

figure {
  border: 2px solid black;
}
</style>