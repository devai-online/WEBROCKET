from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv
from services.groq_service import groq_service
from services.balanced_processor import balanced_processor
from services.humanizer_service import humanizer
from config import config

# Load environment variables
load_dotenv()

# Validate required configuration
try:
    config.validate_required_keys()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please set your GROQ_API_KEY environment variable")

app = FastAPI(title="Blog Generator AI Agent", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class BlogRequest(BaseModel):
    prompt: str
    max_length: Optional[int] = 800
    style: Optional[str] = "informative"
    post_process: Optional[bool] = True
    processing_intensity: Optional[str] = "heavy"

class BlogResponse(BaseModel):
    content: str
    word_count: int
    model_used: str
    plagiarism_score: Optional[float] = None
    post_processing_applied: Optional[bool] = False
    processing_changes: Optional[int] = 0
    success: bool
    error: Optional[str] = None

class HumanizeRequest(BaseModel):
    text: str
    intensity: Optional[str] = "heavy"
    use_groq: Optional[bool] = False

class HumanizeResponse(BaseModel):
    original: str
    humanized: str
    changes_made: list
    success: bool
    word_count_original: int
    word_count_humanized: int
    error: Optional[str] = None

@app.get("/")
async def root():
    return {
        "message": "Blog Generator AI Agent is running!",
        "version": "1.0.0",
        "model": config.GROQ_MODEL,
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "model": config.GROQ_MODEL}

@app.post("/generate-blog", response_model=BlogResponse)
async def generate_blog(request: BlogRequest):
    """Generate a blog post based on the given prompt"""
    
    # Validate prompt
    if not request.prompt or len(request.prompt.strip()) < 5:
        raise HTTPException(
            status_code=400, 
            detail="Prompt must be at least 5 characters long"
        )
    
    # Validate max_length
    if request.max_length and (request.max_length < 100 or request.max_length > 2000):
        raise HTTPException(
            status_code=400,
            detail="max_length must be between 100 and 2000 words"
        )
    
    # Validate processing intensity
    if request.processing_intensity and request.processing_intensity not in ["light", "medium", "heavy", "balanced", "plagiarism_focused", "ai_focused"]:
        raise HTTPException(
            status_code=400,
            detail="processing_intensity must be 'light', 'medium', 'heavy', 'balanced', 'plagiarism_focused', or 'ai_focused'"
        )
    
    try:
        # Generate blog content using Groq service
        result = groq_service.generate_blog_content(
            prompt=request.prompt,
            max_length=request.max_length,
            style=request.style
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Blog generation failed: {result.get('error', 'Unknown error')}"
            )
        
        # Apply balanced processing if requested
        processing_result = None
        if request.post_process:
            processing_result = balanced_processor.process_content(
                result["content"], 
                target_balance=request.processing_intensity or "balanced"
            )
            
            if processing_result["success"]:
                result["content"] = processing_result["processed_content"]
                print(f"✅ Balanced processing applied: {processing_result['total_changes']} changes made")
            else:
                print(f"⚠️ Balanced processing failed: {processing_result.get('error', 'Unknown error')}")
        
        # Return successful response
        return BlogResponse(
            content=result["content"],
            word_count=result["word_count"],
            model_used=result["model_used"],
            post_processing_applied=request.post_process,
            processing_changes=processing_result["total_changes"] if processing_result and processing_result["success"] else 0,
            success=True
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/styles")
async def get_available_styles():
    """Get available writing styles"""
    return {
        "styles": [
            {"name": "informative", "description": "Clear, educational tone with facts and examples"},
            {"name": "casual", "description": "Friendly, conversational tone with simple language"},
            {"name": "professional", "description": "Formal, business-appropriate tone"},
            {"name": "engaging", "description": "Storytelling tone with hooks and compelling narratives"}
        ]
    }

@app.post("/post-process")
async def post_process_content(request: dict):
    """Post-process existing content to reduce plagiarism and AI detection"""
    try:
        content = request.get("content", "")
        intensity = request.get("intensity", "heavy")
        
        if not content:
            raise HTTPException(status_code=400, detail="Content is required")
        
        if intensity not in ["light", "medium", "heavy", "balanced", "plagiarism_focused", "ai_focused"]:
            raise HTTPException(status_code=400, detail="Intensity must be 'light', 'medium', 'heavy', 'balanced', 'plagiarism_focused', or 'ai_focused'")
        
        result = balanced_processor.process_content(content, target_balance=intensity)
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Post-processing failed: {result.get('error', 'Unknown error')}"
            )
        
        return {
            "success": True,
            "original_content": result["original_content"],
            "processed_content": result["processed_content"],
            "changes_made": result["changes_made"],
            "total_changes": result["total_changes"],
            "processing_intensity": result["processing_intensity"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/humanizer", response_class=HTMLResponse)
async def humanizer_ui():
    """Serve the humanizer UI"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Text Humanizer</title>
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
                max-width: 1200px;
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
            
            textarea {
                width: 100%;
                min-height: 200px;
                padding: 15px;
                border: 2px solid #e1e5e9;
                border-radius: 10px;
                font-size: 16px;
                font-family: inherit;
                resize: vertical;
                transition: border-color 0.3s ease;
            }
            
            textarea:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .controls {
                display: flex;
                gap: 15px;
                align-items: center;
                flex-wrap: wrap;
            }
            
            select, input[type="checkbox"] {
                padding: 10px 15px;
                border: 2px solid #e1e5e9;
                border-radius: 8px;
                font-size: 14px;
                background: white;
            }
            
            select:focus {
                outline: none;
                border-color: #667eea;
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
                min-height: 200px;
                white-space: pre-wrap;
                font-family: inherit;
                line-height: 1.6;
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
            
            .changes-list {
                margin-top: 15px;
                padding: 15px;
                background: #e8f4fd;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            
            .changes-list h4 {
                margin-bottom: 10px;
                color: #333;
            }
            
            .changes-list ul {
                list-style: none;
                padding: 0;
            }
            
            .changes-list li {
                padding: 5px 0;
                color: #555;
            }
            
            .changes-list li:before {
                content: "✓ ";
                color: #667eea;
                font-weight: bold;
            }
            
            .error {
                background: #ffe6e6;
                border: 1px solid #ff9999;
                color: #cc0000;
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
                <h1>🤖 AI Text Humanizer</h1>
                <p>Transform AI-generated content into natural, human-like text</p>
            </div>
            
            <div class="content">
                <div class="input-section">
                    <h2 class="section-title">Input Text</h2>
                    <div class="form-group">
                        <label for="inputText">Enter AI-generated text to humanize:</label>
                        <textarea id="inputText" placeholder="Paste your AI-generated text here..."></textarea>
                    </div>
                    
                    <div class="controls">
                        <div class="form-group">
                            <label for="intensity">Humanization Intensity:</label>
                            <select id="intensity">
                                <option value="light">Light</option>
                                <option value="medium">Medium</option>
                                <option value="heavy" selected>Heavy</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <div class="checkbox-group">
                                <input type="checkbox" id="useGroq">
                                <label for="useGroq">Use Groq AI Enhancement</label>
                            </div>
                        </div>
                        
                        <button onclick="humanizeText()" id="humanizeBtn">🚀 Humanize Text</button>
                    </div>
                </div>
                
                <div class="loading" id="loading">
                    <div class="spinner"></div>
                    <p>Processing your text...</p>
                </div>
                
                <div class="output-section">
                    <h2 class="section-title">Humanized Output</h2>
                    <div class="output-box" id="outputText">Your humanized text will appear here...</div>
                    
                    <div class="stats" id="stats" style="display: none;">
                        <div class="stat-item">
                            <div class="stat-value" id="originalWords">0</div>
                            <div class="stat-label">Original Words</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" id="humanizedWords">0</div>
                            <div class="stat-label">Humanized Words</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value" id="wordChange">0</div>
                            <div class="stat-label">Word Change</div>
                        </div>
                    </div>
                    
                    <div class="changes-list" id="changesList" style="display: none;">
                        <h4>Changes Made:</h4>
                        <ul id="changesItems"></ul>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            async function humanizeText() {
                const inputText = document.getElementById('inputText').value.trim();
                const intensity = document.getElementById('intensity').value;
                const useGroq = document.getElementById('useGroq').checked;
                
                if (!inputText) {
                    alert('Please enter some text to humanize.');
                    return;
                }
                
                // Show loading
                document.getElementById('loading').classList.add('show');
                document.getElementById('humanizeBtn').disabled = true;
                
                try {
                    const response = await fetch('/humanize', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            text: inputText,
                            intensity: intensity,
                            use_groq: useGroq
                        })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        // Display humanized text
                        document.getElementById('outputText').textContent = result.humanized;
                        
                        // Show stats
                        document.getElementById('stats').style.display = 'flex';
                        document.getElementById('originalWords').textContent = result.word_count_original;
                        document.getElementById('humanizedWords').textContent = result.word_count_humanized;
                        document.getElementById('wordChange').textContent = result.word_count_humanized - result.word_count_original;
                        
                        // Show changes
                        if (result.changes_made && result.changes_made.length > 0) {
                            document.getElementById('changesList').style.display = 'block';
                            const changesList = document.getElementById('changesItems');
                            changesList.innerHTML = '';
                            result.changes_made.forEach(change => {
                                const li = document.createElement('li');
                                li.textContent = change;
                                changesList.appendChild(li);
                            });
                        } else {
                            document.getElementById('changesList').style.display = 'none';
                        }
                        
                        // Clear any previous errors
                        const errorDiv = document.querySelector('.error');
                        if (errorDiv) errorDiv.remove();
                        
                    } else {
                        throw new Error(result.error || 'Humanization failed');
                    }
                    
                } catch (error) {
                    console.error('Error:', error);
                    
                    // Show error
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'error';
                    errorDiv.textContent = `Error: ${error.message}`;
                    document.getElementById('outputText').parentNode.insertBefore(errorDiv, document.getElementById('outputText'));
                    
                    document.getElementById('outputText').textContent = 'An error occurred while processing your text.';
                } finally {
                    // Hide loading
                    document.getElementById('loading').classList.remove('show');
                    document.getElementById('humanizeBtn').disabled = false;
                }
            }
            
            // Allow Enter key to submit
            document.getElementById('inputText').addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'Enter') {
                    humanizeText();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/humanize", response_model=HumanizeResponse)
async def humanize_text(request: HumanizeRequest):
    """Humanize AI-generated text"""
    
    # Validate text
    if not request.text or len(request.text.strip()) < 5:
        raise HTTPException(
            status_code=400, 
            detail="Text must be at least 5 characters long"
        )
    
    # Validate intensity
    if request.intensity not in ["light", "medium", "heavy"]:
        raise HTTPException(
            status_code=400,
            detail="Intensity must be 'light', 'medium', or 'heavy'"
        )
    
    try:
        # Use the humanizer service
        result = humanizer.humanize_text(
            text=request.text,
            intensity=request.intensity,
            use_groq=request.use_groq or False
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Humanization failed: {result.get('error', 'Unknown error')}"
            )
        
        return HumanizeResponse(
            original=result["original"],
            humanized=result["humanized"],
            changes_made=result["changes_made"],
            success=True,
            word_count_original=result["word_count_original"],
            word_count_humanized=result["word_count_humanized"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/blog-generator", response_class=HTMLResponse)
async def blog_generator_ui():
    """Serve the blog generator UI"""
    html_content = """
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
                    <div class="form-group">
                        <label for="topic">Enter your blog topic:</label>
                        <input type="text" id="topic" placeholder="e.g., The benefits of meditation, How to cook pasta, etc.">
                    </div>
                    
                    <div class="controls">
                        <div class="form-group">
                            <label for="style">Writing Style:</label>
                            <select id="style">
                                <option value="informative">Informative</option>
                                <option value="casual">Casual</option>
                                <option value="professional">Professional</option>
                                <option value="engaging">Engaging</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label for="maxLength">Max Length (words):</label>
                            <select id="maxLength">
                                <option value="400">400 words</option>
                                <option value="600">600 words</option>
                                <option value="800" selected>800 words</option>
                                <option value="1000">1000 words</option>
                                <option value="1200">1200 words</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <div class="checkbox-group">
                                <input type="checkbox" id="postProcess" checked>
                                <label for="postProcess">Apply humanization</label>
                            </div>
                        </div>
                        
                        <button onclick="generateBlog()" id="generateBtn">🚀 Generate Blog</button>
                    </div>
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
            async function generateBlog() {
                const topic = document.getElementById('topic').value.trim();
                const style = document.getElementById('style').value;
                const maxLength = parseInt(document.getElementById('maxLength').value);
                const postProcess = document.getElementById('postProcess').checked;
                
                if (!topic) {
                    alert('Please enter a blog topic.');
                    return;
                }
                
                // Show loading
                document.getElementById('loading').classList.add('show');
                document.getElementById('generateBtn').disabled = true;
                
                try {
                    const response = await fetch('/generate-blog', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            prompt: topic,
                            style: style,
                            max_length: maxLength,
                            post_process: postProcess,
                            processing_intensity: "heavy"
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
            }
            
            // Allow Enter key to submit
            document.getElementById('topic').addEventListener('keydown', function(e) {
                if (e.key === 'Enter') {
                    generateBlog();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 