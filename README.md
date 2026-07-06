# Instagram → Google Drive 영상 백업

인스타그램 프로필의 최근 영상을 다운로드해서 구글 드라이브에 자동으로 업로드하는 스크립트입니다 (`instagram_to_drive.py`).

> 인스타그램은 로그인하지 않은 요청을 데이터센터/클라우드 IP에서 차단하는 경우가 많습니다. 반드시 **로컬 PC(가정용 네트워크)** 에서 실행하세요.

## 1. 준비물

- Python 3.9 이상
- Google Cloud Console에서 만든 OAuth 클라이언트 (아래 3번 참고)

## 2. 설치

```bash
git clone <이 저장소 주소>
cd test
pip install -r requirements.txt
```

## 3. Google Drive OAuth 클라이언트 준비

1. [Google Cloud Console](https://console.cloud.google.com/)에서 프로젝트를 만들고 **Google Drive API**를 활성화합니다.
2. "OAuth 동의 화면"을 구성합니다 (테스트 사용자로 본인 계정 추가).
3. "사용자 인증 정보 만들기" → **OAuth 클라이언트 ID** → 애플리케이션 유형 **데스크톱 앱**으로 생성합니다.
4. 다운로드한 JSON 파일을 프로젝트 루트에 `client_secrets.json` 이름으로 저장합니다.

## 4. 환경 변수 설정

`.env.example`을 복사해서 `.env`를 만들고 값을 채웁니다.

```bash
cp .env.example .env
```

| 변수 | 설명 |
|---|---|
| `IG_TARGET_PROFILE` | 다운로드할 인스타그램 프로필 (예: `garambakerycafe`) |
| `IG_DOWNLOAD_LIMIT` | 최근 몇 개 게시물까지 확인할지 (0이면 전체) |
| `IG_USERNAME` / `IG_PASSWORD` | (선택, 권장) 인스타그램 로그인 정보. 레이트 리밋/차단을 줄여줍니다 |
| `GDRIVE_FOLDER_NAME` | 업로드할 구글 드라이브 폴더 이름 (비워두면 `IG_TARGET_PROFILE`과 동일) |

## 5. 실행

```bash
python instagram_to_drive.py
```

- 처음 실행하면 인스타그램 로그인(설정한 경우) 후, 브라우저가 열리며 구글 계정 로그인/권한 동의 화면이 뜹니다.
- 동의하면 `credentials.json`에 인증 정보가 저장되어 이후 실행부터는 다시 로그인할 필요가 없습니다.
- 영상은 `instagram_downloads/<프로필명>/` 폴더에 저장되고, 같은 이름의 구글 드라이브 폴더에 업로드됩니다.
- 이미 업로드된 파일은 다시 올리지 않고 건너뜁니다.

## 6. 문제 해결

- **403 Forbidden / 프로필을 찾을 수 없음**: 클라우드 서버나 VPN에서 실행 중일 가능성이 높습니다. 가정용 네트워크에서 실행하거나 `IG_USERNAME`/`IG_PASSWORD`를 설정해 로그인 후 시도하세요.
- **`client_secrets.json` 파일이 없습니다**: 3번 단계를 다시 확인하세요. 파일은 절대 git에 커밋하지 마세요 (`.gitignore`에 이미 제외되어 있습니다).
- **구글 로그인 창이 안 뜸**: 방화벽 등으로 로컬 웹서버(`localhost`) 접속이 막혀 있는지 확인하세요.
