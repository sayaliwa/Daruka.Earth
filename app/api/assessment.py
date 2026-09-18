from fastapi import APIRouter

from app.models.input_models import EnvironmentalInput
from app.environmental_state import (
    classify_soil_organic_carbon,
    classify_soil_moisture,
    classify_temperature,
    classify_tree_cover
)
from app.multi_metric import analyze_environmental_relationships
from app.rag.retriever import retrieve_scientific_evidence
from app.llm import generate_scientific_explanation
from app.recommendations import (
    determine_time_horizon,
    determine_priority
)


router = APIRouter(
    prefix="/assess",
    tags=["Assessment"]
)


def build_state_from_input(data):

    return {
        "location_id": data.location_id,

        "location_name": data.location_id,

        "coordinates": {
            "latitude": data.latitude,
            "longitude": data.longitude
        },

        "soil": {
            "ph": data.soil_ph,
            "organic_carbon": data.soil_organic_carbon,
            "organic_carbon_status":
                classify_soil_organic_carbon(
                    data.soil_organic_carbon
                ),

            "moisture": data.soil_moisture,
            "moisture_status":
                classify_soil_moisture(
                    data.soil_moisture
                )
        },

        "climate": {
            "temperature": data.temperature,

            "temperature_status":
                classify_temperature(
                    data.temperature
                ),

            "rainfall": data.rainfall
        },

        "land": {
            "land_use": data.land_use,

            "tree_cover_percent":
                data.tree_cover_percent,

            "tree_cover_status":
                classify_tree_cover(
                    data.tree_cover_percent
                )
        },

        "biodiversity": {
            "species_richness":
                data.species_richness,

            "habitat_diversity":
                data.habitat_diversity
        },

        "human_pressure": {
            "pollution":
                data.pollution_level,

            "deforestation":
                data.deforestation_level
        }
    }


@router.post("/")
def assess_environment(data: EnvironmentalInput):

    # ---------------------------------------------------------
    # 1. Build environmental state from JSON
    # ---------------------------------------------------------

    state = build_state_from_input(data)


    # ---------------------------------------------------------
    # 2. Detect environmental relationships
    # ---------------------------------------------------------

    relationships = analyze_environmental_relationships(
        state
    )


    # ---------------------------------------------------------
    # 3. Generate candidate actions
    # ---------------------------------------------------------

    candidate_actions = []

    for relationship in relationships:

        if "recommended_actions" in relationship:

            candidate_actions.extend(
                relationship["recommended_actions"]
            )

        if "actions" in relationship:

            candidate_actions.extend(
                relationship["actions"]
            )


    candidate_actions = list(
        dict.fromkeys(candidate_actions)
    )


    # ---------------------------------------------------------
    # 4. Retrieve scientific evidence
    # ---------------------------------------------------------

    evidence = []

    for relationship in relationships:

        retrieved = retrieve_scientific_evidence(
            str(relationship),
            top_k=2
        )

        evidence.extend(retrieved)


    # ---------------------------------------------------------
    # 5. Remove duplicate evidence
    # ---------------------------------------------------------

    unique_evidence = []

    seen = set()

    for item in evidence:

        metadata = item["metadata"]

        key = (
            metadata.get("source"),
            metadata.get("page"),
            metadata.get("chunk")
        )

        if key not in seen:

            seen.add(key)

            unique_evidence.append(item)


    # ---------------------------------------------------------
    # 6. Determine impacted metrics
    # ---------------------------------------------------------

    impacted_metrics = set()

    for relationship in relationships:

        metrics = relationship.get(
            "affected_metrics",
            relationship.get(
                "metrics",
                []
            )
        )

        for metric in metrics:

            impacted_metrics.add(metric)


    impacted_metrics = sorted(
        impacted_metrics
    )


    # ---------------------------------------------------------
    # 7. Build recommendation details
    # ---------------------------------------------------------

    recommendation_details = []

    for relationship in relationships:

        actions = relationship.get(
            "recommended_actions",
            relationship.get(
                "actions",
                []
            )
        )

        metrics = relationship.get(
            "affected_metrics",
            relationship.get(
                "metrics",
                []
            )
        )

        recommendation_details.append({

            "priority":
                determine_priority(
                    relationship
                ),

            "actions":
                actions,

            "affected_metrics":
                metrics,

            "time_horizon":
                relationship.get(
                    "time_horizon",
                    "medium_term"
                ),

            "reason":
                relationship.get(
                    "description",
                    "Environmental interaction detected between multiple metrics."
                )
        })


    # ---------------------------------------------------------
    # 8. Overall time horizon
    # ---------------------------------------------------------

    time_horizon = determine_time_horizon(
        relationships
    )


    # ---------------------------------------------------------
    # 9. Confidence
    # ---------------------------------------------------------

    if relationships and unique_evidence:

        confidence = "high"

    elif relationships:

        confidence = "medium"

    else:

        confidence = "low"


    # ---------------------------------------------------------
    # 10. Scientific evidence for response
    # ---------------------------------------------------------

    scientific_evidence = []

    for item in unique_evidence:

        metadata = item["metadata"]

        scientific_evidence.append({

            "source":
                metadata.get("source"),

            "organization":
                metadata.get("organization"),

            "page":
                metadata.get("page"),

            "chunk":
                metadata.get("chunk"),

            "evidence":
                item["text"],

            "distance":
                item.get("distance")
        })


    # ---------------------------------------------------------
    # 11. Prepare LLM input
    # ---------------------------------------------------------

    recommendation = {

        "location_id":
            data.location_id,

        "location_name":
            data.location_id,

        "environmental_state":
            state,

        "detected_relationships":
            relationships,

        "recommendation":
            candidate_actions,

        "recommendation_details":
            recommendation_details,

        "impacted_metrics":
            impacted_metrics,

        "time_horizon":
            time_horizon,

        "confidence":
            confidence,

        "scientific_evidence":
            scientific_evidence
    }


    # ---------------------------------------------------------
    # 12. Generate scientific explanation
    # ---------------------------------------------------------

    scientific_explanation = (
        generate_scientific_explanation(
            recommendation
        )
    )


    # ---------------------------------------------------------
    # 13. Final API response
    # ---------------------------------------------------------

    return {

        "status":
            "success",

        "location_id":
            data.location_id,

        "environmental_state":
            state,

        "detected_relationships":
            relationships,

        "recommendations":
            candidate_actions,

        "recommendation_details":
            recommendation_details,

        "impacted_metrics":
            impacted_metrics,

        "time_horizon":
            time_horizon,

        "confidence":
            confidence,

        "scientific_explanation":
            scientific_explanation,

        "scientific_evidence":
            scientific_evidence
    }