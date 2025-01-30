const express = require("express");
const app = express();
const path = require("path");
const PORT = process.env.PORT || 3000;
const { InfluxDB } = require("@influxdata/influxdb-client");
require("dotenv").config(); //Load .env file
console.log("INFLUX_URL:", process.env.INFLUX_URL); //Checking fron .env

const url = "http://localhost:8086";
const token =
  "";
const org = "hepl";
const bucket = "nichoir";
const capturedImagesjson = [];

const client = new InfluxDB({ url, token });
const query_api = client.getQueryApi(org);

app.use(express.static(path.join(__dirname, "public")));

app.get("/queryReadNichoir", (req, res) => {
  const query = `
    from(bucket: "${bucket}")
      |> range(start: -1d)  // Adjust the time range as needed
      |> filter(fn: (r) => r._measurement == "photos")
      |> sort(columns: ["_time"], desc: true)
  `;

  const capturedImagesjson = [];

  //Execute the query
  query_api.queryRows(query, {
    next(row, tableMeta) {
      const rowData = tableMeta.toObject(row);

      //Extract the combined JSON field
      const dataField = rowData._value || null;
      const timestamp = rowData._time || null;

      let metadata = {};

      if (dataField) {
        try {
          //Parse the JSON data field
          metadata = JSON.parse(dataField);
        } catch (error) {
          console.error("Error parsing JSON field:", error);
        }
      }

      const device = metadata.device || null;
      const location = metadata.location || null;
      const imagePath = metadata.path || null;

      console.log(`Time: ${timestamp}`);
      console.log(`Device: ${device}`);
      console.log(`Location: ${location}`);
      console.log(`Image Path: ${imagePath}`);
      console.log();

      // Store data in JSON format
      const capturedImageJson = {
        timestamp,
        device,
        location,
        imagePath,
      };
      capturedImagesjson.push(capturedImageJson);
    },
    error(error) {
      console.error(`Error executing query: ${error}`);
      res.status(500).json({ error: "Error during query" });
    },
    complete() {
      console.log("Query completed successfully.");
      //Return the collected data as JSON
      res.json(capturedImagesjson);
    },
  });
});

app.get("/images", async (req, res) => {
  const query = `
    from(bucket: "${bucket}")
      |> range(start: -1d)  // Adjust the time range as needed
      |> filter(fn: (r) => r._measurement == "photos")
      |> sort(columns: ["_time"], desc: true)
  `;

  const images = [];

  try {
    const rows = await query_api.collectRows(query);

    //Extract `path` and `timestamp`
    const images = rows.map((row) => {
      const metadata = JSON.parse(row._value); //Parse the JSON data field
      return {
        path: `/images/${metadata.path.split("/").pop()}`,
        timestamp: metadata.timestamp || row._time,
      };
    });

    console.log(images);
    res.json(images); //Return image data as JSON
  } catch (error) {
    console.error("Error querying InfluxDB:", error);
    res.status(500).send("Error fetching images.");
  }
});


app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "views", "index.html"));
});

app.get("/index.html", (req, res) => {
  res.sendFile(path.join(__dirname, "views", "index.html"));
});

app.get("/capturedImages.html", (req, res) => {
  res.sendFile(path.join(__dirname, "views", "capturedImages.html"));
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
