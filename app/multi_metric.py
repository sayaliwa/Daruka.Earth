from app.environmental_state import build_environmental_state


def analyze_environmental_relationships(state):
    """
    Analyze relationships between multiple environmental variables.
    """

    relationships = []

    soil = state["soil"]
    climate = state["climate"]
    land = state["land"]
    biodiversity = state["biodiversity"]
    human_pressure = state["human_pressure"]

    # --------------------------------------------------
    # Relationship 1: Soil carbon + soil moisture
    # --------------------------------------------------

    if (
        soil["organic_carbon_status"] == "low"
        and soil["moisture_status"] == "low"
    ):
        relationships.append({
            "type": "soil_water_relationship",
            "variables": [
                "soil_organic_carbon",
                "soil_moisture"
            ],
            "observation": (
                "Low soil organic carbon and low soil moisture "
                "occur together."
            ),
            "ecological_link": (
                "Soil condition and water availability should "
                "be considered together when assessing environmental stress."
            )
        })

    # --------------------------------------------------
    # Relationship 2: Temperature + soil moisture
    # --------------------------------------------------

    if (
        climate["temperature_status"] == "moderate"
        and soil["moisture_status"] == "low"
    ):
        relationships.append({
            "type": "climate_water_relationship",
            "variables": [
                "temperature",
                "soil_moisture"
            ],
            "observation": (
                "Soil moisture is low while temperature is relatively elevated."
            ),
            "ecological_link": (
                "Climate conditions and soil water availability "
                "can jointly influence plant and habitat conditions."
            )
        })

    # --------------------------------------------------
    # Relationship 3: Monoculture + habitat diversity
    # --------------------------------------------------

    if (
        land["land_use"] == "monoculture"
        and biodiversity["habitat_diversity"] == "low"
    ):
        relationships.append({
            "type": "land_biodiversity_relationship",
            "variables": [
                "land_use",
                "habitat_diversity"
            ],
            "observation": (
                "The location has monoculture land use and low habitat diversity."
            ),
            "ecological_link": (
                "A landscape dominated by a single land-use type "
                "may provide fewer habitat types."
            )
        })

    # --------------------------------------------------
    # Relationship 4: Low tree cover + low species richness
    # --------------------------------------------------

    if (
        land["tree_cover_status"] == "low"
        and biodiversity["species_richness"] == "low"
    ):
        relationships.append({
            "type": "vegetation_biodiversity_relationship",
            "variables": [
                "tree_cover_percent",
                "species_richness"
            ],
            "observation": (
                "Tree cover and species richness are both classified as low."
            ),
            "ecological_link": (
                "Vegetation structure can influence the availability "
                "of habitat and resources for organisms."
            )
        })

    # --------------------------------------------------
    # Relationship 5: Pollution + biodiversity
    # --------------------------------------------------

    if (
        human_pressure["pollution"] == "high"
        and biodiversity["species_richness"] == "low"
    ):
        relationships.append({
            "type": "pollution_biodiversity_relationship",
            "variables": [
                "pollution",
                "species_richness"
            ],
            "observation": (
                "High pollution pressure occurs together with low species richness."
            ),
            "ecological_link": (
                "Pollution can alter environmental conditions and "
                "create stress for organisms."
            )
        })

    return relationships


def generate_candidate_actions(relationships):
    """
    Generate candidate actions based on detected
    multi-metric environmental relationships.
    """

    actions = []

    for relationship in relationships:

        relationship_type = relationship["type"]

        if relationship_type == "soil_water_relationship":
            actions.extend([
                "Improve soil water retention",
                "Maintain vegetation or cover crops",
                "Increase organic matter through appropriate practices"
            ])

        elif relationship_type == "climate_water_relationship":
            actions.extend([
                "Maintain ground cover",
                "Improve soil water retention",
                "Use locally appropriate water-conservation practices"
            ])

        elif relationship_type == "land_biodiversity_relationship":
            actions.extend([
                "Increase habitat diversity",
                "Introduce suitable crop rotation",
                "Maintain habitat patches or field margins"
            ])

        elif relationship_type == "vegetation_biodiversity_relationship":
            actions.extend([
                "Protect existing vegetation",
                "Restore appropriate native vegetation",
                "Improve habitat structure"
            ])

        elif relationship_type == "pollution_biodiversity_relationship":
            actions.extend([
                "Identify major pollution sources",
                "Reduce relevant pollution inputs",
                "Monitor appropriate environmental quality indicators"
            ])

    # Remove duplicate actions
    return list(dict.fromkeys(actions))


def analyze_location(location_id):
    """
    Complete multi-metric analysis for a location.
    """

    state = build_environmental_state(location_id)

    if state is None:
        return None

    relationships = analyze_environmental_relationships(state)

    actions = generate_candidate_actions(relationships)

    return {
        "location_id": location_id,
        "location_name": state["location_name"],
        "relationships_detected": relationships,
        "candidate_actions": actions
    }


if __name__ == "__main__":

    result = analyze_location("LOC001")

    print("\nMulti-Metric Environmental Analysis")
    print("-----------------------------------")

    print(f"Location: {result['location_name']}")

    print("\nRelationships detected:")

    for relationship in result["relationships_detected"]:
        print(f"\n- {relationship['type']}")
        print(f"  Variables: {relationship['variables']}")
        print(f"  Observation: {relationship['observation']}")
        print(f"  Link: {relationship['ecological_link']}")

    print("\nCandidate actions:")

    for action in result["candidate_actions"]:
        print(f"- {action}")