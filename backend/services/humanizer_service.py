#!/usr/bin/env python3
"""
HybridHumanizer Service - Advanced AI Text Humanization

This service transforms AI-generated content to appear more human-written,
helping bypass AI detection tools through multiple sophisticated techniques.
"""

import re
import random
import string
import json
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path

# Try to import optional libraries
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import nltk
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False

class HybridHumanizer:
    """
    Advanced AI text humanizer that combines multiple techniques to create
    human-like content that bypasses AI detection systems.
    """
    
    def __init__(self, groq_api_key: Optional[str] = None):
        """
        Initialize the humanizer with all necessary patterns and data.
        
        Args:
            groq_api_key: Optional Groq API key for enhanced humanization
        """
        self.groq_api_key = groq_api_key
        self.groq_api_url = "https://api.groq.com/openai/v1/chat/completions"
        
        # Initialize NLTK if available
        if HAS_NLTK:
            try:
                nltk.download('punkt', quiet=True)
                nltk.download('wordnet', quiet=True)
            except:
                pass
        
        # Load all patterns and data
        self._load_ai_phrases()
        self._load_human_replacements()
        self._load_contractions()
        self._load_vocabulary_replacements()
        self._load_statistical_patterns()
        self._load_ai_detection_markers()
        self._load_human_templates()
        
        print("🤖 HybridHumanizer initialized successfully!")
    
    def _load_ai_phrases(self):
        """Load common AI phrases that need to be replaced"""
        self.ai_phrases = [
            "It's important to note that",
            "It's worth mentioning",
            "Furthermore",
            "Moreover",
            "Additionally",
            "In conclusion",
            "To summarize",
            "Overall",
            "Ultimately",
            "It's crucial to understand",
            "significantly",
            "substantially",
            "considerably",
            "tremendously",
            "It should be noted that",
            "It is essential to",
            "It is imperative to",
            "One must consider",
            "It is recommended that",
            "It is advisable to",
            "In order to",
            "For the purpose of",
            "With regard to",
            "In relation to",
            "As a result of",
            "Due to the fact that",
            "In the event that",
            "Prior to",
            "Subsequent to",
            "In accordance with"
        ]
    
    def _load_human_replacements(self):
        """Load human-like replacements for AI phrases"""
        self.human_replacements = {
            "It's important to note that": ["Here's the thing:", "What I've noticed is", "Something interesting is", "You should know that"],
            "It's worth mentioning": ["Oh, and", "By the way", "Also worth noting", "Something else"],
            "Furthermore": ["Also", "Plus", "And", "What's more", "On top of that"],
            "Moreover": ["Also", "Plus", "And another thing", "What's more", "Besides that"],
            "Additionally": ["Also", "Plus", "And", "What's more", "On top of that"],
            "In conclusion": ["So", "Bottom line", "What it comes down to", "All in all", "To wrap up"],
            "To summarize": ["So basically", "In short", "Here's what it boils down to", "Long story short"],
            "Overall": ["All in all", "When you step back", "Looking at the big picture", "Generally speaking"],
            "Ultimately": ["At the end of the day", "When push comes to shove", "What really matters", "In the end"],
            "significantly": ["a lot", "quite a bit", "really", "pretty much", "big time"],
            "substantially": ["a lot", "quite a bit", "really", "big time", "majorly"],
            "considerably": ["quite a bit", "a lot", "pretty much", "really", "significantly"],
            "tremendously": ["a ton", "massively", "big time", "like crazy", "hugely"],
            "It should be noted that": ["You should know", "Here's something", "One thing is", "Keep in mind"],
            "It is essential to": ["You really need to", "It's super important to", "You've got to", "Make sure you"],
            "It is imperative to": ["You absolutely must", "It's crucial to", "You need to", "Make sure you"],
            "One must consider": ["You should think about", "Consider this", "Think about", "Keep in mind"],
            "It is recommended that": ["I'd suggest", "You should probably", "It's best to", "I recommend"],
            "It is advisable to": ["You should probably", "It's smart to", "I'd recommend", "You might want to"],
            "In order to": ["To", "So you can", "If you want to"],
            "For the purpose of": ["To", "So you can", "In order to"],
            "With regard to": ["About", "When it comes to", "As for"],
            "In relation to": ["About", "Regarding", "When it comes to"],
            "As a result of": ["Because of", "Due to", "Thanks to"],
            "Due to the fact that": ["Because", "Since", "Given that"],
            "In the event that": ["If", "Should", "In case"],
            "Prior to": ["Before", "Ahead of"],
            "Subsequent to": ["After", "Following"],
            "In accordance with": ["Following", "According to", "Based on"]
        }
    
    def _load_contractions(self):
        """Load formal phrases and their casual contractions"""
        self.contractions = {
            "do not": "don't",
            "does not": "doesn't",
            "did not": "didn't",
            "will not": "won't",
            "would not": "wouldn't",
            "should not": "shouldn't",
            "could not": "couldn't",
            "cannot": "can't",
            "is not": "isn't",
            "are not": "aren't",
            "was not": "wasn't",
            "were not": "weren't",
            "have not": "haven't",
            "has not": "hasn't",
            "had not": "hadn't",
            "I am": "I'm",
            "you are": "you're",
            "he is": "he's",
            "she is": "she's",
            "it is": "it's",
            "we are": "we're",
            "they are": "they're",
            "I have": "I've",
            "you have": "you've",
            "we have": "we've",
            "they have": "they've",
            "I will": "I'll",
            "you will": "you'll",
            "he will": "he'll",
            "she will": "she'll",
            "it will": "it'll",
            "we will": "we'll",
            "they will": "they'll",
            "I would": "I'd",
            "you would": "you'd",
            "he would": "he'd",
            "she would": "she'd",
            "we would": "we'd",
            "they would": "they'd",
            "let us": "let's",
            "that is": "that's",
            "there is": "there's",
            "here is": "here's",
            "what is": "what's",
            "where is": "where's",
            "when is": "when's",
            "who is": "who's",
            "why is": "why's",
            "how is": "how's"
        }
    
    def _load_vocabulary_replacements(self):
        """Load complex words and their simple alternatives"""
        self.vocabulary_replacements = {
            "utilize": "use",
            "implement": "do",
            "facilitate": "help",
            "optimize": "improve",
            "enhance": "make better",
            "demonstrate": "show",
            "subsequent": "next",
            "commence": "start",
            "accomplish": "do",
            "beneficial": "helpful",
            "challenging": "hard",
            "comprehensive": "complete",
            "innovative": "new",
            "effective": "good",
            "efficient": "quick",
            "significant": "big",
            "substantial": "large",
            "considerable": "large",
            "tremendous": "huge",
            "numerous": "many",
            "particular": "specific",
            "individual": "single",
            "appropriate": "right",
            "sufficient": "enough",
            "adequate": "enough",
            "maximum": "most",
            "minimum": "least",
            "optimal": "best",
            "primary": "main",
            "secondary": "second",
            "fundamental": "basic",
            "essential": "key",
            "crucial": "key",
            "vital": "key",
            "critical": "key",
            "important": "key",
            "relevant": "related",
            "applicable": "useful",
            "appropriate": "right",
            "suitable": "good",
            "adequate": "good enough",
            "satisfactory": "good enough",
            "exceptional": "amazing",
            "outstanding": "great",
            "remarkable": "great",
            "extraordinary": "amazing",
            "magnificent": "great",
            "excellent": "great",
            "superior": "better",
            "inferior": "worse",
            "alternative": "other",
            "option": "choice",
            "selection": "choice",
            "variety": "mix",
            "diversity": "mix",
            "modification": "change",
            "adjustment": "change",
            "improvement": "upgrade",
            "development": "growth",
            "advancement": "progress",
            "achievement": "success",
            "accomplishment": "success",
            "requirement": "need",
            "necessity": "need",
            "obligation": "duty",
            "responsibility": "job",
            "opportunity": "chance",
            "possibility": "chance",
            "probability": "chance",
            "likelihood": "chance",
            "potential": "possible",
            "capability": "ability",
            "capacity": "ability",
            "competence": "skill",
            "proficiency": "skill",
            "expertise": "skill",
            "knowledge": "know-how",
            "information": "info",
            "communication": "talk",
            "conversation": "chat",
            "discussion": "talk",
            "explanation": "reason",
            "description": "details",
            "definition": "meaning",
            "interpretation": "take",
            "understanding": "grasp",
            "comprehension": "grasp",
            "perception": "view",
            "perspective": "view",
            "opinion": "view",
            "viewpoint": "view",
            "standpoint": "view",
            "approach": "way",
            "method": "way",
            "technique": "way",
            "procedure": "steps",
            "process": "steps",
            "system": "way",
            "mechanism": "way",
            "strategy": "plan",
            "solution": "answer",
            "resolution": "fix",
            "conclusion": "end",
            "result": "outcome",
            "consequence": "result",
            "outcome": "result",
            "effect": "result",
            "impact": "effect",
            "influence": "effect",
            "significance": "importance",
            "importance": "value",
            "value": "worth",
            "benefit": "plus",
            "advantage": "plus",
            "disadvantage": "minus",
            "drawback": "downside",
            "limitation": "limit",
            "restriction": "limit",
            "constraint": "limit",
            "obstacle": "block",
            "barrier": "block",
            "challenge": "problem",
            "difficulty": "problem",
            "issue": "problem",
            "concern": "worry",
            "problem": "issue",
            "situation": "case",
            "circumstance": "case",
            "condition": "state",
            "status": "state",
            "position": "spot",
            "location": "place",
            "destination": "place",
            "objective": "goal",
            "purpose": "goal",
            "intention": "plan",
            "goal": "aim",
            "target": "goal",
            "focus": "center",
            "emphasis": "focus",
            "priority": "top pick",
            "preference": "pick",
            "choice": "pick",
            "decision": "choice",
            "determination": "choice",
            "conclusion": "end",
            "judgment": "call",
            "assessment": "check",
            "evaluation": "review",
            "analysis": "breakdown",
            "examination": "look",
            "investigation": "dig",
            "research": "study",
            "study": "look at",
            "observation": "look",
            "inspection": "check",
            "review": "look over",
            "survey": "poll",
            "measurement": "measure",
            "calculation": "math",
            "estimation": "guess",
            "approximation": "rough guess",
            "prediction": "guess",
            "forecast": "prediction",
            "projection": "guess",
            "expectation": "hope",
            "anticipation": "wait",
            "assumption": "guess",
            "hypothesis": "theory",
            "theory": "idea",
            "concept": "idea",
            "notion": "idea",
            "thought": "idea",
            "belief": "view",
            "conviction": "belief",
            "confidence": "trust",
            "certainty": "sure thing",
            "uncertainty": "doubt",
            "doubt": "question",
            "question": "ask",
            "inquiry": "question",
            "request": "ask",
            "demand": "want",
            "requirement": "need",
            "specification": "details",
            "instruction": "direction",
            "direction": "way",
            "guidance": "help",
            "assistance": "help",
            "support": "help",
            "aid": "help",
            "contribution": "help",
            "participation": "join in",
            "involvement": "part",
            "engagement": "part",
            "commitment": "promise",
            "dedication": "commitment",
            "devotion": "loyalty",
            "loyalty": "support",
            "faithfulness": "loyalty",
            "reliability": "dependable",
            "dependability": "reliable",
            "trustworthiness": "trustworthy",
            "credibility": "believable",
            "authenticity": "real",
            "genuineness": "real",
            "sincerity": "honest",
            "honesty": "truth",
            "truthfulness": "honesty",
            "integrity": "honesty",
            "morality": "right and wrong",
            "ethics": "right and wrong",
            "principle": "rule",
            "standard": "level",
            "criterion": "rule",
            "guideline": "rule",
            "regulation": "rule",
            "policy": "rule",
            "procedure": "steps",
            "protocol": "rules",
            "framework": "structure",
            "structure": "setup",
            "organization": "setup",
            "arrangement": "setup",
            "configuration": "setup",
            "format": "layout",
            "design": "plan",
            "pattern": "design",
            "model": "example",
            "template": "example",
            "example": "sample",
            "instance": "case",
            "illustration": "example",
            "demonstration": "show",
            "presentation": "show",
            "display": "show",
            "exhibition": "show",
            "performance": "show",
            "achievement": "success",
            "success": "win",
            "victory": "win",
            "triumph": "win",
            "accomplishment": "success",
            "attainment": "reach",
            "acquisition": "get",
            "obtainment": "get",
            "procurement": "get",
            "purchase": "buy",
            "transaction": "deal",
            "exchange": "trade",
            "transfer": "move",
            "movement": "move",
            "motion": "move",
            "action": "move",
            "activity": "action",
            "operation": "work",
            "function": "work",
            "performance": "work",
            "execution": "do",
            "implementation": "do",
            "application": "use",
            "usage": "use",
            "employment": "use",
            "utilization": "use"
        }
    
    def _load_statistical_patterns(self):
        """Load statistical patterns from human writing analysis"""
        self.statistical_patterns = {
            'sentence_lengths': {
                'short': (5, 12),
                'medium': (13, 25),
                'long': (26, 40),
                'distribution': {'short': 0.3, 'medium': 0.5, 'long': 0.2}
            },
            'paragraph_sizes': {
                'sentences_per_paragraph': [2, 3, 4, 5, 3, 4, 2, 6, 3, 4, 5, 2],
                'words_per_paragraph': (50, 200)
            },
            'punctuation_patterns': {
                'comma_frequency': 0.15,  # Commas per word
                'period_variations': ['.', '!', '?'],
                'exclamation_frequency': 0.05,
                'question_frequency': 0.1
            },
            'word_patterns': {
                'avg_word_length': 4.5,
                'syllable_distribution': {'1': 0.6, '2': 0.25, '3+': 0.15},
                'common_starters': ['The', 'I', 'You', 'It', 'This', 'That', 'We', 'They', 'But', 'And', 'So', 'Now', 'Well', 'Actually', 'Honestly']
            }
        }
    
    def _load_ai_detection_markers(self):
        """Load patterns that AI detectors commonly look for"""
        self.ai_detection_markers = {
            'repetitive_patterns': [
                r'(\w+)\s+\1\s+\1',  # Word repeated 3+ times
                r'(In\s+(?:conclusion|summary|short))',  # Formal conclusions
                r'(Furthermore|Moreover|Additionally|However),\s+',  # Formal transitions
                r'(It\s+is\s+important\s+to\s+note\s+that)',  # Formal observations
                r'(First(?:ly)?|Second(?:ly)?|Third(?:ly)?|Finally),\s+',  # Numbered lists
            ],
            'formal_structures': [
                r'(The\s+(?:purpose|goal|objective)\s+of\s+this)',
                r'(In\s+order\s+to\s+understand)',
                r'(It\s+should\s+be\s+noted\s+that)',
                r'(As\s+(?:mentioned|stated|discussed)\s+(?:earlier|above|previously))',
                r'(In\s+the\s+context\s+of)',
            ],
            'ai_vocabulary': [
                'utilize', 'implement', 'facilitate', 'optimize', 'enhance',
                'demonstrate', 'subsequent', 'commence', 'accomplish',
                'substantially', 'significantly', 'considerably', 'tremendously'
            ],
            'sentence_patterns': [
                r'^(The\s+\w+\s+is\s+)',  # "The X is" starts
                r'^(This\s+\w+\s+(?:provides|offers|presents|demonstrates))',  # "This X provides" starts
                r'^(In\s+(?:addition|contrast|comparison|summary))',  # Formal sentence starters
                r'(can\s+be\s+(?:utilized|implemented|optimized|enhanced))',  # Passive constructions
            ]
        }
    
    def _load_human_templates(self):
        """Load human-like templates for different content types"""
        self.human_templates = {
            'introductions': [
                "So I was thinking about {topic}...",
                "You know what's interesting about {topic}?",
                "I've been wondering about {topic} lately...",
                "Let me tell you about {topic}...",
                "Here's something cool about {topic}...",
                "I came across something about {topic} that blew my mind...",
                "Ever wonder about {topic}? Well...",
                "I'm kind of obsessed with {topic} right now...",
                "So {topic} is something I've been diving into...",
                "Okay, so {topic} is actually pretty fascinating..."
            ],
            'transitions': [
                "But here's the thing...",
                "What's crazy is...",
                "And get this...",
                "Now here's where it gets interesting...",
                "Plot twist...",
                "But wait, there's more...",
                "Here's what I found out...",
                "So check this out...",
                "This is where things get wild...",
                "And that's not even the best part..."
            ],
            'conclusions': [
                "So yeah, that's my take on it.",
                "Pretty wild stuff, right?",
                "What do you think about all this?",
                "I'm curious to hear your thoughts.",
                "Anyway, that's what I've been thinking about.",
                "Hope that gives you something to chew on.",
                "Let me know if you've had similar experiences.",
                "I'd love to hear what you think.",
                "That's my two cents, anyway.",
                "What's your experience been like?"
            ],
            'personal_starters': [
                "I think", "I believe", "In my opinion", "From my experience",
                "I've found that", "What I've noticed is", "Personally",
                "I've always thought", "My take is", "The way I see it",
                "I tend to think", "I'm convinced that", "It seems to me",
                "I have a feeling", "I suspect", "I'm pretty sure"
            ],
            'filler_phrases': [
                "honestly", "actually", "really", "basically", "pretty much",
                "kind of", "sort of", "you know", "I mean", "like",
                "obviously", "clearly", "definitely", "certainly", "absolutely",
                "totally", "completely", "essentially", "fundamentally", "ultimately"
            ],
            'casual_transitions': [
                "Plus", "Also", "And", "But", "So", "Now", "Well", "Actually",
                "Honestly", "Look", "Listen", "Here's the thing", "You know what",
                "Speaking of which", "That reminds me", "On a related note",
                "While we're on the topic", "That said", "On the flip side"
            ]
        }
    
    def humanize_text(self, text: str, intensity: str = "heavy", use_groq: bool = False) -> Dict[str, Any]:
        """
        Main method to humanize AI-generated text using multiple techniques.
        
        Args:
            text: The AI-generated text to humanize
            intensity: How much to humanize ("light", "medium", "heavy")
            use_groq: Whether to use Groq API for additional humanization
            
        Returns:
            Dictionary containing original text, humanized text, and changes made
        """
        if not text or not text.strip():
            return {
                'original': text,
                'humanized': text,
                'changes_made': [],
                'success': False,
                'error': 'Empty text provided'
            }
        
        try:
            original_text = text
            changes_made = []
            
            # Multi-pass processing for maximum effectiveness
            print(f"🔄 Starting {intensity} humanization...")
            
            # Pass 1: Apply core transformations
            if intensity in ["medium", "heavy"]:
                text = self._replace_ai_phrases(text)
                changes_made.append("Replaced AI phrases")
                
                text = self._add_contractions(text)
                changes_made.append("Added contractions")
                
                text = self._adjust_vocabulary(text)
                changes_made.append("Simplified vocabulary")
            
            # Pass 2: Add human characteristics
            if intensity == "heavy":
                text = self._add_personal_touches(text)
                changes_made.append("Added personal touches")
                
                text = self._add_human_imperfections(text)
                changes_made.append("Added human imperfections")
                
                text = self._vary_sentence_structure(text)
                changes_made.append("Varied sentence structure")
            
            # Pass 3: Break AI detection patterns
            text = self._break_ai_detection_patterns(text)
            changes_made.append("Broke AI detection patterns")
            
            # Pass 4: Apply statistical conformity
            text = self._apply_statistical_patterns(text)
            changes_made.append("Applied human writing patterns")
            
            # Pass 5: Add final polish
            text = self._final_polish(text)
            changes_made.append("Final polish applied")
            
            # Optional: Use Groq API for additional humanization
            if use_groq and self.groq_api_key:
                try:
                    text = self._humanize_with_groq(text)
                    changes_made.append("Applied Groq AI enhancement")
                except Exception as e:
                    print(f"⚠️ Groq enhancement failed: {e}")
            
            return {
                'original': original_text,
                'humanized': text,
                'changes_made': changes_made,
                'success': True,
                'word_count_original': len(original_text.split()),
                'word_count_humanized': len(text.split()),
                'transformation_intensity': intensity
            }
            
        except Exception as e:
            return {
                'original': text,
                'humanized': text,
                'changes_made': [],
                'success': False,
                'error': str(e)
            }
    
    def _replace_ai_phrases(self, text: str) -> str:
        """Replace AI phrases with human alternatives"""
        for ai_phrase, replacements in self.human_replacements.items():
            if ai_phrase.lower() in text.lower():
                replacement = random.choice(replacements)
                # Use case-insensitive replacement
                pattern = re.compile(re.escape(ai_phrase), re.IGNORECASE)
                text = pattern.sub(replacement, text, count=1)
        return text
    
    def _add_contractions(self, text: str) -> str:
        """Add contractions to make text more casual"""
        for formal, casual in self.contractions.items():
            pattern = r'\b' + re.escape(formal) + r'\b'
            text = re.sub(pattern, casual, text, flags=re.IGNORECASE)
        return text
    
    def _adjust_vocabulary(self, text: str) -> str:
        """Replace complex words with simpler alternatives"""
        for complex_word, simple_word in self.vocabulary_replacements.items():
            pattern = r'\b' + re.escape(complex_word) + r'\b'
            text = re.sub(pattern, simple_word, text, flags=re.IGNORECASE)
        return text
    
    def _add_personal_touches(self, text: str) -> str:
        """Add personal opinions and experiences"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for i, sentence in enumerate(sentences):
            if random.random() < 0.15 and not sentence.strip().startswith('#'):
                personal_starter = random.choice(self.human_templates['personal_starters'])
                # Restructure sentence to include personal touch
                sentence = sentence.strip()
                if sentence:
                    sentences[i] = f"{personal_starter}, {sentence.lower()}"
        
        return ' '.join(sentences)
    
    def _add_human_imperfections(self, text: str) -> str:
        """Add natural human speech patterns and imperfections"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for i, sentence in enumerate(sentences):
            # Add filler words
            if random.random() < 0.1:
                filler = random.choice(self.human_templates['filler_phrases'])
                words = sentence.split()
                if len(words) > 3:
                    insert_pos = random.randint(1, len(words) - 1)
                    words.insert(insert_pos, filler)
                    sentences[i] = ' '.join(words)
            
            # Add casual interjections
            if random.random() < 0.05:
                interjection = random.choice(["you know", "I mean", "right", "yeah"])
                sentences[i] = f"{sentence.rstrip('.')} - {interjection}."
        
        return ' '.join(sentences)
    
    def _vary_sentence_structure(self, text: str) -> str:
        """Change sentence patterns to be less predictable"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for i, sentence in enumerate(sentences):
            # Replace formal starters
            if random.random() < 0.2:
                if sentence.strip().startswith('The '):
                    replacements = ["When you look at", "If you consider", "Looking at"]
                    replacement = random.choice(replacements)
                    sentences[i] = sentence.replace('The ', f"{replacement} the ", 1)
                elif sentence.strip().startswith('This '):
                    replacements = ["When you think about this", "If you consider this", "Looking at this"]
                    replacement = random.choice(replacements)
                    sentences[i] = sentence.replace('This ', f"{replacement} ", 1)
            
            # Add sentence fragments occasionally
            if random.random() < 0.1 and i > 0:
                fragments = ["Simple as that.", "Period.", "End of story.", "That's it."]
                fragment = random.choice(fragments)
                sentences[i] = f"{sentence} {fragment}"
        
        return ' '.join(sentences)
    
    def _break_ai_detection_patterns(self, text: str) -> str:
        """Break patterns that AI detectors commonly look for"""
        # Remove or replace formal transitions
        for pattern in self.ai_detection_markers['formal_structures']:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                casual_replacement = random.choice(self.human_templates['casual_transitions'])
                text = text.replace(match, casual_replacement, 1)
        
        return text
    
    def _apply_statistical_patterns(self, text: str) -> str:
        """Apply statistical patterns to match human writing"""
        # This is a simplified version - in a full implementation,
        # we'd analyze and adjust sentence lengths, paragraph sizes, etc.
        
        # Add some variation to sentence endings
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        for i, sentence in enumerate(sentences):
            if random.random() < 0.05:  # 5% chance to add variation
                if sentence.endswith('.'):
                    if random.random() < 0.3:
                        sentences[i] = sentence[:-1] + '!'
                    elif random.random() < 0.2:
                        sentences[i] = sentence[:-1] + '?'
        
        return ' '.join(sentences)
    
    def _final_polish(self, text: str) -> str:
        """Apply final polish and cleanup"""
        # Fix multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Fix punctuation spacing
        text = re.sub(r'\s+([,.!?])', r'\1', text)
        
        # Ensure proper sentence spacing
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        return text.strip()
    
    def _humanize_with_groq(self, text: str) -> str:
        """Use Groq API for additional humanization"""
        if not HAS_REQUESTS or not self.groq_api_key:
            return text
        
        try:
            headers = {
                'Authorization': f'Bearer {self.groq_api_key}',
                'Content-Type': 'application/json'
            }
            
            prompt = f"""Please rewrite this text to sound more human and natural. Make it conversational, add personal touches, use contractions, and remove any formal or AI-like language:

