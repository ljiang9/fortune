"""fortune —— 终端随机格言。

从内置精选格言库中随机抽取一条。全部为公有领域内容：
中文部分取自先秦典籍、唐宋诗词与传统谚语；英文部分取自
已故超过百年的作者（斯多葛学派、莎士比亚、富兰克林等）
或传统译文的自我转述。纯标准库，离线运行。
"""

import argparse
import json
import random
import sys

QUOTES = [
    # ---------------- 中文（传统典籍 / 谚语，公有领域） ----------------
    {"text": "学而时习之，不亦说乎。", "author": "《论语·学而》", "category": "中文"},
    {"text": "三人行，必有我师焉。择其善者而从之，其不善者而改之。", "author": "《论语·述而》", "category": "中文"},
    {"text": "己所不欲，勿施于人。", "author": "《论语·卫灵公》", "category": "中文"},
    {"text": "温故而知新，可以为师矣。", "author": "《论语·为政》", "category": "中文"},
    {"text": "学而不思则罔，思而不学则殆。", "author": "《论语·为政》", "category": "中文"},
    {"text": "知之者不如好之者，好之者不如乐之者。", "author": "《论语·雍也》", "category": "中文"},
    {"text": "工欲善其事，必先利其器。", "author": "《论语·卫灵公》", "category": "中文"},
    {"text": "不患人之不己知，患不知人也。", "author": "《论语·学而》", "category": "中文"},
    {"text": "道可道，非常道。", "author": "《道德经》", "category": "中文"},
    {"text": "千里之行，始于足下。", "author": "《道德经》", "category": "中文"},
    {"text": "上善若水，水善利万物而不争。", "author": "《道德经》", "category": "中文"},
    {"text": "知人者智，自知者明。胜人者有力，自胜者强。", "author": "《道德经》", "category": "中文"},
    {"text": "天生我材必有用，千金散尽还复来。", "author": "李白《将进酒》", "category": "中文"},
    {"text": "长风破浪会有时，直挂云帆济沧海。", "author": "李白《行路难》", "category": "中文"},
    {"text": "会当凌绝顶，一览众山小。", "author": "杜甫《望岳》", "category": "中文"},
    {"text": "读书破万卷，下笔如有神。", "author": "杜甫《奉赠韦左丞丈二十二韵》", "category": "中文"},
    {"text": "纸上得来终觉浅，绝知此事要躬行。", "author": "陆游《冬夜读书示子聿》", "category": "中文"},
    {"text": "山重水复疑无路，柳暗花明又一村。", "author": "陆游《游山西村》", "category": "中文"},
    {"text": "海内存知己，天涯若比邻。", "author": "王勃《送杜少府之任蜀州》", "category": "中文"},
    {"text": "莫等闲，白了少年头，空悲切。", "author": "岳飞《满江红》", "category": "中文"},
    {"text": "业精于勤，荒于嬉；行成于思，毁于随。", "author": "韩愈《进学解》", "category": "中文"},
    {"text": "书山有路勤为径，学海无涯苦作舟。", "author": "韩愈（传统归属）", "category": "中文"},
    {"text": "宝剑锋从磨砺出，梅花香自苦寒来。", "author": "传统谚语", "category": "中文"},
    {"text": "滴水穿石，非一日之功。", "author": "传统谚语", "category": "中文"},
    {"text": "绳锯木断，水滴石穿。", "author": "传统谚语", "category": "中文"},
    {"text": "不积跬步，无以至千里；不积小流，无以成江海。", "author": "《荀子·劝学》", "category": "中文"},
    {"text": "锲而不舍，金石可镂。", "author": "《荀子·劝学》", "category": "中文"},
    {"text": "生于忧患，死于安乐。", "author": "《孟子·告子下》", "category": "中文"},
    {"text": "天将降大任于是人也，必先苦其心志，劳其筋骨。", "author": "《孟子·告子下》", "category": "中文"},
    {"text": "路漫漫其修远兮，吾将上下而求索。", "author": "屈原《离骚》", "category": "中文"},
    # ---------------- English (public domain authors) ----------------
    {"text": "The impediment to action advances action. What stands in the way becomes the way.", "author": "Marcus Aurelius", "category": "en"},
    {"text": "You have power over your mind — not outside events. Realize this, and you will find strength.", "author": "Marcus Aurelius", "category": "en"},
    {"text": "Waste no more time arguing what a good man should be. Be one.", "author": "Marcus Aurelius", "category": "en"},
    {"text": "The soul becomes dyed with the color of its thoughts.", "author": "Marcus Aurelius", "category": "en"},
    {"text": "It is not that we have a short time to live, but that we waste a great deal of it.", "author": "Seneca", "category": "en"},
    {"text": "We suffer more often in imagination than in reality.", "author": "Seneca", "category": "en"},
    {"text": "Begin at once to live, and count each separate day as a separate life.", "author": "Seneca", "category": "en"},
    {"text": "No man is free who is not master of himself.", "author": "Epictetus", "category": "en"},
    {"text": "First say to yourself what you would be; and then do what you have to do.", "author": "Epictetus", "category": "en"},
    {"text": "It's not what happens to you, but how you react to it that matters.", "author": "Epictetus", "category": "en"},
    {"text": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.", "author": "Aristotle", "category": "en"},
    {"text": "Knowing yourself is the beginning of all wisdom.", "author": "Aristotle", "category": "en"},
    {"text": "Pleasure in the job puts perfection in the work.", "author": "Aristotle", "category": "en"},
    {"text": "Better than a thousand hollow words is one word that brings peace.", "author": "Buddha (Dhammapada)", "category": "en"},
    {"text": "All that we are arises with our thoughts. With our thoughts we make the world.", "author": "Buddha (Dhammapada)", "category": "en"},
    {"text": "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.", "author": "Ralph Waldo Emerson", "category": "en"},
    {"text": "Do not go where the path may lead, go instead where there is no path and leave a trail.", "author": "Ralph Waldo Emerson", "category": "en"},
    {"text": "Our greatest glory is not in never falling, but in rising every time we fall.", "author": "Confucius", "category": "en"},
    {"text": "It does not matter how slowly you go as long as you do not stop.", "author": "Confucius", "category": "en"},
    {"text": "Everything has beauty, but not everyone sees it.", "author": "Confucius", "category": "en"},
    {"text": "A journey of a thousand miles begins with a single step.", "author": "Laozi", "category": "en"},
    {"text": "He who knows others is wise; he who knows himself is enlightened.", "author": "Laozi", "category": "en"},
    {"text": "Nothing in the world is softer than water, yet nothing is better at overcoming the hard.", "author": "Laozi", "category": "en"},
    {"text": "I have not failed. I've just found 10,000 ways that won't work.", "author": "Thomas Edison", "category": "en"},
    {"text": "Genius is one percent inspiration and ninety-nine percent perspiration.", "author": "Thomas Edison", "category": "en"},
    {"text": "An investment in knowledge pays the best interest.", "author": "Benjamin Franklin", "category": "en"},
    {"text": "Well done is better than well said.", "author": "Benjamin Franklin", "category": "en"},
    {"text": "Either write something worth reading or do something worth writing.", "author": "Benjamin Franklin", "category": "en"},
    {"text": "This above all: to thine own self be true.", "author": "William Shakespeare", "category": "en"},
    {"text": "There is nothing either good or bad, but thinking makes it so.", "author": "William Shakespeare", "category": "en"},
]

CATEGORIES = sorted({q["category"] for q in QUOTES})


def pick(category=None, seed=None):
    """抽取一条格言。seed 给定时结果可复现。"""
    rng = random.Random(seed) if seed is not None else random.SystemRandom()
    pool = [q for q in QUOTES if category is None or q["category"] == category]
    if not pool:
        raise ValueError(f"没有这个分类：{category}（可用：{', '.join(CATEGORIES)}）")
    return rng.choice(pool)


def format_text(quote):
    return f"\n  “{quote['text']}”\n  —— {quote['author']}\n"


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="fortune",
        description="终端随机格言：从内置精选库中抽取一条（全部为公有领域内容）。",
    )
    parser.add_argument("--category", "-c", default=None,
                        help=f"按分类过滤（可用：{', '.join(CATEGORIES)}）")
    parser.add_argument("--list-categories", action="store_true",
                        help="列出所有可用分类")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    parser.add_argument("--seed", type=int, default=None,
                        help="随机种子（给定时结果可复现，仅用于演示/测试）")
    args = parser.parse_args(argv)

    if args.list_categories:
        for c in CATEGORIES:
            n = sum(1 for q in QUOTES if q["category"] == c)
            print(f"{c}（{n} 条）")
        return 0

    try:
        quote = pick(category=args.category, seed=args.seed)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(quote, ensure_ascii=False))
    else:
        print(format_text(quote), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
