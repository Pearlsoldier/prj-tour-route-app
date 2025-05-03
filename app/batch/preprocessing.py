from interface.input_parser import Interface_batch


class DatabasePreprocessing:
    """
    データベースへの接続→database.pyから接続
    入力に関しては、interfaceを利用する→新しくinterfaceにクラスを作成する
    __init__の時に、
    """
    def __init__(self):
        batch_input = input()
        
        