#!/usr/bin/env python3
"""
Balanced Processor - Intelligent Content Optimization

This service intelligently balances plagiarism reduction and AI detection avoidance
by using sophisticated algorithms that maintain content quality while addressing both issues.
"""

import re
import random
import string
import json
from typing import List, Dict, Tuple, Optional, Any
from pathlib import Path
import hashlib
import time

class BalancedProcessor:
    """
    Advanced processor that intelligently balances plagiarism reduction and AI detection avoidance
    """
    
    def __init__(self):
        """Initialize the balanced processor with intelligent patterns"""
        self._load_balanced_patterns()
        self._load_human_natural_phrases()
        self._load_unique_content_templates()
        self._load_plagiarism_safe_alternatives()
        self._load_ai_detection_safe_patterns()
        
        print("⚖️ BalancedProcessor initialized successfully!")
    
    def _load_balanced_patterns(self):
        """Load patterns that reduce both plagiarism and AI detection"""
        self.balanced_patterns = {
            # Phrases that are both unique and human-like
            "balanced_phrases": {
                "in today's world": [
                    "nowadays", "these days", "in our current times", 
                    "in this day and age", "in the present era"
                ],
                "it is important to note": [
                    "what's interesting is", "here's the thing", 
                    "something I've noticed", "what I've found is"
                ],
                "furthermore": [
                    "also", "plus", "what's more", "on top of that",
                    "another thing", "besides that"
                ],
                "additionally": [
                    "also", "plus", "what's more", "on top of that",
                    "another point", "something else"
                ],
                "in conclusion": [
                    "so", "bottom line", "what it comes down to",
                    "all in all", "to wrap up", "long story short"
                ],
                "to summarize": [
                    "so basically", "in short", "here's what it boils down to",
                    "the main point is", "what this means is"
                ],
                "overall": [
                    "all in all", "when you step back", "looking at the big picture",
                    "generally speaking", "broadly speaking"
                ],
                "ultimately": [
                    "at the end of the day", "when push comes to shove",
                    "what really matters", "in the end", "when it's all said and done"
                ]
            },
            
            # Sentence starters that are unique but natural
            "natural_starters": [
                "You know what's interesting?",
                "Here's something I've learned",
                "What I've discovered is",
                "Something I've noticed",
                "From my experience",
                "What I've found is",
                "I've realized that",
                "I've come to understand",
                "What I've observed is",
                "I've noticed that",
                "In my view",
                "From what I can see",
                "What strikes me is",
                "I've found that",
                "What I've learned is"
            ]
        }
    
    def _load_human_natural_phrases(self):
        """Load phrases that sound human but are unique enough to avoid plagiarism"""
        self.human_natural_phrases = {
            "opinion_phrases": [
                "I think", "I believe", "I feel", "I reckon", "I suppose",
                "In my opinion", "From my perspective", "As far as I'm concerned",
                "I'd say", "I'd argue", "I'd suggest"
            ],
            "experience_phrases": [
                "I've found that", "I've noticed that", "I've learned that",
                "I've discovered that", "I've realized that", "I've observed that",
                "I've seen that", "I've experienced", "I've encountered",
                "I've dealt with", "I've worked with"
            ],
            "casual_transitions": [
                "You know", "Actually", "Honestly", "To be honest", "Frankly",
                "Truth be told", "Let me tell you", "Here's the thing",
                "What's interesting is", "Something I've learned"
            ]
        }
    
    def _load_unique_content_templates(self):
        """Load templates for creating unique but natural content"""
        self.unique_templates = {
            "personal_insights": [
                "What I've found is that {topic} really {action} when you {condition}.",
                "I've noticed that {topic} tends to {action} especially when {condition}.",
                "From my experience, {topic} works best when you {action}.",
                "I've learned that {topic} can {action} if you {condition}.",
                "What I've discovered is that {topic} often {action} when {condition}."
            ],
            "casual_explanations": [
                "You know, {topic} is actually pretty {adjective} when you think about it.",
                "Here's the thing about {topic} - it's really {adjective} if you {action}.",
                "What's interesting about {topic} is that it {action} in ways you might not expect.",
                "Something I've learned about {topic} is that it {action} when {condition}.",
                "The cool thing about {topic} is that it {action} when you {condition}."
            ]
        }
    
    def _load_plagiarism_safe_alternatives(self):
        """Load alternatives that are unique but don't sound robotic"""
        self.plagiarism_safe_alternatives = {
            "benefits": ["advantages", "upsides", "perks", "pluses", "good things"],
            "important": ["key", "crucial", "essential", "vital", "critical"],
            "help": ["assist", "support", "aid", "facilitate", "enable"],
            "use": ["utilize", "employ", "apply", "leverage", "take advantage of"],
            "make": ["create", "produce", "generate", "develop", "build"],
            "get": ["obtain", "acquire", "receive", "gain", "attain"],
            "know": ["understand", "comprehend", "grasp", "realize", "recognize"],
            "think": ["believe", "feel", "consider", "suppose", "assume"],
            "want": ["desire", "wish", "hope", "need", "seek"],
            "like": ["enjoy", "love", "appreciate", "value", "prefer"],
            "good": ["great", "excellent", "awesome", "fantastic", "amazing"],
            "bad": ["terrible", "awful", "horrible", "dreadful", "lousy"],
            "big": ["large", "huge", "enormous", "massive", "substantial"],
            "small": ["tiny", "little", "miniature", "compact", "minimal"]
        }
    
    def _load_ai_detection_safe_patterns(self):
        """Load patterns that avoid AI detection while maintaining uniqueness"""
        self.ai_safe_patterns = {
            # Avoid overly perfect sentence structures
            "imperfect_structures": [
                "You know, {topic} is actually pretty {adjective}.",
                "Here's the thing - {topic} really {action} when {condition}.",
                "What I've found is that {topic} tends to {action}.",
                "I've noticed that {topic} can {action} if you {condition}.",
                "From my experience, {topic} works best when {condition}."
            ],
            # Add natural breaks and pauses
            "natural_breaks": [
                "You know what?",
                "Here's the thing...",
                "What's interesting is...",
                "Something I've learned...",
                "I've found that...",
                "What I've noticed is...",
                "From what I can see...",
                "The thing is..."
            ]
        }
    
    def process_content(self, content: str, target_balance: str = "balanced") -> Dict[str, Any]:
        """
        Process content with intelligent balance between plagiarism and AI detection
        
        Args:
            content: The original content to process
            target_balance: Target balance ("plagiarism_focused", "ai_focused", "balanced")
            
        Returns:
            Dict containing processed content and metadata
        """
        try:
            original_content = content
            processed_content = content
            changes_made = []
            
            # Step 1: Apply balanced phrase replacement
            processed_content, phrase_changes = self._apply_balanced_phrases(processed_content)
            changes_made.extend(phrase_changes)
            
            # Step 2: Add natural human elements
            processed_content, human_changes = self._add_natural_human_elements(processed_content)
            changes_made.extend(human_changes)
            
            # Step 3: Apply intelligent synonym replacement
            processed_content, synonym_changes = self._apply_intelligent_synonyms(processed_content)
            changes_made.extend(synonym_changes)
            
            # Step 4: Add unique but natural content variations
            processed_content, variation_changes = self._add_unique_variations(processed_content)
            changes_made.extend(variation_changes)
            
            # Step 5: Apply target-specific optimizations
            if target_balance == "plagiarism_focused":
                processed_content, opt_changes = self._optimize_for_plagiarism(processed_content)
                changes_made.extend(opt_changes)
            elif target_balance == "ai_focused":
                processed_content, opt_changes = self._optimize_for_ai_detection(processed_content)
                changes_made.extend(opt_changes)
            else:  # balanced
                processed_content, opt_changes = self._optimize_balanced(processed_content)
                changes_made.extend(opt_changes)
            
            # Step 6: Final polish
            processed_content, polish_changes = self._final_polish(processed_content)
            changes_made.extend(polish_changes)
            
            return {
                "success": True,
                "original_content": original_content,
                "processed_content": processed_content,
                "changes_made": changes_made,
                "total_changes": len(changes_made),
                "target_balance": target_balance
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "original_content": content,
                "processed_content": content
            }
    
    def _apply_balanced_phrases(self, content: str) -> Tuple[str, List[str]]:
        """Apply balanced phrase replacement"""
        changes = []
        
        for phrase, alternatives in self.balanced_patterns["balanced_phrases"].items():
            if phrase.lower() in content.lower():
                replacement = random.choice(alternatives)
                pattern = re.compile(re.escape(phrase), re.IGNORECASE)
                if pattern.search(content):
                    content = pattern.sub(replacement, content)
                    changes.append(f"Replaced '{phrase}' with '{replacement}'")
        
        return content, changes
    
    def _add_natural_human_elements(self, content: str) -> Tuple[str, List[str]]:
        """Add natural human elements without making it too common"""
        changes = []
        
        sentences = re.split(r'[.!?]+', content)
        modified_sentences = []
        
        for sentence in sentences:
            if sentence.strip() and random.random() < 0.25:  # 25% chance
                # Add a natural human element
                if random.random() < 0.5:
                    starter = random.choice(self.balanced_patterns["natural_starters"])
                    sentence = f"{starter} {sentence.strip()}"
                    changes.append("Added natural human starter")
                else:
                    opinion = random.choice(self.human_natural_phrases["opinion_phrases"])
                    sentence = f"{sentence.strip()}, {opinion}."
                    changes.append("Added personal opinion phrase")
            
            modified_sentences.append(sentence)
        
        content = '. '.join(modified_sentences)
        return content, changes
    
    def _apply_intelligent_synonyms(self, content: str) -> Tuple[str, List[str]]:
        """Apply intelligent synonym replacement"""
        changes = []
        
        words = content.split()
        for i, word in enumerate(words):
            word_lower = word.lower().strip(string.punctuation)
            if word_lower in self.plagiarism_safe_alternatives and random.random() < 0.15:  # 15% chance
                synonym = random.choice(self.plagiarism_safe_alternatives[word_lower])
                
                # Preserve original case
                if word[0].isupper():
                    synonym = synonym.capitalize()
                
                words[i] = word.replace(word_lower, synonym)
                changes.append(f"Replaced '{word_lower}' with '{synonym}'")
        
        content = ' '.join(words)
        return content, changes
    
    def _add_unique_variations(self, content: str) -> Tuple[str, List[str]]:
        """Add unique content variations"""
        changes = []
        
        # Add some unique but natural sentence structures
        sentences = re.split(r'[.!?]+', content)
        modified_sentences = []
        
        for sentence in sentences:
            if sentence.strip() and random.random() < 0.2:  # 20% chance
                # Add a natural break
                break_phrase = random.choice(self.ai_safe_patterns["natural_breaks"])
                sentence = f"{break_phrase} {sentence.strip()}"
                changes.append("Added natural break phrase")
            
            modified_sentences.append(sentence)
        
        content = '. '.join(modified_sentences)
        return content, changes
    
    def _optimize_for_plagiarism(self, content: str) -> Tuple[str, List[str]]:
        """Optimize specifically for plagiarism reduction"""
        changes = []
        
        # Use more unique phrases and structures
        # Add more personal experiences and specific examples
        experience_phrases = self.human_natural_phrases["experience_phrases"]
        
        sentences = re.split(r'[.!?]+', content)
        modified_sentences = []
        
        for sentence in sentences:
            if sentence.strip() and random.random() < 0.3:  # 30% chance
                experience = random.choice(experience_phrases)
                sentence = f"{sentence.strip()} {experience}."
                changes.append("Added personal experience reference")
            
            modified_sentences.append(sentence)
        
        content = '. '.join(modified_sentences)
        return content, changes
    
    def _optimize_for_ai_detection(self, content: str) -> Tuple[str, List[str]]:
        """Optimize specifically for AI detection avoidance"""
        changes = []
        
        # Use more casual, imperfect language
        # Add more contractions and informal expressions
        contractions = {
            "it is": "it's",
            "that is": "that's",
            "there is": "there's",
            "here is": "here's",
            "you are": "you're",
            "we are": "we're",
            "they are": "they're",
            "I am": "I'm",
            "do not": "don't",
            "cannot": "can't",
            "will not": "won't"
        }
        
        for formal, casual in contractions.items():
            if formal in content.lower():
                pattern = re.compile(re.escape(formal), re.IGNORECASE)
                if pattern.search(content):
                    content = pattern.sub(casual, content)
                    changes.append(f"Added contraction: '{formal}' to '{casual}'")
        
        return content, changes
    
    def _optimize_balanced(self, content: str) -> Tuple[str, List[str]]:
        """Optimize for balanced approach"""
        changes = []
        
        # Apply moderate changes that address both issues
        # Use a mix of unique phrases and natural language
        
        # Add some casual transitions
        casual_transitions = self.human_natural_phrases["casual_transitions"]
        
        sentences = re.split(r'[.!?]+', content)
        modified_sentences = []
        
        for sentence in sentences:
            if sentence.strip() and random.random() < 0.2:  # 20% chance
                transition = random.choice(casual_transitions)
                sentence = f"{transition}, {sentence.strip()}"
                changes.append("Added casual transition")
            
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
    
    def batch_process(self, contents: List[str], target_balance: str = "balanced") -> List[Dict[str, Any]]:
        """Process multiple contents in batch"""
        results = []
        for content in contents:
            result = self.process_content(content, target_balance)
            results.append(result)
        return results

# Create global instance
balanced_processor = BalancedProcessor() 