from app.conversation.memory import ConversationMemory

from app.recommendations import (
    build_recommendation
)

from app.llm import (
    generate_chat_response
)


class BiodiversityChat:

    def __init__(self):

        self.memory = ConversationMemory()

    # =====================================================
    # PROCESS MESSAGE
    # =====================================================

    def process_message(
        self,
        message,
        location_id=None
    ):

        # -------------------------------------------------
        # Store user message
        # -------------------------------------------------

        self.memory.add_message(
            "user",
            message
        )

        # -------------------------------------------------
        # Check previous environmental context
        # -------------------------------------------------

        previous_context = (
            self.memory.get_environmental_context()
        )

        # -------------------------------------------------
        # Reuse previous location
        # -------------------------------------------------

        if (
            location_id is None
            and previous_context
        ):

            location_id = previous_context.get(
                "location_id"
            )

        # -------------------------------------------------
        # No location + no previous context
        # -------------------------------------------------

        if location_id is None:

            response = (
                "I can help assess the environmental "
                "and biodiversity conditions, but I "
                "need a location first. Please provide "
                "a location such as LOC001."
            )

            self.memory.add_message(
                "assistant",
                response
            )

            return {

                "status":
                    "needs_clarification",

                "message":
                    response,

                "conversation_context":
                    self.memory.get_context()
            }

        # -------------------------------------------------
        # Build assessment
        # -------------------------------------------------

        recommendation = (
            build_recommendation(
                location_id
            )
        )

        # -------------------------------------------------
        # Location not found
        # -------------------------------------------------

        if recommendation is None:

            response = (
                f"I could not find environmental "
                f"data for location {location_id}. "
                "Please provide a valid location ID."
            )

            self.memory.add_message(
                "assistant",
                response
            )

            return {

                "status":
                    "location_not_found",

                "message":
                    response,

                "conversation_context":
                    self.memory.get_context()
            }

        # -------------------------------------------------
        # Store environmental context
        # -------------------------------------------------

        self.memory.set_environmental_context(
            recommendation[
                "environmental_state"
            ]
        )

        # -------------------------------------------------
        # Generate context-aware response
        # -------------------------------------------------

        response = generate_chat_response(

            user_message=message,

            conversation_history=
                self.memory.get_messages(),

            environmental_context=
                self.memory.get_environmental_context(),

            recommendation_data=
                recommendation
        )

        # -------------------------------------------------
        # Store assistant response
        # -------------------------------------------------

        self.memory.add_message(
            "assistant",
            response
        )

        # -------------------------------------------------
        # Return result
        # -------------------------------------------------

        return {

            "status":
                "success",

            "message":
                response,

            "location":
                recommendation[
                    "location_name"
                ],

            "recommendation":
                recommendation[
                    "recommendation"
                ],

            "impacted_metrics":
                recommendation[
                    "impacted_metrics"
                ],

            "time_horizon":
                recommendation[
                    "time_horizon"
                ],

            "confidence":
                recommendation[
                    "confidence"
                ],

            "scientific_evidence":
                recommendation[
                    "scientific_evidence"
                ],

            "environmental_context":
                self.memory.get_environmental_context(),

            "conversation_context":
                self.memory.get_context()
        }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    chatbot = BiodiversityChat()

    print("\n===================================")
    print("CONTEXT-AWARE CHAT TEST")
    print("===================================")

    # -----------------------------------------------------
    # FIRST QUESTION
    # -----------------------------------------------------

    first = chatbot.process_message(

        message=(
            "What is the biodiversity "
            "condition?"
        ),

        location_id="LOC001"
    )

    print("\nFIRST QUESTION")
    print("----------------")

    print(first["message"])

    # -----------------------------------------------------
    # FOLLOW-UP QUESTION
    # -----------------------------------------------------

    second = chatbot.process_message(

        message=(
            "What should I improve first?"
        )
    )

    print("\nFOLLOW-UP QUESTION")
    print("-------------------")

    print(second["message"])

    # -----------------------------------------------------
    # THIRD QUESTION
    # -----------------------------------------------------

    third = chatbot.process_message(

        message=(
            "Why is soil moisture important?"
        )
    )

    print("\nSECOND FOLLOW-UP")
    print("------------------")

    print(third["message"])

    # -----------------------------------------------------
    # MEMORY
    # -----------------------------------------------------

    print("\nCONVERSATION LENGTH")
    print("-------------------")

    print(
        len(
            chatbot.memory.get_messages()
        )
    )

    print("\nCHAT TEST COMPLETE")