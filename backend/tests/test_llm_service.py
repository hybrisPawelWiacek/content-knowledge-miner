# backend/tests/test_llm_service.py

import unittest
from services.llm_service import generate_summary

class TestLLMService(unittest.TestCase):

    def test_generate_summary_openai(self):
        prompt = "Summarize the following text: Hello world."
        summary = generate_summary(prompt, model_choice='gpt-4o-mini')
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary) > 0)

    def test_generate_summary_anthropic(self):
        prompt = "Summarize the following text: Hello world."
        summary = generate_summary(prompt, model_choice='claude-3-5-sonnet-20240620')
        self.assertIsInstance(summary, str)
        self.assertTrue(len(summary) > 0)

if __name__ == '__main__':
    unittest.main()
