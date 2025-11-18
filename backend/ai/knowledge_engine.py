# -*- coding: utf-8 -*-
"""
knowledge_engine.py – EZA Knowledge Engine

Semantic search and fact-based knowledge retrieval for natural conversations.
"""

from typing import Dict, Any, List, Optional
import json
import re


class KnowledgeEngine:
    """
    Knowledge Engine for semantic search and fact retrieval.
    Provides natural answers based on a knowledge base.
    """
    
    def __init__(self):
        """Initialize knowledge base."""
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> Dict[str, Any]:
        """
        Load knowledge base from structured data.
        In production, this could load from a database or vector store.
        """
        return {
            "general": {
                "eza": {
                    "facts": [
                        "EZA (Ethical Zone Assistant) bir etik analiz ve güvenlik sistemidir.",
                        "EZA, kullanıcı mesajlarını analiz ederek risk seviyelerini değerlendirir.",
                        "EZA, şiddet, yasa dışı faaliyetler ve zararlı içerikleri tespit eder.",
                        "EZA, kişisel veri koruma ve kimlik güvenliği konularında hassastır.",
                    ],
                    "capabilities": [
                        "Etik risk analizi",
                        "Niyet tespiti",
                        "Kimlik koruma",
                        "Manipülasyon tespiti",
                        "Yasal risk değerlendirmesi",
                    ]
                },
                "greeting": {
                    "facts": [
                        "Selamlaşma mesajlarına doğal ve samimi cevaplar verilir.",
                        "Kullanıcıya yardımcı olmaya hazır olduğumuz belirtilir.",
                    ]
                },
                "help": {
                    "facts": [
                        "EZA, kullanıcılara etik ve güvenli şekilde yardımcı olur.",
                        "Sorularınızı yanıtlamak için hazırım.",
                        "Bilgi vermek, açıklama yapmak ve rehberlik etmek için buradayım.",
                    ]
                }
            },
            "topics": {
                "etika": {
                    "facts": [
                        "Etik, doğru ve yanlış davranışları belirleyen ahlaki ilkelerdir.",
                        "Etik davranış, başkalarına saygılı ve zarar vermeyen davranışlardır.",
                        "EZA, etik ilkeleri gözeterek kullanıcılara yardımcı olur.",
                    ]
                },
                "güvenlik": {
                    "facts": [
                        "Güvenlik, kişisel verilerin ve kimliğin korunmasıdır.",
                        "Şifreler ve kişisel bilgiler paylaşılmamalıdır.",
                        "EZA, güvenlik risklerini tespit eder ve uyarır.",
                    ]
                },
                "teknoloji": {
                    "facts": [
                        "Teknoloji, hayatımızı kolaylaştıran araçlar ve sistemlerdir.",
                        "Yapay zeka, makine öğrenmesi ve doğal dil işleme modern teknolojilerdir.",
                        "EZA, yapay zeka tabanlı bir etik analiz sistemidir.",
                    ]
                },
                "yapay zeka": {
                    "facts": [
                        "Yapay zeka (AI), makinelerin insan benzeri düşünme ve öğrenme yeteneklerine sahip olmasını sağlayan teknolojidir.",
                        "Yapay zeka, makine öğrenmesi, doğal dil işleme ve derin öğrenme gibi alt alanları içerir.",
                        "Yapay zeka sistemleri, veri analizi, görüntü tanıma, dil çevirisi ve otomatik karar verme gibi görevleri yerine getirebilir.",
                        "EZA, yapay zeka teknolojisini kullanarak etik analiz ve güvenlik değerlendirmesi yapar.",
                    ]
                },
                "bilim": {
                    "facts": [
                        "Bilim, doğal dünyayı anlamak için sistematik gözlem, deney ve analiz yöntemlerini kullanan bir disiplindir.",
                        "Bilim, fizik, kimya, biyoloji, matematik gibi birçok alt dalı içerir.",
                        "Bilimsel yöntem, hipotez kurma, test etme ve sonuçları değerlendirme sürecidir.",
                    ]
                }
            }
        }
    
    def search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """
        Semantic search in knowledge base.
        Returns relevant facts and information.
        """
        query_lower = query.lower()
        results = []
        
        # Search in general topics
        for category, data in self.knowledge_base.get("general", {}).items():
            if category in query_lower or any(keyword in query_lower for keyword in ["eza", "sen", "siz", "yardım", "ne", "nasıl"]):
                if "facts" in data:
                    for fact in data["facts"]:
                        results.append({
                            "category": category,
                            "fact": fact,
                            "relevance": 0.8
                        })
                if "capabilities" in data:
                    for cap in data["capabilities"]:
                        results.append({
                            "category": category,
                            "fact": cap,
                            "relevance": 0.7
                        })
        
        # Search in specific topics
        for topic, data in self.knowledge_base.get("topics", {}).items():
            if topic in query_lower:
                if "facts" in data:
                    for fact in data["facts"]:
                        results.append({
                            "category": topic,
                            "fact": fact,
                            "relevance": 0.9
                        })
        
        # Keyword-based search
        keywords = {
            "eza": "general.eza",
            "etika": "topics.etika",
            "etik": "topics.etika",
            "güvenlik": "topics.güvenlik",
            "teknoloji": "topics.teknoloji",
            "yapay zeka": "topics.yapay zeka",
            "yapay zeka": "topics.yapay zeka",
            "ai": "topics.yapay zeka",
            "artificial intelligence": "topics.yapay zeka",
            "bilim": "topics.bilim",
            "science": "topics.bilim",
            "yardım": "general.help",
            "selam": "general.greeting",
            "merhaba": "general.greeting",
        }
        
        for keyword, path in keywords.items():
            if keyword in query_lower:
                category = path.split(".")[0]
                subcategory = path.split(".")[1] if "." in path else None
                if category in self.knowledge_base:
                    data = self.knowledge_base[category].get(subcategory, {}) if subcategory else {}
                    if "facts" in data:
                        for fact in data["facts"]:
                            results.append({
                                "category": subcategory or category,
                                "fact": fact,
                                "relevance": 0.85
                            })
        
        # Remove duplicates and sort by relevance
        seen = set()
        unique_results = []
        for result in results:
            fact_key = result["fact"]
            if fact_key not in seen:
                seen.add(fact_key)
                unique_results.append(result)
        
        unique_results.sort(key=lambda x: x["relevance"], reverse=True)
        return unique_results[:5]  # Return top 5 results
    
    def get_facts(self, topic: str) -> Dict[str, Any]:
        """
        Get facts about a specific topic.
        Returns structured JSON fact-base.
        """
        topic_lower = topic.lower()
        
        # Search in all categories
        facts = []
        for category, data in self.knowledge_base.items():
            if isinstance(data, dict):
                for key, value in data.items():
                    if topic_lower in key.lower() or key.lower() in topic_lower:
                        if isinstance(value, dict) and "facts" in value:
                            facts.extend(value["facts"])
        
        return {
            "topic": topic,
            "facts": facts,
            "count": len(facts)
        }
    
    def answer_query(self, query: str) -> Optional[str]:
        """
        Answer a query using knowledge base.
        Returns natural language answer or None if no information found.
        """
        # Search for relevant knowledge
        results = self.search_knowledge(query)
        
        if not results:
            return None
        
        # Combine facts into a natural answer
        facts = [r["fact"] for r in results[:3]]  # Use top 3 facts
        
        if len(facts) == 1:
            return facts[0]
        elif len(facts) == 2:
            return f"{facts[0]} Ayrıca, {facts[1].lower()}"
        else:
            answer = facts[0]
            for fact in facts[1:]:
                answer += f" {fact}"
            return answer

