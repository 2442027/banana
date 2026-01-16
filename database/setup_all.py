import os

# 実行したいファイルを順番にリストアップ
scripts = [
    'init_db.py',          # 1. 初期化 (tag対応済み)
    'add_putters.py',      # 2. パター追加
    'add_more_clubs.py',   # 3. その他クラブ追加
    'update_prices.py'     # 4. 価格更新
]

# 自分のいる場所 (databaseフォルダ)
base_dir = os.path.dirname(os.path.abspath(__file__))

print("🚀 全データのセットアップを開始します...")

for script in scripts:
    script_path = os.path.join(base_dir, script)
    print(f"▶ 実行中: {script} ...")
    
    # 別のpythonファイルを実行するコマンド
    exit_code = os.system(f'python "{script_path}"')
    
    if exit_code != 0:
        print(f"❌ エラーが発生しました: {script}")
        break

print("✨ すべての処理が完了しました！アプリを起動してください。")