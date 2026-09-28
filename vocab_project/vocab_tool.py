import csv

# 第一步：读
def read_csv(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

# 第二步：筛
def filter_words(data, level):
    filtered = []
    for row in data:
        if row['HSK等级'] == str(level): 
            filtered.append(row)
    return filtered

# 第三步：统
def count_pos(words):
    pos_count = {}
    for word in words:
        pos = word['词性'] 
        if pos in pos_count:
            pos_count[pos] += 1
        else:
            pos_count[pos] = 1
    return pos_count

# 第四步：写
def generate_exercises(words, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for word in words:
            sentence = f"用“{word['词汇']}”造一个句子。（{word['词性']}）\n"
            f.write(sentence)

if __name__ == "__main__":
    # 注意：这里的路径要确保你的data文件夹和代码在同一个目录下
    input_file = 'data/生词表.csv'  
    output_file = '练习.txt'        
    
    print("正在读取数据...")
    all_data = read_csv(input_file)
    print(f"总词汇 {len(all_data)} 个。")
    
    hsk4_words = filter_words(all_data, 4)
    print(f"其中 HSK4 词汇 {len(hsk4_words)} 个。")
    
    pos_stats = count_pos(hsk4_words)
    print(f"词性分布: {pos_stats}")
    
    generate_exercises(hsk4_words, output_file)
    print(f"已生成: {output_file}")
    print("-" * 20)
    
    # 打印文件内容看看
    with open(output_file, 'r', encoding='utf-8') as f:
        print(f.read())