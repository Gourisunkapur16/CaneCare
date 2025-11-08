const http = require("http");

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "application/json" });
  
  if (req.url === "/") {
    res.end(JSON.stringify({
      message: "🎓 Learnlytics API is working!",
      status: "Success",
      nextStep: "Run npm install to add Express.js"
    }));
  } else if (req.url === "/health") {
    res.end(JSON.stringify({ status: "Healthy", timestamp: new Date().toISOString() }));
  }
});

const PORT = 5000;
server.listen(PORT, () => {
  console.log("🚀 Basic server running on http://localhost:" + PORT);
});
