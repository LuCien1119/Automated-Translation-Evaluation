import csv
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

prompt_template = """
Pretend you are a university-level instructor grading English-to-Chinese translation assignments for an undergraduate translation course. The source text is an abstract of a popular science article for teenagers.
Score each translation based on the following rubric from 1 (minimum) to 30 (maximum):

1. Understanding of the Source Text: The translation demonstrates sufficient comprehension of the original English text, accurately conveying its meaning without significant omissions, distortions, or misunderstandings.
2. Contextual Appropriateness: The translation is well-suited for the intended context, showing appropriate tone, style, and word choice in Chinese, ensuring natural readability and cultural relevance.

For the following translation, provide your response strictly in this format:

Score: <a number between 1 and 30>
Feedback: <your constructive feedback>

#Source Text#
Have you ever exclaimed “Wow!” when looking at the stars, fireworks, or rainbows? This is the magical feeling of awe. Awe makes us feel small in a big world full of mysteries. Awe makes us focus on things other than just ourselves. Could awe make children more caring and helpful to other people? We tested this idea in two experiments. We showed children movie clips that made them feel awe, happiness, or nothing special. We found that children who felt awe became more helpful and caring. They counted more food items for a food drive for refugees and were also more likely to give away their chocolate treats or museum tickets to refugees. They even had a special change in their heart rates and breathing patterns. This bodily change made them feel more relaxed and connected to others. Awe is an amazing force because it makes kids kinder!

#Translation#
{translation}
"""

input_file = "Translations.csv"
output_file = "Rubric_Graded.csv"

with open(input_file, "r", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    translations = [row[0] for row in reader]

with open(output_file, "w", encoding="utf-8", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Score", "Feedback"])

    for translation in translations:
        prompt = prompt_template.format(translation=translation)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        reply = response.choices[0].message.content.strip()

        score, feedback = "", ""

        for line in reply.splitlines():
            if line.strip().lower().startswith("score"):
                score = "".join([c for c in line if c.isdigit()])
            elif line.strip().lower().startswith("feedback"):
                feedback = line.split(":", 1)[-1].strip()

        if not feedback and "Feedback:" in reply:
            feedback = reply.split("Feedback:", 1)[-1].strip()

        writer.writerow([score, feedback])


print("评分已完成")
