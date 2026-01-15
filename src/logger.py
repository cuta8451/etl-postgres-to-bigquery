# src/logger.py

import logging
from pathlib import Path

# -------------------------
# Log 檔案存放目錄設定
# -------------------------
# 所有 ETL pipeline 的 log 都會寫在 logs/ 資料夾底下
LOG_DIR = Path("logs")

# 如果 logs 資料夾不存在就建立
# exist_ok=True 代表「如果已經存在也不要報錯」
LOG_DIR.mkdir(exist_ok=True)


def get_logger(name: str) -> logging.Logger:
    """
    建立並回傳一個 logger 物件

    每個模組（extract / transform / load / main）
    都可以透過不同的 name 取得 logger，
    但所有 log 都會寫到同一個 etl.log 檔案

    Parameters
    ----------
    name : str
        logger 的名稱（通常使用模組名稱）

    Returns
    -------
    logging.Logger
        已設定好 handler 與 formatter 的 logger
    """

    # 取得（或建立）一個指定名稱的 logger
    logger = logging.getLogger(name)

    # 設定 log 等級
    # INFO 代表：記錄一般流程、重要狀態，不記錄 debug 細節
    logger.setLevel(logging.INFO)

    # -------------------------
    # 防止重複新增 handler
    # -------------------------
    # 如果 logger 已經有 handler，代表之前已經設定過
    # 不需要再重複加，否則會造成同一行 log 被寫多次
    if not logger.handlers:

        # 建立一個檔案型 handler
        # 所有 log 都會寫入 logs/etl.log
        file_handler = logging.FileHandler(LOG_DIR / "etl.log")

        # 設定 log 格式
        # asctime     : log 發生時間
        # levelname  : log 等級（INFO / ERROR / etc）
        # name       : logger 名稱（通常是模組名稱）
        # message    : log 內容
        formatter = logging.Folrmatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        # 將格式套用到 handler
        file_handler.setFormatter(formatter)

        # 把 handler 掛到 logger 上
        logger.addHandler(file_handler)

    # 回傳設定完成的 logger
    return logger
