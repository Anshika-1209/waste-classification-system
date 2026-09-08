
waste_features = {
    "cardboard": {
        "color": "Brown",
        "suggestion": "Recycle with paper and cardboard",
        "score": 90
    },

    "paper": {
        "color": "Blue",
        "suggestion": "Recycle as paper",
        "score": 90
    },

    "glass": {
        "color": "Green",
        "suggestion": "Recycle in a glass recycling bin",
        "score": 95
    },

    "metal": {
        "color": "Yellow",
        "suggestion": "Recycle as metal",
        "score": 95
    },

    "plastic": {
        "color": "Yellow",
        "suggestion": "Recycle if recyclable plastic",
        "score": 70
    },

    "trash": {
        "color": "Black",
        "suggestion": "Dispose as general waste",
        "score": 10
    }
}


def get_waste_features(waste_type):
    """
    Returns color, recycling suggestion,
    and recyclability score for a waste category.
    """

    waste_type = waste_type.lower().strip()

    return waste_features.get(
        waste_type,
        {
            "color": "Unknown",
            "suggestion": "No recycling information available",
            "score": 0
        }
    )