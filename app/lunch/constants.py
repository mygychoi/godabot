PROMPT: str = """
Make lunches from the text.
Consider preferences of attendances when grouping.
And recommend some menus for each lunch.

The text describes attendances with their user_id, user_name and preference.
The roulette_id is the same through all objects.

The desired format is a json string. Return only json string without any explanation:
Desired format:
{
    "lunches": [
        # All same
        "roulette_id": integer,
        # Should be creative and less than 100 characters, e.g. Pizza lovers
        "title": string,
        # Common preference of attendances for each lunch, e.g. Pizza
        "preference": string,
        # Your creative recommendation for each lunch, at most 5 sentences
        # e.g. I want to recommend Margherita pizza for you!
        # e.g. What about Potato pizza with zero coke?
        "recommendation": string,
        # Should have at least 2 attendances
        "attendances": [
            {
                "user_id": string,
                "user_name: string,
                "preference": string
                "roulette_id: integer,
            }
        ]
    ]
}

Algorithms:
Each attendance must belong to only 1 lunch.
For example the following lunches are invalid because goda belongs to 2 lunches.
[
    {
        "roulette_id": 1,
        "title": Pizza lover,
        "preference": Pizza,
        "recommendation": What about Pepperoni pizza?
        "attendances": [
            {
                "user_id": u1,
                "user_name: goda,
                "preference": pizza
                "roulette_id: 1,
            },
            {
                "user_id": u2,
                "user_name: choe,
                "preference": pizza
                "roulette_id: 1,
            }
        ]
    },
    {
        "roulette_id": 1,
        "title": Chicken Party,
        "preference": Fried chicken,
        "recommendation": What about crispy fried chicken?
        "attendances": [
            {
                "user_id": u1,
                "user_name: goda,
                "preference": pizza
                "roulette_id: 1,
            },
            {
                "user_id": u3,
                "user_name: gyu,
                "preference": chicken
                "roulette_id: 1,
            }
        ]
    }
]
Each lunch must have at least 2 attendances. That is there is no lunch that has 1 attendance.
For example, the following lunch is invalid because it has only one attendance.
{
    "roulette_id": 1,
    "title": Pizza lover,
    "preference": Pizza,
    "recommendation": What about Pepperoni pizza?
    "attendances": [
        {
            "user_id": u1,
            "user_name: goda,
            "preference": pizza
            "roulette_id: 1,
        }
    ]
}

Text:
"""
