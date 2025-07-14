#!/usr/bin/env python3
"""
Post-Processing Service - Advanced Content Optimization

This service applies post-generation processing techniques to further reduce
plagiarism and AI detection scores while maintaining content quality.
"""

import re
import random
import string
import json
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path
import hashlib
import time

class PostProcessor:
    """
    Advanced post-processing service that applies multiple techniques to
    reduce plagiarism and AI detection while maintaining content quality.
    """
    
    def __init__(self):
        """Initialize the post-processor with all necessary patterns and data"""
        self._load_plagiarism_reduction_patterns()
        self._load_ai_detection_avoidance()
        self._load_content_variation_templates()
        self._load_synonym_database()
        self._load_sentence_restructuring_patterns()
        
        print("🔧 PostProcessor initialized successfully!")
    
    def _load_plagiarism_reduction_patterns(self):
        """Load patterns for reducing plagiarism"""
        self.plagiarism_patterns = {
            # Common phrases that might trigger plagiarism
            "common_phrases": [
                "in today's world",
                "in the modern era",
                "as we all know",
                "it goes without saying",
                "needless to say",
                "obviously",
                "clearly",
                "evidently",
                "apparently",
                "seemingly",
                "undoubtedly",
                "certainly",
                "definitely",
                "absolutely",
                "completely",
                "entirely",
                "thoroughly",
                "comprehensively",
                "extensively",
                "intensively"
            ],
            
            # Alternative expressions
            "alternatives": {
                "in today's world": ["nowadays", "these days", "in our current times", "in this day and age"],
                "in the modern era": ["in today's society", "in our times", "in the current age"],
                "as we all know": ["as you probably know", "as most people know", "as you might know"],
                "it goes without saying": ["obviously", "clearly", "naturally", "of course"],
                "needless to say": ["obviously", "clearly", "naturally", "of course"],
                "obviously": ["clearly", "naturally", "of course", "evidently"],
                "clearly": ["obviously", "naturally", "of course", "evidently"],
                "evidently": ["obviously", "clearly", "apparently", "seemingly"],
                "apparently": ["seemingly", "evidently", "obviously", "clearly"],
                "seemingly": ["apparently", "evidently", "obviously", "clearly"],
                "undoubtedly": ["certainly", "definitely", "absolutely", "without doubt"],
                "certainly": ["definitely", "absolutely", "undoubtedly", "without doubt"],
                "definitely": ["certainly", "absolutely", "undoubtedly", "without doubt"],
                "absolutely": ["definitely", "certainly", "completely", "entirely"],
                "completely": ["entirely", "thoroughly", "absolutely", "totally"],
                "entirely": ["completely", "thoroughly", "totally", "absolutely"],
                "thoroughly": ["completely", "entirely", "comprehensively", "extensively"],
                "comprehensively": ["thoroughly", "extensively", "completely", "entirely"],
                "extensively": ["thoroughly", "comprehensively", "intensively", "completely"],
                "intensively": ["extensively", "thoroughly", "comprehensively", "deeply"]
            }
        }
    
    def _load_ai_detection_avoidance(self):
        """Load patterns to avoid AI detection"""
        self.ai_avoidance_patterns = {
            # AI-like sentence structures to avoid
            "ai_structures": [
                r"\b(First|Second|Third|Fourth|Fifth|Finally)\b.*\.",
                r"\b(Additionally|Furthermore|Moreover|Also)\b.*\.",
                r"\b(In conclusion|To summarize|Overall|Ultimately)\b.*\.",
                r"\b(It is important to|It should be noted that|It is worth mentioning)\b.*\.",
                r"\b(One must|One should|One needs to)\b.*\.",
                r"\b(As a result|Therefore|Thus|Hence|Consequently)\b.*\.",
                r"\b(On the other hand|However|Nevertheless|Nonetheless)\b.*\.",
                r"\b(For example|For instance|Such as|Like)\b.*\.",
                r"\b(According to|Based on|According to research|Studies show)\b.*\.",
                r"\b(It can be argued that|It is believed that|It is thought that)\b.*\."
            ],
            
            # Human-like alternatives
            "human_alternatives": {
                "transitional_phrases": [
                    "You know what's interesting?",
                    "Here's the thing",
                    "What I've found is",
                    "Something else to consider",
                    "Oh, and another thing",
                    "By the way",
                    "Speaking of which",
                    "That reminds me",
                    "You might be wondering",
                    "Let me tell you",
                    "Here's what I think",
                    "In my experience",
                    "From what I've seen",
                    "What I've noticed is",
                    "I've found that"
                ],
                "conclusion_phrases": [
                    "So there you have it",
                    "Bottom line",
                    "What it comes down to",
                    "Long story short",
                    "At the end of the day",
                    "When you think about it",
                    "All things considered",
                    "When push comes to shove",
                    "What really matters is",
                    "The takeaway here is"
                ]
            }
        }
    
    def _load_content_variation_templates(self):
        """Load templates for content variation"""
        self.variation_templates = {
            "sentence_starters": [
                "I think",
                "In my opinion",
                "From what I've seen",
                "What I've noticed is",
                "You know",
                "Actually",
                "Honestly",
                "To be honest",
                "Frankly",
                "Truth be told",
                "Let me tell you",
                "Here's the thing",
                "What's interesting is",
                "Something I've learned",
                "Based on my experience",
                "I've found that",
                "What I've discovered is",
                "From my perspective",
                "In my view",
                "As far as I'm concerned"
            ],
            "personal_experiences": [
                "I remember when",
                "I once",
                "I've experienced",
                "I've seen",
                "I've noticed",
                "I've found",
                "I've learned",
                "I've discovered",
                "I've realized",
                "I've come to understand",
                "I've figured out",
                "I've observed",
                "I've witnessed",
                "I've encountered",
                "I've dealt with"
            ]
        }
    
    def _load_synonym_database(self):
        """Load comprehensive synonym database"""
        self.synonyms = {
            "good": ["great", "excellent", "awesome", "fantastic", "amazing", "wonderful", "terrific", "superb", "outstanding", "brilliant"],
            "bad": ["terrible", "awful", "horrible", "dreadful", "atrocious", "abysmal", "lousy", "poor", "subpar", "mediocre"],
            "big": ["large", "huge", "enormous", "massive", "gigantic", "colossal", "immense", "substantial", "considerable", "significant"],
            "small": ["tiny", "little", "miniature", "petite", "compact", "minuscule", "microscopic", "diminutive", "slight", "minimal"],
            "important": ["crucial", "essential", "vital", "critical", "key", "significant", "major", "primary", "fundamental", "core"],
            "help": ["assist", "support", "aid", "facilitate", "enable", "empower", "guide", "direct", "lead", "mentor"],
            "use": ["utilize", "employ", "apply", "implement", "adopt", "leverage", "harness", "exploit", "take advantage of", "make use of"],
            "make": ["create", "produce", "generate", "develop", "build", "construct", "form", "establish", "set up", "put together"],
            "get": ["obtain", "acquire", "receive", "gain", "attain", "achieve", "secure", "procure", "collect", "gather"],
            "know": ["understand", "comprehend", "grasp", "realize", "recognize", "appreciate", "see", "perceive", "acknowledge", "accept"],
            "think": ["believe", "feel", "consider", "suppose", "assume", "imagine", "guess", "figure", "reckon", "suspect"],
            "want": ["desire", "wish", "hope", "need", "require", "seek", "aim", "intend", "plan", "aspire"],
            "like": ["enjoy", "love", "appreciate", "value", "prefer", "favor", "admire", "respect", "cherish", "treasure"],
            "hate": ["dislike", "loathe", "despise", "abhor", "detest", "can't stand", "can't bear", "find unbearable", "find intolerable", "find repulsive"],
            "see": ["observe", "notice", "perceive", "spot", "detect", "identify", "recognize", "view", "witness", "behold"],
            "say": ["tell", "speak", "talk", "mention", "state", "declare", "announce", "proclaim", "express", "voice"],
            "do": ["perform", "execute", "carry out", "accomplish", "achieve", "complete", "finish", "fulfill", "conduct", "undertake"],
            "go": ["move", "travel", "journey", "proceed", "advance", "progress", "head", "set out", "depart", "leave"],
            "come": ["arrive", "reach", "approach", "draw near", "show up", "turn up", "appear", "emerge", "surface", "materialize"],
            "take": ["grab", "seize", "capture", "obtain", "acquire", "get hold of", "pick up", "collect", "gather", "harvest"]
        }
    
    def _load_sentence_restructuring_patterns(self):
        """Load patterns for sentence restructuring"""
        self.restructuring_patterns = {
            "passive_to_active": [
                (r"is (.*?) by", r"actively \1"),
                (r"are (.*?) by", r"actively \1"),
                (r"was (.*?) by", r"actively \1"),
                (r"were (.*?) by", r"actively \1"),
                (r"has been (.*?) by", r"has actively \1"),
                (r"have been (.*?) by", r"have actively \1"),
                (r"had been (.*?) by", r"had actively \1")
            ],
            "complex_to_simple": [
                (r"in order to", "to"),
                (r"for the purpose of", "to"),
                (r"with regard to", "about"),
                (r"in relation to", "about"),
                (r"as a result of", "because of"),
                (r"due to the fact that", "because"),
                (r"in the event that", "if"),
                (r"prior to", "before"),
                (r"subsequent to", "after"),
                (r"in accordance with", "following")
            ]
        }
    
    def process_content(self, content: str, intensity: str = "heavy") -> Dict[str, Any]:
        """
        Apply comprehensive post-processing to reduce plagiarism and AI detection
        
        Args:
            content: The original content to process
            intensity: Processing intensity (light, medium, heavy)
            
        Returns:
            Dict containing processed content and metadata
        """
        try:
            original_content = content
            processed_content = content
            changes_made = []
            
            # Apply processing based on intensity
            if intensity in ["medium", "heavy"]:
                # Step 1: Reduce plagiarism through phrase replacement
                processed_content, plagiarism_changes = self._reduce_plagiarism(processed_content)
                changes_made.extend(plagiarism_changes)
                
                # Step 2: Avoid AI detection patterns
                processed_content, ai_changes = self._avoid_ai_detection(processed_content)
                changes_made.extend(ai_changes)
                
                # Step 3: Add content variation
                processed_content, variation_changes = self._add_content_variation(processed_content)
                changes_made.extend(variation_changes)
                
                # Step 4: Apply synonym replacement
                processed_content, synonym_changes = self._apply_synonym_replacement(processed_content)
                changes_made.extend(synonym_changes)
                
                # Step 5: Restructure sentences
                processed_content, structure_changes = self._restructure_sentences(processed_content)
                changes_made.extend(structure_changes)
            
            if intensity == "heavy":
                # Additional heavy processing
                processed_content, heavy_changes = self._apply_heavy_processing(processed_content)
                changes_made.extend(heavy_changes)
            
            # Step 6: Final polish and validation
            processed_content, polish_changes = self._final_polish(processed_content)
            changes_made.extend(polish_changes)
            
            return {
                "success": True,
                "original_content": original_content,
                "processed_content": processed_content,
                "changes_made": changes_made,
                "total_changes": len(changes_made),
                "processing_intensity": intensity
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original_content": content,
                "processed_content": content
            }
    
    def _reduce_plagiarism(self, content: str) -> Tuple[str, List[str]]:
        """Reduce plagiarism through phrase replacement"""
        changes = []
        
        # Replace common phrases that might trigger plagiarism detection
        for phrase in self.plagiarism_patterns["common_phrases"]:
            if phrase.lower() in content.lower():
                alternatives = self.plagiarism_patterns["alternatives"].get(phrase, [phrase])
                replacement = random.choice(alternatives)
                
                # Use case-insensitive replacement
                pattern = re.compile(re.escape(phrase), re.IGNORECASE)
                if pattern.search(content):
                    content = pattern.sub(replacement, content)
                    changes.append(f"Replaced '{phrase}' with '{replacement}'")
        
        return content, changes
    
    def _avoid_ai_detection(self, content: str) -> Tuple[str, List[str]]:
        """Avoid AI detection patterns"""
        changes = []
        
        # Replace AI-like sentence structures
        for pattern_str in self.ai_avoidance_patterns["ai_structures"]:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            matches = pattern.findall(content)
            
            for match in matches:
                if "First" in match or "Second" in match or "Third" in match:
                    replacement = random.choice(self.variation_templates["sentence_starters"])
                    content = content.replace(match, replacement, 1)
                    changes.append(f"Replaced AI transition '{match}' with '{replacement}'")
                elif "In conclusion" in match or "To summarize" in match:
                    replacement = random.choice(self.ai_avoidance_patterns["human_alternatives"]["conclusion_phrases"])
                    content = content.replace(match, replacement, 1)
                    changes.append(f"Replaced AI conclusion '{match}' with '{replacement}'")
                elif "Additionally" in match or "Furthermore" in match:
                    replacement = random.choice(self.ai_avoidance_patterns["human_alternatives"]["transitional_phrases"])
                    content = content.replace(match, replacement, 1)
                    changes.append(f"Replaced AI transition '{match}' with '{replacement}'")
        
        return content, changes
    
    def _add_content_variation(self, content: str) -> Tuple[str, List[str]]:
        """Add content variation to make it more unique"""
        changes = []
        
        # Add personal touches to some sentences
        sentences = re.split(r'[.!?]+', content)
        modified_sentences = []
        
        for i, sentence in enumerate(sentences):
            if sentence.strip() and random.random() < 0.3:  # 30% chance
                if random.random() < 0.5:
                    starter = random.choice(self.variation_templates["sentence_starters"])
                    sentence = f"{starter}, {sentence.strip()}"
                    changes.append(f"Added personal starter to sentence")
                else:
                    experience = random.choice(self.variation_templates["personal_experiences"])
                    sentence = f"{sentence.strip()} {experience}."
                    changes.append(f"Added personal experience reference")
            
            modified_sentences.append(sentence)
        
        content = '. '.join(modified_sentences)
        return content, changes
    
    def _apply_synonym_replacement(self, content: str) -> Tuple[str, List[str]]:
        """Apply synonym replacement to reduce repetition"""
        changes = []
        
        words = content.split()
        for i, word in enumerate(words):
            word_lower = word.lower().strip(string.punctuation)
            if word_lower in self.synonyms and random.random() < 0.2:  # 20% chance
                synonym = random.choice(self.synonyms[word_lower])
                
                # Preserve original case
                if word[0].isupper():
                    synonym = synonym.capitalize()
                
                words[i] = word.replace(word_lower, synonym)
                changes.append(f"Replaced '{word_lower}' with '{synonym}'")
        
        content = ' '.join(words)
        return content, changes
    
    def _restructure_sentences(self, content: str) -> Tuple[str, List[str]]:
        """Restructure sentences to avoid AI patterns"""
        changes = []
        
        # Convert passive to active voice where appropriate
        for pattern, replacement in self.restructuring_patterns["passive_to_active"]:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                changes.append(f"Converted passive to active voice")
        
        # Simplify complex phrases
        for pattern, replacement in self.restructuring_patterns["complex_to_simple"]:
            if re.search(pattern, content, re.IGNORECASE):
                content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
                changes.append(f"Simplified complex phrase '{pattern}' to '{replacement}'")
        
        return content, changes
    
    def _apply_heavy_processing(self, content: str) -> Tuple[str, List[str]]:
        """Apply heavy processing techniques"""
        changes = []
        
        # Add more personal anecdotes and experiences
        personal_phrases = [
            "I've found that",
            "In my experience",
            "What I've learned is",
            "I've noticed that",
            "From what I've seen",
            "I've discovered that",
            "I've realized that",
            "I've come to understand that"
        ]
        
        sentences = re.split(r'[.!?]+', content)
        modified_sentences = []
        
        for sentence in sentences:
            if sentence.strip() and random.random() < 0.4:  # 40% chance for heavy processing
                phrase = random.choice(personal_phrases)
                sentence = f"{phrase} {sentence.strip()}"
                changes.append(f"Added personal phrase to sentence")
            
            modified_sentences.append(sentence)
        
        content = '. '.join(modified_sentences)
        return content, changes
    
    def _final_polish(self, content: str) -> Tuple[str, List[str]]:
        """Final polish and validation"""
        changes = []
        
        # Clean up multiple spaces
        content = re.sub(r'\s+', ' ', content)
        
        # Fix punctuation
        content = re.sub(r'\s+([.!?])', r'\1', content)
        
        # Ensure proper spacing after periods
        content = re.sub(r'\.([A-Z])', r'. \1', content)
        
        changes.append("Applied final polish and formatting")
        
        return content, changes
    
    def batch_process(self, contents: List[str], intensity: str = "heavy") -> List[Dict[str, Any]]:
        """Process multiple contents in batch"""
        results = []
        for content in contents:
            result = self.process_content(content, intensity)
            results.append(result)
        return results

# Create global instance
post_processor = PostProcessor() 