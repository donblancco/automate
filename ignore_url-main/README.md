# WOVN URL除外管理ツール

WOVNの除外設定ページでURLの追加・削除を自動化するSeleniumスクリプトです。

## 機能

- **URL追加**: CSVファイルからURLを読み込み、WOVN除外リストに一括追加
- **URL削除**: WOVN除外リストから指定した数だけURLを削除

## ファイル構成

```
ignore_url/
├── add_to_ignore_url.py          # URL追加スクリプト
├── remove_urls.py                # URL削除スクリプト
├── run_add_to_ignore_url.sh      # URL追加実行用シェルスクリプト
├── run_remove_urls.sh            # URL削除実行用シェルスクリプト
├── csv/
│   └── urllist.csv              # 追加するURLリスト
├── csv_org/                     # バックアップ・組織用CSVファイル
└── venv/                        # Python仮想環境
```

## セットアップ

### 1. 依存関係のインストール

```bash
# 仮想環境の作成（既に作成済み）
python3 -m venv venv

# 仮想環境のアクティベート
source venv/bin/activate

# 必要なパッケージのインストール
pip install pandas selenium webdriver-manager
```

### 2. CSVファイルの準備

`csv/urllist.csv` にヘッダー行 `url` と追加したいURLリストを記載：

```csv
url
https://example1.com
https://example2.com
https://example3.com
```

## 使用方法

### URL追加

1. **シェルスクリプト実行**:
   ```bash
   ./run_add_to_ignore_url.sh
   ```

2. **直接Python実行**:
   ```bash
   source venv/bin/activate
   python3 add_to_ignore_url.py
   ```

3. **実行手順**:
   - ブラウザが自動で開きます
   - サイトにログインします
   - 「設定 → 詳細 → Auto page add → Exclusion setting」に移動
   - ターミナルでEnterキーを押します
   - スクリプトが自動でURLを追加します

### URL削除

1. **シェルスクリプト実行**:
   ```bash
   ./run_remove_urls.sh
   ```

2. **直接Python実行**:
   ```bash
   source venv/bin/activate
   python3 remove_urls.py
   ```

3. **実行手順**:
   - ブラウザが自動で開きます
   - サイトにログインします
   - 「設定 → 詳細 → Auto page add → Exclusion setting」に移動
   - 削除したいURL数を入力します
   - ターミナルでEnterキーを押します
   - スクリプトが上から順に指定した数だけURLを削除します

## 注意事項

- スクリプト実行前にWOVNにログインする必要があります
- Google Chromeブラウザが必要です
- ChromeDriverは自動でダウンロードされます
- 処理中はブラウザを操作しないでください
- エラーが発生した場合は、手動で作業を完了させてください

## トラブルシューティング

### よくある問題

1. **`python: command not found`**
   - `python3`コマンドを使用してください
   - シェルスクリプトが`python3`を使用するように修正済み

2. **モジュールが見つからない**
   - 仮想環境がアクティブになっているか確認
   - 必要なパッケージがインストールされているか確認

3. **要素が見つからない**
   - WOVNのページ構造が変更された可能性があります
   - ログイン状態を確認してください
   - 正しいページにいるか確認してください

### デバッグ

- スクリプトは詳細なログを出力します
- エラーメッセージを確認してください
- 必要に応じてヘッドレスモードを無効にして動作を確認できます