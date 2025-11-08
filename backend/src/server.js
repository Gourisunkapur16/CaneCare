const express = require("express");
const cors = require("cors");

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Test route
app.get("/", (req, res) => {
  res.json({ 
    message: "🎓 Learnlytics API Server is Running!",
    version: "1.0.0",
    timestamp: new Date().toISOString(),
    features: [
      "AI-Powered Recommendations",
      "Progress Analytics", 
      "Gamified Learning",
      "Interactive Coding"
    ]
  });
});

// Health check route
app.get("/health", (req, res) => {
  res.json({ 
    status: "✅ Healthy",
    server: "Learnlytics API",
    timestamp: new Date().toISOString()
  });
});

// Recommendation API route
app.get("/api/recommendations", (req, res) => {
  res.json({
    success: true,
    recommendations: [
      {
        id: 1,
        title: "JavaScript Fundamentals",
        difficulty: "beginner",
        matchScore: 95,
        reason: "Matches your interest in web development"
      },
      {
        id: 2,
        title: "React for Beginners", 
        difficulty: "beginner",
        matchScore: 88,
        reason: "Popular among learners with your profile"
      },
      {
        id: 3,
        title: "Node.js Backend Mastery",
        difficulty: "intermediate", 
        matchScore: 76,
        reason: "Next step in your learning path"
      }
    ]
  });
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log("🚀 Learnlytics Server started successfully!");
  console.log("📚 API running on: http://localhost:" + PORT);
  console.log("❤️  Health check: http://localhost:" + PORT + "/health");
  console.log("🎯 Recommendations: http://localhost:" + PORT + "/api/recommendations");
  console.log("");
  console.log("💡 Test these endpoints in your browser!");
});
