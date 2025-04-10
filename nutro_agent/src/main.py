from langchain.agents import initialize_agent, Tool
from langchain.tools import tool
from langchain_gigachat.chat_models import GigaChat
from settings import settings  # Import the settings module
from pydantic import ValidationError
from schemes.schemes import MenuParams
import json


@tool
def generate_menu_tool(params: str) -> str:
    """
    Generates a menu based on user parameters provided in JSON format.
    Expected JSON keys: gender, weight, age, activity, complexity, period, portions.
    """
    try:
        # Parse and validate the JSON input using Pydantic
        user_params = MenuParams.model_validate_json(params)

        # Generate a mock menu (replace this with actual logic)
        menu = []
        for day in range(1, user_params.period + 1):
            menu.append(
                {
                    "day": day,
                    "meals": [
                        {
                            "meal": "Breakfast",
                            "dish": f"{user_params.complexity.capitalize()} Pancakes",
                        },
                        {
                            "meal": "Lunch",
                            "dish": f"{user_params.complexity.capitalize()} Salad",
                        },
                        {
                            "meal": "Dinner",
                            "dish": f"{user_params.complexity.capitalize()} Pasta",
                        },
                    ],
                    "portions": user_params.portions,
                }
            )

        return json.dumps(
            {
                "gender": user_params.gender,
                "weight": user_params.weight,
                "age": user_params.age,
                "activity": user_params.activity,
                "menu": menu,
            },
            indent=4,
        )
    except ValidationError as e:
        return f"Invalid input: {e.json()}"


# Initialize the tools
tools = [
    Tool(
        name="GenerateMenu",
        func=generate_menu_tool,
        description="Generates a menu based on user parameters in JSON format.",
    )
]

# Initialize the language model using settings
llm = GigaChat(
    credentials=settings.gigachat_credentials,
    scope=settings.gigachat_scope,
    model=settings.gigachat_model,
    verify_ssl_certs=settings.verify_ssl_certs,
)

# Initialize the agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Run the agent
if __name__ == "__main__":
    print("Nutro AI Agent is running...")
    # Example JSON input for menu generation
    example_input = json.dumps(
        {
            "gender": "male",
            "weight": 70,
            "age": 30,
            "activity": "moderate",
            "complexity": "medium",
            "period": 3,
            "portions": 2,
        }
    )
    response = agent.run(f"Generate a menu with these parameters: {example_input}")
    print(response)
