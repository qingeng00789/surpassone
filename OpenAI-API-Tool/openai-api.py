from openai import OpenAI
import pickle
import os  # osモジュールを追加
import sys

# OpenAI APIキーを環境変数から取得します。
api_key = os.getenv("OPENAI_API_KEY")  # 環境変数に設定することを推奨

client = OpenAI(api_key=api_key)

def query_gpt_chat(model, filename_input, history_file=None):
    messages = []
    if history_file and os.path.exists(history_file):
        with open(history_file, 'rb') as f:
            messages = pickle.load(f)
        project_name = os.path.splitext(os.path.basename(history_file))[0]
    else:
        project_name = input("project名を入力してください: ")
        history_file = f"{project_name}.pickle"
        messages = [{"role": "system", "content": "システム開発サポート"}]

    # filename_output = f"output-{project_name}.txt"
    filename_output = f"output.txt"

    # inputファイルからユーザーの入力を読み込みます。
    with open(filename_input, 'r', encoding='utf-8') as file:
        input_str = file.read().strip()
        messages.append({"role": "user", "content": input_str})

    try:
        # ChatCompletion.createを正しく使用する
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.2
        )
        # 応答の内容を取得
        result = response.choices[0].message.content
        messages.append({"role": "assistant", "content": result})  # 修正箇所
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        result = error_message

    # 結果をファイルに追記します。
    with open(filename_output, 'a', encoding='utf-8') as file:
        file.write("\n" + "--------------------------------------------" + "\n")
        file.write(result)
    # 会話履歴を保存します。
    with open(history_file, 'wb') as f:
        pickle.dump(messages, f)

    return result

# スクリプトの実行時に引数を取得します。
if len(sys.argv) < 2:
    print("使用法: python openai-api.py <inputファイル> [historyファイル]")
    sys.exit(1)

filename_input = sys.argv[1]
history_file = sys.argv[2] if len(sys.argv) > 2 else None

# チャットクエリを実行し、結果をファイルに保存します。
query_gpt_chat("gpt-4o", filename_input, history_file)
# query_gpt_chat("gpt-4", filename_input, history_file)
# query_gpt_chat("gpt-4-1106-preview", filename_input, history_file)
