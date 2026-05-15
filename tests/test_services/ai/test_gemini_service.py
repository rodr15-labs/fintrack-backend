from unittest.mock import MagicMock, patch

import pytest

from app.services.ai.gemini_service import GeminiService


@pytest.fixture
def gemini_service():
    """Provides a GeminiService instance with a fake API key."""
    return GeminiService(api_key="fake_api_key_for_testing")


def test_analyze_transaction_language_dynamic_injection(gemini_service):
    """Verifies that the 'lang' parameter is correctly injected into the prompt."""

    with patch.object(
        gemini_service.client.models, "generate_content"
    ) as mock_generate:
        mock_generate.return_value = MagicMock(text='{"category":"x","saving_tip":"y"}')

        gemini_service.analyze_transaction("Gift", 100.0, lang="French")

        _, kwargs = mock_generate.call_args
        assert "French" in kwargs["contents"]
        assert "Gift" in kwargs["contents"]


def test_analyze_transaction_complex_json_cleaning(gemini_service):
    """Verifies that the service cleans different variations of Markdown JSON blocks."""
    with patch.object(
        gemini_service.client.models, "generate_content"
    ) as mock_generate:
        mock_response = MagicMock()

        mock_response.text = """
        ```json
        {
            "category": "Education",
            "saving_tip": "Check for scholarships"
        }
        """
        mock_generate.return_value = mock_response

        result = gemini_service.analyze_transaction("Course", 200.0)

        assert result["category"] == "Education"
        assert result["saving_tip"] == "Check for scholarships"


def test_send_petition_config_validation(gemini_service):
    """Verifies that the system instructions (Role/Task) are correctly passed in the config."""
    with patch.object(
        gemini_service.client.models, "generate_content"
    ) as mock_generate:
        mock_generate.return_value = MagicMock(
            text='{"category":"Tools","saving_tip":"Keep it up"}'
        )
        gemini_service.analyze_transaction("Tools", 50.0)
        _, kwargs = mock_generate.call_args
        config = kwargs["config"]
        assert "expert financial advisor" in config.system_instruction
        assert "Be concise" in config.system_instruction


def test_analyze_transaction_api_exception_handling(gemini_service):
    """Verifies that the service propagates general exceptions from the SDK."""
    with patch.object(
        gemini_service.client.models, "generate_content"
    ) as mock_generate:
        mock_generate.side_effect = Exception("Google API Error: Over Quota")
        with pytest.raises(Exception) as exc:
            gemini_service.analyze_transaction("Coffee", 5.0)
        assert "Over Quota" in str(exc.value)
