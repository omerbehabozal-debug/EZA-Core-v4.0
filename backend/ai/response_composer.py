# -*- coding: utf-8 -*-
"""
response_composer.py – EZA Response Composer

Natural response composition for different intents and contexts.
"""

from typing import Dict, Any, Optional, List
import random


class ResponseComposer:
    """
    Composes natural, fluent responses based on facts, intent, and safety context.
    """
    
    def __init__(self):
        """Initialize response templates."""
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, List[str]]:
        """Load response templates for different intents."""
        return {
            "greeting": [
                "Selam! Buradayım, hazırım. Sana nasıl yardımcı olabilirim? 😊",
                "Merhaba! Yardımcı olmak için buradayım. Ne hakkında konuşmak istersin?",
                "Selam! EZA olarak buradayım. Sana nasıl yardımcı olabilirim?",
                "Merhaba! Hazırım ve yardımcı olmaya hazırım. Ne öğrenmek istersin?",
            ],
            "information": [
                "{fact}",
                "{fact} Başka bir sorun varsa yardımcı olabilirim.",
                "Bildiğim kadarıyla: {fact}",
                "{fact} Bu konuda başka bir şey merak ediyorsan sorabilirsin.",
            ],
            "explanation": [
                "{fact}",
                "Açıklayayım: {fact}",
                "{fact} Daha detaylı bilgi istersen sorabilirsin.",
                "Şöyle açıklayabilirim: {fact}",
            ],
            "help": [
                "Tabii ki! {fact}",
                "Elbette yardımcı olabilirim. {fact}",
                "Memnuniyetle! {fact}",
                "Tabii, {fact}",
            ],
            "general": [
                "{fact}",
                "{fact} Başka bir sorun varsa yardımcı olabilirim.",
                "Bildiğim kadarıyla: {fact}",
            ]
        }
    
    def compose_natural_response(
        self,
        fact: str,
        intent: str = "information",
        safety: str = "safe"
    ) -> str:
        """
        Compose a natural response based on fact, intent, and safety level.
        
        Args:
            fact: The fact or information to include in the response
            intent: The detected intent (greeting, information, explanation, help, general)
            safety: Safety level (safe, low, medium, high, critical)
        
        Returns:
            Natural language response string
        """
        # Normalize intent
        intent_lower = intent.lower()
        
        # Select appropriate template category based on intent
        # IMPORTANT: greeting should NOT reach here (handled separately)
        if intent_lower == "greeting":
            # This shouldn't happen, but fallback to greeting
            return self.compose_greeting_response()
        elif intent_lower in ["information", "info"]:
            template_category = "information"
        elif intent_lower in ["explanation", "explain"]:
            template_category = "explanation"
        elif intent_lower in ["help", "assistance"]:
            template_category = "help"
        else:
            # Default to information for unknown intents
            template_category = "information"
        
        # Get templates for this category
        templates = self.templates.get(template_category, self.templates["information"])
        
        # Select random template
        template = random.choice(templates)
        
        # Format template with fact
        try:
            response = template.format(fact=fact)
        except KeyError:
            # If template doesn't have {fact}, just use the fact
            response = fact
        
        # Add safety context if needed (for non-safe responses)
        if safety not in ["safe", "low"]:
            # For medium/high/critical, we might want to add a note
            # But for now, we'll keep it simple for natural conversation
            pass
        
        return response
    
    def compose_greeting_response(self) -> str:
        """Compose a greeting response."""
        templates = self.templates["greeting"]
        return random.choice(templates)
    
    def compose_fallback_response(self) -> str:
        """Compose a fallback response when no information is found."""
        fallback_templates = [
            "Bu konuda elimde bir veri yok ama yine de yardımcı olmaya hazırım.",
            "Bu konu hakkında bilgim yok, ama başka bir konuda yardımcı olabilirim.",
            "Bu konuda bilgim sınırlı, ama başka soruların varsa yardımcı olabilirim.",
            "Bu konu hakkında detaylı bilgim yok, ama başka bir şey sorabilirsin.",
        ]
        return random.choice(fallback_templates)

