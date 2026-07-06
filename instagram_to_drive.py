import os
import sys
from dotenv import load_dotenv
import instaloader
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

load_dotenv()

TARGET_PROFILE = os.getenv("IG_TARGET_PROFILE", "garambakerycafe")
DOWNLOAD_LIMIT = int(os.getenv("IG_DOWNLOAD_LIMIT", "10"))  # 0 이하면 전체 다운로드
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PASSWORD = os.getenv("IG_PASSWORD")
GDRIVE_FOLDER_NAME = os.getenv("GDRIVE_FOLDER_NAME", TARGET_PROFILE)

DOWNLOAD_DIR = os.path.join("instagram_downloads", TARGET_PROFILE)
SESSION_FILE = os.path.join("instagram_downloads", f".session-{IG_USERNAME}") if IG_USERNAME else None
VIDEO_EXTENSIONS = (".mp4", ".mov", ".avi", ".mkv")


def download_instagram_videos():
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)

    loader = instaloader.Instaloader(
        dirname_pattern=DOWNLOAD_DIR,
        download_pictures=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        post_metadata_txt_pattern="",
    )

    if IG_USERNAME and IG_PASSWORD:
        try:
            loader.load_session_from_file(IG_USERNAME, SESSION_FILE)
            print(f"[{IG_USERNAME}] 저장된 로그인 세션을 불러왔습니다.")
        except FileNotFoundError:
            print(f"[{IG_USERNAME}] 인스타그램에 로그인합니다...")
            loader.login(IG_USERNAME, IG_PASSWORD)
            loader.save_session_to_file(SESSION_FILE)

    print(f"[{TARGET_PROFILE}] 인스타그램 영상 다운로드를 시작합니다...")
    try:
        profile = instaloader.Profile.from_username(loader.context, TARGET_PROFILE)
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"프로필 '{TARGET_PROFILE}'을(를) 찾을 수 없습니다.")
        sys.exit(1)

    count = 0
    for post in profile.get_posts():
        if DOWNLOAD_LIMIT > 0 and count >= DOWNLOAD_LIMIT:
            break
        if not (post.is_video or post.typename == "GraphSidecar"):
            continue  # 영상이 없는 사진 게시물은 건너뜁니다

        try:
            loader.download_post(post, target=DOWNLOAD_DIR)
        except instaloader.exceptions.InstaloaderException as e:
            print(f"게시물 다운로드 실패 ({post.shortcode}): {e}")
            continue
        count += 1

    print("인스타그램 다운로드 완료!")


def get_drive():
    if not os.path.exists("client_secrets.json"):
        print(
            "client_secrets.json 파일이 없습니다. "
            "Google Cloud Console에서 OAuth 클라이언트(데스크톱 앱)를 생성하고 "
            "다운로드한 파일을 프로젝트 루트에 client_secrets.json 으로 저장하세요."
        )
        sys.exit(1)

    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)


def get_or_create_drive_folder(drive, folder_name):
    query = (
        f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' "
        "and trashed=false"
    )
    existing = drive.ListFile({"q": query}).GetList()
    if existing:
        return existing[0]["id"]

    folder = drive.CreateFile({
        "title": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    })
    folder.Upload()
    return folder["id"]


def upload_videos_to_drive():
    print("구글 드라이브 인증을 시작합니다...")
    drive = get_drive()
    folder_id = get_or_create_drive_folder(drive, GDRIVE_FOLDER_NAME)

    existing_titles = {
        f["title"]
        for f in drive.ListFile({"q": f"'{folder_id}' in parents and trashed=false"}).GetList()
    }

    print("구글 드라이브 업로드를 시작합니다...")
    for root, _dirs, files in os.walk(DOWNLOAD_DIR):
        for file_name in files:
            if not file_name.lower().endswith(VIDEO_EXTENSIONS):
                continue
            if file_name in existing_titles:
                print(f"이미 업로드됨, 건너뜀: {file_name}")
                continue

            file_path = os.path.join(root, file_name)
            print(f"업로드 중: {file_name}")
            gfile = drive.CreateFile({"title": file_name, "parents": [{"id": folder_id}]})
            gfile.SetContentFile(file_path)
            gfile.Upload()

    print("모든 작업이 완료되었습니다!")


if __name__ == "__main__":
    download_instagram_videos()
    upload_videos_to_drive()
