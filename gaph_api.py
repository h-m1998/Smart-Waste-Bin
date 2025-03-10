from fastapi import FastAPI
from neo4j import GraphDatabase

app = FastAPI()

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_waste_disposal_info(waste_item):
    query = """
    MATCH (w:WasteItem {name: $waste_item})-[:BELONGS_TO]->(c)-[:DISPOSED_BY]->(d)-[:AVAILABLE_AT]->(r)
    RETURN c.type AS waste_category, d.method AS disposal_method, d.guidelines AS guidelines, r.name AS recycling_center, r.location AS location
    """
    with driver.session() as session:
        result = session.run(query, waste_item=waste_item)
        data = [record for record in result]
    return data

@app.get("/get_disposal/{item}")
def get_disposal(item: str):
    disposal_info = get_waste_disposal_info(item)
    return {"waste_item": item, "disposal_info": disposal_info}