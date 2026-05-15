import json
import logging
from typing import Any, Dict

from google import genai
from google.genai import types

from app.core import prompts
from app.services.ai.ai_service import AIService

logger = logging.getLogger(__name__)


class GeminiService(AIService):
    """
    Implementation of the AIService using Google Gemini 1.5 Flash.

    This service handles the interaction with the Gemini API,
    structuring prompts according to the Role-Task-Context-Format framework
    to ensure high-quality and cost-effective responses.
    """

    def __init__(self, api_key: str):
        """
        Initializes the Gemini SDK.

        Args:
            api_key (str): The Google API Key for authentication.
        """
        self.client = genai.Client(api_key=api_key)
        self.model_name = "gemini-1.5-flash"

    def send_petition(self, system_instruction: str, user_prompt: str) -> str:
        config = types.GenerateContentConfig(system_instruction=system_instruction)
        response = self.client.models.generate_content(
            model=self.model_name, config=config, contents=user_prompt
        )

        return response.text

    def analyze_transaction(
        self, description: str, amount: float, lang: str = "Spanish"
    ) -> Dict[str, Any]:
        """
        Analyzes a bank transaction to categorize it and provide a saving tip.

        The method constructs an optimized prompt in English to leverage
        the model's reasoning capabilities, while requesting the final
        output in the user's preferred language.

        Args:
            description (str): The transaction description (e.g., "Starbucks").
            amount (float): The transaction amount.
            lang (str): The language for the 'saving_tip' value. Defaults to "Spanish".

        Returns:
            Dict[str, Any]: A dictionary containing 'category' and 'saving_tip'.

        Example:
            {
                "category": "Food & Drink",
                "saving_tip": "Consider making coffee at home to save $150 monthly."
            }
        """

        system_instruction = (
            f"{prompts.TRANSACTION_ROLE}\n"
            f"{prompts.TRANSACTION_TASK}\n"
            f"{prompts.GLOBAL_CONSTRAINT}"
        )

        format_instruction = prompts.TRANSACTION_FORMAT.format(language=lang)

        user_prompt = (
            f"Context: User spent {amount} on '{description}'.\n"
            f"Output Format: {format_instruction}"
        )

        try:
            raw_response = self.send_petition(system_instruction, user_prompt)

            clean_json = (
                raw_response.strip().removeprefix("```json").removesuffix("```")
            )
            return json.loads(clean_json)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response: {raw_response}. Error: {e}")
            return {
                "category": "Uncategorized",
                "saving_tip": "Analyze your spending habits to find saving opportunities.",
            }
        except Exception as e:
            logger.error(f"Gemini Service Error: {e}")
            raise e
