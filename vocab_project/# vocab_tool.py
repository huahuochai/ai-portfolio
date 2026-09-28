# vocab_tool.py
# 功能：读取单词，生成填空题，并强制写入 练习.txt

import json

# ============================================================
# 1. 生成填空题函数
# ============================================================
def make_blank(sentence, target_word):
    # 根据单词长度生成下划线（比如 apple 生成 _____）
    blanks = "_" * len(target_word)
    
    # 替换小写
    result = sentence.replace(target_word, blanks)
    # 替换首字母大写（处理句首单词）
    result = result.replace(target_word.capitalize(), blanks)
    return result


# ============================================================
# 2. 读取数据（这里我用了模拟数据，保证能跑通）
# ============================================================
def load_vocab_data():
    # 如果你有自己的单词文件，以后可以在这里替换成读取逻辑
    vocab_data = [
        {"word": "apple", "pos": "n.", "example": "I like to eat apple every day."},
        {"word": "run", "pos": "v.", "example": "I run to school in the morning."},
        {"word": "happy", "pos": "adj.", "example": "She is very happy today."},
        {"word": "orange", "pos": "n.", "example": "Orange is my favorite fruit."},
    ]
    return vocab_data


# ============================================================
# 3. 主流程
# ============================================================
def main():
    vocab_list = load_vocab_data()
    output_lines = []

    print("正在生成填空题...\n")

    for item in vocab_list:
        word = item["word"]
        example = item["example"]
        pos = item["pos"]

        # 生成填空题
        blank_sentence = make_blank(example, word)

        # 拼成最终输出的一行
        line = f"[{pos}] {blank_sentence}   (答案: {word})"
        output_lines.append(line)
        print(line)

    # ========================================================
    # 4. 强制写入 练习.txt（注意：文件名是 .txt，不是 .py）
    # ========================================================
    filename = "练习.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")

    print(f"\n✅ 已成功生成 {filename}！请去文件夹里查看。")


# ============================================================
# 5. 程序入口
# ============================================================
if __name__ == "__main__":
    main()