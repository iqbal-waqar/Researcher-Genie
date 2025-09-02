from backend.agents.graph import graph
from backend.agents.prompts import INITIAL_PROMPT
from backend.schemas.chat import ChatMessage, ChatResponse
from langchain_core.messages import HumanMessage, SystemMessage

class ChatInteractor:
    def process_chat(self, chat_message: ChatMessage) -> ChatResponse:
        chat_config = {"configurable": {"thread_id": chat_message.thread_id}}

        try:
            existing_state = graph.get_state(chat_config)
            if existing_state and existing_state.values.get("messages"):
                messages = [HumanMessage(content=chat_message.message)]
            else:
                messages = [
                    SystemMessage(content=INITIAL_PROMPT),
                    HumanMessage(content=chat_message.message)
                ]
        except:
            messages = [
                SystemMessage(content=INITIAL_PROMPT),
                HumanMessage(content=chat_message.message)
            ]
        
        input_data = {"messages": messages}
        
        try:
            response_stream = graph.stream(input_data, chat_config, stream_mode="values")
            
            final_response = ""
            all_responses = []
            
            for chunk in response_stream:
                if "messages" in chunk and chunk["messages"]:
                    for message in chunk["messages"]:
                        if hasattr(message, 'content') and message.content and type(message).__name__ == 'AIMessage':
                            if not message.content.startswith('<function=') and not 'function=' in message.content:
                                all_responses.append(message.content)
                                final_response = message.content
                        elif type(message).__name__ == 'ToolMessage' and hasattr(message, 'content') and message.content:
                            all_responses.append(message.content)
                            final_response = message.content
            
            if all_responses:
                tool_result = None
                ai_response = None
                
                for response in all_responses:
                    if any(marker in response for marker in [
                        "📚 Recent Papers", "## **Paper", "👥 **Authors:**", "📄 **Summary:**",
                        "Key Contributions:", "Methodology:", "Research Directions:",
                        "Selected Research Topics", "Paper Completed", "PDF Generated",
                        "✅ PDF Successfully Generated", "Research Paper Generated Successfully"
                    ]):
                        tool_result = response
                    else:
                        ai_response = response
                
                final_response = tool_result if tool_result else (ai_response or all_responses[-1])
            
            if not final_response:
                final_response = "I'm sorry, I couldn't process your request. Please try again."
                
        except Exception as e:
            final_response = "I encountered an error processing your request. Please try again."
        
        return ChatResponse(
            response=final_response,
            thread_id=chat_message.thread_id
        )