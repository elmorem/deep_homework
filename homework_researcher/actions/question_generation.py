import asyncio
from typing import List, Dict, Any
from ..actions.utils import stream_output
from ..config.config import Config
from ..utils.llm import create_chat_completion
from ..utils.logger import get_formatted_logger
from ..utils.enum import Tone, EducationLevel
from ..prompts import generate_research_questions_prompt


logger = get_formatted_logger()

async def generate_questions(
    query: str,
    context,
    agent_role_prompt: str,
    report_type: str,
    tone: Tone,
    education_level: EducationLevel,
    report_source: str,
    websocket,
    cfg,
    main_topic: str = "",
    existing_headers: list = [],
    relevant_written_contents: list = [],
    cost_callback: callable = None,
    headers=None,
):