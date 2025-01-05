from swarm import Swarm
from swarm.repl import run_demo_loop
from dotenv import load_dotenv
from src.service.agents import (
    triage_agent,
    expert_agent,
    researcher_agent,
    analyst_agent,
)

load_dotenv()
client = Swarm()
print("Swarm initialized")

# Conversation
print("Starting conversation...")
print("How can we help you curate your perfect fragrance vibe?")
run_demo_loop(triage_agent, stream=True, debug=True)
