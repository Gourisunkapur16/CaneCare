from flask import Flask, render_template_string, request
import os
import webbrowser
import threading
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload directory
os.makedirs('uploads', exist_ok=True)

def open_browser():
    """Open the browser automatically after a short delay"""
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open_new('http://localhost:5000')

# Sugarcane Analysis HTML templates
HOME_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>CaneSight AI - Sugarcane Crop Analysis</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
            min-height: 100vh; 
            color: #333;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            margin-bottom: 50px;
            color: white;
        }
        header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .modes-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-top: 30px;
        }
        .mode-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            cursor: pointer;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-decoration: none;
            color: inherit;
            display: block;
        }
        .mode-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        .mode-card h3 {
            margin-bottom: 15px;
            color: #2e7d32;
        }
        .mode-card p {
            color: #666;
            margin-bottom: 10px;
        }
        .btn {
            background: #2e7d32;
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
        }
        .btn:hover {
            background: #1b5e20;
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🌾 CaneSight AI</h1>
            <p>AI-Powered Sugarcane Crop Analysis & Disease Detection</p>
        </header>
        
        <div class="modes-grid">
            <a href="/analyze?mode=disease" class="mode-card">
                <div class="feature-icon">🦠</div>
                <h3>Disease Detection</h3>
                <p>Identify common sugarcane diseases</p>
                <small>Red rot, Smut, Mosaic Virus</small>
            </a>
            
            <a href="/analyze?mode=health" class="mode-card">
                <div class="feature-icon">💚</div>
                <h3>Crop Health Score</h3>
                <p>Analyze overall plant health</p>
                <small>Nutrient deficiency, Stress levels</small>
            </a>
            
            <a href="/analyze?mode=pest" class="mode-card">
                <div class="feature-icon">🐛</div>
                <h3>Pest Identification</h3>
                <p>Detect common sugarcane pests</p>
                <small>Borers, Aphids, Whiteflies</small>
            </a>
            
            <a href="/analyze?mode=yield" class="mode-card">
                <div class="feature-icon">📈</div>
                <h3>Yield Prediction</h3>
                <p>Estimate sugarcane yield potential</p>
                <small>Based on crop conditions</small>
            </a>
            
            <a href="/analyze?mode=nutrient" class="mode-card">
                <div class="feature-icon">🧪</div>
                <h3>Nutrient Analysis</h3>
                <p>Detect nutrient deficiencies</p>
                <small>Nitrogen, Phosphorus, Potassium</small>
            </a>
            
            <a href="/analyze?mode=growth" class="mode-card">
                <div class="feature-icon">📏</div>
                <h3>Growth Stage</h3>
                <p>Determine crop growth stage</p>
                <small>Germination, Tillering, Maturity</small>
            </a>
        </div>
        
        <div style="text-align: center; margin-top: 40px; color: white;">
            <p><strong>Status:</strong> ✅ Sugarcane Analysis System Active</p>
            <p>Upload images of sugarcane crops for AI analysis</p>
        </div>
    </div>
</body>
</html>
'''

ANALYZE_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Analyze - CaneSight AI</title>
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%);
            min-height: 100vh;
            margin: 0;
            padding: 20px;
            color: white;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 { text-align: center; margin-bottom: 20px; }
        .mode-info {
            background: rgba(255,255,255,0.2);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .upload-area {
            border: 3px dashed #fff;
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .upload-area:hover {
            background: rgba(255,255,255,0.1);
        }
        .btn {
            background: #fff;
            color: #2e7d32;
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            margin: 10px;
        }
        .back-btn {
            background: transparent;
            color: white;
            border: 2px solid white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📷 Analyze Sugarcane - {{ mode.upper() }}</h1>
        
        <div class="mode-info">
            <h3>Analysis Type: {{ mode_display }}</h3>
            <p>{{ mode_description }}</p>
        </div>
        
        <form method="POST" enctype="multipart/form-data">
            <input type="hidden" name="mode" value="{{ mode }}">
            
            <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                <h3>📁 Upload Sugarcane Image</h3>
                <p>Take a clear photo of sugarcane leaves/stems</p>
                <p><small>Supported formats: JPG, PNG, GIF, BMP</small></p>
                <input type="file" name="image" id="fileInput" accept="image/*" required style="display: none;">
            </div>
            
            <div style="text-align: center;">
                <button type="submit" class="btn">🔍 Analyze Crop</button>
                <a href="/" class="btn back-btn">← Back to Home</a>
            </div>
        </form>
    </div>
</body>
</html>
'''

# Mode descriptions for sugarcane analysis
MODE_INFO = {
    'disease': {
        'display': 'Disease Detection',
        'description': 'Identify common sugarcane diseases like Red Rot, Smut, Mosaic Virus, and Rust.'
    },
    'health': {
        'display': 'Crop Health Score', 
        'description': 'Analyze overall plant health and detect stress factors.'
    },
    'pest': {
        'display': 'Pest Identification',
        'description': 'Detect common sugarcane pests and insect damage.'
    },
    'yield': {
        'display': 'Yield Prediction',
        'description': 'Estimate potential yield based on crop conditions.'
    },
    'nutrient': {
        'display': 'Nutrient Analysis',
        'description': 'Detect nutrient deficiencies (N, P, K) from leaf coloration.'
    },
    'growth': {
        'display': 'Growth Stage',
        'description': 'Determine current growth stage of the sugarcane crop.'
    }
}

@app.route('/')
def home():
    return render_template_string(HOME_HTML)

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    mode = request.args.get('mode', 'disease')
    mode_data = MODE_INFO.get(mode, MODE_INFO['disease'])
    
    if request.method == 'POST':
        # Handle sugarcane image analysis
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                # Save file
                filename = f"sugarcane_{mode}_{len(os.listdir('uploads'))}.jpg"
                filepath = os.path.join('uploads', filename)
                file.save(filepath)
                
                # Mock analysis results (will be replaced with real AI)
                analysis_results = {
                    'disease': 'No major diseases detected. Minor leaf spot observed.',
                    'health': 'Crop Health: 85% - Good overall condition',
                    'pest': 'No significant pest damage detected',
                    'yield': 'Estimated yield: 75-85 tons/hectare',
                    'nutrient': 'Adequate NPK levels detected',
                    'growth': 'Growth Stage: Tillering phase'
                }
                
                return f'''
                <div style="padding: 40px; text-align: center; background: white; margin: 20px; border-radius: 15px; color: #333;">
                    <h2 style="color: #2e7d32;">✅ Sugarcane Analysis Complete!</h2>
                    <div style="background: #f5f5f5; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h3>🌾 Analysis Results</h3>
                        <p><strong>Mode:</strong> {mode_data['display']}</p>
                        <p><strong>Findings:</strong> {analysis_results[mode]}</p>
                        <p><strong>Image:</strong> {filename}</p>
                    </div>
                    <p>Next: Advanced AI analysis will be implemented here</p>
                    <a href="/analyze?mode={mode}" class="btn" style="display: inline-block; margin: 20px;">Analyze Another</a>
                    <a href="/" class="btn" style="display: inline-block; margin: 20px;">Home</a>
                </div>
                '''
    
    return render_template_string(ANALYZE_HTML, mode=mode, 
                                mode_display=mode_data['display'],
                                mode_description=mode_data['description'])

if __name__ == '__main__':
    print("🚀 Starting CaneSight AI - Sugarcane Analysis System...")
    print("📍 Opening browser automatically...")
    print("🌾 Focus: Sugarcane crop disease detection & analysis")
    
    # Start browser in a separate thread
    threading.Thread(target=open_browser).start()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)