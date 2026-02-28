import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import random

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="质量工程师学习平台",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&family=Rajdhani:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans SC', sans-serif;
}

/* Main gradient background */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    color: #e0e0e0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(15, 12, 41, 0.95) !important;
    border-right: 1px solid rgba(99, 179, 237, 0.2);
}

/* Cards */
.card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}
.card:hover {
    border-color: rgba(99,179,237,0.6);
    background: rgba(255,255,255,0.08);
}

/* Hero Banner */
.hero {
    background: linear-gradient(90deg, rgba(99,179,237,0.15), rgba(168,85,247,0.15));
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    margin-bottom: 20px;
}
.hero h1 {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.5em;
    color: #63b3ed;
    margin: 0;
}
.hero p { color: #a0aec0; font-size: 1.1em; }

/* Tags */
.tag {
    display: inline-block;
    background: rgba(99,179,237,0.2);
    border: 1px solid rgba(99,179,237,0.4);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.8em;
    color: #63b3ed;
    margin: 2px;
}
.tag-green {
    background: rgba(72,187,120,0.2);
    border-color: rgba(72,187,120,0.4);
    color: #48bb78;
}
.tag-purple {
    background: rgba(168,85,247,0.2);
    border-color: rgba(168,85,247,0.4);
    color: #a855f7;
}
.tag-orange {
    background: rgba(237,137,54,0.2);
    border-color: rgba(237,137,54,0.4);
    color: #ed8936;
}

/* Section headers */
.section-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.6em;
    color: #63b3ed;
    border-bottom: 2px solid rgba(99,179,237,0.3);
    padding-bottom: 8px;
    margin: 20px 0 15px 0;
}

/* Quiz buttons */
.stButton > button {
    background: linear-gradient(135deg, rgba(99,179,237,0.2), rgba(168,85,247,0.2));
    border: 1px solid rgba(99,179,237,0.4);
    color: #e0e0e0;
    border-radius: 8px;
    transition: all 0.3s;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(99,179,237,0.4), rgba(168,85,247,0.4));
    border-color: #63b3ed;
    transform: translateY(-1px);
}

