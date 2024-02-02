import urllib.request
import urllib.parse
import json


def naver_search(
    search: str, query: str, client_id: str, client_secret: str, output_file: str
):
    """
    네이버 검색 API를 사용하여 검색어에 대한 결과를 최대 100건까지 수집하여 JSON 파일로 저장합니다.

    Parameters:
    - search: 검색 종류 (예: "blog", "webkr")
    - query: 검색어 (예: "송파구 맛집")
    - output_file: 검색 결과를 저장할 JSON 파일의 경로
    """
    encText = urllib.parse.quote(query)
    all_data = []

    for start in range(1, 101, 100):
        url = f"https://openapi.naver.com/v1/search/{search}?query={encText}&start={start}&display=100"
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", client_id)
        request.add_header("X-Naver-Client-Secret", client_secret)

        try:
            response = urllib.request.urlopen(request)
            response_body = response.read()
            data = json.loads(response_body.decode)
            all_data.extend(data["items"])
        except urllib.error.URLError as e:
            print(f"데이터 검색 중에 오류가 발생했습니다: {e.reason}")
            break

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(all_data, file, ensure_ascii=False, indent=4)
