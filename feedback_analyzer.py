import pandas as pd
from openai import OpenAI

client = OpenAI()

def analyze_single_feedback(text: str) -> dict:
    prompt = f"""
    Analyze the customer feedback below.

    Tasks:
    - Identify sentiment (Positive, Neutral, Negative)
    - Detect main topic
    - Assess urgency (Low, Medium, High)
    - Suggest a business action

    Feedback:
    {text}

    Respond in JSON with keys:
    sentiment, topic, urgency, action
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return eval(response.choices[0].message.content)


def analyze_feedback_batch(csv_file):
    df = pd.read_csv(csv_file)

    results = []
    for feedback in df["feedback"]:
        analysis = analyze_single_feedback(feedback)
        analysis["feedback"] = feedback
        results.append(analysis)

    result_df = pd.DataFrame(results)

    summary = {
        "total_feedback": len(result_df),
        "negative_feedback": (result_df["sentiment"] == "Negative").sum(),
        "high_urgency_cases": (result_df["urgency"] == "High").sum(),
        "top_topics": result_df["topic"].value_counts().head(3).to_dict()
    }

    return {
        "summary": summary,
        "detailed_results": result_df
    }
