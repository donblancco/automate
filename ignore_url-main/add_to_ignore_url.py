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

CSV_PATH = "/path/to/csvfile.csv"
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
print("3. URL追加の準備ができたら下記のEnterキーを押してください")
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

def click_save_button():
    try:
        print(f"📍 ステップ4: 保存ボタンをクリックしています...")
        
        # 保存ボタンを探す - 編集中のアイテム内で探す
        save_button_selectors = [
            ".m-line-input--editing .m-item-control__item__button--save",
            ".excluded-url__item .m-item-control__item__button--save",
            "button.m-item-control__item__button--save",
            "button[aria-label='Control button save']",
            ".m-item-control__item__button--save"
        ]
        
        for selector in save_button_selectors:
            try:
                save_buttons = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"🔍 セレクタ '{selector}' で{len(save_buttons)}個の保存ボタンを発見")
                
                for save_button in save_buttons:
                    try:
                        # ボタンが表示されているかチェック
                        if save_button.is_displayed() and save_button.is_enabled():
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_button)
                            time.sleep(0.5)
                            driver.execute_script("arguments[0].click();", save_button)
                            print(f"✅ 保存ボタンクリック完了")
                            time.sleep(5)  # 保存処理完了まで待機
                            return True
                    except Exception as button_e:
                        print(f"⚠️ 個別ボタンクリック失敗: {button_e}")
                        continue
                        
            except Exception as e:
                print(f"⚠️ セレクタ '{selector}' で保存ボタン失敗: {e}")
                continue
        
        print(f"❌ 保存ボタンが見つかりませんでした")
        return False
        
    except Exception as e:
        print(f"❌ 保存ボタンクリックエラー: {e}")
        return False

