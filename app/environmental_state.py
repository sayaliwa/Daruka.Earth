from app.data_loader import get_location


def classify_soil_organic_carbon(value):
    if value < 0.5:
        return "low"
    elif value < 1.0:
        return "medium"
    else:
        return "high"


def classify_soil_moisture(value):
    if value < 15:
        return "low"
    elif value < 25:
        return "medium"
    else:
        return "high"


def classify_temperature(value):
    if value > 35:
        return "high"
    elif value >= 25:
        return "moderate"
    else:
        return "low"


def classify_tree_cover(value):
    if value < 10:
        return "low"
    elif value < 40:
        return "medium"
    else:
        return "high"


def build_environmental_state(location_id):
    """
    Convert raw environmental measurements
    into a structured environmental state.
    """

    location = get_location(location_id)

    if location is None:
        return None

    state = {
        "location_id": location["location_id"],
        "location_name": location["location_name"],

        "soil": {
            "ph": location["soil_ph"],
            "organic_carbon": location["soil_organic_carbon"],
            "organic_carbon_status": classify_soil_organic_carbon(
                location["soil_organic_carbon"]
            ),
            "moisture": location["soil_moisture"],
            "moisture_status": classify_soil_moisture(
                location["soil_moisture"]
            )
        },

        "climate": {
            "temperature": location["temperature"],
            "temperature_status": classify_temperature(
                location["temperature"]
            ),
            "rainfall": location["rainfall"]
        },

        "land": {
            "land_use": location["land_use"],
            "tree_cover_percent": location["tree_cover_percent"],
            "tree_cover_status": classify_tree_cover(
                location["tree_cover_percent"]
            )
        },

        "biodiversity": {
            "species_richness": location["species_richness"],
            "habitat_diversity": location["habitat_diversity"]
        },

        "human_pressure": {
            "pollution": location["pollution_level"],
            "deforestation": location["deforestation_level"]
        }
    }

    return state


if __name__ == "__main__":

    location_id = "LOC001"

    environmental_state = build_environmental_state(location_id)

    print("\nEnvironmental State")
    print("-------------------")

    print(environmental_state)