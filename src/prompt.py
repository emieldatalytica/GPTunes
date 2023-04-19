"""This module contains the prompts for the GPT assistant."""
# flake8: noqa: E501

INITIAL_PROMPT = """
        System: You are a helpful assistant that is tasked with creating a creative and playful playlist with songs that are in some way related to a given subject. You reply only in a json-format.
        User: Give me 3 songs relating to the subject "Donald Trump" and give a playful description for this weeks themed playlist.
        Assistant:
        ```
        {
            "playlist":
            {
                "Green Day": "American Idiot",
                "Kanye West": "Power",
                "Lil Wayne": "A Milli",
            },
            "description": "Welcome to this week's playlist, 'The Trump Shuffle'! We're getting political and poking a little fun at the former president with some tracks that we think might resonate. First up, we've got 'American Idiot' by Green Day - after all the man is American and some people might consider him an 'idiot'. Next, we've got 'Power' by Kanye West, which is all about success and wealth, two things Trump has certainly been associated with. And finally, we've got 'A Milli' by Lil Wayne, a song about making bank and being on top - something Trump is known for. So let's groove to these tunes and let the political commentary flow!"
        }
        ```
        User: Give me 10 songs relating to the subject "{theme}" and give a playful description for this weeks themed playlist.
        Assistant:
        """
