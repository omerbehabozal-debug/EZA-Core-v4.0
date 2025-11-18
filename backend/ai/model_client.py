# -*- coding: utf-8 -*-
"""
model_client.py – EZA LLM Client
Unified interface for calling external LLM providers (OpenAI, Anthropic, etc.)
"""

import os
import httpx
from typing import Optional


class LLMClient:
    """
    Unified LLM client for multiple providers.
    Supports OpenAI, Anthropic, and other providers via environment variables.
    """
    
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.api_key = os.getenv("LLM_API_KEY", "")
        self.model = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.base_url = os.getenv("LLM_BASE_URL", None)  # For custom endpoints
    
    async def call(
        self, 
        prompt: str, 
        system: Optional[str] = None, 
        temperature: float = 0.3,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Call LLM provider with prompt and optional system message.
        
        Args:
            prompt: User prompt/message
            system: Optional system message
            temperature: Temperature for generation (0.0-2.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
            
        Raises:
            NotImplementedError: If provider is not implemented
            httpx.HTTPError: If API call fails
        """
        if not self.api_key:
            raise ValueError("LLM_API_KEY environment variable is not set")
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        if self.provider == "openai":
            return await self._call_openai(prompt, system, temperature, max_tokens, headers)
        elif self.provider == "anthropic":
            return await self._call_anthropic(prompt, system, temperature, max_tokens, headers)
        elif self.provider == "gemini":
            return await self._call_gemini(prompt, system, temperature, max_tokens, headers)
        else:
            raise NotImplementedError(f"LLM provider '{self.provider}' is not implemented")
    
    async def _call_openai(
        self, 
        prompt: str, 
        system: Optional[str], 
        temperature: float,
        max_tokens: Optional[int],
        headers: dict
    ) -> str:
        """Call OpenAI API"""
        url = self.base_url or "https://api.openai.com/v1/chat/completions"
        
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            body["max_tokens"] = max_tokens
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, json=body, headers=headers)
            res.raise_for_status()
            data = res.json()
            return data["choices"][0]["message"]["content"]
    
    async def _call_anthropic(
        self, 
        prompt: str, 
        system: Optional[str], 
        temperature: float,
        max_tokens: Optional[int],
        headers: dict
    ) -> str:
        """Call Anthropic Claude API"""
        url = self.base_url or "https://api.anthropic.com/v1/messages"
        
        headers["anthropic-version"] = "2023-06-01"
        headers["x-api-key"] = self.api_key
        headers.pop("Authorization", None)  # Anthropic uses x-api-key
        
        messages = [{"role": "user", "content": prompt}]
        
        body = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens or 1024,
        }
        
        if system:
            body["system"] = system
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, json=body, headers=headers)
            res.raise_for_status()
            data = res.json()
            return data["content"][0]["text"]
    
    async def _call_gemini(
        self, 
        prompt: str, 
        system: Optional[str], 
        temperature: float,
        max_tokens: Optional[int],
        headers: dict
    ) -> str:
        """Call Google Gemini API"""
        url = self.base_url or f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
        # Gemini uses API key as query parameter
        params = {"key": self.api_key}
        
        contents = [{"parts": [{"text": prompt}]}]
        
        body = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
            }
        }
        
        if max_tokens:
            body["generationConfig"]["maxOutputTokens"] = max_tokens
        
        if system:
            body["systemInstruction"] = {"parts": [{"text": system}]}
        
        headers.pop("Authorization", None)  # Gemini uses query param
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, json=body, headers=headers, params=params)
            res.raise_for_status()
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

