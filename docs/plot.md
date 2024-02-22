# Plot

```js
import {map} from "./components/timeline.js";
```

```js
const world = await FileAttachment("./data/world.json").json();
const data = await FileAttachment("./data/data.json").json();
```

```js
const dates = Object.keys(data).filter(k => k !== "domain")

const counter = view(Inputs.button([
  ["Previous", value => value > 0 ? value - 1 : value],
  ["Next", value => value < dates.length - 1 ? value + 1 : value],
  ["Reset", value => 0]
], {value: 0, label: "Controls"}))
```

```js
const date = dates[counter]
const dataToPlot = data[date]
```

```js
display(date)
```

```js
map(world, dataToPlot, data["domain"])
```
