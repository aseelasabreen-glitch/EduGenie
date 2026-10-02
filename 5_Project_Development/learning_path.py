from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    topic = topic.strip()
    if not topic:
        raise ValueError("Topic cannot be empty.")

    prompt = f"""Create a personalized learning path for:
{topic}

Organize it from beginner to advanced.

Include:
1. Prerequisites
2. Beginner concepts
3. Intermediate concepts
4. Advanced concepts
5. Practice activities or projects
6. Suggested resource types (videos, articles, books, documentation)
7. A simple weekly progression

Keep the recommendations practical and student-friendly.
Do not invent specific URLs. If mentioning a resource, identify the type or well-known resource name only when you are confident.
"""
    return generate_text(
        prompt,
        system_instruction="You are EduGenie, a learning-path advisor. Adapt the path to a beginner unless the user clearly specifies another level.",
        temperature=0.45,
        max_output_tokens=3000,
    )
