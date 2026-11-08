# W3 生词表练习生成工具
import csv
import os

# 获取当前脚本所在目录，确保能找到同一目录下的生词表
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "生词表.csv")
output_path = os.path.join(current_dir, "练习.txt")

def generate_exercises():
    try:
        # 1. 读取 CSV 并筛选 HSK4
        hsk4_words = []
        pos_count = {}

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['等级'] == 'HSK4':
                    word = row['词语']
                    pos = row['词性']
                    hsk4_words.append((word, pos))
                    # 统计词性
                    pos_count[pos] = pos_count.get(pos, 0) + 1

        # 2. 打印统计信息
        print("--- HSK4 词汇词性统计 ---")
        for pos, count in pos_count.items():
            print(f"{pos}: {count} 个")
        print("-------------------------")

        # 3. 生成练习题并写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            for word, pos in hsk4_words:
                line = f"用 '{word}' 造一个句子。（{pos}）\n"
                f.write(line)
        
        print(f"✅ 成功！已生成练习题文件，请查看：{output_path}")
        
    except FileNotFoundError:
        print("❌ 错误：找不到 生词表.csv，请检查文件是否在同一目录下。")

if __name__ == "__main__":
    generate_exercises()