def add_url_to_exclude_list(url):
    try:
        print(f"📍 ステップ1: ページ全体から+ Addボタンを探しています...")
        
        # 複数の方法で"+ Add"ボタンを探す
        add_button = None
        
        # 方法1: excluded-url__add-buttonクラス
        try:
            add_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.excluded-url__add-button"))
            )
            print(f"✅ 方法1でAddボタン発見")
        except:
            print(f"⚠️ 方法1失敗")
        
        # 方法2: テキストで探す
        if not add_button:
            try:
                add_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., '+ Add')]"))
                )
                print(f"✅ 方法2でAddボタン発見")
            except:
                print(f"⚠️ 方法2失敗")
        
        # 方法3: より広範囲で探す
        if not add_button:
            try:
                add_button = driver.find_element(By.XPATH, "//button[contains(@class, 'add-button') or contains(., 'Add') or contains(., '追加')]")
                print(f"✅ 方法3でAddボタン発見")
            except:
                print(f"⚠️ 方法3失敗")
        
        if not add_button:
            print(f"❌ + Addボタンが見つかりませんでした")
            print(f"⏰ 5秒待機してからリトライします...")
            time.sleep(5)
            
            # 再度Addボタンを探す
            try:
                add_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.excluded-url__add-button"))
                )
                print(f"✅ リトライでAddボタン発見")
            except:
                print(f"❌ リトライでもAddボタンが見つかりませんでした")
                return False
        
        print(f"📍 ステップ2: + Addボタンをクリックしています...")
        
        # より確実なクリック方法を試す
        try:
            # 方法1: JavaScriptクリック
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
            time.sleep(0.2)
            driver.execute_script("arguments[0].click();", add_button)
            print(f"✅ 方法1でAddボタンクリック完了")
        except Exception as click_e1:
            print(f"⚠️ 方法1クリック失敗: {click_e1}")
            try:
                # 方法2: ActionChainsクリック
                actions = ActionChains(driver)
                actions.move_to_element(add_button).click().perform()
                print(f"✅ 方法2でAddボタンクリック完了")
            except Exception as click_e2:
                print(f"❌ 全てのクリック方法が失敗: {click_e2}")
                return False
        
        # 新しい行が追加されるまで待つ
        time.sleep(0.2)
        
        # Addボタンが再び有効になるまで待つ
        try:
            WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.excluded-url__add-button:not([disabled])"))
            )
            print(f"✅ Addボタンが再び有効になりました")
        except:
            print(f"⚠️ Addボタンの有効化待機がタイムアウト")
        
        print(f"📍 ステップ3: 入力フィールドを探しています...")
        
        # すべての可能な入力フィールドを探す
        input_selectors = [
            ".excluded-url__item input"
        ]
        
        for selector in input_selectors:
            try:
                path_inputs = driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"🔍 セレクタ '{selector}' で{len(path_inputs)}個の入力フィールドを発見")
                
                if path_inputs:
                    # 有効な（disabled でない）入力フィールドを探す
                    for i, input_field in enumerate(path_inputs):
                        try:
                            is_disabled = input_field.get_attribute("disabled")
                            is_readonly = input_field.get_attribute("readonly")
                            #print(f"📍 入力フィールド {i+1}: disabled={is_disabled}, readonly={is_readonly}")
                            
                            if not is_disabled and not is_readonly:
                                print(f"📍 ステップ4: URLを入力しています...")
                                
                                # より確実な入力方法を試す
                                try:
                                    # 方法1: 通常の入力
                                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
                                    time.sleep(1)
                                    driver.execute_script("arguments[0].focus();", input_field)
                                    time.sleep(1)
                                    input_field.clear()
                                    input_field.send_keys(url)
                                    print(f"✅ 方法1でURL入力完了: {url}")
                                    time.sleep(2)
                                    
                                    # 保存ボタンをクリック
                                    if click_save_button():
                                        return True
                                    else:
                                        print(f"⚠️ 保存ボタンクリック失敗")
                                        return False
                                except Exception as input_e1:
                                    print(f"⚠️ 方法1入力失敗: {input_e1}")
                                    try:
                                        # 方法2: JavaScriptで入力
                                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
                                        time.sleep(1)
                                        driver.execute_script("arguments[0].value = arguments[1];", input_field, url)
                                        driver.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));", input_field)
                                        driver.execute_script("arguments[0].dispatchEvent(new Event('change', { bubbles: true }));", input_field)
                                        print(f"✅ 方法2でURL入力完了: {url}")
                                        time.sleep(2)
                                        
                                        # 保存ボタンをクリック
                                        if click_save_button():
                                            return True
                                        else:
                                            print(f"⚠️ 保存ボタンクリック失敗")
                                            return False
                                    except Exception as input_e2:
                                        print(f"⚠️ 方法2入力失敗: {input_e2}")
                                        try:
                                            # 方法3: より長い待機時間で再試行
                                            time.sleep(3)
                                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
                                            time.sleep(1)
                                            driver.execute_script("arguments[0].removeAttribute('disabled');", input_field)
                                            driver.execute_script("arguments[0].removeAttribute('readonly');", input_field)
                                            time.sleep(0.5)
                                            input_field.clear()
                                            input_field.send_keys(url)
                                            print(f"✅ 方法3でURL入力完了: {url}")
                                            time.sleep(2)
                                            
                                            # 保存ボタンをクリック
                                            if click_save_button():
                                                return True
                                            else:
                                                print(f"⚠️ 保存ボタンクリック失敗")
                                                return False
                                        except Exception as input_e3:
                                            print(f"⚠️ 方法3入力失敗: {input_e3}")
                                            continue
                        except Exception as field_e:
                            print(f"⚠️ フィールド {i+1} 処理エラー: {field_e}")
                            continue
            except Exception as selector_e:
                print(f"⚠️ セレクタ '{selector}' エラー: {selector_e}")
                continue
        
        print(f"❌ 有効な入力フィールドが見つかりませんでした")
        return False
        
    except Exception as e:
        print(f"❌ URL追加エラー: {url} → {e}")
        return False

# CSVファイルを読み込み
df = pd.read_csv(CSV_PATH)

# URLを一つずつ処理
success_count = 0
for idx, row in df.iterrows():
    url = row["url"]
    if pd.isna(url) or url == "url":  # ヘッダー行をスキップ
        continue
    
    print(f"🔗 処理中: {url}")
    
    if add_url_to_exclude_list(url):
        success_count += 1
        print(f"✅ 追加成功: {url}")
    else:
        print(f"❌ 追加失敗: {url}")
    
    # 次のURLの処理前に少し待つ
    time.sleep(2)

print(f"🎉 処理完了! 成功: {success_count}/{len(df)} URLs")
driver.quit()