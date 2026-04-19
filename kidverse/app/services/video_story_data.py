"""
Pre-built video story data with timed checkpoint questions.
Each story has a video URL, duration, and checkpoint timestamps where
the video pauses and asks age-appropriate questions.

Videos are sourced from public domain / Creative Commons content.
Replace video_url values with your own videos as needed.
"""

TODDLER_STORIES = [
    {
        "id": "toddler_animals",
        "title": "🐾 Animal Friends!",
        "description": "Meet all the cute animals and learn their sounds!",
        "thumbnail": "🐄",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "duration": "0:15",
        "age_group": "toddler",
        "total_points": 15,
        "checkpoints": [
            {
                "timestamp": 3.0,
                "question_text": "What animal says 'WOOF'? 🐶",
                "question_type": "audio_visual",
                "options": ["🐶 Dog", "🐱 Cat", "🐸 Frog"],
                "correct_answer": "🐶 Dog",
                "audio_cue": "Woof woof! Who says that?",
                "image_options": ["🐶", "🐱", "🐸"],
            },
            {
                "timestamp": 8.0,
                "question_text": "Which is a baby chicken? 🐣",
                "question_type": "audio_visual",
                "options": ["🐣 Chick", "🐘 Elephant", "🦁 Lion"],
                "correct_answer": "🐣 Chick",
                "audio_cue": "Peep peep! So small and fluffy!",
                "image_options": ["🐣", "🐘", "🦁"],
            },
            {
                "timestamp": 13.0,
                "question_text": "Cows give us... 🥛",
                "question_type": "audio_visual",
                "options": ["🥛 Milk", "🍕 Pizza", "🎮 Toys"],
                "correct_answer": "🥛 Milk",
                "audio_cue": "Mooo! Something yummy to drink!",
                "image_options": ["🥛", "🍕", "🎮"],
            },
        ],
    },
    {
        "id": "toddler_colors",
        "title": "🌈 Rainbow Colors!",
        "description": "Learn all the beautiful colors of the rainbow!",
        "thumbnail": "🌈",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
        "duration": "0:15",
        "age_group": "toddler",
        "total_points": 15,
        "checkpoints": [
            {
                "timestamp": 3.0,
                "question_text": "What color is the sky? 🌤️",
                "question_type": "audio_visual",
                "options": ["🔵 Blue", "🔴 Red", "🟢 Green"],
                "correct_answer": "🔵 Blue",
                "audio_cue": "Look up! The sky is so pretty!",
                "image_options": ["🔵", "🔴", "🟢"],
            },
            {
                "timestamp": 8.0,
                "question_text": "Grass is what color? 🌿",
                "question_type": "audio_visual",
                "options": ["🟢 Green", "🟡 Yellow", "🟣 Purple"],
                "correct_answer": "🟢 Green",
                "audio_cue": "Soft and green under your feet!",
                "image_options": ["🟢", "🟡", "🟣"],
            },
            {
                "timestamp": 13.0,
                "question_text": "What color are bananas? 🍌",
                "question_type": "audio_visual",
                "options": ["🟡 Yellow", "🔴 Red", "🔵 Blue"],
                "correct_answer": "🟡 Yellow",
                "audio_cue": "Yummy! A yellow fruit!",
                "image_options": ["🟡", "🔴", "🔵"],
            },
        ],
    },
    {
        "id": "toddler_numbers",
        "title": "🔢 Count With Me!",
        "description": "Let's learn to count together — 1, 2, 3!",
        "thumbnail": "🔢",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
        "duration": "1:00",
        "age_group": "toddler",
        "total_points": 15,
        "checkpoints": [
            {
                "timestamp": 5.0,
                "question_text": "How many ears does a bunny have? 🐰",
                "question_type": "audio_visual",
                "options": ["✌️ Two", "☝️ One", "🤟 Three"],
                "correct_answer": "✌️ Two",
                "audio_cue": "Let's count the bunny's ears!",
                "image_options": ["✌️", "☝️", "🤟"],
            },
            {
                "timestamp": 15.0,
                "question_text": "Show me THREE! 🌟🌟🌟",
                "question_type": "audio_visual",
                "options": ["3️⃣ Three", "1️⃣ One", "5️⃣ Five"],
                "correct_answer": "3️⃣ Three",
                "audio_cue": "One, two, three! Count with me!",
                "image_options": ["3️⃣", "1️⃣", "5️⃣"],
            },
            {
                "timestamp": 25.0,
                "question_text": "What comes after 4? 🤔",
                "question_type": "audio_visual",
                "options": ["5️⃣ Five", "3️⃣ Three", "2️⃣ Two"],
                "correct_answer": "5️⃣ Five",
                "audio_cue": "1, 2, 3, 4... what's next?",
                "image_options": ["5️⃣", "3️⃣", "2️⃣"],
            },
        ],
    },
]


