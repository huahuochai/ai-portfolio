# W3 生词表练习生成工具（升级版）
import csv
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "生词表.csv")
output_path = os.path.join(current_dir, "练习.txt")

def generate_exercises():
    try:
        hsk4_words = []
        pos_count = {}

        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['等级'] == 'HSK4':
                    hsk4_words.append((row['词语'], row['词性']))
                    pos = row['词性']
                    pos_count[pos] = pos_count.get(pos, 0) + 1

        print("--- HSK4 词汇词性统计 ---")
        # 作业1：使用了列表推导式来打印统计结果
        print(", ".join([f"{pos}: {count}个" for pos, count in pos_count.items()]))
        print("-------------------------")

        # 作业2扩展：生成填空题
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=== 填空题练习 ===\n")
            for word, pos in hsk4_words:
                # 将目标词挖空成下划线
                line = f"请填空：我们要学会____（{pos}）面对困难。\n"
                f.write(line)
            
            f.write("\n=== 造句练习 ===\n")
            for word, pos in hsk4_words:
                f.write(f"用 '{word}' 造一个句子。（{pos}）\n")
        
        print(f"✅ 成功！已生成填空题与造句，请查看：{output_path}")
        
    except FileNotFoundError:
        print("❌ 错误：找不到 生词表.csv。")

if __name__ == "__main__":
    generate_exercises()