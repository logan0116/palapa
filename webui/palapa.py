import streamlit as st

st.set_page_config(
    page_title="Palapa",
    page_icon="👋",
)

st.title("Palapa 👋")
st.subheader("Personal Assistant Leveraging AI for Progressive Advancement")

st.markdown(
    """
### 项目简介 🚀

**Palapa**致力于利用先进的人工智能技术，为学术研究提供一站式支持。无论是文献检索、研究主题分析，还是技术日报生成和创新分析，Palapa都能为您提供全面而高效的解决方案，帮助您在更短时间内取得更高的学术成果。

### 我们的特点 🌟

1. **领域/研究主题分析 🔍**：
    - 相比于现有工具主要关注单篇文献，Palapa能对某个研究领域或主题进行全面分析，识别研究趋势和主题演化，帮助用户理解领域内的宏观趋势和热点问题。

2. **本地部署支持 🏠**：
    - 许多现有工具需要连接OpenAI等线上大模型API，而Palapa支持本地部署，确保数据安全和隐私，特别适合对数据安全有高要求的用户，如企业或政府研究机构。

### 主要功能 📊

1. **主题演化分析 📈**
    - **描述**：针对一个研究问题，检索相关文献，通过聚类算法识别研究主题，并分析这些主题的演化过程。
    - **优势**：深入分析整个研究领域的主题演化，帮助研究人员发现发展趋势和新兴热点。

2. **技术日报 📰**
    - **描述**：对每日新增的预印论文进行爬取和筛选，生成日报，捕捉最新研究动向。
    - **优势**：确保研究人员及时获取最新研究动态，提供个性化的筛选结果。

3. **创新特征分析 💡**
    - **描述**：根据被引信息与颠覆性创新指标，筛选出颠覆性创新文献和渐进式创新文献，对其进行分析并形成报告。
    - **优势**：深入分析创新文献，帮助研究人员识别重要创新点，为研究设计和战略规划提供有力支持。

4. **Chatbot 🤖**
    - **描述**：根据生成的文档进行问答，支持研究设计、研究gap分析等。
    - **优势**：基于大模型的问答功能，快速回答研究人员的各种问题，支持研究设计和gap分析等复杂任务，提高研究效率。
---
感谢您使用Palapa！我们希望这个工具能显著提升您的研究生产力和创新能力。
"""
)