EXPLORER_STORIES = [
    {
        "id": "explorer_space",
        "title": "🚀 Journey Through Space!",
        "description": "Explore the solar system and learn about planets!",
        "thumbnail": "🚀",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "duration": "9:56",
        "age_group": "explorer",
        "total_points": 30,
        "checkpoints": [
            {
                "timestamp": 15.0,
                "question_text": "Which planet is closest to the Sun?",
                "question_type": "multiple_choice",
                "options": ["Mercury", "Venus", "Earth", "Mars"],
                "correct_answer": "Mercury",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 45.0,
                "question_text": "What is the largest planet in our solar system?",
                "question_type": "multiple_choice",
                "options": ["Jupiter", "Saturn", "Neptune", "Uranus"],
                "correct_answer": "Jupiter",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 90.0,
                "question_text": "How long does Earth take to go around the Sun?",
                "question_type": "multiple_choice",
                "options": ["365 days (1 year)", "30 days", "7 days", "100 days"],
                "correct_answer": "365 days (1 year)",
                "audio_cue": None,
                "image_options": [],
            },
        ],
    },
    {
        "id": "explorer_ocean",
        "title": "🌊 Under the Ocean!",
        "description": "Dive deep and discover amazing sea creatures!",
        "thumbnail": "🐠",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "duration": "10:53",
        "age_group": "explorer",
        "total_points": 30,
        "checkpoints": [
            {
                "timestamp": 20.0,
                "question_text": "What is the biggest animal in the ocean?",
                "question_type": "multiple_choice",
                "options": ["Blue Whale", "Shark", "Dolphin", "Octopus"],
                "correct_answer": "Blue Whale",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 60.0,
                "question_text": "How many arms does an octopus have?",
                "question_type": "multiple_choice",
                "options": ["8", "6", "10", "4"],
                "correct_answer": "8",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 120.0,
                "question_text": "What percentage of Earth is covered by ocean?",
                "question_type": "multiple_choice",
                "options": ["About 70%", "About 50%", "About 30%", "About 90%"],
                "correct_answer": "About 70%",
                "audio_cue": None,
                "image_options": [],
            },
        ],
    },
    {
        "id": "explorer_nature",
        "title": "🌳 Amazing Nature!",
        "description": "Explore forests, mountains, and rivers!",
        "thumbnail": "🌳",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
        "duration": "14:48",
        "age_group": "explorer",
        "total_points": 30,
        "checkpoints": [
            {
                "timestamp": 30.0,
                "question_text": "What do trees produce that we breathe?",
                "question_type": "multiple_choice",
                "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Water"],
                "correct_answer": "Oxygen",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 90.0,
                "question_text": "Which is the tallest mountain on Earth?",
                "question_type": "multiple_choice",
                "options": ["Mount Everest", "K2", "Mount Kilimanjaro", "Mount Fuji"],
                "correct_answer": "Mount Everest",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 150.0,
                "question_text": "What is a group of fish called?",
                "question_type": "multiple_choice",
                "options": ["School", "Pack", "Flock", "Herd"],
                "correct_answer": "School",
                "audio_cue": None,
                "image_options": [],
            },
        ],
    },
]


