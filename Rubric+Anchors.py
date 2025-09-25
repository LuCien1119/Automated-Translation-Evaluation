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

#Prescored Translations#
High Score (26-30):
当你看到点点繁星、绚丽烟花、缤纷彩虹，会不会大呼一声“哇噻”？这种神奇的感觉就是震撼感。震撼感让我们在浩瀚莫测的世界中体会到自己是多么渺小；震撼感还让我们不仅关注自身，也关心身边的一切。那么，震撼感可以让小朋友变得更友善、更乐于助人吗？我们通过两个实验来检验这个想法。我们给小朋友播放几段视频，分别产生震撼、开心或平静的情绪。实验发现：感到震撼的小朋友变得更友善、更乐于助人。他们在公益活动中表现得更积极，让难民获得更多食物；他们也更愿意把参与活动所得的奖励（巧克力和博物馆门票）送给难民。实验还发现他们的心率和呼吸节奏有特别的变化。这些身心变化让他们更放松、更容易共情他人。由此可见，震撼感是一股神奇的力量，让小朋友变得更善良。
Upper Medium Score (21-25):
你有沒有在看到星星、煙花或彩虹時大喊過「哇」？ 這就是敬畏的神奇感覺！ 在這個充滿神秘的大世界里，敬畏讓我們感到自己很渺小，也讓我們關注別人。敬畏是否能讓孩子更加关爱他人、樂於助人呢？我們做了兩個有趣的實驗來找答案。 我們讓孩子們看一些電影片段，有的讓他們敬畏，有的讓他們開心，還有的沒什麼特別感覺。 結果顯示，感到敬畏的孩子變得更樂於助人！ 他們為難民準備了更多食物，還願意把自己的巧克力和博物館門票送給難民。 甚至他們的心跳和呼吸也發生了變化，這些變化讓他們更放鬆，更容易和別人交流。 敬畏真是一種神奇的力量，它讓孩子們變得更善良！ 
Lower Medium Score (16-20):
你是否曾在仰望星空、欣賞煙花或彩虹時驚呼「哇！」？這正是敬畏所帶來的的神奇感受。敬畏讓我們在這個充滿神秘的大千世界中體會到自己的渺小，並促使我們更關注自身以外的事物。敬畏是否能促使孩子們更加關心他人、樂於助人？我們在兩個實驗中測試了這個觀點。我們向孩子們播放了能引發敬畏、幸福或無特別感受的電影片段。我們發現，感到敬畏的孩子變得更樂於助人和有關懷心。他們在為難民的食物捐贈活動中清點了更多的食品，並更願意將巧克力或博物館門票贈予難民。甚至他們的心率和呼吸模式也發生了特殊變化。這種生理變化使他們感到更加放鬆，對他人的連結感也隨之增強。敬畏是一種奇妙的力量，因為它能讓孩子們變得更加善良！
Low Score (11-15):
你看著星空，煙花和彩虹的時候會不會驚歎道“哇！”？這就是心懷讚歎的魔力。讚歎使我們在廣大又充滿疑團的世界裡感到渺小，也使我們得以專注於自己。讚歎可以令孩子更願意關心和幫助別人嗎？我們做了兩個實驗來證實這個理論。實驗內容是讓孩子觀看一些電影片段，這些片段會讓他們感到讚歎，快樂，或者無感。結果發現，感到讚歎的孩子比其他孩子更樂於助人。在難民食品募捐活動中，他們給難民更多食物，也更願意和他們分享自己的巧克力零食或博物館門票。甚至他們的心率和呼吸規律都有所變化。這些變化能讓孩子們放鬆並和其他人產生聯繫。心懷讚歎是一種神奇的魔力，能讓孩子變得更善良！

For the following translation, learn from the rubrics and prescored translations above, and then provide your response strictly in this format:

Score: <a number between 1 and 30>
Feedback: <your constructive feedback>

#Source Text#
Have you ever exclaimed “Wow!” when looking at the stars, fireworks, or rainbows? This is the magical feeling of awe. Awe makes us feel small in a big world full of mysteries. Awe makes us focus on things other than just ourselves. Could awe make children more caring and helpful to other people? We tested this idea in two experiments. We showed children movie clips that made them feel awe, happiness, or nothing special. We found that children who felt awe became more helpful and caring. They counted more food items for a food drive for refugees and were also more likely to give away their chocolate treats or museum tickets to refugees. They even had a special change in their heart rates and breathing patterns. This bodily change made them feel more relaxed and connected to others. Awe is an amazing force because it makes kids kinder!

#Translation#
{translation}

"""

input_file = "Translations.csv"
output_file = "Rubric+Anchors_Graded.csv"

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
