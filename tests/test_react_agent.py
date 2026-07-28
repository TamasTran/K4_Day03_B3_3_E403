import contextlib
import io
import sys
import unittest
from pathlib import Path


SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

import app
from providers import MockProvider
from tools import get_candidate_profile


class ScriptedProvider:
    """Provider giả lập để kiểm tra loop LLM mà không gọi API thật."""

    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = []

    def generate(self, prompt, system_prompt=""):
        self.calls.append((prompt, system_prompt))
        return next(self.responses)


class ReActAgentTests(unittest.TestCase):
    def run_silently(self, query, provider, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()):
            return app.run_react_agent(query, provider, **kwargs)

    def test_real_provider_path_runs_action_then_uses_observation(self):
        provider = ScriptedProvider(
            [
                'Thought: Cần đọc JD.\nAction: get_job_description["JOB-2024-001"]',
                "Thought: Đã đủ dữ liệu.\nFinal Answer: Đây là vị trí Python Developer.",
            ]
        )

        result = self.run_silently(
            "Cho tôi biết JD JOB-2024-001",
            provider,
        )

        self.assertEqual(result, "Đây là vị trí Python Developer.")
        self.assertEqual(len(provider.calls), 2)
        self.assertIn("REACT", provider.calls[0][1].upper())
        self.assertIn("Observation:", provider.calls[1][0])
        self.assertIn("Python Developer", provider.calls[1][0])

    def test_malformed_llm_output_stops_safely(self):
        provider = ScriptedProvider(["Tôi sẽ tự làm mà không theo định dạng."])

        result = self.run_silently("Thực hiện tác vụ", provider)

        self.assertIn("không trả về Action hoặc Final Answer", result)

    def test_missing_candidate_stops_after_tool_error(self):
        result = self.run_silently(
            "Đánh giá CD-999 với JOB-2024-001",
            MockProvider(),
        )

        self.assertIn("Tool báo lỗi nên Agent dừng lại", result)
        self.assertIn("CD-999", result)

    def test_unavailable_slot_is_not_scheduled(self):
        result = self.run_silently(
            "Hẹn CD-001 với INT-001 vào 2024-12-25 15:00",
            MockProvider(),
        )

        self.assertIn("không có trong lịch trống", result)
        self.assertNotIn("ĐÃ TẠO LỊCH PHỎNG VẤN", result)

    def test_tool_exception_is_returned_as_error_string(self):
        result = get_candidate_profile([])

        self.assertIsInstance(result, str)
        self.assertIn("LỖI", result)


if __name__ == "__main__":
    unittest.main()
