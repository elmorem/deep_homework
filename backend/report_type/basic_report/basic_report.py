from fastapi import WebSocket
from typing import Any

from homework_researcher.actions.utils import stream_output
from homework_researcher.agent import HomeworkResearcher


class BasicReport:
    def __init__(
        self,
        query: str,
        query_domains: list,
        report_type: str,
        report_source: str,
        source_urls,
        document_urls,
        tone: Any,
        config_path: str,
        websocket: WebSocket,
        headers=None,
    ):
        self.query = query
        self.query_domains = query_domains
        self.report_type = report_type
        self.report_source = report_source
        self.source_urls = source_urls
        self.document_urls = document_urls
        self.tone = tone
        self.config_path = config_path
        self.websocket = websocket
        self.headers = headers or {}

        # Initialize researcher
        self.researcher = HomeworkResearcher(
            query=self.query,
            query_domains=self.query_domains,
            report_type=self.report_type,
            report_source=self.report_source,
            source_urls=self.source_urls,
            document_urls=self.document_urls,
            tone=self.tone,
            config_path=self.config_path,
            websocket=self.websocket,
            headers=self.headers,
        )

    async def run(self):
        await stream_output(
            "logs",
            "planning_research",
            f"🌐 we are now starting to conduct our research. This is a BasicReport",
            self.researcher.websocket,
        )

        await self.researcher.conduct_research()
        report = await self.researcher.write_report()
        
        # await stream_output(
        #     "logs",
        #     "planning_research",
        #     f"report is now generated {report}",
        #     self.researcher.websocket,
        # )
        return report
