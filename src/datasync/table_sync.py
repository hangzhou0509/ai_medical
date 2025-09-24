import json

from neo4j import GraphDatabase

from configuration import config



class TableSynchronizer:
    def __init__(self):
        self.driver = GraphDatabase.driver(**config.NEO4J_CONFIG)

    def sync(self):
        with open(config.KNOWLEDGE_DATA_DIR, 'r', encoding='utf-8') as f:
            for line in f:
                if not line.strip():
                    continue
                data = json.loads(line)
                cypher = """
                    MERGE (di:Disease{name:$data.name,desc:$data.desc})
                    MERGE (ca:Cause{desc:$data.cause})
                    MERGE (di)<-[:CAUSE]- (ca)
                    MERGE (w:Way{name:$data.way})
                    MERGE (di)-[:TRANSMIT]-> (w)
                    MERGE (pr:Prevent{desc:$data.prevent})
                    MERGE (di)<-[:PREVENT]- (pr)
                    MERGE (pe:People{desc:$data.people})
                    MERGE (di)-[:COMMON_ON]-> (pe)
                    MERGE (du:Duration{name:$data.duration})
                    MERGE (di)-[:TREAT_DURATION]-> (du)
                    FOREACH(dept IN $data.department |
                        MERGE (de:Department{name:dept})
                        MERGE (di)-[:BELONG]->(de)
                    )
                    FOREACH(aco IN $data.acompany |
                        MERGE (dis:Disease{name:aco})
                        MERGE (di)-[:ACOMPANY]->(dis)
                    )
                    FOREACH(s IN $data.symptom |
                        MERGE (sy:Symptom{name:s})
                        MERGE (di)-[:HAVE]->(sy)
                    )
                    FOREACH(d IN $data.drug |
                        MERGE (dr:Drug{name:d})
                        MERGE (di)-[:COMMON_USE]->(dr)
                    )
                    FOREACH(e IN $data.eat |
                        MERGE (f:Food{name:e})
                        MERGE (di)-[:EAT]->(f)
                    )
                    FOREACH(ne IN $data.not_eat |
                        MERGE (nf:Food{name:ne})
                        MERGE (di)-[:NOT_EAT]->(nf)
                    )
                    FOREACH(tr IN $data.treat |
                        MERGE (t:Treat{name:tr})
                        MERGE (di)<-[:TREAT]-(t)
                    )
                    FOREACH(ch IN $data.check |
                        MERGE (c:Check{name:ch})
                        MERGE (di)<-[:CHECK]-(c)
                    )
                    
                """
                self.driver.execute_query(cypher, data=data)



if __name__ == '__main__':
    sync = TableSynchronizer()
    sync.sync()