import argparse
import asyncio
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

async def check_host(host: str, timeout: int = 2) -> bool:
    """Асинхронная проверка доступности хоста через системный ping."""
    host = host.strip()
    if not host or host.startswith("#"):
        return None

    cmd = f"ping -c 1 -W {timeout} {host}"

    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )

    await proc.wait()
    is_up = (proc.returncode == 0)

    if is_up:
        logging.info(f"✅ Host {host:<20} is UP")
    else:
        logging.warning(f"❌ Host {host:<20} is DOWN")

    return is_up

async def main():

    parser = argparse.ArgumentParser(description="Async Network Host Checker")
    parser.add_argument("-f", "--file", default="targets.txt", help="Путь к файлу со списком хостов")
    parser.add_argument("-t", "--timeout", type=int, default=2, help="Таймаут ответа (сек)")
    args = parser.parse_args()

    targets_path = Path(args.file)
    if not targets_path.exists():
        logging.error(f"Файл {args.file} не найден!")
        return


    with open(targets_path, "r") as f:
        hosts = [line.strip() for line in f if line.strip()]

    logging.info(f"Запуск проверки {len(hosts)} хостов...")

    tasks = [check_host(host, args.timeout) for host in hosts]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
