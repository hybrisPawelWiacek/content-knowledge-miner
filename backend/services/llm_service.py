# /backend/services/llm_service.py

import os
from config import Config
from openai import OpenAI
# Import Anthropic client if available
try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None
import logging

logger = logging.getLogger(__name__)

# Dictionary to store model information
MODEL_INFO = {
    "openai": [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo-0125",
        "gpt-3.5-turbo"
    ],
    "anthropic": [
        "claude-3-5-sonnet-20240620",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307"
    ]
}


openai_api_key = Config.OPENAI_API_KEY

if Config.ANTHROPIC_API_KEY and Anthropic:
    anthropic_client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
else:
    anthropic_client = None

def generate_summary(prompt, model='gpt-4o-mini'):
    logger.info(f"Generating summary using model: {model}")
    try:
        for provider, models in MODEL_INFO.items():
            if model in models:
                if provider == 'openai':
                    return generate_openai_summary(prompt, model=model)
                elif provider == 'anthropic' and anthropic_client:
                    return generate_anthropic_summary(prompt, model=model)
        logger.error(f"Unsupported model specified: {model}")
        raise ValueError('Unsupported model specified')
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise ValueError(f'Error generating summary: {str(e)}')

def generate_openai_summary(prompt, model='gpt-4o-mini'):
    logger.info(f"Generating OpenAI summary using model: {model}")
    client = OpenAI(api_key=openai_api_key)  
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        summary = response.choices[0].message.content
        logger.info("OpenAI summary generated successfully")
        return summary
    except Exception as e:
        logger.error(f"OpenAI API error: {e}")
        return 'An error occurred while generating the summary with OpenAI.'

def generate_anthropic_summary(prompt, model='anthropic-claude-1'):
    logger.info(f"Generating Anthropic summary using model: {model}")
    if not anthropic_client:
        logger.error("Anthropic client not initialized")
        raise ValueError('Anthropic client not initialized.')
    try:
        response = anthropic_client.completions.create(
            model=model,
            prompt=prompt,
            max_tokens_to_sample=500
        )
        summary = response.completion
        logger.info("Anthropic summary generated successfully")
        return summary
    except Exception as e:
        logger.error(f"Anthropic API error: {e}")
        return 'An error occurred while generating the summary with Anthropic.'
