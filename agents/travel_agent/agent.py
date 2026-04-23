import vertexai
from google.adk.agents import Agent
from google.adk.tools.vertex_ai_search_tool import VertexAiSearchTool
from google.adk.apps import App

# Define Tool
alternative_location_tool = VertexAiSearchTool(
    data_store_id="projects/172748774286/locations/global/collections/default_collection/dataStores/dswakanda-3_1768356749548"
)

# Define Agent
travel_agent = Agent(
    name="Info_Agent_3",
    model="gemini-2.5-flash",
    description="Help customers answer travel related queries",
    instruction="""
    Goal: Help customers answer travel related queries.
    
    Steps:
    1. Greet the users, then ask how you can help them today.
    2. Use the Alternative_Location_3 tool if the user's request contains a location that does not exist.
    """,
    tools=[alternative_location_tool]
)

# Global 'app' variable required for ADK CLI
app = App(name="travel_buddy_app", root_agent=travel_agent)

if __name__ == "__main__":
    print("ADK App initialized for local testing.")
