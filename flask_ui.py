#!/usr/bin/env python3
"""
Flask UI for Blog Generator
A simple web interface for generating blog posts using the FastAPI backend
"""

from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__)

# FastAPI backend URL
BACKEND_URL = "http://localhost:8000"

# HTML template for the blog generator UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .input-section, .output-section {
            margin-bottom: 30px;
        }
        
        .section-title {
            font-size: 1.5em;
            color: #333;
            margin-bottom: 15px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }
        
        input[type="text"], select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            font-size: 16px;
            font-family: inherit;
            transition: border-color 0.3s ease;
        }
        
        input[type="text"]:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .controls {
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .checkbox-group {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .checkbox-group input[type="checkbox"] {
            width: 18px;
            height: 18px;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
            color: #667eea;
        }
        
        .loading.show {
            display: block;
        }
        
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .output-box {
            background: #f8f9fa;
            border: 2px solid #e1e5e9;
            border-radius: 10px;
            padding: 20px;
            min-height: 300px;
            white-space: pre-wrap;
            font-family: inherit;
            line-height: 1.6;
            max-height: 600px;
            overflow-y: auto;
        }
        
        .stats {
            display: flex;
            gap: 20px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        
        .stat-item {
            background: white;
            padding: 10px 15px;
            border-radius: 8px;
            border: 1px solid #e1e5e9;
            text-align: center;
        }
        
        .stat-value {
            font-size: 1.2em;
            font-weight: 600;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }
        
        .error {
            background: #ffe6e6;
            border: 1px solid #ff9999;
            color: #cc0000;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
        
        .success {
            background: #e6ffe6;
            border: 1px solid #99ff99;
            color: #006600;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }
        
        @media (max-width: 768px) {
            .content {
                padding: 20px;
            }
            
            .controls {
                flex-direction: column;
                align-items: stretch;
            }
            
            .stats {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📝 Blog Generator</h1>
            <p>Generate high-quality blog posts on any topic</p>
        </div>
        
        <div class="content">
            <div class="input-section">
                <h2 class="section-title">Blog Topic</h2>
                <form id="blogForm" method="POST">
                    <div class="form-group">
                        <label for="topic">Enter your blog topic:</label>
                        <input type="text" id="topic" name="topic" placeholder="e.g., The benefits of meditation, How to cook pasta, etc." required>
                    </div>
                    
                    <div class="controls">
                        <div class="form-group">
                            <label for="style">Writing Style:</label>
                            <select id="style" name="style">
                                <option value="informative">Informative</option>
                                <option value="casual">Casual</option>
                                <option value="professional">Professional</option>
                                <option value="engaging">Engaging</option>
                                <option value="factual">Factual</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="maxLength">Word Count:</label>
                            <select id="maxLength" name="maxLength">
                                <option value="300">300 words</option>
                                <option value="500">500 words</option>
                                <option value="800" selected>800 words</option>
                                <option value="1000">1000 words</option>
                                <option value="1200">1200 words</option>
                                <option value="1500">1500 words</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <div class="checkbox-group">
                                <input type="checkbox" id="postProcess" name="postProcess">
                                <label for="postProcess">Apply humanization</label>
                            </div>
                        </div>
                        
                        <button type="submit" id="generateBtn">🚀 Generate Blog</button>
                    </div>
                </form>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Generating your blog post...</p>
            </div>
            
            <div class="output-section">
                <h2 class="section-title">Generated Blog</h2>
                <div class="output-box" id="outputText">Your generated blog will appear here...</div>
                
                <div class="stats" id="stats" style="display: none;">
                    <div class="stat-item">
                        <div class="stat-value" id="wordCount">0</div>
                        <div class="stat-label">Words</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="modelUsed">-</div>
                        <div class="stat-label">Model Used</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="processingChanges">0</div>
                        <div class="stat-label">Processing Changes</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        document.getElementById('blogForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const topic = formData.get('topic').trim();
            const style = formData.get('style');
            const maxLength = parseInt(formData.get('maxLength'));
            const postProcess = formData.get('postProcess') === 'on';
            
            if (!topic) {
                alert('Please enter a blog topic.');
                return;
            }
            
            // Show loading
            document.getElementById('loading').classList.add('show');
            document.getElementById('generateBtn').disabled = true;
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        topic: topic,
                        style: style,
                        maxLength: maxLength,
                        postProcess: postProcess
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    // Display generated blog
                    document.getElementById('outputText').textContent = result.content;
                    
                    // Show stats
                    document.getElementById('stats').style.display = 'flex';
                    document.getElementById('wordCount').textContent = result.word_count;
                    document.getElementById('modelUsed').textContent = result.model_used;
                    document.getElementById('processingChanges').textContent = result.processing_changes || 0;
                    
                    // Clear any previous errors
                    const errorDiv = document.querySelector('.error');
                    if (errorDiv) errorDiv.remove();
                    
                } else {
                    throw new Error(result.error || 'Blog generation failed');
                }
                
            } catch (error) {
                console.error('Error:', error);
                
                // Show error
                const errorDiv = document.createElement('div');
                errorDiv.className = 'error';
                errorDiv.textContent = `Error: ${error.message}`;
                document.getElementById('outputText').parentNode.insertBefore(errorDiv, document.getElementById('outputText'));
                
                document.getElementById('outputText').textContent = 'An error occurred while generating your blog.';
            } finally {
                // Hide loading
                document.getElementById('loading').classList.remove('show');
                document.getElementById('generateBtn').disabled = false;
            }
        });
        
        // Allow Enter key to submit
        document.getElementById('topic').addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                document.getElementById('blogForm').dispatchEvent(new Event('submit'));
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page with the blog generator UI"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/generate', methods=['POST'])
def generate_blog():
    """Generate blog by calling the FastAPI backend"""
    try:
        data = request.get_json()
        
        # Prepare request for FastAPI backend
        backend_request = {
            "prompt": data.get('topic'),
            "style": data.get('style', 'informative'),
            "max_length": data.get('maxLength', 800),
            "post_process": data.get('postProcess', True),
            "processing_intensity": "heavy"
        }
        
        # Call FastAPI backend
        response = requests.post(
            f"{BACKEND_URL}/generate-blog",
            json=backend_request,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'success': True,
                'content': result.get('content', ''),
                'word_count': result.get('word_count', 0),
                'model_used': result.get('model_used', ''),
                'processing_changes': result.get('processing_changes', 0)
            })
        else:
            error_data = response.json() if response.content else {}
            return jsonify({
                'success': False,
                'error': error_data.get('detail', f'Backend error: {response.status_code}')
            }), 400
            
    except requests.exceptions.ConnectionError:
        return jsonify({
            'success': False,
            'error': 'Cannot connect to backend server. Make sure the FastAPI server is running on port 8000.'
        }), 500
    except requests.exceptions.Timeout:
        return jsonify({
            'success': False,
            'error': 'Request timed out. The blog generation is taking too long.'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'healthy', 'backend': 'connected'})
        else:
            return jsonify({'status': 'unhealthy', 'backend': 'error'}), 500
    except:
        return jsonify({'status': 'unhealthy', 'backend': 'disconnected'}), 500

if __name__ == '__main__':
    print("🚀 Starting Flask Blog Generator UI...")
    print(f"📡 Backend URL: {BACKEND_URL}")
    print("🌐 UI will be available at: http://localhost:5000")
    print("⚠️  Make sure your FastAPI backend is running on port 8000")
    app.run(debug=True, host='0.0.0.0', port=5000) 