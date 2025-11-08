class RecommendationService {
  constructor() {
    this.courses = [
      {
        id: 1,
        title: "JavaScript Fundamentals",
        category: "programming",
        difficulty: "beginner",
        tags: ["javascript", "web-development"],
        popularity: 95
      },
      {
        id: 2,
        title: "Advanced React Patterns",
        category: "frontend", 
        difficulty: "advanced",
        tags: ["react", "javascript"],
        popularity: 87
      },
      {
        id: 3,
        title: "Node.js Backend Development",
        category: "backend",
        difficulty: "intermediate", 
        tags: ["nodejs", "javascript"],
        popularity: 92
      }
    ];
  }

  getRecommendations(userPreferences) {
    const { interests = [], skillLevel = "beginner" } = userPreferences;
    
    return this.courses
      .filter(course => course.difficulty === skillLevel)
      .map(course => ({
        ...course,
        matchScore: this.calculateMatchScore(course, interests),
        reason: this.generateRecommendationReason(course, interests)
      }))
      .sort((a, b) => b.matchScore - a.matchScore)
      .slice(0, 5);
  }

  calculateMatchScore(course, interests) {
    let score = 0;
    
    interests.forEach(interest => {
      if (course.tags.includes(interest.toLowerCase())) {
        score += 30;
      }
    });

    score += course.popularity * 0.7;
    return Math.min(100, score);
  }

  generateRecommendationReason(course, interests) {
    const matches = interests.filter(interest => 
      course.tags.includes(interest.toLowerCase())
    );

    if (matches.length > 0) {
      return "Matches your interests in " + matches.join(", ");
    }
    
    return "Popular choice for your skill level";
  }
}

module.exports = new RecommendationService();
