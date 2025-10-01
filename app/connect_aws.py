import boto3
from botocore.exceptions import ClientError, NoCredentialsError

def quick_rds_test():
    """簡単なRDS権限テスト"""
    print("🔍 AWS RDS接続テスト開始...")
    
    try:
        # 現在の認証情報を確認
        sts = boto3.client('sts')
        identity = sts.get_caller_identity()
        
        print("✅ AWS認証成功!")
        print(f"   ユーザーARN: {identity['Arn']}")
        print(f"   アカウントID: {identity['Account']}")
        print(f"   リージョン: {boto3.Session().region_name}")
        
        # RDSクライアントを作成
        rds = boto3.client('rds')
        
        # RDSインスタンス一覧を取得（権限テスト）
        print("\n📋 RDSインスタンス一覧取得テスト...")
        response = rds.describe_db_instances()
        
        print("✅ RDS読み取り権限: OK")
        
        # 結果の表示
        instances = response['DBInstances']
        print(f"   既存のRDSインスタンス数: {len(instances)}")
        
        if instances:
            print("\n   📊 既存のRDSインスタンス:")
            for db in instances:
                status = db['DBInstanceStatus']
                engine = db['Engine']
                db_class = db['DBInstanceClass']
                print(f"   - {db['DBInstanceIdentifier']}")
                print(f"     エンジン: {engine}, ステータス: {status}, クラス: {db_class}")
                if 'Endpoint' in db:
                    print(f"     エンドポイント: {db['Endpoint']['Address']}")
                print()
        else:
            print("   （RDSインスタンスは見つかりませんでした）")
        
        # PostgreSQLバージョン確認
        print("🐘 利用可能なPostgreSQLバージョン確認...")
        pg_versions = rds.describe_db_engine_versions(
            Engine='postgres',
            DefaultOnly=False
        )
        
        latest_versions = [v['EngineVersion'] for v in pg_versions['DBEngineVersions'][-5:]]
        print(f"   最新の5バージョン: {', '.join(latest_versions)}")
        
        print("\n🎉 全ての基本テストが成功しました!")
        print("   PostgreSQL RDSインスタンスの作成準備が整っています。")
        
        return True
        
    except NoCredentialsError:
        print("❌ AWS認証情報が設定されていません")
        print("\n📝 設定方法:")
        print("1. aws configure コマンドを実行")
        print("2. アクセスキーIDとシークレットアクセスキーを入力")
        print("3. リージョンを 'ap-northeast-1' に設定")
        return False
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"❌ AWS APIエラー: {error_code}")
        
        if error_code == 'AccessDenied':
            print("   RDS操作の権限がありません")
            print("   管理者にRDS権限の追加を依頼してください")
        elif error_code == 'InvalidUserID.NotFound':
            print("   アクセスキーが無効です")
            print("   正しいアクセスキーを設定してください")
        else:
            print(f"   詳細: {e}")
        
        return False
        
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AWS RDS 簡単接続テスト")
    print("=" * 40)
    
    success = quick_rds_test()
    
    if success:
        print("\n✅ 次のステップ:")
        print("1. PostgreSQL RDSインスタンスの作成")
        print("2. セキュリティグループの設定")
        print("3. データベースへの接続")
    else:
        print("\n❌ 認証情報を設定してから再試行してください")
        print("   設定コマンド: aws configure")