import streamlit as st
import os
from openai import OpenAI
#页面设置
st.set_page_config(page_title="AI Partner", page_icon=":robot_face:", layout="wide", initial_sidebar_state="expanded")
#大标题
st.title("AI Partner")
#系统提示词
prompt_system = "你的是一名非常可爱的AI助手，名字叫小爱，你的任务是帮助用户解答问题，提供有用的信息，并且尽可能友好地与用户交流。请确保你的回答简洁明了，并且尽量使用通俗易懂的语言。"
#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
#展示聊天信息
for message in st.session_state.messages:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])
#消息输入框
client = OpenAI(
   api_key = os.getenv("DEEPSEEK_API_KEY", "sk-a910aacb624644af9b4b32f474336baf"),
    base_url="https://api.deepseek.com"
)
prompt = st.chat_input("请输入你要问的问题")
if prompt:
    #显示用户输入的消息
    st.chat_message("user").write(prompt)
    #保存用户输入的消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    #生成AI回复
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt_system},
           
            {"role": "user", "content": prompt}
        ]
    )
#输出AI回复
    print(response.choices[0].message.content)
    st.chat_message("assistant").write(response.choices[0].message.content)
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})
