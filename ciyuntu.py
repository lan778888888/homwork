import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import numpy as np
import re
from PIL import Image

# ----------------------------
# 用户配置区域
# ----------------------------
CSV_FILE = 'ci.csv'          # CSV 文件路径
TEXT_COLUMN = 'text'           # 文本列名称
OUTPUT_FILE = 'wordcloud.png'  # 输出图片路径（设为 None 则不保存）
MASK_IMAGE = None              # 自定义形状图片路径（设为 None 则使用默认矩形）
COLORMAP = 'viridis'           # 颜色主题（seaborn 调色板名称）
BACKGROUND_COLOR = 'white'     # 背景颜色
MAX_WORDS = 200                # 最大词数
STOPWORDS_SET = STOPWORDS      # 停用词集合（可自定义）
FONT_PATH = 'C:/Windows/Fonts/simhei.ttf'  # 黑体字体路径
# ----------------------------

def generate_wordcloud():
    """从 CSV 文件生成词云图，支持自定义形状和颜色"""
    try:
        # 读取 CSV 文件
        df = pd.read_csv(CSV_FILE)
        
        # 检查列是否存在
        if TEXT_COLUMN not in df.columns:
            print(f"错误: CSV 文件中不存在列 '{TEXT_COLUMN}'")
            print(f"可用列: {', '.join(df.columns)}")
            return
        
        # 合并所有文本
        text = ' '.join(df[TEXT_COLUMN].astype(str).dropna().tolist())
        
        # 文本预处理
        text = re.sub(r'[^\w\s]', '', text)  # 移除标点符号
        text = text.lower()  # 转换为小写
        
        # 使用 seaborn 调色板设置词云颜色
        colors = sns.color_palette(COLORMAP, 10)
        color_func = lambda *args, **kwargs: tuple(int(255 * c) for c in colors[np.random.randint(0, len(colors))])
        
        # 加载自定义形状掩码（如果提供）
        if MASK_IMAGE:
            try:
                mask_image = np.array(Image.open(MASK_IMAGE).convert("L"))
                # 将白色背景转换为透明
                mask_image = np.where(mask_image > 240, 255, 0)
            except Exception as e:
                print(f"警告: 无法加载掩码图像 - {e}")
                mask_image = None
        else:
            mask_image = None
        
        # 生成词云
        wordcloud = WordCloud(
            width=800, 
            height=400,
            background_color=BACKGROUND_COLOR,
            max_words=MAX_WORDS,
            mask=mask_image,
            color_func=color_func,
            stopwords=STOPWORDS_SET,
            contour_width=1,
            contour_color='steelblue',
            font_path=FONT_PATH  # 使用指定的黑体字体
        ).generate(text)
        
        # 显示词云图
        plt.figure(figsize=(12, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        
        # 添加标题
        plt.title(f"{TEXT_COLUMN} 词云图", fontsize=15, fontproperties='SimHei')
        
        # 保存图片（如果指定）
        if OUTPUT_FILE:
            plt.savefig(OUTPUT_FILE, bbox_inches='tight', dpi=300)
            print(f"词云图已保存到 {OUTPUT_FILE}")
        
        plt.show()
        
        # 打印词频统计
        top_words = wordcloud.process_text(text)
        top_words = sorted(top_words.items(), key=lambda x: x[1], reverse=True)[:10]
        print("\n词频统计（前10个）:")
        for word, freq in top_words:
            print(f"{word}: {freq}")
            
    except FileNotFoundError:
        print(f"错误: 文件 '{CSV_FILE}' 不存在")
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    generate_wordcloud()    