import vertexai
from google.adk.agents import Agent
from google.adk.tools.vertex_ai_search_tool import VertexAiSearchTool
from google.adk.apps import AdkApp

# 1. Initialize Vertex AI with your project details from app.py
# vertexai.init(project="mydummy-1", location="us-central1")
vertexai.init()

# 2. Re-create the "Alternative Location 3" Data Store Tool
# We use the exact Data Store ID found in your JSON file
alternative_location_tool = VertexAiSearchTool(
    name="Alternative_Location_3",
    description="Use this tool if user's request contains a location that doesn't exist",
    data_store_id="projects/172748774286/locations/global/collections/default_collection/dataStores/dswakanda-3_1768356749548"
)

# 3. Re-create the "Info Agent 3" Playbook as an ADK Agent
# The instructions are mapped directly from your Playbook JSON
travel_agent = Agent(
    name="Info_Agent_3",
    model="gemini-2.5-flash",  # Recommended model for conversational agents
    goal="Help customers answer travel related queries",
    instruction="""
    Goal: Help customers answer travel related queries.
    
    Steps:
    1. Greet the users, then ask how you can help them today.
    2. Use the Alternative_Location_3 tool if the user's request contains a location that does not exist.
    """,
    tools=[alternative_location_tool]
)


# 4. Wrap the Agent in an AdkApp
# The 'app' variable is what the 'adk deploy' command looks for 
# when it inspects your file.
app = AdkApp(agents=[travel_agent])

# This allows you to deploy the agent via CI/CD
if __name__ == "__main__":
    # In a real CI/CD, you would use 'adk deploy' or this SDK method:
    # travel_agent.deploy() 
    # print("Agent configuration loaded successfully.")
    print("ADK App initialized with Info_Agent_3.")