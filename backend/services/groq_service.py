import os
from groq import Groq
from typing import Optional
import sys
from pathlib import Path

# Import config - handle relative imports properly
try:
    from config import config
except ImportError:
    # If running from different directory, try parent directory
    sys.path.append(str(Path(__file__).parent.parent))
    from config import config

class GroqService:
    """Service for generating blog content using Groq API"""
    
    def __init__(self):
        """Initialize the Groq client"""
        if not config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is required")
        
        self.client = Groq(api_key=config.GROQ_API_KEY)
        self.model = config.GROQ_MODEL
    
    def generate_blog_content(
        self, 
        prompt: str, 
        max_length: Optional[int] = None,
        style: Optional[str] = "informative"
    ) -> dict:
        """
        Generate blog content based on the given prompt
        
        Args:
            prompt: The topic or brief description for the blog
            max_length: Maximum length of the blog content
            style: Writing style (informative, casual, professional, etc.)
            
        Returns:
            dict: Contains generated content and metadata
        """
        try:
            # Set default max_length if not provided
            if max_length is None:
                max_length = config.DEFAULT_MAX_LENGTH
            
            # Create a comprehensive system prompt for blog generation
            system_prompt = self._create_system_prompt(style, max_length)
            
            # Create the user prompt
            user_prompt = self._create_user_prompt(prompt, max_length)
            
            # Generate content using Groq with higher randomness for human-like output
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.9,  # Higher temperature for more creative, human-like output
                max_tokens=max_length * 2,  # Allow more tokens for better generation
                top_p=0.95,  # Higher top_p for more variation
                frequency_penalty=0.1,  # Slight penalty to avoid repetition
                presence_penalty=0.1,  # Encourage diverse vocabulary
                stream=False
            )
            
            # Extract the generated content
            content = response.choices[0].message.content.strip()
            
            # Apply comprehensive humanization
            try:
                from .humanizer_service import humanizer
                humanization_result = humanizer.humanize_text(
                    content, 
                    intensity="heavy", 
                    use_groq=True if config.GROQ_API_KEY else False
                )
                
                if humanization_result['success']:
                    content = humanization_result['humanized']
                    print(f"✅ Humanization applied: {len(humanization_result['changes_made'])} changes made")
                else:
                    print(f"⚠️ Humanization failed: {humanization_result.get('error', 'Unknown error')}")
                    # Fall back to simple humanization
                    content = self._humanize_content(content)
                    
            except Exception as e:
                print(f"⚠️ Advanced humanization failed: {e}")
                # Fall back to simple humanization
                content = self._humanize_content(content)
            
            # Calculate word count
            word_count = len(content.split())
            
            return {
                "content": content,
                "word_count": word_count,
                "model_used": self.model,
                "success": True
            }
            
        except Exception as e:
            return {
                "content": "",
                "word_count": 0,
                "model_used": self.model,
                "success": False,
                "error": str(e)
            }
    
    def _create_system_prompt(self, style: str, max_length: int) -> str:
        """Create a comprehensive system prompt for blog generation"""
        
        style_instructions = {
            "informative": "Write in a clear, educational tone. Use facts and examples to support your points.",
            "casual": "Write in a friendly, conversational tone. Use simple language and relatable examples.",
            "professional": "Write in a formal, business-appropriate tone. Use industry terminology when appropriate.",
            "engaging": "Write in an engaging, storytelling tone. Use hooks and compelling narratives."
        }
        
        style_instruction = style_instructions.get(style, style_instructions["informative"])
        
        return f"""You are a human blogger with years of experience writing authentic, personal content. Write naturally as if you're sharing your thoughts with a friend.

CRITICAL HUMAN-LIKE WRITING REQUIREMENTS:
1. Write in a {style} style: {style_instruction}
2. Target approximately {max_length} words
3. Use NATURAL human language patterns:
   - Mix short and long sentences randomly
   - Use contractions (I'll, don't, can't, it's, you're)
   - Include personal opinions and phrases like "I think", "In my experience", "I've noticed"
   - Add occasional filler words or phrases naturally
   - Use incomplete thoughts sometimes, then complete them
4. VARY your writing style:
   - Some paragraphs should be longer, others shorter
   - Use different sentence starters
   - Mix formal and informal language naturally
5. Include HUMAN imperfections:
   - Slight repetition of ideas (but rephrase them)
   - Personal anecdotes or examples
   - Emotional language and personal reactions
   - Questions that you then answer yourself
6. Add SPECIFIC details and examples that show personal knowledge
7. Use transitional phrases that humans use: "Speaking of which", "That reminds me", "On a related note"
8. End with a personal reflection or call to action

AVOID AI-LIKE PATTERNS:
- Don't use numbered lists excessively
- Don't be overly structured or formal
- Don't use too many perfect transitions
- Don't sound like a textbook or manual

Write as if you're genuinely passionate about this topic and sharing your personal insights."""
    
    def _create_user_prompt(self, prompt: str, max_length: int) -> str:
        """Create the user prompt for blog generation"""
        
        return f"""Hey, I want you to write a blog post about: {prompt}

Write this like you're a real person who's genuinely interested in this topic. Make it about {max_length} words, but don't worry if it's a bit more or less - that's natural!

Write it like you're talking to a friend who asked you about this topic. Share your thoughts, maybe throw in some personal opinions or experiences. Don't make it sound like a Wikipedia article or a formal essay. 

You know what I mean? Just write naturally, like how you'd actually explain this to someone in real life. Include some "I think" or "In my opinion" statements, use contractions, and don't be afraid to sound a bit conversational.

Topic: {prompt}

Write away!"""
    
    def _humanize_content(self, content: str) -> str:
        """Post-process content to make it more human-like and less AI-detectable"""
        import re
        import random
        
        # Add some human-like imperfections and variations
        humanizations = [
            # Add contractions
            (r"\bis not\b", "isn't"),
            (r"\bdo not\b", "don't"),
            (r"\bcan not\b", "can't"),
            (r"\bwill not\b", "won't"),
            (r"\bshould not\b", "shouldn't"),
            (r"\bwould not\b", "wouldn't"),
            (r"\byou are\b", "you're"),
            (r"\bwe are\b", "we're"),
            (r"\bthey are\b", "they're"),
            (r"\bit is\b", "it's"),
            (r"\bthat is\b", "that's"),
            (r"\bI will\b", "I'll"),
            (r"\bI would\b", "I'd"),
            (r"\bI have\b", "I've"),
            
            # Add some human-like transition phrases randomly
            (r"\bMoreover,\b", random.choice(["Plus,", "Also,", "On top of that,", "What's more,"])),
            (r"\bFurthermore,\b", random.choice(["Besides,", "Also,", "And another thing,", "Not to mention,"])),
            (r"\bHowever,\b", random.choice(["But,", "Though,", "That said,", "On the flip side,"])),
            (r"\bIn conclusion,\b", random.choice(["So,", "All in all,", "At the end of the day,", "To wrap things up,"])),
            (r"\bAdditionally,\b", random.choice(["Plus,", "Also,", "And,", "What's more,"])),
        ]
        
        # Apply random humanizations
        for pattern, replacement in humanizations:
            if random.random() < 0.4:  # 40% chance to apply each humanization
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        # Add some personal touches randomly
        personal_phrases = [
            "I think",
            "In my experience",
            "I've noticed",
            "From what I've seen",
            "I believe",
            "It seems to me",
            "I find that",
            "I've found that"
        ]
        
        # Sometimes add a personal phrase at the beginning of paragraphs
        paragraphs = content.split('\n\n')
        for i, paragraph in enumerate(paragraphs):
            if random.random() < 0.2 and not paragraph.startswith('#'):  # 20% chance, not for headings
                personal_phrase = random.choice(personal_phrases)
                # Add to beginning of paragraph if it doesn't already have one
                if not any(phrase in paragraph[:50] for phrase in personal_phrases):
                    paragraphs[i] = f"{personal_phrase}, {paragraph.lower()}"
        
        content = '\n\n'.join(paragraphs)
        
        # Add some variety to sentence starters
        sentence_starters = [
            "Now, ",
            "Well, ",
            "So, ",
            "Actually, ",
            "Honestly, ",
            "Look, ",
            "Here's the thing: ",
            "You know what? "
        ]
        
        # Sometimes add casual starters to sentences
        sentences = content.split('. ')
        for i, sentence in enumerate(sentences):
            if random.random() < 0.1 and i > 0:  # 10% chance, not for first sentence
                starter = random.choice(sentence_starters)
                sentences[i] = f"{starter}{sentence}"
        
        content = '. '.join(sentences)
        
        return content

# Create a global instance of the service
groq_service = GroqService() 