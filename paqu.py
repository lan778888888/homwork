import requests
import pandas as pd
import re
import time
import random
from datetime import datetime


def get_bvid_from_url(url):
    """从B站视频URL提取bvid"""
    match = re.search(r'(BV[0-9a-zA-Z]+)', url)
    if match:
        return match.group(1)
    else:
        raise ValueError("⚠️ 无法从URL提取bvid，请检查URL是否正确（如 https://www.bilibili.com/video/BV1yW421N7aH）")


def get_all_comments(bvid, max_pages=100, cookie=None):
    """获取全部评论（支持模拟登录和速度控制）"""
    comments = []
    next_page = 0  # 初始页码
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": f"https://www.bilibili.com/video/{bvid}",
        "Cookie": cookie if cookie else "",  # 传递Cookie模拟登录
    }

    while next_page is not None and next_page < max_pages:
        # API请求（mode=3按时间排序，最新优先）
        api_url = f"https://api.bilibili.com/x/v2/reply/main?jsonp=jsonp&next={next_page}&type=1&oid={bvid}&mode=3&plat=1"

        try:
            # 随机延迟（1~3秒）控制速度
            delay = random.uniform(2, 5)
            print(f"⏳ 正在爬取第 {next_page + 1} 页，延迟 {delay:.1f} 秒...")
            time.sleep(delay)

            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            # 提取当前页评论
            if data.get("data") and data["data"].get("replies"):
                for reply in data["data"]["replies"]:
                    comment_time = datetime.fromtimestamp(reply["ctime"])
                    comment_content = reply["content"]["message"]
                    comments.append({"time": comment_time, "text": comment_content})

            # 检查是否还有下一页
            if data.get("data") and data["data"].get("cursor"):
                next_page = data["data"]["cursor"]["next"]
                if data["data"]["cursor"]["is_end"]:  # B站返回的结束标志
                    break
            else:
                break

            print(f"✅ 已获取 {len(comments)} 条评论，下一页：{next_page}")

        except Exception as e:
            print(f"❌ 第 {next_page} 页请求失败：{e}")
            break

    return comments


def main():
    print("数据爬取中ing")
    print("----------------------------------")
    # 视频链接
    video_url = "https://www.bilibili.com/video/BV1tCdUYPEdL/?share_source=copy_web"
    # 预留cookie位置，需要时可以在这里填入
    cookie = "buvid3=13B8E90A-DFB2-71E4-2C40-F5D933A8476812535infoc; b_nut=1742862912; _uuid=610A3D4C1-4741-2188-E18A-45C9B6D3D10FF12772infoc; enable_web_push=DISABLE; enable_feed_channel=ENABLE; buvid4=78C0F9E2-9E38-9DC1-12AC-76E1669518BC12946-025032500-G%2Bte6dU%2Fe8YyFEFKtSqQbQ%3D%3D; header_theme_version=CLOSE; DedeUserID=3537111844129701; DedeUserID__ckMd5=669270cc7bd0dcbc; rpdid=|(u~)|mYRkRY0J'u~Rk))uk)J; hit-dyn-v2=1; buvid_fp_plain=undefined; LIVE_BUVID=AUTO6717437662592461; PVID=1; CURRENT_QUALITY=80; home_feed_column=5; browser_resolution=1432-744; CURRENT_FNVAL=4048; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDkxMDg5NjYsImlhdCI6MTc0ODg0OTcwNiwicGx0IjotMX0.djw1putjLZE20tjErsFS3gNTTQjNceIIkJ4U-EZU3PM; bili_ticket_expires=1749108906; SESSDATA=f3264532%2C1764401768%2Cdd234%2A61CjD5zjw1HxmIiKWh_B-ttny2w1rPSx7rGqeNgkpk0nwKrffkvBR-9YYdMsaJayGi-7USVmF4LW5zT0d0c0JLM1JaQ2ZPVFNTU2VVcFYyTlhGYV8wakxRNHVlSmV1a2NoRVdwbndtUWwwazh6UDludDRfOF9QZlp0VjNHU21OSE9hc0V5bWZ2M2l3IIEC; bili_jct=ddab84543a33ae18cc27ec1b65bae37b; sid=7612b3ec; b_lsid=DF10106911_1973B0DDBE8; bp_t_offset_3537111844129701=1074618469774786560; fingerprint=c3d30e2ba0e6181ae763a4b842f5024e; buvid_fp=13B8E90A-DFB2-71E4-2C40-F5D933A8476812535infoc"  

    try:
        bvid = get_bvid_from_url(video_url)
        print(f"🔍 提取到视频ID: {bvid}")
        print("⏳ 正在获取全部评论（按最新排序）...")

        comments = get_all_comments(bvid, cookie=cookie)
        if not comments:
            print("未获取到评论，可能是视频无评论或API限制")
            return

        # 按时间降序排列
        df = pd.DataFrame(comments)
        df = df.sort_values("time", ascending=False)
        df["time"] = df["time"].dt.strftime('%Y-%m-%d %H:%M:%S')

        df.to_csv("ci.csv", index=False, encoding='utf_8_sig')
        print(f"共获取 {len(df)} 条评论（登录模式），已保存到csv文件")
    except Exception as e:
        print(f" 出错: {e}")


if __name__ == "__main__":
    main()