import time
from typing import Any, AsyncGenerator, List, Optional, Type
from pydantic import BaseModel
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage as LcAIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings
from app.ai.llm.base import BaseLLM
from app.ai.framework.messages import AIMessage, AIResponse
from app.ai.llm.exceptions import LLMConnectionError
from app.infrastructure.logging.logger import logger

class GeminiLLM(BaseLLM):
    """Google Gemini adapter class wrapping ChatGoogleGenerativeAI client operations."""

    def __init__(self):
        self.client = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.3
        )

    def _convert_messages(self, messages: List[AIMessage]) -> List[Any]:
        """Converts app AIMessage objects to LangChain message models."""
        converted = []
        for msg in messages:
            role = msg.role.lower()
            if role == "system":
                converted.append(SystemMessage(content=msg.content))
            elif role == "user":
                converted.append(HumanMessage(content=msg.content))
            elif role in ("assistant", "ai"):
                converted.append(LcAIMessage(content=msg.content))
            else:
                # Default fallback
                converted.append(HumanMessage(content=msg.content))
        return converted

    async def invoke(
        self, 
        messages: List[AIMessage], 
        schema: Optional[Type[BaseModel]] = None,
        system_instruction: Optional[str] = None
    ) -> AIResponse:
        try:
            lc_messages = self._convert_messages(messages)
            if system_instruction:
                lc_messages.insert(0, SystemMessage(content=system_instruction))
                
            start_time = time.time()
            
            if schema:
                structured_client = self.client.with_structured_output(schema)
                res = await structured_client.ainvoke(lc_messages)
                elapsed = time.time() - start_time
                
                # For structured outputs, the output is directly the schema instance
                return AIResponse(
                    content=str(res.model_dump() if hasattr(res, "model_dump") else res),
                    structured_output=res,
                    latency=elapsed,
                    finish_reason="stop",
                    cost=0.001
                )
            else:
                res = await self.client.ainvoke(lc_messages)
                elapsed = time.time() - start_time
                
                metadata = res.response_metadata or {}
                token_usage = metadata.get("token_usage", {})
                prompt_tokens = token_usage.get("prompt_tokens", 0)
                completion_tokens = token_usage.get("completion_tokens", 0)
                total_tokens = token_usage.get("total_tokens", 0)
                
                cost = self.estimate_cost(prompt_tokens, completion_tokens)
                
                return AIResponse(
                    content=res.content,
                    token_usage={
                        "prompt": prompt_tokens,
                        "completion": completion_tokens,
                        "total": total_tokens
                    },
                    latency=elapsed,
                    cost=cost,
                    finish_reason="stop"
                )
        except Exception as e:
            logger.error("Gemini invocation failed", error=str(e))
            raise LLMConnectionError(f"Gemini API failure: {str(e)}")

    async def stream(self, messages: List[AIMessage]) -> AsyncGenerator[str, None]:
        try:
            lc_messages = self._convert_messages(messages)
            async for chunk in self.client.astream(lc_messages):
                yield chunk.content
        except Exception as e:
            logger.error("Gemini streaming failed", error=str(e))
            raise LLMConnectionError(f"Gemini stream failure: {str(e)}")

    async def batch(self, inputs: List[List[AIMessage]]) -> List[AIResponse]:
        import asyncio
        tasks = [self.invoke(messages) for messages in inputs]
        return list(await asyncio.gather(*tasks))

    async def embed(self, text: str) -> List[float]:
        # Trivial float embedding placeholder for pgvector compat
        return [0.01 * i for i in range(128)]

    async def health(self) -> bool:
        try:
            res = await self.client.ainvoke("ping")
            return res is not None
        except Exception:
            return False

    async def token_count(self, prompt: str) -> int:
        try:
            return await self.client.get_num_tokens_async(prompt)
        except Exception:
            return len(prompt.split())

    def estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        input_cost = (prompt_tokens / 1_000_000) * 1.25
        output_cost = (completion_tokens / 1_000_000) * 5.00
        return input_cost + output_cost
