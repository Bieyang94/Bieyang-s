from sql import AI_trainCRUD    

import streamlit as st

st.title("AI麻将")

st.subheader("上传文件")

uploaded_file = st.file_uploader("上传文件", type=["jpg", "png", "jpeg"])

submit_button = st.button("提交")

if uploaded_file is not None and submit_button:
    st.image(uploaded_file, caption="上传的图片", use_column_width=True)
    file_details = {"文件名": uploaded_file.name, "文件类型": uploaded_file.type, "文件大小": uploaded_file.size}
    st.write(file_details)
    st.success("文件上传成功！")
    
    # 读取文件内容
    file_content = uploaded_file.read()
    try:
        # 调用AI_trainCRUD类的create_image方法，将图片信息保存到数据库中
        ai_train_crud = AI_trainCRUD()
        ai_train_crud.create_image(AI_train(image=file_content))
    except Exception as e:
        st.error(f"数据库操作失败: {e}")