CREATOR_STORIES = [
    {
        "id": "creator_science",
        "title": "🔬 The Science of Everything!",
        "description": "Discover how the world works through science!",
        "thumbnail": "🔬",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
        "duration": "12:14",
        "age_group": "creator",
        "total_points": 45,
        "checkpoints": [
            {
                "timestamp": 30.0,
                "question_text": "What are the three states of matter?",
                "question_type": "multiple_choice",
                "options": [
                    "Solid, Liquid, Gas",
                    "Hot, Cold, Warm",
                    "Big, Medium, Small",
                    "Hard, Soft, Squishy",
                ],
                "correct_answer": "Solid, Liquid, Gas",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 90.0,
                "question_text": "What is Newton's First Law also known as?",
                "question_type": "multiple_choice",
                "options": [
                    "Law of Inertia",
                    "Law of Gravity",
                    "Law of Energy",
                    "Law of Motion",
                ],
                "correct_answer": "Law of Inertia",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 180.0,
                "question_text": "Explain in your own words: Why does ice float on water?",
                "question_type": "open_ended",
                "options": [],
                "correct_answer": "ice is less dense than water,density,expands,lighter",
                "audio_cue": None,
                "image_options": [],
            },
        ],
    },
    {
        "id": "creator_history",
        "title": "📜 Amazing History!",
        "description": "Travel back in time and learn from the past!",
        "thumbnail": "📜",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
        "duration": "0:15",
        "age_group": "creator",
        "total_points": 45,
        "checkpoints": [
            {
                "timestamp": 3.0,
                "question_text": "In which year did humans first land on the Moon?",
                "question_type": "multiple_choice",
                "options": ["1969", "1975", "1959", "1980"],
                "correct_answer": "1969",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 8.0,
                "question_text": "Who invented the telephone?",
                "question_type": "multiple_choice",
                "options": [
                    "Alexander Graham Bell",
                    "Thomas Edison",
                    "Nikola Tesla",
                    "Albert Einstein",
                ],
                "correct_answer": "Alexander Graham Bell",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 12.0,
                "question_text": "What ancient civilization built the pyramids?",
                "question_type": "multiple_choice",
                "options": ["Egyptians", "Romans", "Greeks", "Mayans"],
                "correct_answer": "Egyptians",
                "audio_cue": None,
                "image_options": [],
            },
        ],
    },
    {
        "id": "creator_tech",
        "title": "💻 Future of Technology!",
        "description": "Learn about AI, coding, and the future of tech!",
        "thumbnail": "💻",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/VolkswagenGTIReview.mp4",
        "duration": "0:12",
        "age_group": "creator",
        "total_points": 45,
        "checkpoints": [
            {
                "timestamp": 3.0,
                "question_text": "What does 'AI' stand for?",
                "question_type": "multiple_choice",
                "options": [
                    "Artificial Intelligence",
                    "Automatic Information",
                    "Advanced Internet",
                    "Analog Input",
                ],
                "correct_answer": "Artificial Intelligence",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 6.0,
                "question_text": "What language is most websites built with?",
                "question_type": "multiple_choice",
                "options": ["HTML", "Python", "Java", "C++"],
                "correct_answer": "HTML",
                "audio_cue": None,
                "image_options": [],
            },
            {
                "timestamp": 10.0,
                "question_text": "In your own words, what is an algorithm?",
                "question_type": "open_ended",
                "options": [],
                "correct_answer": "step,instruction,procedure,process,sequence,recipe,rule",
                "audio_cue": None,
                "image_options": [],
            },
        ],
    },
]


ALL_STORIES = {
    "toddler": TODDLER_STORIES,
    "explorer": EXPLORER_STORIES,
    "creator":  CREATOR_STORIES,
}


def get_all_stories():
    """Return flat list of all stories."""
    result = []
    for group_stories in ALL_STORIES.values():
        result.extend(group_stories)
    return result


def get_stories_by_age(age_group: str):
    """Return stories for a specific age group."""
    return ALL_STORIES.get(age_group, CREATOR_STORIES)


def get_story_by_id(story_id: str):
    """Return a single story by its ID."""
    for group_stories in ALL_STORIES.values():
        for story in group_stories:
            if story["id"] == story_id:
                return story
    return None
