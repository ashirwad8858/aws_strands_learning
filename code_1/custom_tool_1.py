from Strands import Agent, tool

@tool
def retrieve_from_quadrent(query: str):
    """
    Retrieve the most relevent document form Qadrant database based on the give text

    Agrs:
        query (str): the user query to search the knowledge base

    Returns:
        list: List pf path to match images
    """ 
    global clinet , COLLECTION_NAME