from app.environmental_state import build_environmental_state
from app.multi_metric import (
    analyze_environmental_relationships,
    generate_candidate_actions
)
from app.rag.retriever import retrieve_scientific_evidence
from app.llm import generate_scientific_explanation


def determine_time_horizon(relationships):
    """
    Determine the overall time horizon based on detected
    environmental relationships.
    """

    horizons = []

    for relationship in relationships:
        horizon = relationship.get("time_horizon")

        if horizon:
            horizons.append(horizon)

    if not horizons:
        return "medium_term"

    if "long" in horizons or "long_term" in horizons:
        return "long_term"

    if "short" in horizons or "short_term" in horizons:
        return "short_term"

    return "medium_term"


def determine_priority(relationship):
    """
    Assign a priority based on the number of environmental
    metrics affected by the relationship.
    """

    affected_metrics = relationship.get(
        "affected_metrics",
        relationship.get("metrics", [])
    )

    metric_count = len(affected_metrics)

    if metric_count >= 4:
        return "high"

    if metric_count >= 2:
        return "medium"

    return "low"


def build_recommendation(location_id, top_k=3):

    # ---------------------------------------------------------
    # 1. Build environmental state
    # ---------------------------------------------------------

    state = build_environmental_state(location_id)

    if state is None:
        return None

    # ---------------------------------------------------------
    # 2. Detect environmental relationships
    # ---------------------------------------------------------

    relationships = analyze_environmental_relationships(state)

    # ---------------------------------------------------------
    # 3. Generate candidate actions
    # ---------------------------------------------------------

    candidate_actions = generate_candidate_actions(
        relationships
    )

    # Remove duplicate actions
    candidate_actions = list(dict.fromkeys(candidate_actions))

    # ---------------------------------------------------------
    # 4. Retrieve scientific evidence
    # ---------------------------------------------------------

    evidence = []

    for relationship in relationships:

        query = str(relationship)

        retrieved = retrieve_scientific_evidence(
            query,
            top_k=top_k
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

        if "affected_metrics" in relationship:

            for metric in relationship["affected_metrics"]:
                impacted_metrics.add(metric)

        if "metrics" in relationship:

            for metric in relationship["metrics"]:
                impacted_metrics.add(metric)

    impacted_metrics = sorted(impacted_metrics)

    # ---------------------------------------------------------
    # 7. Build structured recommendation details
    # ---------------------------------------------------------

    recommendation_details = []

    for relationship in relationships:

        actions = relationship.get(
            "recommended_actions",
            relationship.get("actions", [])
        )

        affected_metrics_for_relationship = relationship.get(
            "affected_metrics",
            relationship.get("metrics", [])
        )

        recommendation_details.append({

            "priority": determine_priority(
                relationship
            ),

            "actions": actions,

            "affected_metrics": affected_metrics_for_relationship,

            "time_horizon": relationship.get(
                "time_horizon",
                "medium_term"
            ),

            "reason": relationship.get(
                "description",
                "Environmental interaction detected between multiple metrics."
            )
        })

    # ---------------------------------------------------------
    # 8. Determine overall time horizon
    # ---------------------------------------------------------

    time_horizon = determine_time_horizon(
        relationships
    )

    # ---------------------------------------------------------
    # 9. Estimate confidence
    # ---------------------------------------------------------

    if relationships and unique_evidence:

        confidence = "high"

    elif relationships:

        confidence = "medium"

    else:

        confidence = "low"

    # ---------------------------------------------------------
    # 10. Build final recommendation object
    # ---------------------------------------------------------

    recommendation = {

        "location_id": state["location_id"],

        "location_name": state["location_name"],

        "environmental_state": state,

        "detected_relationships": relationships,

        "recommendation": candidate_actions,

        "recommendation_details": recommendation_details,

        "impacted_metrics": impacted_metrics,

        "time_horizon": time_horizon,

        "confidence": confidence,

        "scientific_evidence": []
    }

    # ---------------------------------------------------------
    # 11. Add scientific evidence
    # ---------------------------------------------------------

    for item in unique_evidence:

        metadata = item["metadata"]

        recommendation["scientific_evidence"].append({

            "source": metadata.get("source"),

            "organization": metadata.get("organization"),

            "page": metadata.get("page"),

            "chunk": metadata.get("chunk"),

            "evidence": item["text"],

            "distance": item.get("distance")
        })

    # ---------------------------------------------------------
    # 12. Generate scientific explanation using LLM
    # ---------------------------------------------------------

    recommendation["scientific_explanation"] = (
        generate_scientific_explanation(
            recommendation
        )
    )

    return recommendation


if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("DARUKAA RECOMMENDATION ENGINE TEST")
    print("=" * 70)

    result = build_recommendation("LOC001")

    if result is None:

        print("Location not found.")

    else:

        print("\nLocation:")
        print(result["location_name"])

        print("\nDetected Relationships:")

        for relationship in result[
            "detected_relationships"
        ]:
            print(relationship)

        print("\nRecommendations:")

        for action in result["recommendation"]:
            print(f"- {action}")

        print("\nImpacted Metrics:")

        for metric in result[
            "impacted_metrics"
        ]:
            print(f"- {metric}")

        print("\nRecommendation Details:")

        for detail in result[
            "recommendation_details"
        ]:
            print(detail)

        print("\nTime Horizon:")
        print(result["time_horizon"])

        print("\nConfidence:")
        print(result["confidence"])

        print("\nScientific Explanation:")
        print(result["scientific_explanation"])

        print("\n")
        print("=" * 70)
        print("RECOMMENDATION ENGINE TEST COMPLETE")
        print("=" * 70)