from enum import Enum


class EducationLevel(Enum):
    JuniorHigh = "Junior high school level (introductory concepts, basic sources, simple language). MAX_SUBTOPICS=2"
    HighSchool = "High school level (introdutory and background sources, moderate complexity, accessible language, some critical thinkg, some primary sources).MAX_SUBTOPICS=3"
    Undergraduate = "Undergraduate level (allow for some prior knoledge, more complex sources, moderate to high complexity, critical thinking expected, some primary sources, highlight academic sources, discourage non-academic sources). MAX_SUBTOPICS=4"
    Graduate = "Graduate level (advanced concepts, in-depth analysis, high complexity, critical thinking and synthesis of information expected, extensive use of primary sources, highlight academic sources, ignore non-academic sources) MAX_SUBTOPICS=5"


class ReportType(Enum):
    PrecisReport = "precis_report"
    ResearchReport = "research_report"
    ResourceReport = "resource_report"
    OutlineReport = "outline_report"
    CustomReport = "custom_report"
    DetailedReport = "detailed_report"
    SubtopicReport = "subtopic_report"
    DeepResearch = "deep"


class ReportSource(Enum):
    Web = "web"
    Local = "local"
    Azure = "azure"
    LangChainDocuments = "langchain_documents"
    LangChainVectorStore = "langchain_vectorstore"
    Static = "static"
    Hybrid = "hybrid"


class Tone(Enum):
    Objective = "Objective (impartial and unbiased presentation of facts and findings)"
    Formal = "Formal (adheres to academic standards with sophisticated language and structure)"
    Analytical = (
        "Analytical (critical evaluation and detailed examination of data and theories)"
    )
    Persuasive = (
        "Persuasive (convincing the audience of a particular viewpoint or argument)"
    )
    Informative = (
        "Informative (providing clear and comprehensive information on a topic)"
    )
    Explanatory = "Explanatory (clarifying complex concepts and processes)"
    Descriptive = (
        "Descriptive (detailed depiction of phenomena, experiments, or case studies)"
    )
    Critical = "Critical (judging the validity and relevance of the research and its conclusions)"
    Comparative = "Comparative (juxtaposing different theories, data, or methods to highlight differences and similarities)"
    Speculative = "Speculative (exploring hypotheses and potential implications or future research directions)"
    Reflective = "Reflective (considering the research process and personal insights or experiences)"
    Narrative = (
        "Narrative (telling a story to illustrate research findings or methodologies)"
    )
    Humorous = "Humorous (light-hearted and engaging, usually to make the content more relatable)"
    Optimistic = "Optimistic (highlighting positive findings and potential benefits)"
    Pessimistic = (
        "Pessimistic (focusing on limitations, challenges, or negative outcomes)"
    )
