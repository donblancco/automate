import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from getpass import getpass
from pathlib import Path

LOGIN_URL = "https://example.io/ja/sign_in_form/"

options = webdriver.ChromeOptions()
# ヘッドレスモードを有効にする場合は以下のコメントアウトを解除
# options.add_argument("--headless")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(LOGIN_URL)

print("🌐 ブラウザが開きました。手動でログインを行ってください。")
print("1. メールアドレスとパスワードを入力してログイン")
print("2. 設定 → 詳細 → Auto page add → Exclusion setting に移動")
print("3. URL削除の準備ができたら下記のEnterキーを押してください")

# 削除回数を入力
try:
    delete_count = int(input("削除するURL数を入力してください: "))
    if delete_count <= 0:
        print("削除数は1以上である必要があります。")
        driver.quit()
        exit()
except ValueError:
    print("無効な数値です。")
    driver.quit()
    exit()

input("🛑 準備完了後、Enter を押してください → ")

def safe_click(selector, by=By.CSS_SELECTOR, retries=3, wait_sec=10):
    for i in range(retries):
        try:
            element = WebDriverWait(driver, wait_sec).until(EC.element_to_be_clickable((by, selector)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.2)
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            print(f"🔁 クリックリトライ中... ({i+1}/{retries}) → {e}")
            time.sleep(1)
    return False

def remove_first_url():
    try:
        print(f"📍 一番上のURL項目を探しています...")
        
        # 削除ボタンのセレクタ
        delete_button_selectors = [
            ".excluded-url__item:first-child .m-item-control__item__button--delete",
            ".excluded-url__item .m-item-control__item__button--delete",
            "button.m-item-control__item__button--delete",
            "button[aria-label='Control button delete']"
        ]
        
        for selector in delete_button_selectors:
            try:
                delete_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"🔍 セレクタ '{selector}' で{len(delete_buttons)}個の削除ボタンを発見")
                
                if delete_buttons:
                    # 最初のボタン（一番上のURL）を取得
                    delete_button = delete_buttons[0]
                    
                    if delete_button.is_displayed() and delete_button.is_enabled():
                        print(f"📍 削除ボタンをクリックしています...")
                        
                        # より確実なクリック方法を試す
                        try:
                            # 方法1: JavaScriptクリック
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", delete_button)
                            time.sleep(0.5)
                            driver.execute_script("arguments[0].click();", delete_button)
                            print(f"✅ 削除ボタンクリック完了")
                            
                            # 確認モーダルの"Remove"ボタンを探してクリック
                            time.sleep(1)  # モーダル表示を待つ
                            confirm_button = WebDriverWait(driver, 5).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-footer-buttons__button--confirm"))
                            )
                            driver.execute_script("arguments[0].click();", confirm_button)
                            print(f"✅ 確認ボタンクリック完了")
                            time.sleep(2)  # 削除処理完了まで待機
                            return True
                        except Exception as click_e1:
                            print(f"⚠️ 方法1クリック失敗: {click_e1}")
                            try:
                                # 方法2: ActionChainsクリック
                                actions = ActionChains(driver)
                                actions.move_to_element(delete_button).click().perform()
                                print(f"✅ 削除ボタンクリック完了")
                                
                                # 確認モーダルの"Remove"ボタンを探してクリック
                                time.sleep(1)
                                confirm_button = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".modal-footer-buttons__button--confirm"))
                                )
                                actions = ActionChains(driver)
                                actions.move_to_element(confirm_button).click().perform()
                                print(f"✅ 確認ボタンクリック完了")
                                time.sleep(2)
                                return True
                            except Exception as click_e2:
                                print(f"❌ 全てのクリック方法が失敗: {click_e2}")
                                continue
                        
            except Exception as e:
                print(f"⚠️ セレクタ '{selector}' で削除ボタン探索失敗: {e}")
                continue
        
        print(f"❌ 削除可能なURLが見つかりませんでした")
        return False
        
    except Exception as e:
        print(f"❌ URL削除エラー: {e}")
        return False

# 指定回数分のURL削除を実行
success_count = 0
for i in range(delete_count):
    print(f"🔗 削除処理 {i+1}/{delete_count}")
    
    if remove_first_url():
        success_count += 1
        print(f"✅ 削除成功: {i+1}番目のURL")
    else:
        print(f"❌ 削除失敗: {i+1}番目のURL")
        # 削除に失敗した場合、残りの処理を続行するか確認
        continue_process = input("削除に失敗しました。続行しますか？ (y/n): ")
        if continue_process.lower() != 'y':
            break
    
    # 次の削除前に少し待つ（最後の削除後は待機しない）
    if i < delete_count - 1:
        time.sleep(10)

print(f"🎉 処理完了! 成功: {success_count}/{delete_count} URLs")
driver.quit()