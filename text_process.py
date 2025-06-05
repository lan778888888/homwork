import pandas as pd
import jieba
import re
from collections import Counter
import os

def load_stopwords(file_path='stopwords.txt'):
    """
    加载停用词文件
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            stopwords = set([line.strip() for line in f])
        print(f"成功加载停用词，共 {len(stopwords)} 个")
        return stopwords
    except FileNotFoundError:
        print(f"警告：找不到停用词文件 {file_path}，将不使用停用词过滤")
        return set()
    except Exception as e:
        print(f"警告：加载停用词文件时出错 - {e}，将不使用停用词过滤")
        return set()

def process_text():
    """
    对CSV文件进行文本去重和分词处理
    """
    try:
        # 显示当前工作目录
        print(f"当前工作目录：{os.getcwd()}")
        
        # 加载停用词
        stopwords = load_stopwords()
        
        # 检查文件是否存在
        csv_file = 'ci.csv'
        if not os.path.exists(csv_file):
            print(f"错误：文件 '{csv_file}' 不存在")
            return
            
        # 读取CSV文件
        print(f"正在读取文件：{csv_file}")
        df = pd.read_csv(csv_file)
        
        # 检查是否存在text列
        if 'text' not in df.columns:
            print("错误：CSV文件中不存在'text'列")
            print(f"可用的列：{', '.join(df.columns)}")
            return
        
        # 文本去重
        df = df.drop_duplicates(subset=['text'])
        print(f"去重后的文本数量：{len(df)}")
        
        # 文本预处理和分词
        all_words = []
        for text in df['text']:
            # 转换为字符串并清理文本
            text = str(text)
            text = re.sub(r'[^\w\s]', '', text)  # 移除标点符号
            
            # 使用jieba进行分词，但不使用默认词典
            words = jieba.cut(text, HMM=False)
            # 过滤停用词和空字符串
            words = [word for word in words if len(word.strip()) > 0 and word not in stopwords]
            all_words.extend(words)
        
        # 统计词频
        word_freq = Counter(all_words)
        
        # 输出前20个高频词
        print("\n词频统计（前20个）：")
        for word, freq in word_freq.most_common(20):
            print(f"{word}: {freq}")
        
        # 保存处理后的结果
        df.to_csv('ci_processed.csv', index=False, encoding='utf-8')
        print("\n处理后的文件已保存为 'ci_processed.csv'")
        
        # 保存词频统计结果
        with open('word_frequency.txt', 'w', encoding='utf-8') as f:
            for word, freq in word_freq.most_common():
                f.write(f"{word}\t{freq}\n")
        print("词频统计结果已保存为 'word_frequency.txt'")
        
    except FileNotFoundError as e:
        print(f"错误：找不到文件 - {str(e)}")
    except Exception as e:
        print(f"发生错误：{str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    process_text() 