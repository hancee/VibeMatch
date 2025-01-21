from functools import partial
from swarm import Agent
from src.service.tools.error_handler import mock_an_error, send_details_to_human
from src.service.tools.web_search import (
    search_fragrantica_forum,
    search_fragrantica_news,
    search_fragrantica_perfume,
    search_fragrantica_notes,
)
from src.service.tools.data_retriever import retrieve_data_based_on_reference_perfume
from src.service.tools.recommender import (
    get_perfumes_with_similar_notes_based_on_perfume_id,
    get_perfumes_x_flankers_with_similar_accords_based_on_perfume_id,
    get_perfumes_with_similar_accords_based_on_perfume_id,
)


from src.service.prompts import (
    triage_instructions,
    expert_instructions,
    researcher_instructions,
    analyst_instructions,
    mock_instructions,
)


# Transfer functions
def transfer_to_triage():
    print("Transfering to Triage...")
    return triage_agent


def transfer_to_expert():
    print("Transfering to Expert...")
    return expert_agent


def transfer_to_researcher():
    print("Transfering to Researcher...")
    return researcher_agent


def transfer_to_analyst():
    print("Transfering to Analyst...")
    return analyst_agent


def transfer_to_mock():
    print("Transfering to Mock...")
    return mock_agent


# Agents
# TODO: Optimize model for task types
base_agent = partial(
    Agent, model="gpt-4o-mini"  # , name="Alex"
)  # Use same name, users don't care about agents

triage_agent = base_agent(
    name="Triage",
    instructions=triage_instructions,
    functions=[
        transfer_to_expert,
        transfer_to_researcher,
        transfer_to_analyst,
        transfer_to_mock,
    ],
)

expert_agent = base_agent(
    name="Expert",
    instructions=expert_instructions,
    functions=[
        transfer_to_triage,
        search_fragrantica_forum,
        search_fragrantica_news,
        search_fragrantica_perfume,
        search_fragrantica_notes,
    ],
)

researcher_agent = base_agent(
    name="Researcher",
    instructions=researcher_instructions,
    functions=[
        transfer_to_triage,
        search_fragrantica_forum,
        search_fragrantica_news,
        search_fragrantica_perfume,
        search_fragrantica_notes,
    ],
)

analyst_agent = base_agent(
    name="Analyst",
    instructions=analyst_instructions,
    functions=[
        transfer_to_triage,
        retrieve_data_based_on_reference_perfume,
        get_perfumes_with_similar_notes_based_on_perfume_id,
        get_perfumes_with_similar_accords_based_on_perfume_id,
        get_perfumes_x_flankers_with_similar_accords_based_on_perfume_id,
    ],
)

mock_agent = base_agent(
    name="Mock",
    instructions=mock_instructions,
    functions=[mock_an_error, send_details_to_human],
)
