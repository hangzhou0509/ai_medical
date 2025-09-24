from dotenv import load_dotenv

load_dotenv()
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_neo4j import Neo4jGraph

from configuration import config

class IndexUtil:
    def __init__(self):
        self.graph = Neo4jGraph(url = config.NEO4J_CONFIG['uri'],
                                username=config.NEO4J_CONFIG['auth'][0],
                                password=config.NEO4J_CONFIG['auth'][1])
        self.embedding_model = HuggingFaceEmbeddings(model_name = 'BAAI/bge-m3',
                                                     encode_kwargs = {'normalize_embeddings': True})

    def create_full_text_index(self,index_name,label,property):
        cypher = f"""
            CREATE FULLTEXT INDEX {index_name} IF NOT EXISTS 
            FOR (n:{label}) ON EACH [n.{property}]        
        """
        self.graph.query(cypher)

    def create_vector_index(self,index_name,label,source_property,embedding_property):
        embedding_dim = self._add_embedding(label,source_property,embedding_property)

        cypher = f"""
            CREATE VECTOR INDEX {index_name} IF NOT EXISTS 
            FOR (m:{label}) 
            ON m.{embedding_property}
            OPTIONS {{indexConfig:{{`vector.dimensions`:{embedding_dim},
            `vector.similarity_function`:'cosine'}}   
            }}     
        """
        self.graph.query(cypher)

    def _add_embedding(self,label,source_property,embedding_property):
        cypher = f"""
            MATCH (n:{label})
            RETURN n.{source_property} AS text,id(n) AS id
        """
        results = self.graph.query(cypher)
        docs = [result['text'] for result in results]
        embeddings = self.embedding_model.embed_documents(docs)
        batch = []
        for result,embedding in zip(results,embeddings):
            item = {
                'id':result['id'],
                'embedding':embedding
            }
            batch.append(item)
        cypher = f"""
            UNWIND $batch AS item
            MATCH (n:{label}) WHERE id(n) = item.id
            SET n.{embedding_property} = item.embedding
        """
        self.graph.query(cypher,params={'batch':batch})
        return len(embeddings[0])

if __name__ == '__main__':
    index_util = IndexUtil()
    index_util.create_full_text_index('disease_full_text_index', 'Disease', 'name')
    index_util.create_vector_index('disease_vector_index', "Disease", 'name', "embedding")

    index_util.create_full_text_index('department_full_text_index', 'Department', 'name')
    index_util.create_vector_index('department_vector_index', "Department", 'name', "embedding")

    index_util.create_full_text_index('symptom_full_text_index', 'Symptom', 'name')
    index_util.create_vector_index('symptom_vector_index', "Symptom", 'name', "embedding")

    index_util.create_full_text_index('cause_full_text_index', 'Cause', 'desc')
    index_util.create_vector_index('cause_vector_index', "Cause", 'desc', "embedding")

    index_util.create_full_text_index('drug_full_text_index', 'Drug', 'name')
    index_util.create_vector_index('drug_vector_index', "Drug", 'name', "embedding")

    index_util.create_full_text_index('food_full_text_index', 'Food', 'name')
    index_util.create_vector_index('food_vector_index', "Food", 'name', "embedding")

    index_util.create_full_text_index('way_full_text_index', 'Way', 'name')
    index_util.create_vector_index('way_vector_index', "Way", 'name', "embedding")

    index_util.create_full_text_index('prevent_full_text_index', 'Prevent', 'desc')
    index_util.create_vector_index('prevent_vector_index', "Prevent", 'desc', "embedding")

    index_util.create_full_text_index('check_full_text_index', 'Check', 'name')
    index_util.create_vector_index('check_vector_index', "Check", 'name', "embedding")

    index_util.create_full_text_index('treat_full_text_index', 'Treat', 'name')
    index_util.create_vector_index('treat_vector_index', "Treat", 'name', "embedding")

    index_util.create_full_text_index('people_full_text_index', 'People', 'desc')
    index_util.create_vector_index('people_vector_index', "People", 'desc', "embedding")

    index_util.create_full_text_index('duration_full_text_index', 'Duration', 'name')
    index_util.create_vector_index('duration_vector_index', "Duration", 'name', "embedding")





