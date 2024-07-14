from .factory import ChatbotFactory

def generate_response(chatbot, message_content, thread_id):
    chatbot_class = ChatbotFactory.get_chatbot_class(chatbot.chatbot_type)
    chatbot_instance = chatbot_class(chatbot.to_dict())
    return chatbot_instance.generate_response(message_content, thread_id)