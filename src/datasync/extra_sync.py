import json

from langchain_neo4j import Neo4jVector, Neo4jGraph
from langchain_neo4j.vectorstores.neo4j_vector import SearchType
from configuration import config
from langchain_huggingface import HuggingFaceEmbeddings



graph = Neo4jGraph(url = config.NEO4J_CONFIG['uri'],
                                username=config.NEO4J_CONFIG['auth'][0],
                                password=config.NEO4J_CONFIG['auth'][1])

embedding_model = HuggingFaceEmbeddings(model_name = 'BAAI/bge-m3',
                                                     encode_kwargs = {'normalize_embeddings': True})
neo4j_vectors = {
            'Disease':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='disease_vector_index',
            keyword_index_name='disease_full_text_index',
            search_type=SearchType.HYBRID
    ),
            'Department':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='department_vector_index',
            keyword_index_name='department_full_text_index',
            search_type=SearchType.HYBRID
    ),      'Symptom':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='symptom_vector_index',
            keyword_index_name='symptom_full_text_index',
            search_type=SearchType.HYBRID
    ),      'Cause':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='cause_vector_index',
            keyword_index_name='cause_full_text_index',
            search_type=SearchType.HYBRID
    ),      'Drug':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='drug_vector_index',
            keyword_index_name='drug_full_text_index',
            search_type=SearchType.HYBRID
    ),      'Food':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='food_vector_index',
            keyword_index_name='food_full_text_index',
            search_type=SearchType.HYBRID
    ),      'Way':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='way_vector_index',
            keyword_index_name='way_full_text_index',
            search_type=SearchType.HYBRID
    ),      'Prevent':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='prevent_vector_index',
            keyword_index_name='prevent_full_text_index',
            search_type=SearchType.HYBRID
    ),      'Check':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='check_vector_index',
            keyword_index_name='check_full_text_index',
            search_type=SearchType.HYBRID
    ),      'Treat':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='treat_vector_index',
            keyword_index_name='treat_full_text_index',
            search_type=SearchType.HYBRID
    ),      'People':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='people_vector_index',
            keyword_index_name='people_full_text_index',
            search_type=SearchType.HYBRID
    ),      'Duration':Neo4jVector.from_existing_index(
            embedding_model,
            url=config.NEO4J_CONFIG['uri'],
            username=config.NEO4J_CONFIG['auth'][0],
            password=config.NEO4J_CONFIG['auth'][1],
            index_name='duration_vector_index',
            keyword_index_name='duration_full_text_index',
            search_type=SearchType.HYBRID
    )
        }

