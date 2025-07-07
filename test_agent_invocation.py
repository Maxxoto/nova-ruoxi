from backend.nova import RuoAgent
from langchain_core.messages import HumanMessage

def test_agent_message_format():
    """Test that agent handles message formatting correctly"""
    agent = RuoAgent()

    # Test simple message
    test_message = HumanMessage(content="Hello")
    response = agent.agent.invoke({"messages": [test_message]})

    # Verify response contains properly formatted messages
    assert "messages" in response
    assert len(response["messages"]) > 0
    assert hasattr(response["messages"][0], "content")

    print("✅ Message formatting test passed!")
    print(f"Response: {response['messages'][0].content}")

if __name__ == "__main__":
    test_agent_message_format()
