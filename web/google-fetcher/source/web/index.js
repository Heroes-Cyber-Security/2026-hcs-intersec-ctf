const express = require("express");
const axios = require("axios");
const app = express();
const PORT = 8080;

app.get("/", (req, res) => {
  res.send(`
        <h1>URL Fetcher (BETA)</h1>
        <p>Gunakan endpoint /fetch?url=http://google.com untuk mengambil data dari URL.</p>
    `);
});

app.get("/fetch", async (req, res) => {
  const { url } = req.query;

  if (!url) {
    return res.status(400).send("Parameter 'url' dibutuhkan!");
  }

  if (!url.startsWith("http://google") && !url.startsWith("https://google")) {
    return res
      .status(403)
      .send(
        "Akses Ditolak: URL harus berawalan http://google atau https://google",
      );
  }

  try {
    const response = await axios.get(url, { timeout: 3000 });
    res.send(response.data);
  } catch (error) {
    res.status(500).send("Gagal melakukan fetch: " + error.message);
  }
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Web service listening on port ${PORT}`);
});