{text}

Make it sound like a real person wrote it naturally."""
            
            data = {
                'model': 'llama-3.3-70b-versatile',
                'messages': [
                    {'role': 'system', 'content': 'You are a skilled editor who makes text sound more human and natural.'},
                    {'role': 'user', 'content': prompt}
                ],
                'temperature': 0.9,
                'max_tokens': len(text.split()) * 2
            }
            
            response = requests.post(self.groq_api_url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content'].strip()
            else:
                print(f"⚠️ Groq API error: {response.status_code}")
                return text
                
        except Exception as e:
            print(f"⚠️ Groq humanization failed: {e}")
            return text
    
    def batch_humanize(self, texts: List[str], intensity: str = "heavy", use_groq: bool = False) -> List[Dict[str, Any]]:
        """
        Humanize multiple texts at once.
        
        Args:
            texts: List of texts to humanize
            intensity: Humanization intensity
            use_groq: Whether to use Groq API
            
        Returns:
            List of humanization results
        """
        results = []
        
        for i, text in enumerate(texts):
            print(f"🔄 Processing text {i+1}/{len(texts)}")
            result = self.humanize_text(text, intensity, use_groq)
            results.append(result)
        
        return results
    
    def analyze_changes(self, original: str, humanized: str) -> Dict[str, Any]:
        """
        Analyze changes made during humanization.
        
        Args:
            original: Original text
            humanized: Humanized text
            
        Returns:
            Analysis of changes made
        """
        analysis = {
            'word_count_change': len(humanized.split()) - len(original.split()),
            'contractions_added': humanized.count("'") - original.count("'"),
            'character_count_change': len(humanized) - len(original),
            'sentences_modified': 0,
            'ai_phrases_replaced': 0
        }
        
        # Count AI phrases replaced
        for ai_phrase in self.ai_phrases:
            if ai_phrase.lower() in original.lower() and ai_phrase.lower() not in humanized.lower():
                analysis['ai_phrases_replaced'] += 1
        
        # Count sentences modified (simplified check)
        original_sentences = re.split(r'[.!?]', original)
        humanized_sentences = re.split(r'[.!?]', humanized)
        
        if len(original_sentences) == len(humanized_sentences):
            for orig, human in zip(original_sentences, humanized_sentences):
                if orig.strip() != human.strip():
                    analysis['sentences_modified'] += 1
        
        return analysis

# Create a global instance
humanizer = HybridHumanizer() 