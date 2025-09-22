from dotenv import load_dotenv

load_dotenv()


import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- 専門家モードごとのシステムメッセージ ---
EXPERT_SYSTEM_MESSAGES = {
    "ビジネス戦略の専門家": (
        "あなたは企業の経営戦略に詳しいコンサルタントです。"
        "課題整理→選択肢→推奨→次アクション、の流れで簡潔に答えてください。"
    ),
    "SNSマーケティング専門家": (
        "あなたはSNS運用の専門家です。"
        "ターゲット→企画→投稿テンプレ→CTA提案、の流れで答えてください。"
    ),
}

# --- LLM呼び出し用関数 ---
def ask_llm(input_text: str, expert_choice: str) -> str:
    system_msg = EXPERT_SYSTEM_MESSAGES.get(
        expert_choice, "あなたは有能なアシスタントです。"
    )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.3,
        api_key=os.getenv("OPENAI_API_KEY")
    )

    prompt = ChatPromptTemplate.from_messages(
        [("system", system_msg), ("human", "{user_input}")]
    )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"user_input": input_text})


# --- Streamlit UI ---
st.title("サンプルアプリ: 専門家モード付きLLMチャット")

st.write("##### モードA: ビジネス戦略の専門家")
st.write("経営課題や事業計画について相談できます。")
st.write("##### モードB: SNSマーケティング専門家")
st.write("SNS集客・投稿企画について相談できます。")

# モード選択ラジオボタン
selected_item = st.radio(
    "専門家モードを選択してください。",
    list(EXPERT_SYSTEM_MESSAGES.keys())
)

st.divider()

# 入力フォーム
input_message = st.text_area(
    "相談内容を入力してください。",
    placeholder="例：ラーメン屋を開業予定。初月の集客プランを提案して。"
)

# 実行ボタン
if st.button("実行"):
    st.divider()
    if input_message.strip():
        try:
            with st.spinner("LLMに問い合わせ中..."):
                answer = ask_llm(input_message.strip(), selected_item)
            st.subheader("回答")
            st.write(answer)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
    else:
        st.error("テキストを入力してから『実行』を押してください。")
