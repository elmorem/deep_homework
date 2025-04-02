import asyncio
import datetime
from typing import Dict, List

from fastapi import WebSocket

from backend.report_type.basic_report.basic_report import BasicReport
from backend.report_type.detailed_report.detailed_report import DetailedReport
from backend.chat.chat import ChatAgentWithMemory

from homework_researcher.utils.enum import ReportType, Tone, EducationLevel
from multi_agents.main import run_research_task

from homework_researcher.actions.utils import (
    stream_output,
)  # Import stream_output for streaming
from backend.server.server_utils import CustomLogsHandler


class WebSocketManager:
    """Manage websockets"""

    def __init__(self):
        """Initialize the WebSocketManager class."""
        self.active_connections: List[WebSocket] = []
        self.sender_tasks: Dict[WebSocket, asyncio.Task] = {}
        self.message_queues: Dict[WebSocket, asyncio.Queue] = {}
        self.chat_agent = None

    async def start_sender(self, websocket: WebSocket):
        """Start the sender task."""
        queue = self.message_queues.get(websocket)
        if not queue:
            return

        while True:
            try:
                message = await queue.get()
                if message is None:  # Shutdown signal
                    break

                if websocket in self.active_connections:
                    if message == "ping":
                        await websocket.send_text("pong")
                    else:
                        await websocket.send_text(message)
                else:
                    break
            except Exception as e:
                print(f"Error in sender task: {e}")
                break

    async def connect(self, websocket: WebSocket):
        """Connect a websocket."""
        try:
            await websocket.accept()
            self.active_connections.append(websocket)
            self.message_queues[websocket] = asyncio.Queue()
            self.sender_tasks[websocket] = asyncio.create_task(
                self.start_sender(websocket)
            )
        except Exception as e:
            print(f"Error connecting websocket: {e}")
            if websocket in self.active_connections:
                await self.disconnect(websocket)

    async def disconnect(self, websocket: WebSocket):
        """Disconnect a websocket."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            if websocket in self.sender_tasks:
                self.sender_tasks[websocket].cancel()
                await self.message_queues[websocket].put(None)
                del self.sender_tasks[websocket]
            if websocket in self.message_queues:
                del self.message_queues[websocket]
            try:
                await websocket.close()
            except:
                pass  # Connection might already be closed

    async def start_streaming(
        self,
        task,
        report_type,
        report_source,
        source_urls,
        document_urls,
        tone,
        education_level,
        websocket,
        headers=None,
        query_domains=[],
    ):
        """Start streaming the output."""
        tone = Tone[tone]
        education_level = EducationLevel[education_level]
        print(f"Tone: {tone}")
        print(f"Education Level: {education_level}")
        config_path = "default"

        await stream_output(
            "logs",
            "planning_research",
            f"🌐 Here is what we are working with: ed level = {education_level}tone ={tone}task = {task} report_type={report_type} ...",
            websocket,
        )

        report = await run_agent(
            task,
            report_type,
            report_source,
            source_urls,
            document_urls,
            tone,
            education_level,
            websocket,
            headers=headers,
            query_domains=query_domains,
            config_path=config_path,
        )
        # Create new Chat Agent whenever a new report is written
        self.chat_agent = ChatAgentWithMemory(report, config_path, headers)
        return report

    async def chat(self, message, websocket):
        """Chat with the agent based message diff"""
        if self.chat_agent:
            await self.chat_agent.chat(message, websocket)
        else:
            await websocket.send_json(
                {
                    "type": "chat",
                    "content": "Knowledge empty, please run the research first to obtain knowledge",
                }
            )


async def run_agent(
    task,
    report_type,
    report_source,
    source_urls,
    document_urls,
    tone: Tone,
    education_level: EducationLevel,
    websocket,
    stream_output=stream_output,
    headers=None,
    query_domains=[],
    config_path="",
    return_researcher=False,
):
    """Run the agent."""
    # Create logs handler for this research task
    logs_handler = CustomLogsHandler(websocket, task)

    # Initialize researcher based on report type
    if report_type == "multi_agents":
        report = await run_research_task(
            query=task,
            websocket=logs_handler,  # Use logs_handler instead of raw websocket
            stream_output=stream_output,
            tone=tone,
            education_level=education_level,
            headers=headers,
        )
        report = report.get("report", "")

    elif report_type == ReportType.DetailedReport.value:
        researcher = DetailedReport(
            query=task,
            query_domains=query_domains,
            report_type=report_type,
            report_source=report_source,
            source_urls=source_urls,
            document_urls=document_urls,
            tone=tone,
            education_level=education_level,
            config_path=config_path,
            websocket=logs_handler,  # Use logs_handler instead of raw websocket
            headers=headers,
        )
        report = await researcher.run()

    else:
        researcher = BasicReport(
            query=task,
            query_domains=query_domains,
            report_type=report_type,
            report_source=report_source,
            source_urls=source_urls,
            document_urls=document_urls,
            tone=tone,
            education_level=education_level,
            config_path=config_path,
            websocket=logs_handler,  # Use logs_handler instead of raw websocket
            headers=headers,
        )
        report = await researcher.run()

    if report_type != "multi_agents" and return_researcher:
        return report, researcher.gpt_researcher
    else:
        return report
