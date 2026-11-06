import os
import requests

ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
PAGE_ID = os.getenv("FB_PAGE_ID")
BASE_MEDIA_DIR = r"E:\herologo\ZZ"

POST_CAPTION = """📲 可在 Google Play 和 App Store 下载，立即观看最新热播内容，享受超高清画质！
👉 下载 HeroDrama，精彩不间断！

#HeroDrama #爱无止境 #热门短剧 #追剧 #高清画质 #短剧推荐 #好剧推荐 #必看剧集 #GooglePlay #AppStore #下载观看 #电视剧"""

# التعليق الثابت المستهدف لعشاق الميكرودراما
TARGET_COMMENT = """🔥 精彩短剧看不停！下载 HeroDrama 享受沉浸式追剧体验 👇
#Microdrama #ShortDrama #ClippedDrama #BingeWatch #DramaLovers #短剧党 #追剧日常 #超高清短剧 #爽剧推荐"""

def get_next_episode():
    if not os.path.exists(BASE_MEDIA_DIR):
        print(f"المسار غير موجود: {BASE_MEDIA_DIR}")
        return None, None

    for drama_series in sorted(os.listdir(BASE_MEDIA_DIR)):
        series_path = os.path.join(BASE_MEDIA_DIR, drama_series)
        if os.path.isdir(series_path):
            episodes = sorted(os.listdir(series_path))
            for ep in episodes:
                ep_path = os.path.join(series_path, ep)
                if os.path.isfile(ep_path) and ep.lower().endswith(('.mp4', '.mov', '.jpg', '.png')):
                    return ep_path, drama_series
    return None, None

def post_to_social_media():
    if not ACCESS_TOKEN or not PAGE_ID:
        print("بيانات الاتصال بفيسبوك (Tokens) غير متوفرة.")
        return

    file_path, series_name = get_next_episode()
    if not file_path:
        print("انتهت جميع الحلقات، لا توجد ملفات جديدة للنشر.")
        return

    print(f"جاري رفع مسلسل: {series_name} - ملف: {os.path.basename(file_path)}")

    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    
    # تنسيق النص بحيث يبرز اسم المسلسل بوضوح للجمهور
    full_message = f"🎬 热门短剧推荐：《 {series_name} 》\n\n{POST_CAPTION}"
    
    payload = {
        "message": full_message,
        "access_token": ACCESS_TOKEN
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        res_data = response.json()
        post_id = res_data.get("id")
        print(f"تم بنجاح نشر حلقة من مسلسل: {series_name} (Post ID: {post_id})")
        
        # إضافة التعليق التلقائي بالهاشتاجات أسفل المنشور
        if post_id:
            comment_url = f"https://graph.facebook.com/{post_id}/comments"
            comment_payload = {
                "message": TARGET_COMMENT,
                "access_token": ACCESS_TOKEN
            }
            comm_res = requests.post(comment_url, data=comment_payload)
            if comm_res.status_code == 200:
                print("تم اضافة التعليق المستهدف بنجاح تحت المنشور.")
            else:
                print(f"فشل إضافة التعليق: {comm_res.text}")

        # حذف الملف بعد اكتمال نشره للانتقال للحلقة التالية
        os.remove(file_path)
    else:
        print(f"فشل النشر: {response.text}")

if __name__ == "__main__":
    post_to_social_media()