/* Metric cards */
.metric-box {
    background: rgba(99,179,237,0.1);
    border: 1px solid rgba(99,179,237,0.3);
    border-radius: 10px;
    padding: 15px;
    text-align: center;
}
.metric-num {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.5em;
    color: #63b3ed;
    line-height: 1;
}
.metric-label { color: #a0aec0; font-size: 0.85em; }

/* Answer feedback */
.correct { background: rgba(72,187,120,0.15); border: 1px solid rgba(72,187,120,0.4); border-radius: 8px; padding: 12px; color: #48bb78; }
.wrong   { background: rgba(245,101,101,0.15); border: 1px solid rgba(245,101,101,0.4); border-radius: 8px; padding: 12px; color: #fc8181; }

/* Info box */
.info-box {
    background: rgba(99,179,237,0.08);
    border-left: 3px solid #63b3ed;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    color: #cbd5e0;
}

/* Formula box */
.formula {
    background: rgba(168,85,247,0.1);
    border: 1px dashed rgba(168,85,247,0.4);
    border-radius: 8px;
    padding: 12px 16px;
    font-family: monospace;
    color: #d6bcfa;
    margin: 8px 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA
# ─────────────────────────────────────────────
QUALITY_SYSTEMS = {
    "ISO 9001": {
        "icon": "🏆",
        "full_name": "质量管理体系",
        "tag": "体系认证",
        "tag_color": "tag",
        "version": "ISO 9001:2015",
        "description": "全球最广泛采用的质量管理体系标准，基于七大质量管理原则，适用于任何规模和行业的组织。",
        "principles": [
            "以顾客为关注焦点",
            "领导作用",
            "全员积极参与",
            "过程方法",
            "改进",
            "循证决策",
            "关系管理"
        ],
        "key_clauses": {
            "第4条": "组织环境（内外部议题、相关方需求）",
            "第5条": "领导作用（质量方针、职责权限）",
            "第6条": "策划（风险与机遇、质量目标）",
            "第7条": "支持（资源、能力、意识、文件化信息）",
            "第8条": "运行（产品和服务策划、外部供方控制）",
            "第9条": "绩效评价（监视测量、内审、管理评审）",
            "第10条": "改进（不合格品控制、纠正措施、持续改进）"
        },
        "pdca": "计划(Plan)→执行(Do)→检查(Check)→行动(Act) 是ISO 9001的核心循环"
    },
    "IATF 16949": {
        "icon": "🚗",
        "full_name": "汽车质量管理体系",
        "tag": "汽车行业",
        "tag_color": "tag-orange",
        "version": "IATF 16949:2016",
        "description": "汽车行业专用质量管理体系标准，在ISO 9001基础上增加汽车行业特定要求。",
        "principles": [
            "以顾客为导向",
            "APQP产品质量先期策划",
            "生产件批准程序PPAP",
            "FMEA失效模式分析",
            "测量系统分析MSA",
            "统计过程控制SPC"
        ],
        "key_clauses": {
            "顾客特定要求CSR": "各OEM客户的特殊要求须完全符合",
            "产品安全": "安全相关零件需额外控制措施",
            "保修与现场退回": "保修分析及根本原因调查",
            "零缺陷目标": "以预防为主，向零缺陷迈进",
            "分层过程审核LPA": "定期对制造过程进行分层审核",
            "持续改进": "需制定年度改进目标和计划"
        },
        "pdca": "IATF 16949强调制造过程的稳健性和持续改进文化"
    },
    "ISO 14001": {
        "icon": "🌱",
        "full_name": "环境管理体系",
        "tag": "环境体系",
        "tag_color": "tag-green",
        "version": "ISO 14001:2015",
        "description": "国际环境管理体系标准，帮助组织识别、管理和减少环境影响，实现可持续发展目标。",
        "principles": [
            "生命周期视角",
            "合规义务",
            "环境绩效改进",
            "基于风险的思维",
            "领导力与承诺",
            "持续改进"
        ],
        "key_clauses": {
            "环境因素识别": "识别活动、产品和服务的环境因素",
            "合规义务": "法律法规及其他要求的遵守",
            "环境目标": "制定可测量的环境目标并跟踪",
            "应急准备": "应对潜在紧急环境事故",
            "内部审核": "定期评价体系有效性",
            "管理评审": "最高管理者定期评审环境体系"
        },
        "pdca": "环境方针→规划→实施→检查→改进"
    },
    "ISO 45001": {
        "icon": "⛑️",
        "full_name": "职业健康安全管理",
        "tag": "安全体系",
        "tag_color": "tag-orange",
        "version": "ISO 45001:2018",
        "description": "职业健康安全管理体系标准，用于控制职业健康安全风险，防止工伤事故和职业病。",
        "principles": [
            "工人参与和协商",
            "危险源识别和风险评估",
            "法律合规",
            "领导力与承诺",
            "持续改进",
            "应急准备和响应"
        ],
        "key_clauses": {
            "危险源识别": "系统识别工作场所危险源",
            "风险评估": "评估危险源相关风险和机遇",
            "变更管理": "管理影响OH&S绩效的变更",
            "采购控制": "控制供应商和承包商的OH&S",
            "事件调查": "对事故、事件和不符合的调查",
            "绩效监测": "监测、测量、分析OH&S绩效"
        },
        "pdca": "危险源识别→风险控制→实施→绩效评价→改进"
    }
}

QUALITY_TOOLS = {
    "7大质量工具（QC七大工具）": {
        "icon": "🔧",
        "tools": [
            {"name": "检查表 Check Sheet", "purpose": "数据收集和整理", "when": "数据收集阶段", "desc": "系统性收集和记录数据的表格，便于后续分析"},
            {"name": "层别法 Stratification", "purpose": "数据分层分析", "when": "数据分析阶段", "desc": "将数据按类别分层，揭示不同类别间的差异"},
            {"name": "柏拉图 Pareto Chart", "purpose": "识别主要问题", "when": "问题优先排序", "desc": "基于80/20原则，识别影响质量的主要因素"},
            {"name": "因果图 Cause-Effect", "purpose": "根因分析", "when": "问题分析阶段", "desc": "鱼骨图/石川图，系统识别问题原因"},
            {"name": "散点图 Scatter Diagram", "purpose": "相关性分析", "when": "关系验证阶段", "desc": "显示两个变量之间的关系和相关性"},
            {"name": "直方图 Histogram", "purpose": "数据分布分析", "when": "过程能力评估", "desc": "显示数据的频率分布，评估过程稳定性"},
            {"name": "控制图 Control Chart", "purpose": "过程监控", "when": "持续监控阶段", "desc": "基于统计控制限，实时监控过程变异"}
        ]
    },
    "新7大管理工具": {
        "icon": "📊",
        "tools": [
            {"name": "亲和图 Affinity Diagram", "purpose": "整理创意想法", "when": "头脑风暴后", "desc": "将大量想法归类整理，揭示主题和模式"},
            {"name": "关联图 Relations Diagram", "purpose": "复杂关系分析", "when": "因果关系复杂时", "desc": "分析多个因素之间的因果关系"},
            {"name": "系统图 Tree Diagram", "purpose": "目标分解", "when": "策略规划时", "desc": "将目标逐级分解为具体措施"},
            {"name": "矩阵图 Matrix Diagram", "purpose": "多因素关系", "when": "需求与功能对比", "desc": "显示多组要素之间的关系和权重"},
            {"name": "矩阵数据分析法", "purpose": "定量矩阵分析", "when": "数据量化分析", "desc": "对矩阵图中关系进行定量分析"},
            {"name": "过程决策图 PDPC", "purpose": "风险预防", "when": "计划执行前", "desc": "预测可能出现的问题并制定对策"},
            {"name": "箭线图 Arrow Diagram", "purpose": "项目进度管理", "when": "项目规划时", "desc": "规划和管理复杂项目的时间和资源"}
        ]
    },
    "核心质量工具": {
        "icon": "⚙️",
        "tools": [
            {"name": "FMEA 失效模式分析", "purpose": "预防性风险分析", "when": "设计/过程开发阶段", "desc": "识别潜在失效模式，评估风险优先数RPN，制定预防措施"},
            {"name": "SPC 统计过程控制", "purpose": "过程实时监控", "when": "生产过程中", "desc": "使用控制图监控过程，区分普通原因和特殊原因变异"},
            {"name": "MSA 测量系统分析", "purpose": "测量系统评估", "when": "新量具/过程验证时", "desc": "评估测量系统的重复性、再现性，确保测量数据可靠"},
            {"name": "APQP 产品质量先期策划", "purpose": "产品开发质量策划", "when": "新产品开发阶段", "desc": "系统规划新产品开发过程，降低风险"},
            {"name": "PPAP 生产件批准程序", "purpose": "供应商件批准", "when": "量产前", "desc": "验证供应商制造过程满足客户要求"},
            {"name": "8D 问题解决", "purpose": "系统性问题解决", "when": "质量问题发生后", "desc": "8个步骤系统解决质量问题，防止再发"}
        ]
    }
}

SIX_SIGMA = {
    "基础概念": {
        "icon": "📐",
        "content": {
            "什么是六西格玛": "六西格玛（6σ）是一种以数据为驱动的质量管理方法，目标是将过程缺陷率降低到百万分之3.4（DPMO），即过程能力达到6σ水平。",
            "西格玛水平对照": {
                "1σ": "68.27% 合格率，317,300 DPMO",
                "2σ": "95.45% 合格率，45,500 DPMO",
                "3σ": "99.73% 合格率，2,700 DPMO",
                "4σ": "99.9937% 合格率，63 DPMO",
                "5σ": "99.99994% 合格率，0.57 DPMO",
                "6σ": "99.9999998% 合格率，0.002 DPMO（含1.5σ漂移后为3.4 DPMO）"
            },
            "关键指标": {
                "DPMO": "每百万机会缺陷数 = (缺陷数 / 机会总数) × 1,000,000",
                "Cp": "过程能力指数 = (USL - LSL) / 6σ",
                "Cpk": "过程性能指数 = min[(USL-μ)/3σ, (μ-LSL)/3σ]",
                "Pp/Ppk": "长期过程性能指数（用总体标准差）"
            }
        }
    },
    "DMAIC方法论": {
        "icon": "🔄",
        "phases": {
            "D - Define 定义": {
                "color": "#63b3ed",
                "goal": "定义项目范围、顾客需求和业务目标",
                "tools": ["项目章程 Project Charter", "SIPOC图", "顾客之声VOC", "CTQ树（关键质量特性）", "帕累托图"],
                "outputs": ["项目章程", "SIPOC流程图", "CTQ指标", "项目计划"]
            },
            "M - Measure 测量": {
                "color": "#48bb78",
                "goal": "建立基准，量化当前过程性能",
                "tools": ["过程流程图", "数据收集计划", "MSA测量系统分析", "过程能力分析", "基线σ水平"],
                "outputs": ["过程基准数据", "MSA报告", "过程σ水平"]
            },
            "A - Analyze 分析": {
                "color": "#ed8936",
                "goal": "识别根本原因，分析影响质量的关键因素",
                "tools": ["因果图鱼骨图", "假设检验", "回归分析", "方差分析ANOVA", "5Why分析"],
                "outputs": ["根本原因列表", "关键X因子验证", "数据统计分析报告"]
            },
            "I - Improve 改善": {
                "color": "#a855f7",
                "goal": "开发和实施解决方案，验证改善效果",
                "tools": ["头脑风暴", "DOE实验设计", "Poka-Yoke防错法", "FMEA", "试点方案"],
                "outputs": ["改善方案", "试点结果", "改善后σ水平"]
            },
            "C - Control 控制": {
                "color": "#f6e05e",
                "goal": "维持改善成果，建立标准化控制机制",
                "tools": ["控制计划", "SPC统计过程控制", "标准作业程序SOP", "培训计划", "反应计划"],
                "outputs": ["控制计划", "SPC控制图", "更新的SOP", "项目收益总结"]
            }
        }
    },
    "统计工具": {
        "icon": "📊",
        "content": [
            {"name": "假设检验", "desc": "检验样本数据是否支持总体假设，包括t检验、F检验、卡方检验等", "formula": "H₀: μ₁ = μ₂（零假设）  H₁: μ₁ ≠ μ₂（备择假设）"},
            {"name": "方差分析 ANOVA", "desc": "比较多组均值是否存在显著差异，分析因子对结果的影响", "formula": "F = 组间方差(MSB) / 组内方差(MSW)"},
            {"name": "回归分析", "desc": "建立自变量（X）与因变量（Y）之间的数学关系模型", "formula": "Y = β₀ + β₁X₁ + β₂X₂ + ... + ε"},
            {"name": "实验设计 DOE", "desc": "系统安排实验，同时研究多个因素对结果的影响", "formula": "全因子设计: 实验次数 = L^k（L=水平数，k=因子数）"},
            {"name": "过程能力分析", "desc": "量化过程满足规格要求的能力", "formula": "Cp = (USL-LSL)/6σ；Cpk = min[(USL-μ)/3σ, (μ-LSL)/3σ]"}
        ]
    },
    "角色与认证": {
        "icon": "🎓",
        "roles": {
            "白带 White Belt": "了解六西格玛基本概念，参与改善项目",
            "黄带 Yellow Belt": "掌握基础工具，参与并支持绿带/黑带项目",
            "绿带 Green Belt": "掌握DMAIC方法论和统计工具，能独立主导中小型改善项目",
            "黑带 Black Belt": "精通六西格玛所有工具，全职推动改善，辅导绿带",
            "大黑带 Master Black Belt": "组织内六西格玛专家，制定战略，培训黑带"
        }
    }
}

INTERVIEW_QA = [
    {
        "category": "质量体系",
        "q": "ISO 9001:2015的七大质量管理原则是什么？",
        "a": "七大原则：①以顾客为关注焦点、②领导作用、③全员积极参与、④过程方法、⑤改进、⑥循证决策、⑦关系管理。记忆法：顾客领导全员，过程改进，循证关系。",
        "level": "基础"
    },
    {
        "category": "质量体系",
        "q": "IATF 16949与ISO 9001的主要区别是什么？",
        "a": "IATF 16949是在ISO 9001基础上增加了汽车行业特定要求：①APQP产品质量先期策划、②PPAP生产件批准程序、③FMEA失效模式分析、④SPC统计过程控制、⑤MSA测量系统分析，以及各OEM的顾客特定要求(CSR)。",
        "level": "中级"
    },
    {
        "category": "质量工具",
        "q": "什么是FMEA？RPN如何计算？",
        "a": "FMEA（失效模式与影响分析）是预防性质量工具，系统识别产品/过程的潜在失效模式。RPN = 严重度(S) × 发生度(O) × 探测度(D)，每项评分1-10分，RPN越高风险越大（一般>100需优先采取措施）。",
        "level": "中级"
    },
    {
        "category": "六西格玛",
        "q": "解释Cp和Cpk的区别？",
        "a": "Cp是过程能力指数，衡量过程固有能力（规格宽度÷过程宽度），不考虑过程均值偏移。Cpk考虑了均值偏移，= min[(USL-μ)/3σ, (μ-LSL)/3σ]。Cp≥Cpk，当Cp=Cpk时表示过程居中。行业一般要求Cpk≥1.33（4σ）",
        "level": "中级"
    },
    {
        "category": "六西格玛",
        "q": "DMAIC五个阶段各自的主要目标是什么？",
        "a": "D(Define定义)：明确项目范围和顾客需求；M(Measure测量)：量化当前过程基准；A(Analyze分析)：找到根本原因；I(Improve改善)：实施和验证解决方案；C(Control控制)：维持改善成果，防止问题复发。",
        "level": "基础"
    },
    {
        "category": "质量工具",
        "q": "什么是MSA（测量系统分析），Gage R&R是什么？",
        "a": "MSA评估测量系统的可靠性。Gage R&R（量规重复性与再现性）是MSA的核心，包括：重复性(Repeatability)=同一操作员用同一量具重复测量的变差；再现性(Reproducibility)=不同操作员之间的变差。判定标准：%R&R<10%优秀，10-30%可接受，>30%不可接受。",
        "level": "高级"
    },
    {
        "category": "质量工具",
        "q": "SPC控制图中的8条判异规则是什么？",
        "a": "①1点超出控制限；②连续9点在中心线同侧；③连续6点递增或递减；④连续14点交替上下；⑤连续3点中有2点在2σ~3σ；⑥连续5点中有4点在1σ~3σ；⑦连续15点在1σ内（过于稳定）；⑧连续8点在1σ~3σ（两侧）。",
        "level": "高级"
    },
    {
        "category": "质量体系",
        "q": "内部审核的目的和基本步骤是什么？",
        "a": "目的：验证质量体系是否有效运行，发现不符合项和改进机会。步骤：①制定审核计划→②编制检查表→③召开首次会议→④现场审核（访谈/观察/查证）→⑤整理审核发现→⑥召开末次会议→⑦发布审核报告→⑧跟踪纠正措施。",
        "level": "中级"
    },
    {
        "category": "六西格玛",
        "q": "什么是DOE（实验设计），与传统试验法有什么区别？",
        "a": "DOE是系统地安排实验、研究多个因素对结果影响的统计方法。与传统OFAT（一次改变一个因素）相比：①效率更高，实验次数少；②能研究因素间的交互作用；③结果更可靠，有统计显著性保证；④可建立因素与响应的数学模型。常用设计：全因子、部分因子、中心复合设计(CCD)、田口方法。",
        "level": "高级"
    },
    {
        "category": "质量工具",
        "q": "8D问题解决法的步骤是什么？",
        "a": "D0:准备（评估是否需要8D）；D1:成立小组；D2:描述问题（5W2H）；D3:实施临时措施（遏制行动）；D4:确定并验证根本原因；D5:选择和验证永久纠正措施；D6:实施和验证永久纠正措施；D7:预防再发（横向展开）；D8:祝贺小组和总结。",
        "level": "基础"
    }
]

QUIZ_QUESTIONS = [
    {
        "q": "ISO 9001:2015基于几大质量管理原则？",
        "options": ["5大原则", "6大原则", "7大原则", "8大原则"],
        "correct": 2,
        "explain": "ISO 9001:2015基于7大质量管理原则：顾客焦点、领导作用、全员参与、过程方法、改进、循证决策、关系管理（2015版从8大原则调整为7大）。"
    },
    {
        "q": "六西格玛水平对应的DPMO（每百万机会缺陷数）约为多少？",
        "options": ["3.4", "34", "340", "3400"],
        "correct": 0,
        "explain": "六西格玛对应3.4 DPMO（含1.5σ的长期漂移）。这意味着每百万次机会中只有3.4次缺陷，即99.99966%的合格率。"
    },
    {
        "q": "FMEA中RPN的计算公式是？",
        "options": ["S + O + D", "S × O × D", "S × O / D", "(S + O + D) / 3"],
        "correct": 1,
        "explain": "RPN（风险优先数）= 严重度(Severity) × 发生度(Occurrence) × 探测度(Detection)，每项1-10分，RPN最大为1000。"
    },
    {
        "q": "Cpk ≥ 多少通常被认为是过程能力良好的最低要求？",
        "options": ["1.00", "1.33", "1.50", "1.67"],
        "correct": 1,
        "explain": "行业普遍要求Cpk ≥ 1.33（对应4σ水平）。汽车行业关键特性通常要求Cpk ≥ 1.67（5σ水平）。"
    },
    {
        "q": "在DMAIC方法中，'Analyze（分析）'阶段的主要目标是？",
        "options": ["收集过程数据", "识别根本原因", "实施解决方案", "定义项目范围"],
        "correct": 1,
        "explain": "Analyze阶段的核心是通过数据分析（鱼骨图、假设检验、回归分析等）识别导致问题的根本原因（关键X因子）。"
    },
    {
        "q": "Gage R&R结果中，%R&R小于多少认为测量系统优秀？",
        "options": ["5%", "10%", "20%", "30%"],
        "correct": 1,
        "explain": "%R&R < 10%：优秀可接受；10%-30%：视情况可接受；> 30%：不可接受，需改进测量系统。"
    },
    {
        "q": "柏拉图（Pareto Chart）基于哪个原则？",
        "options": ["50/50原则", "70/30原则", "80/20原则", "90/10原则"],
        "correct": 2,
        "explain": "柏拉图基于80/20原则（帕累托法则）：80%的问题/缺陷来自20%的原因。帮助团队聚焦最重要的少数关键因素。"
    },
    {
        "q": "PPAP（生产件批准程序）中，最完整的提交等级是第几级？",
        "options": ["1级", "2级", "3级", "5级"],
        "correct": 2,
        "explain": "PPAP有5个提交等级，3级是标准提交级别（提交样件和完整文件包），1级只提交合规保证书，5级在客户现场审查。"
    },
    {
        "q": "控制图中，UCL和LCL通常设定在中心线±多少σ？",
        "options": ["±1σ", "±2σ", "±3σ", "±6σ"],
        "correct": 2,
        "explain": "控制限通常设在±3σ（99.73%的正常变异在此范围内），超出控制限的点表示可能存在特殊原因变异，需要调查。"
    },
    {
        "q": "8D问题解决法中，'遏制行动'属于哪个步骤？",
        "options": ["D1", "D2", "D3", "D4"],
        "correct": 2,
        "explain": "D3是实施临时遏制措施（Containment Actions），目的是在找到根本原因之前，立即保护顾客不受问题影响。"
    }
]

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "quiz_idx" not in st.session_state:
    st.session_state.quiz_idx = 0
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = 0
if "quiz_answered" not in st.session_state:
    st.session_state.quiz_answered = False
if "quiz_selected" not in st.session_state:
    st.session_state.quiz_selected = None
if "quiz_history" not in st.session_state:
    st.session_state.quiz_history = []
if "shuffled_quiz" not in st.session_state:
    shuffled = QUIZ_QUESTIONS.copy()
    random.shuffle(shuffled)
    st.session_state.shuffled_quiz = shuffled

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:15px 0;'>
        <div style='font-family:Rajdhani,sans-serif; font-size:1.5em; color:#63b3ed;'>🎯 质量工程师</div>
        <div style='color:#a0aec0; font-size:0.85em;'>学习备考平台</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    menu = st.radio(
        "导航",
        ["🏠 首页总览", "📋 质量体系", "🔧 质量工具", "📐 六西格玛", "💼 面试题库", "🧠 随机测验", "📊 能力图谱"],
        label_visibility="collapsed"
    )
    
    st.divider()
    
    if st.session_state.quiz_history:
        total = len(st.session_state.quiz_history)
        correct = sum(st.session_state.quiz_history)
        pct = correct / total * 100
        st.markdown(f"""
        <div style='text-align:center;'>
            <div style='font-size:0.8em; color:#a0aec0;'>测验成绩</div>
            <div style='font-size:2em; color:{"#48bb78" if pct>=70 else "#ed8936" if pct>=50 else "#fc8181"}; font-family:Rajdhani,sans-serif;'>{pct:.0f}%</div>
            <div style='font-size:0.75em; color:#718096;'>{correct}/{total} 题正确</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────

# ─── 首页 ───
if menu == "🏠 首页总览":
    st.markdown("""
    <div class='hero'>
        <h1>🎯 质量工程师学习平台</h1>
        <p>系统学习质量体系 · 质量工具 · 六西格玛 · 面试备考</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("4", "质量体系", "#63b3ed"),
        ("20+", "质量工具", "#48bb78"),
        ("5", "DMAIC阶段", "#a855f7"),
        ("10", "面试题目", "#ed8936"),
    ]
    for col, (num, label, color) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(f"""
            <div class='metric-box'>
                <div class='metric-num' style='color:{color};'>{num}</div>
                <div class='metric-label'>{label}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>📌 学习路径建议</div>", unsafe_allow_html=True)
    
    path_cols = st.columns(5)
    steps = [
        ("1️⃣", "了解质量体系", "掌握ISO 9001、IATF 16949等标准框架", "#63b3ed"),
        ("2️⃣", "学习质量工具", "QC七大工具、FMEA、SPC、MSA等", "#48bb78"),
        ("3️⃣", "六西格玛入门", "理解DMAIC方法论和统计基础", "#a855f7"),
        ("4️⃣", "刷面试题库", "熟悉常见面试问题和标准答案", "#ed8936"),
        ("5️⃣", "随机测验", "测试知识掌握程度，查漏补缺", "#f6e05e"),
    ]
    for col, (num, title, desc, color) in zip(path_cols, steps):
        with col:
            st.markdown(f"""
            <div class='card' style='text-align:center;'>
                <div style='font-size:1.5em;'>{num}</div>
                <div style='color:{color}; font-weight:bold; margin:5px 0; font-size:0.9em;'>{title}</div>
                <div style='color:#718096; font-size:0.78em;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-title'>🔑 质量工程师核心能力</div>", unsafe_allow_html=True)
    
    skills = {
        "质量体系理解": 90,
        "FMEA应用": 85,
        "SPC/控制图": 80,
        "问题解决(8D)": 88,
        "统计分析": 75,
        "内部审核": 82,
        "顾客沟通": 78,
        "持续改进": 85
    }
    
    fig = go.Figure(go.Scatterpolar(
        r=list(skills.values()),
        theta=list(skills.keys()),
        fill='toself',
        fillcolor='rgba(99,179,237,0.2)',
        line=dict(color='#63b3ed', width=2),
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#a0aec0')),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#e0e0e0'))
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=350,
        margin=dict(l=50, r=50, t=30, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)

# ─── 质量体系 ───
elif menu == "📋 质量体系":
    st.markdown("<div class='hero'><h1>📋 质量管理体系</h1><p>ISO 9001 · IATF 16949 · ISO 14001 · ISO 45001</p></div>", unsafe_allow_html=True)
    
    selected = st.selectbox("选择体系标准", list(QUALITY_SYSTEMS.keys()), format_func=lambda x: f"{QUALITY_SYSTEMS[x]['icon']} {x} - {QUALITY_SYSTEMS[x]['full_name']}")
    
    sys = QUALITY_SYSTEMS[selected]
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f"""
        <div class='card'>
            <div style='font-size:3em; text-align:center;'>{sys['icon']}</div>
            <div style='text-align:center; margin-top:10px;'>
                <span class='{sys["tag_color"]}'>{sys['tag']}</span>
            </div>
            <div style='color:#63b3ed; font-size:0.85em; text-align:center; margin-top:8px;'>{sys['version']}</div>
            <div style='color:#a0aec0; font-size:0.85em; margin-top:12px; line-height:1.6;'>{sys['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
        st.markdown("**核心原则**")
        for i, p in enumerate(sys['principles']):
            st.markdown(f"<div class='info-box'>{'①②③④⑤⑥⑦⑧'[i]} {p}</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("**主要条款/要求**")
        for clause, desc in sys['key_clauses'].items():
            with st.expander(f"📌 {clause}"):
                st.write(desc)
        
        st.markdown(f"<div class='info-box'>💡 <b>管理循环：</b>{sys['pdca']}</div>", unsafe_allow_html=True)
    
    # PDCA Diagram
    st.markdown("<div class='section-title'>PDCA 循环</div>", unsafe_allow_html=True)
    
    fig = go.Figure()
    phases = [("Plan\n计划", "#63b3ed", 0.25, 0.75), ("Do\n执行", "#48bb78", 0.75, 0.75), 
               ("Check\n检查", "#ed8936", 0.75, 0.25), ("Act\n行动", "#a855f7", 0.25, 0.25)]
    for label, color, x, y in phases:
        fig.add_shape(type="circle", x0=x-0.18, y0=y-0.18, x1=x+0.18, y1=y+0.18,
                      fillcolor=color+'44', line=dict(color=color, width=2))
        fig.add_annotation(x=x, y=y, text=f"<b>{label}</b>", showarrow=False,
                           font=dict(color='white', size=14), align='center')
    
    arrows = [(0.43, 0.75, 0.57, 0.75), (0.75, 0.57, 0.75, 0.43), (0.57, 0.25, 0.43, 0.25), (0.25, 0.43, 0.25, 0.57)]
    for x0, y0, x1, y1 in arrows:
        fig.add_annotation(x=x1, y=y1, ax=x0, ay=y0, xref='x', yref='y', axref='x', ayref='y',
                           arrowhead=2, arrowwidth=2, arrowcolor='#a0aec0')
    
    fig.update_layout(xaxis=dict(range=[0,1], visible=False), yaxis=dict(range=[0,1], visible=False),
                      paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250,
                      margin=dict(l=20,r=20,t=20,b=20))
    st.plotly_chart(fig, use_container_width=True)

# ─── 质量工具 ───
elif menu == "🔧 质量工具":
    st.markdown("<div class='hero'><h1>🔧 质量工具大全</h1><p>QC七大工具 · 新七大工具 · 核心质量工具</p></div>", unsafe_allow_html=True)
    
    tool_cat = st.selectbox("选择工具类别", list(QUALITY_TOOLS.keys()))
    cat_data = QUALITY_TOOLS[tool_cat]
    
    st.markdown(f"<div class='section-title'>{cat_data['icon']} {tool_cat}</div>", unsafe_allow_html=True)
    
    for tool in cat_data['tools']:
        with st.expander(f"📌 {tool['name']}"):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"**用途：** {tool['purpose']}")
            c2.markdown(f"**使用时机：** {tool['when']}")
            c3.markdown(f"**说明：** {tool['desc']}")
    
    # 控制图演示
    if "控制图" in tool_cat or tool_cat == "7大质量工具（QC七大工具）":
        st.markdown("<div class='section-title'>📈 控制图演示（X-bar图）</div>", unsafe_allow_html=True)
        
        np.random.seed(42)
        n_points = 30
        data = np.random.normal(10, 0.5, n_points)
        data[12] = 11.8  # special cause
        data[22] = 8.5   # special cause
        
        mean = np.mean(data)
        std = np.std(data)
        ucl = mean + 3 * std
        lcl = mean - 3 * std
        
        fig = go.Figure()
        colors = ['#fc8181' if (v > ucl or v < lcl) else '#63b3ed' for v in data]
        
        fig.add_trace(go.Scatter(x=list(range(1, n_points+1)), y=data, mode='lines+markers',
                                 name='测量值', line=dict(color='#63b3ed', width=1.5),
                                 marker=dict(color=colors, size=8)))
        fig.add_hline(y=ucl, line=dict(color='#fc8181', dash='dash', width=2), annotation_text=f"UCL={ucl:.2f}")
        fig.add_hline(y=mean, line=dict(color='#48bb78', width=2), annotation_text=f"CL={mean:.2f}")
        fig.add_hline(y=lcl, line=dict(color='#fc8181', dash='dash', width=2), annotation_text=f"LCL={lcl:.2f}")
        
        fig.update_layout(
            title="X-bar 控制图（红点=超出控制限，需调查）",
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.03)',
            font=dict(color='#e0e0e0'), xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)'), height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # 柏拉图演示
    st.markdown("<div class='section-title'>📊 柏拉图演示</div>", unsafe_allow_html=True)
    
    defects = {"焊接缺陷": 45, "尺寸超差": 28, "外观不良": 15, "标签错误": 7, "包装破损": 3, "其他": 2}
    names = list(defects.keys())
    values = list(defects.values())
    total = sum(values)
    cumulative = [sum(values[:i+1])/total*100 for i in range(len(values))]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=names, y=values, name='缺陷数量', marker_color='#63b3ed'))
    fig.add_trace(go.Scatter(x=names, y=cumulative, name='累计百分比%', yaxis='y2',
                             mode='lines+markers', line=dict(color='#fc8181', width=2)))
    fig.add_hline(y=80, yref='y2', line=dict(color='#f6e05e', dash='dash'), annotation_text="80%")
    
    fig.update_layout(
        title="缺陷类型柏拉图 (80/20原则)",
        yaxis=dict(title="缺陷数量", gridcolor='rgba(255,255,255,0.1)'),
        yaxis2=dict(title="累计%", overlaying='y', side='right', range=[0,105]),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.03)',
        font=dict(color='#e0e0e0'), legend=dict(bgcolor='rgba(0,0,0,0)'), height=350
    )
    st.plotly_chart(fig, use_container_width=True)

# ─── 六西格玛 ───
elif menu == "📐 六西格玛":
    st.markdown("<div class='hero'><h1>📐 六西格玛</h1><p>DMAIC方法论 · 统计工具 · 过程能力分析</p></div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📌 基础概念", "🔄 DMAIC详解", "📊 统计工具", "🎓 认证等级"])
    
    with tab1:
        basics = SIX_SIGMA["基础概念"]["content"]
        st.markdown(f"<div class='info-box'>{basics['什么是六西格玛']}</div>", unsafe_allow_html=True)
        
        st.markdown("**σ水平对照表**")
        sigma_data = pd.DataFrame([
            {"σ水平": k, "说明": v} for k, v in basics["西格玛水平对照"].items()
        ])
        st.dataframe(sigma_data, use_container_width=True, hide_index=True)
        
        # 正态分布可视化
        x = np.linspace(-4, 4, 500)
        y = (1/(np.sqrt(2*np.pi))) * np.exp(-0.5*x**2)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', fillcolor='rgba(99,179,237,0.1)',
                                 line=dict(color='#63b3ed', width=2), name='正态分布'))
        
        sigma_regions = [(3, '#fc8181'), (2, '#ed8936'), (1, '#48bb78')]
        for s, c in sigma_regions:
            mask = (x >= -s) & (x <= s)
            fig.add_trace(go.Scatter(x=x[mask], y=y[mask], fill='tozeroy',
                                     fillcolor=c+'33', line=dict(width=0), name=f'±{s}σ', showlegend=True))
        
        for s in [-3, -2, -1, 1, 2, 3]:
            fig.add_vline(x=s, line=dict(color='rgba(255,255,255,0.3)', dash='dot'), annotation_text=f"{s}σ")
        
        fig.update_layout(title="正态分布与西格玛水平", paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(255,255,255,0.03)', font=dict(color='#e0e0e0'),
                          xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
                          yaxis=dict(gridcolor='rgba(255,255,255,0.1)'), height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**关键指标公式**")
        for k, v in basics["关键指标"].items():
            st.markdown(f"<div class='formula'>📐 <b>{k}：</b>{v}</div>", unsafe_allow_html=True)
    
    with tab2:
        phases = SIX_SIGMA["DMAIC方法论"]["phases"]
        
        # DMAIC流程图
        phase_names = list(phases.keys())
        colors_hex = [phases[p]['color'] for p in phase_names]
        
        fig = go.Figure()
        for i, (phase, color) in enumerate(zip(phase_names, colors_hex)):
            fig.add_shape(type="rect", x0=i*1.2, y0=0, x1=i*1.2+1, y1=0.8,
                          fillcolor=color+'44', line=dict(color=color, width=2))
            fig.add_annotation(x=i*1.2+0.5, y=0.4, text=f"<b>{phase[0]}</b><br>{phase[4:]}",
                                showarrow=False, font=dict(color='white', size=13), align='center')
            if i < 4:
                fig.add_annotation(x=i*1.2+1.1, y=0.4, text="→", showarrow=False,
                                   font=dict(color='#a0aec0', size=20))
        
        fig.update_layout(xaxis=dict(range=[-0.1, 6.1], visible=False),
                          yaxis=dict(range=[-0.1, 1], visible=False),
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          height=130, margin=dict(l=10,r=10,t=10,b=10))
        st.plotly_chart(fig, use_container_width=True)
        
        for phase_name, phase_data in phases.items():
            with st.expander(f"📋 {phase_name} — {phase_data['goal']}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**常用工具**")
                    for tool in phase_data['tools']:
                        st.markdown(f"• {tool}")
                with c2:
                    st.markdown("**阶段输出**")
                    for output in phase_data['outputs']:
                        st.markdown(f"✅ {output}")
    
    with tab3:
        tools_data = SIX_SIGMA["统计工具"]["content"]
        for tool in tools_data:
            with st.expander(f"📊 {tool['name']}"):
                st.markdown(f"**说明：** {tool['desc']}")
                st.markdown(f"<div class='formula'>{tool['formula']}</div>", unsafe_allow_html=True)
        
        # 过程能力分析演示
        st.markdown("<div class='section-title'>过程能力分析演示</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        mean_val = col1.slider("过程均值 μ", 9.0, 11.0, 10.0, 0.1)
        std_val = col2.slider("过程标准差 σ", 0.1, 1.0, 0.3, 0.05)
        lsl = col3.slider("下规格限 LSL", 8.0, 9.5, 9.0, 0.1)
        usl = 11.0
        
        cp = (usl - lsl) / (6 * std_val)
        cpk = min((usl - mean_val) / (3 * std_val), (mean_val - lsl) / (3 * std_val))
        
        x = np.linspace(lsl - 1, usl + 1, 500)
        y = (1/(std_val * np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mean_val)/std_val)**2)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', fillcolor='rgba(99,179,237,0.2)',
                                 line=dict(color='#63b3ed', width=2), name='过程分布'))
        fig.add_vline(x=lsl, line=dict(color='#fc8181', width=2), annotation_text=f"LSL={lsl}")
        fig.add_vline(x=usl, line=dict(color='#fc8181', width=2), annotation_text=f"USL={usl}")
        fig.add_vline(x=mean_val, line=dict(color='#48bb78', dash='dash'), annotation_text=f"μ={mean_val}")
        
        status_color = '#48bb78' if cpk >= 1.33 else '#ed8936' if cpk >= 1.0 else '#fc8181'
        
        fig.update_layout(title=f"过程能力分布  |  Cp={cp:.2f}  Cpk={cpk:.2f}",
                          paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.03)',
                          font=dict(color='#e0e0e0'), height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Cp", f"{cp:.3f}", "≥1.33 为良好")
        m2.metric("Cpk", f"{cpk:.3f}", "≥1.33 为良好")
        m3.metric("状态", "良好✅" if cpk >= 1.33 else "边界⚠️" if cpk >= 1.0 else "不合格❌")
    
    with tab4:
        roles = SIX_SIGMA["角色与认证"]["roles"]
        belt_colors = {"白带": "#e0e0e0", "黄带": "#f6e05e", "绿带": "#48bb78", "黑带": "#718096", "大黑带": "#63b3ed"}
        
        for role, desc in roles.items():
            color_key = next((k for k in belt_colors if k in role), "白带")
            color = belt_colors[color_key]
            st.markdown(f"""
            <div class='card'>
                <span style='color:{color}; font-size:1.1em; font-weight:bold;'>🥋 {role}</span>
                <div style='color:#a0aec0; margin-top:6px;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ─── 面试题库 ───
elif menu == "💼 面试题库":
    st.markdown("<div class='hero'><h1>💼 面试题库</h1><p>高频面试题 · 标准答案 · 分级训练</p></div>", unsafe_allow_html=True)
    
    categories = ["全部"] + list(set(q['category'] for q in INTERVIEW_QA))
    levels = ["全部", "基础", "中级", "高级"]
    
    c1, c2 = st.columns(2)
    cat_filter = c1.selectbox("按类别筛选", categories)
    level_filter = c2.selectbox("按难度筛选", levels)
    
    filtered = INTERVIEW_QA
    if cat_filter != "全部":
        filtered = [q for q in filtered if q['category'] == cat_filter]
    if level_filter != "全部":
        filtered = [q for q in filtered if q['level'] == level_filter]
    
    st.markdown(f"<div style='color:#a0aec0; margin-bottom:10px;'>共 {len(filtered)} 道题目</div>", unsafe_allow_html=True)
    
    level_colors = {"基础": "tag-green", "中级": "tag", "高级": "tag-orange"}
    
    for i, qa in enumerate(filtered):
        with st.expander(f"Q{i+1}. [{qa['category']}] {qa['q']}"):
            lc = level_colors.get(qa['level'], 'tag')
            st.markdown(f"<span class='{lc}'>{qa['level']}</span> <span class='tag-purple'>{qa['category']}</span>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(f"**💡 参考答案：**")
            st.markdown(f"<div class='info-box'>{qa['a']}</div>", unsafe_allow_html=True)

# ─── 随机测验 ───
elif menu == "🧠 随机测验":
    st.markdown("<div class='hero'><h1>🧠 随机测验</h1><p>即时检验学习效果</p></div>", unsafe_allow_html=True)
    
    total_q = len(st.session_state.shuffled_quiz)
    
    if st.session_state.quiz_idx >= total_q:
        # 结束页面
        score = st.session_state.quiz_score
        pct = score / total_q * 100
        
        color = "#48bb78" if pct >= 80 else "#ed8936" if pct >= 60 else "#fc8181"
        grade = "优秀🏆" if pct >= 80 else "良好👍" if pct >= 60 else "继续努力💪"
        
        st.markdown(f"""
        <div class='card' style='text-align:center; padding:30px;'>
            <div style='font-size:4em;'>{"🏆" if pct>=80 else "👍" if pct>=60 else "💪"}</div>
            <div style='font-family:Rajdhani,sans-serif; font-size:2.5em; color:{color};'>{pct:.0f}%</div>
            <div style='font-size:1.2em; color:#e0e0e0; margin:10px 0;'>{grade}</div>
            <div style='color:#a0aec0;'>答对 {score}/{total_q} 题</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 重新开始测验", use_container_width=True):
            shuffled = QUIZ_QUESTIONS.copy()
            random.shuffle(shuffled)
            st.session_state.shuffled_quiz = shuffled
            st.session_state.quiz_idx = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answered = False
            st.session_state.quiz_selected = None
            st.session_state.quiz_history = []
            st.rerun()
    else:
        q = st.session_state.shuffled_quiz[st.session_state.quiz_idx]
        
        # Progress
        progress = st.session_state.quiz_idx / total_q
        st.progress(progress)
        st.markdown(f"<div style='color:#a0aec0; text-align:right; font-size:0.85em;'>第 {st.session_state.quiz_idx + 1} / {total_q} 题</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='card'>
            <div style='font-size:1.1em; color:#e0e0e0; font-weight:500; line-height:1.6;'>
                {q['q']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.quiz_answered:
            for i, option in enumerate(q['options']):
                if st.button(f"{'ABCD'[i]}. {option}", key=f"opt_{i}", use_container_width=True):
                    st.session_state.quiz_selected = i
                    st.session_state.quiz_answered = True
                    if i == q['correct']:
                        st.session_state.quiz_score += 1
                    st.session_state.quiz_history.append(1 if i == q['correct'] else 0)
                    st.rerun()
        else:
            for i, option in enumerate(q['options']):
                if i == q['correct']:
                    st.markdown(f"<div class='correct'>✅ {'ABCD'[i]}. {option}（正确答案）</div>", unsafe_allow_html=True)
                elif i == st.session_state.quiz_selected:
                    st.markdown(f"<div class='wrong'>❌ {'ABCD'[i]}. {option}（你的选择）</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='padding:8px; color:#718096;'>{'ABCD'[i]}. {option}</div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='info-box'>💡 <b>解析：</b>{q['explain']}</div>", unsafe_allow_html=True)
            
            if st.button("下一题 →", use_container_width=True):
                st.session_state.quiz_idx += 1
                st.session_state.quiz_answered = False
                st.session_state.quiz_selected = None
                st.rerun()

# ─── 能力图谱 ───
elif menu == "📊 能力图谱":
    st.markdown("<div class='hero'><h1>📊 自测能力图谱</h1><p>评估你的质量知识掌握程度</p></div>", unsafe_allow_html=True)
    
    st.markdown("请对以下各领域的掌握程度进行自评（1=不了解，5=精通）")
    
    areas = {
        "ISO 9001 七大原则": 3,
        "IATF 16949 核心工具": 3,
        "FMEA 应用": 3,
        "SPC 控制图分析": 3,
        "MSA 测量系统分析": 3,
        "8D 问题解决": 3,
        "DMAIC 方法论": 3,
        "统计假设检验": 3,
        "过程能力分析(Cpk)": 3,
        "DOE 实验设计": 3,
        "内部审核技能": 3,
        "柏拉图与根因分析": 3,
    }
    
    scores = {}
    col1, col2 = st.columns(2)
    area_list = list(areas.items())
    
    for i, (area, default) in enumerate(area_list):
        with col1 if i < len(area_list)//2 else col2:
            scores[area] = st.slider(area, 1, 5, default, key=f"skill_{i}")
    
    if st.button("📊 生成我的能力图谱", use_container_width=True):
        labels = list(scores.keys())
        values = list(scores.values())
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=labels + [labels[0]],
            fill='toself',
            fillcolor='rgba(99,179,237,0.25)',
            line=dict(color='#63b3ed', width=2),
            marker=dict(size=6, color='#63b3ed'),
            name='我的水平'
        ))
        fig.add_trace(go.Scatterpolar(
            r=[5]*len(labels) + [5],
            theta=labels + [labels[0]],
            fill='toself',
            fillcolor='rgba(255,255,255,0.03)',
            line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'),
            name='满分水平'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], gridcolor='rgba(255,255,255,0.1)',
                                tickvals=[1,2,3,4,5], tickfont=dict(color='#a0aec0', size=10)),
                angularaxis=dict(gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#e0e0e0', size=11))
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#e0e0e0')),
            height=500,
            title=dict(text="质量工程师能力图谱", font=dict(color='#63b3ed', size=16))
        )
        st.plotly_chart(fig, use_container_width=True)
        
        avg = sum(values) / len(values)
        weak = [area for area, score in scores.items() if score <= 2]
        strong = [area for area, score in scores.items() if score >= 4]
        
        st.markdown(f"**综合评分：{avg:.1f}/5.0**")
        if weak:
            st.markdown(f"<div class='wrong'>📌 需要加强的领域：{' · '.join(weak)}</div>", unsafe_allow_html=True)
        if strong:
            st.markdown(f"<div class='correct'>✅ 掌握较好的领域：{' · '.join(strong)}</div>", unsafe_allow_html=True)
