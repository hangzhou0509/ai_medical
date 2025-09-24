from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent

ANNOTATED_DATA_DIR = ROOT_DIR / 'data' / 'annotated_data'/'CMeIE-V2.jsonl'
KNOWLEDGE_DATA_DIR = ROOT_DIR / "data" / 'knowledge_graph' / 'medical_kg.jsonl'
WEB_STATIC_DIR = ROOT_DIR / 'src'/'web'/'static'

MODEL_NAME = "google-bert/bert-base-chinese"


NEO4J_CONFIG = {
    'uri':"neo4j://localhost:7687",
    'auth':('neo4j','Zh091512.')
}



types_dict = {
    '发病率': 'INCIDENCE',
    '相关（导致）': 'CAUSE',
    '鉴别诊断': 'DIAGNOSIS',
    '传播途径': 'TRANSMIT',
    '病理生理': 'PATHOPHYSIOLOGY',
    '放射治疗': 'TREAT',
    '多发群体': 'COMMON_ON',
    '同义词': 'SYNONYM',
    '多发地区': 'AREA',
    '发病性别倾向': 'COMMON_ON',
    '组织学检查': 'CHECK',
    '就诊科室': 'BELONG',
    '病史': 'HISTORY',
    '并发症': 'ACOMPANY',
    '阶段': 'STAGE',
    '预后生存率': 'SURVIVAL',
    '发病部位': 'PART',
    '风险评估因素': 'CAUSE',
    '侵及周围组织转移的症状': 'HAVE',
    '筛查': 'CHECK',
    '内窥镜检查': 'CHECK',
    '预防': 'PREVENT',
    '转移部位': 'PART',
    '辅助检查': 'CHECK',
    '病理分型': 'CATEGORY',
    '药物治疗': 'TREAT',
    '手术治疗': 'TREAT',
    '临床表现': 'HAVE',
    '实验室检查': 'CHECK',
    '相关（转化）': 'CAUSE',
    '治疗后症状': 'HAVE',
    '预后状况': 'CONDITION',
    '外侵部位': 'PART',
    '辅助治疗': 'TREAT',
    '死亡率': 'FATALITY',
    '遗传因素': 'CAUSE',
    '病因': 'CAUSE',
    '发病年龄': 'COMMON_ON',
    '影像学检查': 'CHECK',
    '高危因素': 'CAUSE',
    '发病机制': 'CAUSE',
    '化疗': 'TREAT',
    '多发季节': 'SEASON',
    '相关（症状）': 'HAVE'
}


object_tpyes={'疾病':'Disease', '流行病学':'People', '症状':"Symptom",  '其他治疗':'Treat',
              '手术治疗':'Treat', '药物':'Drug',  '社会学':'Cause', '检查':'Check'}
others_tpyes= {'部位':'Part','其他':'Other','预后':'Conditon'}