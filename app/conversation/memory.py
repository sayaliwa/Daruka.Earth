class ConversationMemory:

    def __init__(self):
        self.messages = []
        self.environmental_context = {}

    def add_message(self, role, content):

        self.messages.append(
            {
                "role": role,
                "content": content
            }
        )

    def set_environmental_context(self, context):

        self.environmental_context = context

    def get_messages(self):

        return self.messages

    def get_environmental_context(self):

        return self.environmental_context

    def get_context(self):

        return {
            "conversation": self.messages,
            "environmental_context":
                self.environmental_context
        }

    def clear(self):

        self.messages = []
        self.environmental_context = {}

if __name__ == "__main__":

    memory = ConversationMemory()

    memory.add_message(
        "user",
        "What is the biodiversity condition?"
    )

    memory.add_message(
        "assistant",
        "The assessment indicates several environmental pressures."
    )

    memory.set_environmental_context(
        {
            "location_id": "LOC001",
            "location_name": "Nagpur Sample"
        }
    )

    print("\nConversation Memory Test")
    print("=======================")

    print("\nMessages:")

    for message in memory.get_messages():
        print(message)

    print("\nEnvironmental Context:")

    print(
        memory.get_environmental_context()
    )

    print("\nComplete Context:")

    print(
        memory.get_context()
    )        