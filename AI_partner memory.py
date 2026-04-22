import streamlit as st
import os
from openai import OpenAI
from datetime import datetime
import json 
#生成会话标识的函数
def generate_session_id():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#保存会话信息的函数
def save_session():
    if st.session_state.current_session:
        #构建新的会话信息
        session_data ={
            "nick_name": st.session_state.nick_name,
            "gender": st.session_state.gender,
            "persenality": st.session_state.persenality,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }
        #如果sessions不存在，则创建一个新的sessions列表
        if not os.path.exists("sessions"):
            os.makedirs("sessions")
        #保存会话信息到文件，文件名使用当前会话的时间戳
        with open(f"sessions/{st.session_state.current_session}.txt", "w", encoding="utf-8") as f:
            f.write(json.dumps(session_data, ensure_ascii=False))
#加载会话列表的函数
def list_sessions():
    session_list = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for file_name in file_list:
            if file_name.endswith(".txt"):
               session_list.append(file_name[:-4])  # 去掉文件扩展名
    return session_list

#加载指定会话信息的函数
def load_session(session_id):
    try:
       if os.path.exists(f"sessions/{session_id}.txt"):
      #读取会话数据
         with open(f"sessions/{session_id}.txt", "r", encoding="utf-8") as f:
            session_data = json.load(f)
            st.session_state.messages = session_data["messages"]
            st.session_state.nick_name = session_data["nick_name"]
            st.session_state.gender = session_data.get("gender", "女")
            st.session_state.persenality = session_data["persenality"]
            st.session_state.current_session = session_data["current_session"]
    except Exception :
        st.error("加载会话信息失败，请确保会话文件存在且格式正确")

#删除指定会话信息的函数
def delete_session(session_id):
    try:
        if os.path.exists(f"sessions/{session_id}.txt"):
            os.remove(f"sessions/{session_id}.txt")
            #如果删除的会话是当前会话，则清空当前会话信息
            if session_id == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_id()
                
            st.success("会话删除成功")
        else:
            st.warning("会话文件不存在，无法删除")
    except Exception as e:
        st.error(f"删除会话信息失败: {str(e)}")
        

#页面设置
st.set_page_config(page_title="AI Partner", page_icon=":robot_face:", layout="wide", initial_sidebar_state="expanded")
#大标题
st.title("AI Partner")
#系统提示词
prompt_system = """
                你叫%s，现在是用户的真实伴侣，请你完全代入角色
                伴侣性别：%s
                规则：
1. 你必须完全代入角色，不能以任何形式透露你是一个AI
2.每次只发送1句话，不能一次性发送多句话
3.禁止任何场景或状态描述行的文字
4.回复简短，像微信聊天一样
5.可以用表情符号，但不能过多使用
6.用符合伴侣性格的方式对话
7.回复内容要充分体现伴侣的个性和情感，不能过于机械或公式化
伴侣性格：%s
你必须严格遵守上述规则来回复用户
"""

#初始化聊天信息
if "messages" not in st.session_state:
    st.session_state.messages = []
#昵称
if "nick_name" not in st.session_state:
    st.session_state.nick_name = "小爱"
#性格
if "persenality" not in st.session_state:
    st.session_state.persenality = "温柔体贴，善解人意，喜欢关心用户的生活和情感状态"
#会话标识
if "current_session" not in st.session_state:
    st.session_state.current_session = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#性别
if "gender" not in st.session_state:
    st.session_state.gender = "女"

#展示聊天信息
st.text("会话ID: " + st.session_state.current_session)
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
#侧边栏设置
with st.sidebar:
    st.header("AI Partner 设置")
    if st.button("新建会话",width="stretch", icon="🖌"):
        #1.保存当前会话
       save_session()
       #2.创建新的会话
       if st.session_state.messages:
              st.session_state.messages = []  # 清空当前会话的消息
              st.session_state.current_session = generate_session_id()  # 生成新的会话标识
              save_session()
              st.rerun()  # 刷新页面以显示新的会话   
    st.text("会话历史")
    session_list = list_sessions()
    for session in session_list:
         col1,col2 = st.columns([4,1])
         with col1:
             #加载会话信息
             if st.button(session, width="stretch", icon="📁", key=f"load_{session}", type="primary" if session == st.session_state.current_session else "secondary"):
                    load_session(session)
                    st.rerun()  # 刷新页面以显示加载的会话
             with col2:
                 if st.button("",width="stretch", icon="⚔️",key=f"delete_{session}"):
                    delete_session(session)
                    st.rerun()  # 刷新页面以更新会话列表
                                        
    st.header("伴侣信息")
    nick_name = st.text_input("昵称", placeholder="请输入昵称", value=st.session_state.nick_name)
    if nick_name:
        st.session_state.nick_name = nick_name
    gender_options = ["女", "男", "非二元"]
    gender = st.selectbox(
        "性别",
        options=gender_options,
        index=gender_options.index(st.session_state.gender) if st.session_state.gender in gender_options else 0
    )
    st.session_state.gender = gender
    persenality = st.text_area("性格", placeholder="请输入性格", value=st.session_state.persenality)
    if persenality:
        st.session_state.persenality = persenality
    

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
            {"role": "system", "content": prompt_system % (st.session_state.nick_name, st.session_state.gender, st.session_state.persenality)},
            *st.session_state.messages
        ],
        stream=True  # 启用流式输出
    )
    response_message = st.empty()  # 创建一个空的 Streamlit 元素来显示回复
    full_response = ""  # 用于存储完整的回复文本
    for chunk in response:  # 迭代流式输出的每个块
        if chunk.choices[0].delta.content:  # 检查是否有新的内容
            content = chunk.choices[0].delta.content
            full_response += content  # 累积回复文本
            response_message.chat_message("assistant").write(full_response)  # 实时更新显示回复


    # 输出AI回复        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    #保存会话信息
    save_session()
