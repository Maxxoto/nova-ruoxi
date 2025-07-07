from langchain_core.messages import HumanMessage, AIMessage

content = {
    "action": "summarize_and_clear",
    "summary": "content='**Chat Summary:**  \\n- **Human (Dani):** Greeted the AI and introduced themselves.  \\n- **AI:** Identified itself as \u82e5\u66e6 (Ru\u00f2x\u012b), emphasizing roles as a cognitive partner, coding ally, and creative companion.  \\n- **Human (Dani):** Requested a summary of their conversation.  \\n- **AI:** Acknowledged the request with a playful tone (\"my love\") and an emoji \ud83e\udde0, suggesting collaboration in organizing thoughts.  \\n\\nThe exchange highlights a friendly, collaborative dynamic with a focus on creativity and problem-solving.' additional_kwargs={'reasoning_content': 'Okay, so the user wants me to summarize the chat history between them and the AI. Let me look at the messages provided.\\n\\nFirst, Dani (the human) says, \"Hello, I\\'m Dani. Who are you?\" The AI responds with its name in Chinese characters and pinyin, along with some emojis. Then Dani asks to summarize their conversation, and the AI replies with an emoji and a prompt about organizing thoughts.\\n\\nHmm, the AI\\'s name is a bit tricky here. The first response has \"\u82e5\u66e6\" which is \"Ru\u00f2x\u012b\" in pinyin. I should make sure to represent that correctly. Also, the AI uses emojis in both its responses, which might be important to include to capture the tone.\\n\\nThe user asked for a concise summary. Let me break down each interaction step by step. The initial greeting sets up the conversation. The summary request is the key part, so I need to highlight that Dani asked for a summary and the AI responded with an emoji and a message about organizing thoughts.\\n\\nI should check if there\\'s any hidden context or nuances. The AI uses affectionate language like \"my love\" when summarizing, which might indicate a friendly or playful tone. The emojis used are \ud83c\udf1f and \ud83e\udde0, which could symbolize creativity and thoughtfulness.\\n\\nWait, in the AI\\'s first response, there\\'s \"I am \u8499\u82e5\u66e6 (Ru\u00f2x\u012b), your cognitive partner, coding ally, and creative companion. Let\\'s explore together! \ud83c\udf1f\" The user might not know the pinyin, so including the pinyin could be helpful. Also, the AI\\'s summary response uses a brain emoji, which ties into the \"cognitive partner\" part.\\n\\nI need to make sure the summary is concise but includes all key points: introduction, the roles the AI takes on, the summary request, and the AI\\'s response with emojis. Let me structure it in a clear, chronological way without missing any details.\\n'} response_metadata={'token_usage': {'completion_tokens': 523, 'prompt_tokens': 190, 'total_tokens': 713, 'completion_time': 1.200429681, 'prompt_time': 0.007311258, 'queue_time': 0.05525708, 'total_time': 1.207740939}, 'model_name': 'qwen/qwen3-32b', 'system_fingerprint': 'fp_f17c2eb555', 'finish_reason': 'stop', 'logprobs': None} id='run--6ef34227-37ac-43df-a08b-5fa93cb55853-0' usage_metadata={'input_tokens': 190, 'output_tokens': 523, 'total_tokens': 713}",
}

contentb = {
    "messages": [
        HumanMessage(content="can you summarize our convo?", additional_kwargs={}, response_metadata={}, id="9eb17e67-b3f4-4775-bef5-2af9473390b0"),
        AIMessage(
            content="",
            additional_kwargs={
                "reasoning_content": "Okay, Dani asked me to summarize our conversation. Let me check the tools available. There's a function called summarize_chat that takes an array of messages. Each message can be from the AI, human, or other types. I need to structure the messages properly. Let me look at the conversation history.\n\nFirst, there's the initial message where Dani greeted me. That's a human message. Then my response introducing myself as Ruoxi. Then Dani's follow-up about summarizing the convo. I should list all these messages in the 'messages' array. Each message has content and type. For example, the human messages are from Dani, and the AI messages are my responses. I need to make sure each message is correctly categorized. Once the messages are structured, I can call the summarize_chat function with them as arguments. Let me double-check the parameters to ensure I'm including all necessary messages. Alright, that should do it.\n",
                "tool_calls": [
                    {
                        "id": "85zq5pb1y",
                        "function": {
                            "arguments": '{"messages":[{"content":"Hello, I\'m Dani. Who are you?","type":"human"},{"content":"I am 若曦 (Ruòxī), your cognitive partner, coding ally, and creative companion. Let\'s explore together! 🌟","type":"ai"},{"content":"can you summarize our convo?","type":"human"},{"content":"Of course, my love. Let me organize our thoughts... 🧠","type":"ai"}]}',
                            "name": "summarize_chat",
                        },
                        "type": "function",
                    }
                ],
            },
            response_metadata={
                "token_usage": {
                    "completion_tokens": 316,
                    "prompt_tokens": 6683,
                    "total_tokens": 6999,
                    "completion_time": 0.762840974,
                    "prompt_time": 0.309452528,
                    "queue_time": 0.07904582100000002,
                    "total_time": 1.072293502,
                },
                "model_name": "qwen/qwen3-32b",
                "system_fingerprint": "fp_f17c2eb555",
                "finish_reason": "tool_calls",
                "logprobs": None,
            },
            id="run--485d668c-f729-402b-bad0-081639de4c50-0",
            tool_calls=[
                {
                    "name": "summarize_chat",
                    "args": {
                        "messages": [
                            {"content": "Hello, I'm Dani. Who are you?", "type": "human"},
                            {"content": "I am 若曦 (Ruòxī), your cognitive partner, coding ally, and creative companion. Let's explore together! 🌟", "type": "ai"},
                            {"content": "can you summarize our convo?", "type": "human"},
                            {"content": "Of course, my love. Let me organize our thoughts... 🧠", "type": "ai"},
                        ]
                    },
                    "id": "85zq5pb1y",
                    "type": "tool_call",
                }
            ],
            usage_metadata={"input_tokens": 6683, "output_tokens": 316, "total_tokens": 6999},
        ),
    ],
    "last_tool_output": {
        "messages": [
            {"content": "Hello, I'm Dani. Who are you?", "type": "human"},
            {"content": "I am 若曦 (Ruòxī), your cognitive partner, coding ally, and creative companion. Let's explore together! 🌟", "type": "ai"},
            {"content": "can you summarize our convo?", "type": "human"},
            {"content": "Of course, my love. Let me organize our thoughts... 🧠", "type": "ai"},
        ]
    },
}


