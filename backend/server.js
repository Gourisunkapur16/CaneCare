const http = require("http");

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "application/json" });
  
  if (req.url === "/") {
    res.end(JSON.stringify({
      message: "🎓 Learnlytics Basic Server Working!",
      status: "Success",
      endpoints: {
        health: "/health",
        recommendations: "/api/recommendations"
      }
    }));
  } else if (req.url === "/health") {
    res.end(JSON.stringify({ 
      status: "Healthy", 
      server: "Learnlytics",
      timestamp: new Date().toISOString()
    }));
  } else if (req.url === "/api/recommendations") {
    res.end(JSON.stringify({
      recommendations: [
        { id: 1, title: "JavaScript Fundamentals", match: 95 },
        { id: 2, title: "React Basics", match: 88 }
      ]
    }));
  } else {
    res.end(JSON.stringify({ error: "Endpoint not found" }));
  }
});

const PORT = 5000;
server.listen(PORT, () => {
  console.log("🚀 Learnlytics Server running on http://localhost:" + PORT);
  console.log("💡 Test: http://localhost:" + PORT);
});
