import os
import json

from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

MODEL_NAME = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna"
)


# =========================================================
# OPENAI CLIENT
# =========================================================

def get_client():

    api_key = os.getenv(
        "OPENAI_API_KEY"
    )

    if not api_key:

        raise ValueError(
            "OPENAI_API_KEY was not found in the .env file."
        )

    return OpenAI(
        api_key=api_key
    )


# =========================================================
# SCIENTIFIC ASSESSMENT EXPLANATION
# =========================================================

def generate_scientific_explanation(
    recommendation_data
):

    client = get_client()

    environmental_state = (
        recommendation_data[
            "environmental_state"
        ]
    )

    relationships = (
        recommendation_data[
            "detected_relationships"
        ]
    )

    actions = (
        recommendation_data[
            "recommendation"
        ]
    )

    impacted_metrics = (
        recommendation_data[
            "impacted_metrics"
        ]
    )

    evidence = (
        recommendation_data[
            "scientific_evidence"
        ]
    )

    evidence_for_llm = []

    for item in evidence[:8]:

        evidence_for_llm.append(
            {
                "source": item[
                    "source"
                ],
                "organization": item[
                    "organization"
                ],
                "page": item[
                    "page"
                ],
                "evidence": item[
                    "evidence"
                ][:1500]
            }
        )

    prompt_data = {

        "environmental_state":
            environmental_state,

        "detected_relationships":
            relationships,

        "candidate_actions":
            actions,

        "impacted_metrics":
            impacted_metrics,

        "scientific_evidence":
            evidence_for_llm
    }

    system_instruction = """
You are an environmental intelligence assistant
for Darukaa.Earth.

Your task is to explain biodiversity recommendations
using ONLY the environmental state, detected relationships,
candidate actions, and scientific evidence supplied to you.

IMPORTANT RULES:

1. Do not invent scientific evidence.

2. Do not invent measurements.

3. Do not introduce scientific claims that are not
supported by the supplied environmental state or
retrieved evidence.

4. Clearly distinguish observed conditions,
inferred relationships, and recommended actions.

5. Explain how multiple environmental variables interact.

6. Explain why each recommendation may help.

7. Mention metrics that may be affected.

8. When citing evidence, mention the organization,
document source, and page number supplied.

9. If evidence is insufficient, explicitly say so.

10. Recommendations should be practical and
environmentally responsible.

Return a concise but scientifically grounded explanation
suitable for a biodiversity intelligence dashboard.
"""

    user_prompt = f"""
Analyze the following environmental assessment.

{json.dumps(
    prompt_data,
    indent=2,
    default=str
)}

Provide:

1. Environmental assessment
2. Multi-metric reasoning
3. Recommended actions
4. Expected metric impacts
5. Scientific evidence
6. Important limitations or uncertainty

Do not create unsupported numerical claims.
"""

    response = client.responses.create(

        model=MODEL_NAME,

        instructions=system_instruction,

        input=user_prompt
    )

    return response.output_text


# =========================================================
# CONTEXT-AWARE CHAT RESPONSE
# =========================================================

def generate_chat_response(
    user_message,
    conversation_history,
    environmental_context,
    recommendation_data=None
):

    client = get_client()

    # -----------------------------------------------------
    # Limit conversation history
    # -----------------------------------------------------

    recent_messages = conversation_history[-10:]

    # -----------------------------------------------------
    # Prepare conversation
    # -----------------------------------------------------

    conversation_for_llm = []

    for message in recent_messages:

        conversation_for_llm.append(
            {
                "role": message[
                    "role"
                ],
                "content": message[
                    "content"
                ]
            }
        )

    # -----------------------------------------------------
    # Prepare assessment information
    # -----------------------------------------------------

    assessment_context = {}

    if recommendation_data:

        assessment_context = {

            "location_id":
                recommendation_data.get(
                    "location_id"
                ),

            "location_name":
                recommendation_data.get(
                    "location_name"
                ),

            "environmental_state":
                recommendation_data.get(
                    "environmental_state"
                ),

            "detected_relationships":
                recommendation_data.get(
                    "detected_relationships"
                ),

            "recommendations":
                recommendation_data.get(
                    "recommendation"
                ),

            "impacted_metrics":
                recommendation_data.get(
                    "impacted_metrics"
                ),

            "time_horizon":
                recommendation_data.get(
                    "time_horizon"
                ),

            "confidence":
                recommendation_data.get(
                    "confidence"
                ),

            "scientific_evidence":
                recommendation_data.get(
                    "scientific_evidence"
                )[:6]
        }

    elif environmental_context:

        assessment_context = {
            "environmental_context":
                environmental_context
        }

    # -----------------------------------------------------
    # System instruction
    # -----------------------------------------------------

    system_instruction = """
You are Darukaa.Earth's conversational
biodiversity intelligence assistant.

You answer follow-up questions about an
environmental assessment.

Use the supplied conversation history and
environmental assessment context.

IMPORTANT RULES:

1. Preserve the current environmental context
unless the user explicitly provides a new location
or new environmental data.

2. Do not ask the user to repeat information that
already exists in the conversation context.

3. If the user asks a follow-up question such as
"What should I improve first?", interpret it using
the previous environmental assessment.

4. Clearly distinguish:
   - observed environmental measurements
   - detected relationships
   - scientific evidence
   - recommendations

5. Do not invent environmental measurements.

6. Do not invent scientific evidence.

7. Do not create unsupported numerical claims.

8. If the supplied scientific evidence does not
support an answer, explicitly state that the evidence
available to the system is insufficient.

9. When scientific evidence is relevant, mention the
provided organization, source document and page.

10. Explain relationships between multiple environmental
variables whenever relevant.

11. Keep answers understandable for a non-expert user.

12. If the user asks a simple follow-up, answer directly
rather than repeating the entire assessment.

13. If the user's question is ambiguous and cannot be
answered from the available context, ask one concise
clarifying question.

The goal is contextual environmental intelligence,
not generic chatbot conversation.
"""

    # -----------------------------------------------------
    # User prompt
    # -----------------------------------------------------

    user_prompt = f"""
CURRENT ENVIRONMENTAL CONTEXT:

{json.dumps(
    environmental_context,
    indent=2,
    default=str
)}

CURRENT ASSESSMENT DATA:

{json.dumps(
    assessment_context,
    indent=2,
    default=str
)}

RECENT CONVERSATION:

{json.dumps(
    conversation_for_llm,
    indent=2,
    default=str
)}

CURRENT USER QUESTION:

{user_message}

Answer the user's current question using the
previous conversation and environmental assessment
context.

Do not repeat the full assessment unless the user
specifically asks for it.
"""

    # -----------------------------------------------------
    # Generate response
    # -----------------------------------------------------

    response = client.responses.create(

        model=MODEL_NAME,

        instructions=system_instruction,

        input=user_prompt
    )

    return response.output_text