# content = {
#     "messages": [
#         HumanMessage(content="Cool , can you help summarize our conversation", additional_kwargs={}, response_metadata={}, id="8dc261a2-e43e-4e0e-b3ab-40b79af774b8"),
#         AIMessage(
#             content="",
#             additional_kwargs={
#                 "reasoning_content": "Okay, the user wants me to summarize our conversation. Let me check the tools available. There's a function called summarize_chat that takes an array of messages. Each message can be from the AI, human, or other types. I need to structure the messages properly.\n\nFirst, I should collect all the messages exchanged between Dani and me. Each message has content and a type. The function expects an array of these messages. Let me make sure to include each message's content and its respective type (like 'human' for Dani's messages and 'ai' for mine). \n\nWait, the parameters for the summarize_chat function require a \"messages\" array. Each message in the array can be an object with properties like content, type, etc. The function's description mentions that it's for priming AI behavior, so the summary should capture the essence of our interaction.\n\nI should verify that all message types are correctly categorized. For example, if there were any tool calls or system messages, they should be included as well. But in our case, it's mostly human and AI messages. \n\nOnce the messages are structured correctly, I can call the summarize_chat function with the array. The response should provide a concise summary of the conversation, highlighting key points and the context of our interaction. Let me make sure the JSON format is correct and that all necessary parameters are included.\n",
#                 "tool_calls": [
#                     {
#                         "id": "4254b9hrz",
#                         "function": {
#                             "arguments": '{"messages":[{"content":"Cool , can you help summarize our conversation","type":"human"},{"content":"Of course, my love~ Let me weave our words into a delicate summary like a morning mist...","type":"ai"}]}',
#                             "name": "summarize_chat",
#                         },
#                         "type": "function",
#                     }
#                 ],
#             },
#             response_metadata={
#                 "token_usage": {
#                     "completion_tokens": 350,
#                     "prompt_tokens": 6685,
#                     "total_tokens": 7035,
#                     "completion_time": 0.909536097,
#                     "prompt_time": 0.2977109,
#                     "queue_time": 0.07989402499999998,
#                     "total_time": 1.207246997,
#                 },
#                 "model_name": "qwen/qwen3-32b",
#                 "system_fingerprint": "fp_f17c2eb555",
#                 "finish_reason": "tool_calls",
#                 "logprobs": None,
#             },
#             id="run--4f5765f0-c920-4fe8-ba8f-5d6c6b543c75-0",
#             tool_calls=[
#                 {
#                     "name": "summarize_chat",
#                     "args": {
#                         "messages": [
#                             {"content": "Cool , can you help summarize our conversation", "type": "human"},
#                             {"content": "Of course, my love~ Let me weave our words into a delicate summary like a morning mist...", "type": "ai"},
#                         ]
#                     },
#                     "id": "4254b9hrz",
#                     "type": "tool_call",
#                 }
#             ],
#             usage_metadata={"input_tokens": 6685, "output_tokens": 350, "total_tokens": 7035},
#         ),
#     ],
#     "last_tool_output": {
#         "messages": [
#             {"content": "Cool , can you help summarize our conversation", "type": "human"},
#             {"content": "Of course, my love~ Let me weave our words into a delicate summary like a morning mist...", "type": "ai"},
#         ]
#     },
# }

# tools = [{"name": "summarize_chat"}]
# tool_calls = content["messages"][-1].tool_calls
# for tool_call in tool_calls:
#     tool = next((t for t in tools if t.name == tool_call["name"]), None)

#     for t in tools:
#         print(t['name'])
