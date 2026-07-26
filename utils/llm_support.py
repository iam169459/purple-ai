"""
LLM Support Module - Unified interface for multiple LLM providers
Supports: Ollama, OpenAI, LM Studio, and local models
"""
import os
import json
import logging
import requests
import threading
from typing import Dict, Any, List, Optional, AsyncGenerator
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from config import config
from logger import logger

class LLMProvider(Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    LMSTUDIO = "lmstudio"
    LOCAL = "local"

@dataclass
class LLMConfig:
    provider: LLMProvider
    host: str = "http://localhost:11434"
    api_key: str = ""
    model: str = ""
    temperature: float = 0.7
    max_tokens: int = 2048
    stream: bool = True

@dataclass
class LLMMessage:
    role: str  # system, user, assistant
    content: str

@dataclass
class LLMResponse:
    content: str
    model: str
    usage: Dict[str, int] = None
    finish_reason: str = "stop"
    error: str = None

class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.session = requests.Session()
        self._health_cache = {"status": None, "timestamp": 0}
    
    @abstractmethod
    def chat(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        pass
    
    @abstractmethod
    def chat_stream(self, messages: List[LLMMessage], **kwargs) -> AsyncGenerator[str, None]:
        pass
    
    @abstractmethod
    def list_models(self) -> List[str]:
        pass
    
    @abstractmethod
    def pull_model(self, model_name: str) -> bool:
        pass
    
    @abstractmethod
    def health_check(self) -> bool:
        pass

class OllamaProvider(BaseLLMProvider):
    """Ollama local LLM provider"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.base_url = config.host.rstrip('/')
    
    def chat(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        try:
            payload = {
                "model": self.config.model or "llama3",
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "num_predict": kwargs.get("max_tokens", self.config.max_tokens),
                }
            }
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            return LLMResponse(
                content=data["message"]["content"],
                model=data.get("model", self.config.model),
                usage={"prompt_tokens": data.get("prompt_eval_count", 0),
                       "completion_tokens": data.get("eval_count", 0)},
                finish_reason=data.get("done_reason", "stop")
            )
        except Exception as e:
            logger.error(f"Ollama chat error: {e}")
            return LLMResponse(content="", model="", error=str(e))
    
    def chat_stream(self, messages: List[LLMMessage], **kwargs):
        try:
            payload = {
                "model": self.config.model or "llama3",
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "stream": True,
                "options": {
                    "temperature": kwargs.get("temperature", self.config.temperature),
                    "num_predict": kwargs.get("max_tokens", self.config.max_tokens),
                }
            }
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=payload,
                stream=True,
                timeout=120
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    if "message" in data and "content" in data["message"]:
                        yield data["message"]["content"]
        except Exception as e:
            logger.error(f"Ollama stream error: {e}")
            yield f"Error: {e}"
    
    def list_models(self) -> List[str]:
        try:
            response = self.session.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            return [m["name"] for m in response.json().get("models", [])]
        except Exception as e:
            logger.error(f"Ollama list models error: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        try:
            response = self.session.post(
                f"{self.base_url}/api/pull",
                json={"name": model_name},
                stream=True,
                timeout=300
            )
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode('utf-8'))
                    if data.get("status") == "success":
                        return True
                    if "error" in data:
                        return False
            return True
        except Exception as e:
            logger.error(f"Ollama pull error: {e}")
            return False
    
    def health_check(self) -> bool:
        try:
            response = self.session.get(f"{self.base_url}/api/version", timeout=5)
            return response.status_code == 200
        except:
            return False

class OpenAIProvider(BaseLLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.base_url = "https://api.openai.com/v1"
        self.session.headers.update({
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        })
    
    def chat(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        try:
            payload = {
                "model": self.config.model or "gpt-4o",
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "temperature": kwargs.get("temperature", self.config.temperature),
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                "stream": False
            }
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            data = response.json()
            choice = data["choices"][0]
            return LLMResponse(
                content=choice["message"]["content"],
                model=data.get("model", self.config.model),
                usage=data.get("usage", {}),
                finish_reason=choice.get("finish_reason", "stop")
            )
        except Exception as e:
            logger.error(f"OpenAI chat error: {e}")
            return LLMResponse(content="", model="", error=str(e))
    
    def chat_stream(self, messages: List[LLMMessage], **kwargs):
        try:
            payload = {
                "model": self.config.model or "gpt-4o",
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "temperature": kwargs.get("temperature", self.config.temperature),
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                "stream": True
            }
            response = self.session.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                stream=True,
                timeout=60
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8').strip()
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            data = json.loads(data)
                            if "choices" in data and data["choices"]:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except:
                            pass
        except Exception as e:
            logger.error(f"OpenAI stream error: {e}")
            yield f"Error: {e}"
    
    def list_models(self) -> List[str]:
        try:
            response = self.session.get(f"{self.base_url}/models", timeout=10)
            response.raise_for_status()
            return [m["id"] for m in response.json().get("data", [])]
        except Exception as e:
            logger.error(f"OpenAI list models error: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        return False  # Not applicable for OpenAI
    
    def health_check(self) -> bool:
        try:
            response = self.session.get(f"{self.base_url}/models", timeout=5)
            return response.status_code == 200
        except:
            return False

class LMStudioProvider(BaseLLMProvider):
    """LM Studio local server provider (OpenAI-compatible API)"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        self.base_url = config.host.rstrip('/')
        self.session.headers.update({"Content-Type": "application/json"})
    
    def chat(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        try:
            payload = {
                "model": self.config.model or "local-model",
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "temperature": kwargs.get("temperature", self.config.temperature),
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                "stream": False
            }
            response = self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            choice = data["choices"][0]
            return LLMResponse(
                content=choice["message"]["content"],
                model=data.get("model", self.config.model),
                usage=data.get("usage", {}),
                finish_reason=choice.get("finish_reason", "stop")
            )
        except Exception as e:
            logger.error(f"LM Studio chat error: {e}")
            return LLMResponse(content="", model="", error=str(e))
    
    def chat_stream(self, messages: List[LLMMessage], **kwargs):
        try:
            payload = {
                "model": self.config.model or "local-model",
                "messages": [{"role": m.role, "content": m.content} for m in messages],
                "temperature": kwargs.get("temperature", self.config.temperature),
                "max_tokens": kwargs.get("max_tokens", self.config.max_tokens),
                "stream": True
            }
            response = self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                stream=True,
                timeout=120
            )
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8').strip()
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            data = json.loads(data)
                            if "choices" in data and data["choices"]:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except:
                            pass
        except Exception as e:
            logger.error(f"LM Studio stream error: {e}")
            yield f"Error: {e}"
    
    def list_models(self) -> List[str]:
        try:
            response = self.session.get(f"{self.base_url}/v1/models", timeout=10)
            response.raise_for_status()
            return [m["id"] for m in response.json().get("data", [])]
        except Exception as e:
            logger.error(f"LM Studio list models error: {e}")
            return []
    
    def pull_model(self, model_name: str) -> bool:
        return False
    
    def health_check(self) -> bool:
        try:
            response = self.session.get(f"{self.base_url}/v1/models", timeout=5)
            return response.status_code == 200
        except:
            return False

class LLMManager:
    """Unified LLM manager for multiple providers"""
    
    def __init__(self):
        self.providers: Dict[LLMProvider, BaseLLMProvider] = {}
        self.active_provider: Optional[BaseLLMProvider] = None
        self.active_provider_type: Optional[LLMProvider] = None
        self.config_dir = Path.home() / ".purple_ai"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / "llm_config.json"
        
        # Load saved config
        self._load_config()
        
        # Auto-detect available providers
        self._auto_detect()
    
    def _load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                    # Restore last active provider
                    if "active_provider" in data:
                        provider_type = LLMProvider(data["active_provider"])
                        self.set_active_provider(provider_type)
            except Exception as e:
                logger.error(f"Failed to load LLM config: {e}")
    
    def _save_config(self):
        try:
            data = {
                "active_provider": self.active_provider_type.value if self.active_provider_type else None
            }
            with open(self.config_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save LLM config: {e}")
    
    def _auto_detect(self):
        """Auto-detect available LLM providers"""
        # Check Ollama
        try:
            ollama = OllamaProvider(LLMConfig(provider=LLMProvider.OLLAMA))
            if ollama.health_check():
                self.add_provider(LLMProvider.OLLAMA, ollama)
                logger.info("Ollama detected and available")
        except:
            pass
        
        # Check LM Studio
        try:
            lms = LMStudioProvider(LLMConfig(provider=LLMSTUDIO, host="http://localhost:1234"))
            if lms.health_check():
                self.add_provider(LLMProvider.LMSTUDIO, lms)
                logger.info("LM Studio detected and available")
        except:
            pass
        
        # Check OpenAI (if API key present)
        if os.getenv("OPENAI_API_KEY"):
            try:
                openai = OpenAIProvider(LLMConfig(provider=LLMProvider.OPENAI, api_key=os.getenv("OPENAI_API_KEY")))
                if openai.health_check():
                    self.add_provider(LLMProvider.OPENAI, openai)
                    logger.info("OpenAI API available")
            except:
                pass
    
    def add_provider(self, provider_type: LLMProvider, provider: BaseLLMProvider):
        self.providers[provider_type] = provider
    
    def set_active_provider(self, provider_type: LLMProvider) -> bool:
        if provider_type in self.providers:
            self.active_provider = self.providers[provider_type]
            self.active_provider_type = provider_type
            self._save_config()
            logger.info(f"Active LLM provider set to: {provider_type.value}")
            return True
        return False
    
    def get_available_providers(self) -> List[LLMProvider]:
        return list(self.providers.keys())
    
    def get_active_provider(self) -> Optional[BaseLLMProvider]:
        return self.active_provider
    
    def get_active_provider_type(self) -> Optional[LLMProvider]:
        return self.active_provider_type
    
    def chat(self, messages: List[LLMMessage], **kwargs) -> LLMResponse:
        if not self.active_provider:
            return LLMResponse(content="", model="", error="No active LLM provider. Set one first.")
        return self.active_provider.chat(messages, **kwargs)
    
    def chat_stream(self, messages: List[LLMMessage], **kwargs):
        if not self.active_provider:
            yield "Error: No active LLM provider. Set one first."
            return
        yield from self.active_provider.chat_stream(messages, **kwargs)
    
    def list_models(self) -> List[str]:
        if not self.active_provider:
            return []
        return self.active_provider.list_models()
    
    def pull_model(self, model_name: str) -> bool:
        if not self.active_provider:
            return False
        return self.active_provider.pull_model(model_name)
    
    def set_model(self, model_name: str):
        if self.active_provider:
            self.active_provider.config.model = model_name
    
    def get_status(self) -> Dict[str, Any]:
        return {
            "active_provider": self.active_provider_type.value if self.active_provider_type else None,
            "available_providers": [p.value for p in self.providers.keys()],
            "current_model": self.active_provider.config.model if self.active_provider else None,
            "models": self.list_models() if self.active_provider else [],
            "health": {
                p.value: self.providers[p].health_check() for p in self.providers
            }
        }

# Global instance
llm_manager = LLMManager()