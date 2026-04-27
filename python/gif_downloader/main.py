import re
from pathlib import Path

import httpx

source = Path("source.txt")

tenor_regex = re.compile(r'class="Gif"[^<]+<img src="([^"]+)"')

def get_tenor_inner_gif(url: httpx.URL) -> None | httpx.URL:
    response = httpx.get(url)

    try:
        response.raise_for_status()
    except Exception as error:
        print(f"Error for url {url} {error}")
        return None

    inner_gif_match = tenor_regex.search(response.text)

    if inner_gif_match is not None:
        return httpx.URL(inner_gif_match.group(1))
    else:
        print(f"Couldn't find inner gif for {url}")
        return None

def main():
    output = Path("output")
    output.mkdir(exist_ok=True)

    for url in source.read_text().splitlines():
        url = httpx.URL(url)

        output_path = output / url.path.split("/")[-1]
        output_path = output_path.with_suffix(".gif")

        if url.host == "tenor.com":
            inner_gif = get_tenor_inner_gif(url)

            if inner_gif is None:
                continue

            url = inner_gif

        response = httpx.get(url)

        try:
            response.raise_for_status()
        except Exception as error:
            print(f"Error for url {url} {error}")
            continue

        print(f"Downloading: {url}")
        output_path.write_bytes(response.read())


if __name__ == "__main__":
    main()
