import psycopg2
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

def test_rds_via_ssh_tunnel():
    """SSHトンネル経由でRDSに接続"""
    
    # パスの確認
    current_file = Path(__file__).resolve()
    print(f"現在のファイル: {current_file}")
    
    # .envファイルの場所を確認
    env_path = current_file.parent.parent / ".env"
    print(f".envファイルパス: {env_path}")
    print(f".envファイル存在確認: {env_path.exists()}")
    
    # .envファイルを読み込み
    if env_path.exists():
        load_dotenv(env_path)
        print("✅ .envファイル読み込み完了")
    else:
        # 別の場所も試してみる
        alt_env_path = Path.cwd() / ".env"
        print(f"代替パス: {alt_env_path}")
        print(f"代替パス存在確認: {alt_env_path.exists()}")
        
        if alt_env_path.exists():
            load_dotenv(alt_env_path)
            print("✅ 代替パスから.envファイル読み込み完了")
    
    # パスワード確認
    password = os.getenv("AWS_RDS_PASSWORD")
    print(f"パスワード取得結果: {'✅ 成功' if password else '❌ 失敗'}")
    if password:
        print(f"パスワード長: {len(password)}文字")
    
    # 環境変数を直接確認
    print("全ての環境変数:")
    for key, value in os.environ.items():
        if "RDS" in key or "AWS" in key:
            print(f"  {key}: {'*' * len(value) if value else 'なし'}")

# ここが重要！関数を実際に呼び出す
if __name__ == "__main__":
    test_rds_via_ssh_tunnel()