with open(config.ANNOTATED_DATA_DIR, 'r', encoding='utf-8') as f:
    for line in f:
        if not line.strip():
            continue
        data = json.loads(line)
        data = data['spo_list']
        for items in data:
            subject = items['subject']
            subject_type = items['subject_type']
            object_name = items['object']['@value']
            object_type = items['object_type']['@value']
            predicate = items['predicate']
            if subject_type != "疾病":
                continue
            if predicate in ['发病率','预后生存率','死亡率','病理生理','同义词','多发地区','多发季节']:
                result = neo4j_vectors['Disease'].similarity_search_with_score(subject, k=1)[0]
                text = result[0].page_content
                score = result[1]
                cypher = f"""
                        MERGE (n:Disease{{name:$text}})
                        SET n.{config.types_dict[predicate]} = "{object_name}"
                    """
                if score > 0.9:
                    params ={"text":text}
                else:
                    params ={"text":subject}
                graph.query(cypher, params=params)

            elif items['predicate'] in ['鉴别诊断','病史','阶段','病理分型','预后状况']:
                subject_result = neo4j_vectors['Disease'].similarity_search_with_score(subject, k=1)[0]
                subject_text = subject_result[0].page_content
                subject_score = subject_result[1]
                if subject_score < 0.9:
                    subject_text = subject
                if object_type in config.object_tpyes:
                    type_result = neo4j_vectors[config.object_tpyes[object_type]].similarity_search_with_score(object_name, k=1)[0]
                    object_text = type_result[0].page_content
                    object_score = type_result[1]
                    if object_score < 0.9:
                        object_text = object_name
                elif object_type in config.others_tpyes:
                    object_type = config.others_tpyes[object_type]
                    object_text = object_name

                if object_type in config.object_tpyes:
                    cypher =f"""
                        MERGE (a:Disease{{name:$subject_text}})
                        MERGE (b:{config.object_tpyes[object_type]}{{name:$object_text}})
                        MERGE (a)-[:{config.types_dict[predicate]}]->(b)
                    """
                else:
                    cypher = f"""
                        MERGE (a:Disease{{name:$subject_text}})
                        MERGE (b:{object_type}{{name:$object_text}})
                        MERGE (a)-[:{config.types_dict[predicate]}]->(b)
                    """
                params ={"subject_text":subject_text,"object_text":object_text}
                graph.query(cypher, params=params)
            elif items['predicate'] in ['相关（导致）', '风险评估因素', '相关（转化）', '遗传因素', '病因', '高危因素', '发病机制'
                                        ,'放射治疗','药物治疗', '手术治疗', '辅助治疗', '化疗','预防','组织学检查', '筛查',
                                        '内窥镜检查', '辅助检查', '实验室检查', '影像学检查']:
                subject_result = neo4j_vectors['Disease'].similarity_search_with_score(subject, k=1)[0]
                subject_text = subject_result[0].page_content
                subject_score = subject_result[1]
                if subject_score < 0.9:
                    subject_text = subject
                if object_type in config.object_tpyes:
                    type_result = neo4j_vectors[config.object_tpyes[object_type]].similarity_search_with_score(object_name, k=1)[0]
                    object_text = type_result[0].page_content
                    object_score = type_result[1]
                    if object_score < 0.9:
                        object_text = object_name
                elif object_type in config.others_tpyes:
                    object_type = config.others_tpyes[object_type]
                    object_text = object_name

                if object_type in config.object_tpyes:
                    cypher =f"""
                        MERGE (a:Disease{{name:$subject_text}})
                        MERGE (b:{config.object_tpyes[object_type]}{{name:$object_text}})
                        MERGE (a)<-[:{config.types_dict[predicate]}]-(b)
                    """
                else:
                    cypher = f"""
                        MERGE (a:Disease{{name:$subject_text}})
                        MERGE (b:{object_type}{{name:$object_text}})
                        MERGE (a)<-[:{config.types_dict[predicate]}]-(b)
                    """
                params ={"subject_text":subject_text,"object_text":object_text}
                graph.query(cypher, params=params)

            else:
                subject_result = neo4j_vectors['Disease'].similarity_search_with_score(items['subject'], k=1)[0]
                subject_text = subject_result[0].page_content
                subject_score = subject_result[1]
                if object_type in config.object_tpyes:

                    type_result = neo4j_vectors[config.object_tpyes[object_type]].similarity_search_with_score(object_name, k=1)[0]
                    object_text = type_result[0].page_content
                    object_score = type_result[1]
                    if object_score < 0.9:
                        object_text = object_name
                elif object_type in config.others_tpyes:
                    object_type = config.others_tpyes[object_type]
                    object_text = object_name
                if object_type in config.object_tpyes:
                    cypher =f"""
                        MERGE (a:Disease{{name:$subject_text}})
                        MERGE (b:{config.object_tpyes[object_type]}{{name:$object_text}})
                        MERGE (a)-[:{config.types_dict[predicate]}]->(b)
                    """
                else:
                    cypher = f"""
                        MERGE (a:Disease{{name:$subject_text}})
                        MERGE (b:{object_type}{{name:$object_text}})
                        MERGE (a)-[:{config.types_dict[predicate]}]->(b)
                    """
                params ={"subject_text":subject_text,"object_text":object_text}
                graph.query(cypher, params=params)
