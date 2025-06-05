import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_word_frequency():
    """
    从word_frequency.txt生成词频柱状图
    """
    try:
        # 读取词频文件
        df = pd.read_csv('word_frequency.txt', sep='\t', header=None, names=['word', 'frequency'])
        
        # 获取前20个高频词
        top_words = df.head(20)
        
        # 设置中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字体
        plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号
        
        # 创建图形
        plt.figure(figsize=(15, 8))
        
        # 使用seaborn创建柱状图
        sns.barplot(x='word', y='frequency', data=top_words)
        
        # 设置标题和标签
        plt.title('词频统计（前20个高频词）', fontsize=16)
        plt.xlabel('词语', fontsize=12)
        plt.ylabel('频次', fontsize=12)
        
        # 旋转x轴标签，防止重叠
        plt.xticks(rotation=45, ha='right')
        
        # 调整布局
        plt.tight_layout()
        
        # 保存图片
        plt.savefig('word_frequency.png', dpi=300, bbox_inches='tight')
        print("词频柱状图已保存为 'word_frequency.png'")
        
        # 显示图形
        plt.show()
        
    except FileNotFoundError:
        print("错误：找不到 'word_frequency.txt' 文件")
    except Exception as e:
        print(f"发生错误：{e}")

if __name__ == "__main__":
    plot_word_frequency() 