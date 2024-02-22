import * as Plot from "npm:@observablehq/plot";

export function map(world, data, domain, { width, height } = {}) {
  return Plot.plot({
    projection: {
      type: "equirectangular",
      domain: domain,
    },
    color: {
      type: "quantile",
      n: 7,
      scheme: "BuRd",
      label: "Anomaly in °C",
      legend: true,
      tickFormat: (t) => (Math.round(t * 100) / 100).toFixed(2),
    },
    marks: [
      Plot.geo(data, {
        fill: (d) => d.properties.a,
        r: 1,
      }),
      Plot.geo(world, { fill: "currentColor" }),
    ],
  });
}
