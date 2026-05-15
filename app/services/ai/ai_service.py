from abc import ABC, abstractmethod


class AIService(ABC):
    """
    Abstract inteface for AI services.
    Any provider (OpenAI, Anthropic, Local) must adhere to this contract.1
    """

    model_name: str

    @abstractmethod
    def send_petition(
        self, system_instruction: str, user_prompt: str, lang: str = "Spanish"
    ) -> dict:
        """
        Core method to send a request to the Generative Model.

        It instantiates a new model per request to properly inject the
        System Instructions, which is the most token-efficient way to set
        context in Gemini.

        Args:
            system_instruction (str): Instructions defining the AI's role and rules.
            user_prompt (str): The specific user data or query.

        Returns:
            str: The raw text response from the AI.
        """

        pass
