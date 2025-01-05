from functools import partial
from swarm import Agent
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


# def transfer_to_data_retriever():
#     print("Transfering to Data Retriever...")
#     return data_retriever_agent


# Agents
# TODO: Optimize model for task types
base_agent = partial(Agent, model="gpt-4o-mini")  # name="Alex",

triage_agent = base_agent(
    name="triage",
    instructions=triage_instructions,
    functions=[
        transfer_to_expert,
        transfer_to_researcher,
        transfer_to_analyst,
    ],
)

expert_agent = base_agent(
    name="expert",
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
    name="researcher",
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
    name="analyst",
    instructions=analyst_instructions,
    functions=[
        transfer_to_triage,
        retrieve_data_based_on_reference_perfume,
        get_perfumes_with_similar_notes_based_on_perfume_id,
        get_perfumes_with_similar_accords_based_on_perfume_id,
        get_perfumes_x_flankers_with_similar_accords_based_on_perfume_id,
    ],
)


# data_retriever_agent = base_agent(
#     name="data_retriever",
#     instructions=data_retriever_instructions,
#     functions=[transfer_to_analyst, retrieve_data_based_on_reference_perfume],
# )